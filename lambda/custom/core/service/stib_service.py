# -*- coding: utf-8 -*-

#   Copyright 2020 Antonin Jousson
#
#  Licensed under the Apache License, Version 2.0 (the "License").
#  You may not use this file except in compliance with the License.
#  A copy of the License is located at
#
#  http://www.apache.org/licenses/LICENSE-2.0
#
#  or in the "license" file accompanying this file. This file is
#  distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS
#  OF ANY KIND, either express or implied. See the License for the
#  specific language governing permissions and limitations under the
#  License.

import io
import logging
import os
import zipfile
from typing import Dict, List, Optional

import elasticache_auto_discovery
import hermes.backend.dict
import hermes.backend.memcached
from ask_sdk_core.exceptions import ApiClientException
from ask_sdk_model.services import ApiClient, ApiClientRequest

from .exceptions import (GTFSDataError, NetworkDescriptionError,
                         OperationMonitoringError)
from .model.line_stops import LineDetails
from .model.passing_times import PassingTime, PointPassingTimes

logger = logging.getLogger("Lambda")

ENVIRONMENT = os.environ["env"]
ELASTICACHE_CONFIG_ENDPOINT = os.environ["elasticache_config_endpoint"]


def initialize_cache() -> hermes.Hermes:
    if ENVIRONMENT == "Sandbox":
        logger.info("Using local dictionary as caching backend")
        cache = hermes.Hermes(backendClass=hermes.backend.dict.Backend)

    elif ENVIRONMENT == "Production":
        logger.info("Using ElastiCache memcached as caching backend")
        nodes = elasticache_auto_discovery.discover(ELASTICACHE_CONFIG_ENDPOINT)
        servers = list(
            map(lambda x: x[1].decode("UTF-8") + ":" + x[2].decode("UTF-8"), nodes)
        )
        cache = hermes.Hermes(
            backendClass=hermes.backend.memcached.Backend, servers=servers
        )

    else:
        logger.info("Using local memcached instance as caching backend")
        cache = hermes.Hermes(
            backendClass=hermes.backend.memcached.Backend,
            servers=[ELASTICACHE_CONFIG_ENDPOINT],
        )
    return cache


class OpenDataService:
    """Service to handle custom OpenData API endpoints queries."""

    GTFS_FILES_SUFFIX: str = "/Files/2.0/Gtfs"
    PASSING_TIME_BY_POINT_SUFFIX: str = "/OperationMonitoring/4.0/PassingTimeByPoint/"
    STOPS_BY_LINE_SUFFIX: str = "/NetworkDescription/1.0/PointByLine/"
    cache = initialize_cache()

    def __init__(self, stib_api_client: ApiClient):
        self.api_client = stib_api_client

    @cache(ttl=20)
    def get_passing_times_for_stop_id_and_line_id(
        self, stop_id: str, line_id: str
    ) -> Optional[List[PassingTime]]:
        """
        Retrieve arrival times at a given stop based on the stop ID and line ID of the STIB network.
        The data is cached for 20 seconds following Open Data API recommendations.
        """

        logger.debug(
            "Getting arrival times for line [%s] at stop [%s]", line_id, stop_id
        )
        request_url = self.PASSING_TIME_BY_POINT_SUFFIX + stop_id
        api_request = ApiClientRequest(url=request_url, method="GET")
        try:
            response = self.api_client.invoke(api_request)
            raw_passages = response.body.json()
            point_passing_times = PointPassingTimes.schema().load(
                raw_passages["points"], many=True
            )

            return self._filter_passing_times_by_line_id(point_passing_times, line_id)
        except ApiClientException as e:
            raise OperationMonitoringError(e, line_id=line_id, stop_id=stop_id)

    @cache(ttl=86400)
    def get_stops_by_line_id(self, line_id: str) -> Optional[List[LineDetails]]:
        """
        Retrieve line information based on a line ID of the STIB network.
        The data is cached for one day following Open Data API recommendations.
.       """

        logger.info("Getting line details for line [%s]", line_id)
        request_url = self.STOPS_BY_LINE_SUFFIX + line_id
        api_request = ApiClientRequest(url=request_url, method="GET")
        try:
            response = self.api_client.invoke(api_request)
            raw_lines_info = response.body.json()
            line_details = LineDetails.schema().load(raw_lines_info["lines"], many=True)
            self._enrich_line_details_with_gtfs_data(line_details)

            return line_details
        except ApiClientException as e:
            raise NetworkDescriptionError(e, line_id)

    @cache(ttl=1209600)
    def get_gtfs_data(self, csv_filenames: List[str]) -> Dict[str, io.BytesIO]:
        """
        Retrieve GTFS files of the STIB network.
        The data is cached for two weeks following Open Data API recommendations.
        """

        logger.debug("Getting GTFS files %s", csv_filenames)
        api_request = ApiClientRequest(
            url=self.GTFS_FILES_SUFFIX,
            method="GET",
            headers=[("Accept", "application/zip")],
        )
        try:
            response = self.api_client.invoke(api_request)
            file = io.BytesIO(response.body.content)
            if zipfile.is_zipfile(file):
                with zipfile.ZipFile(file) as gtfs_zip_file:
                    logger.debug(
                        "GTFS data zip file content: %s", gtfs_zip_file.namelist()
                    )
                    csv_files = {
                        csv_filename: io.BytesIO(gtfs_zip_file.read(name=csv_filename))
                        for csv_filename in csv_filenames
                    }
                    return csv_files
        except ApiClientException as e:
            raise GTFSDataError("Error getting GTFS files", e)

    def _enrich_line_details_with_gtfs_data(
        self, line_details: List[LineDetails]
    ) -> None:
        """Enrich line details dynamically using GTFS data."""

        logger.debug("Enriching line details with STIB network GTFS data")
        filenames = ["routes.txt", "stops.txt", "translations.txt"]
        csv_files = self.get_gtfs_data(csv_filenames=filenames)
        for line_detail in line_details:
            line_detail.set_route_type(csv_files["routes.txt"])
            [
                line_point.set_stop_names(
                    csv_files["stops.txt"], csv_files["translations.txt"]
                )
                for line_point in line_detail.points
            ]

    @staticmethod
    def _filter_passing_times_by_line_id(
        point_passing_times: List[PointPassingTimes], line_id: str
    ) -> Optional[List[PassingTime]]:
        """Filter arrival times by line ID."""

        if point_passing_times:
            passing_times = point_passing_times[0].passing_times
            line_passing_times = [
                passing_time
                for passing_time in passing_times
                if passing_time.line_id == line_id
            ]
            max_line_id_passing_times = OpenDataService._get_max_line_passing_times(
                line_passing_times
            )
            return max_line_id_passing_times
        else:
            return point_passing_times

    @staticmethod
    def _get_max_line_passing_times(
        line_passing_times: List[PassingTime], max_passing_times: int = 2
    ) -> List[PassingTime]:
        """Limit maximum amount of passing times returned."""

        if line_passing_times and (len(line_passing_times) >= max_passing_times):
            return line_passing_times[:max_passing_times]
        else:
            return line_passing_times
