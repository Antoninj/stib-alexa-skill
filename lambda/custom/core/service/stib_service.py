# -*- coding: utf-8 -*-
import logging
from ask_sdk_model.services import ApiClientRequest, ApiClient
from .model.passing_times import PointPassingTimes, PassingTime
from .model.line_stops import LineDetails
from typing import List, Optional

logger = logging.getLogger("Lambda")


class OpenDataService:
    """Define class here"""

    DEFAULT_STOP_ID: str = "1059"
    DEFAULT_LINE_ID: str = "93"
    PASSING_TIME_BY_POINT_SUFFIX: str = "/OperationMonitoring/4.0/PassingTimeByPoint/"
    STOPS_BY_LINE_SUFFIX: str = "/NetworkDescription/1.0/PointByLine/"

    def __init__(self, stib_api_client: ApiClient):
        self.api_client = stib_api_client

    @staticmethod
    def _get_max_line_passing_times(
        line_passing_times: List[PassingTime], max_passing_times: int = 2
    ) -> List[PassingTime]:
        """Define method here."""

        if line_passing_times and (len(line_passing_times) >= max_passing_times):
            return line_passing_times[:max_passing_times]
        else:
            return line_passing_times

    def _get_passing_times_for_line_id(
        self, point_passing_times: List[PointPassingTimes], line_id: str
    ) -> Optional[List[PassingTime]]:
        """Define method here."""

        if point_passing_times:
            passing_times = point_passing_times[0].passing_times
            line_passing_times = [
                passing_time
                for passing_time in passing_times
                if passing_time.line_id == line_id
            ]
            max_line_id_passing_times = self._get_max_line_passing_times(
                line_passing_times
            )
            return max_line_id_passing_times
        else:
            return point_passing_times

    def get_passing_times_for_stop_id_and_line_id(
        self, stop_id: str = DEFAULT_STOP_ID, line_id: str = DEFAULT_LINE_ID
    ) -> Optional[List[PassingTime]]:
        """Define method here."""

        logger.debug(
            "Getting arrival times for line [%s] at stop [%s]", line_id, stop_id
        )
        request_url = self.PASSING_TIME_BY_POINT_SUFFIX + stop_id
        api_request = ApiClientRequest(url=request_url, method="GET")
        response = self.api_client.invoke(api_request)
        raw_passages = response.body.json()
        point_passing_times = PointPassingTimes.schema().load(
            raw_passages["points"], many=True
        )

        return self._get_passing_times_for_line_id(point_passing_times, line_id)

    def get_stops_by_line_id(self, line_id: str = DEFAULT_LINE_ID) -> List[LineDetails]:
        """Define method here."""

        logger.debug("Getting line details for line [%s]", line_id)
        request_url = self.STOPS_BY_LINE_SUFFIX + line_id
        api_request = ApiClientRequest(url=request_url, method="GET")
        response = self.api_client.invoke(api_request)
        raw_lines_info = response.body.json()
        line_details = LineDetails.schema().load(raw_lines_info["lines"], many=True)

        return line_details
