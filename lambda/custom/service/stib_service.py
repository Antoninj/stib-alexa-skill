import json
from datetime import datetime

import logging

from ask_sdk_model.services import ApiClientRequest, ApiClient

from .utils.time_utils import TimeUtils
from .model.passing_times import PointPassingTimes

logger = logging.getLogger("Lambda")


class OpenDataService:
    DEFAULT_STOP_ID = "1059"
    DEFAULT_LINE_ID = "93"
    PASSING_TIME_BY_POINT_SUFFIX = "/OperationMonitoring/4.0/PassingTimeByPoint/"

    def __init__(self, stib_api_client: ApiClient):
        self.api_client = stib_api_client

    @staticmethod
    def _parse_expected_arrival_times_for_line_id(passages: [dict], line_id=DEFAULT_LINE_ID):
        str_expected_arrival_times = [passage.expected_arrival_time for passage in passages if
                                  passage.line_id == line_id]
        expected_arrival_times = [datetime.fromisoformat(str_expected_arrival_time) for str_expected_arrival_time in
                                  str_expected_arrival_times]
        return expected_arrival_times

    @staticmethod
    def _format_waiting_time(waiting_time_dict, line_id):
        formatted_response = "The next tram {} is in {} minutes and {} seconds, hurry up!".format(line_id,
                                                                                                  waiting_time_dict[
                                                                                                      "minutes"],
                                                                                                  waiting_time_dict[
                                                                                                      "seconds"])
        return formatted_response

    def get_waiting_times_for_stop_id_and_line_id(self, stop_id=DEFAULT_STOP_ID, line_id=DEFAULT_LINE_ID,
                                                  lang: str = 'fr'):
        request_url = self.PASSING_TIME_BY_POINT_SUFFIX + stop_id
        api_request = ApiClientRequest(url=request_url, method='GET')
        response = self.api_client.invoke(api_request)
        raw_passages = response.body.json()

        point_passing_times = PointPassingTimes.schema().load(raw_passages['points'], many=True)
        first_point_passing_times = point_passing_times[0]
        passing_times = first_point_passing_times.passing_times

        expected_arrival_times = self._parse_expected_arrival_times_for_line_id(passing_times, line_id=line_id)
        first_tram_arrival_time = expected_arrival_times[0]
        current_localized_time = TimeUtils.get_current_localized_time()
        first_tram_waiting_time_dict = TimeUtils.compute_time_diff(current_localized_time, first_tram_arrival_time)

        return self._format_waiting_time(first_tram_waiting_time_dict, line_id=line_id)
