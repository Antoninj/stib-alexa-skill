from datetime import datetime

import requests
import os
import logging

from ask_sdk_model.services import ApiClient

from .time_utils import TimeUtils

logger = logging.getLogger("Lambda")


class OpenDataAPIClient(ApiClient):
    DEFAULT_STOP_ID = "1059"
    DEFAULT_LINE_ID = "93"

    def __init__(self, token_helper=None):
        self.OPEN_DATA_API_ENDPOINT = os.environ['open_data_api_endpoint']
        self.token_helper = token_helper

    @staticmethod
    def _parse_expected_arrival_times_for_line_id(json_payload, line_id=DEFAULT_LINE_ID):
        passing_times = json_payload['points'][0]['passingTimes']
        str_expected_arrival_times = [passing_time['expectedArrivalTime'] for passing_time in passing_times if
                                      passing_time['lineId'] == line_id]
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

    def get_waiting_times_for_stop_id_and_line_id(self, stop_id=DEFAULT_STOP_ID, line_id=DEFAULT_LINE_ID):
        open_data_api_waiting_time_endpoint = self.OPEN_DATA_API_ENDPOINT + "/OperationMonitoring/4.0/PassingTimeByPoint/"
        request_url = open_data_api_waiting_time_endpoint + stop_id
        api_security_token = self.token_helper.get_security_token()
        response = requests.get(request_url, auth=BearerAuth(api_security_token))
        json_payload = response.json()
        expected_arrival_times = self._parse_expected_arrival_times_for_line_id(json_payload, line_id=line_id)
        first_tram_arrival_time = expected_arrival_times[0]
        current_localized_time = TimeUtils.get_current_localized_time()
        first_tram_waiting_time_dict = TimeUtils.compute_time_diff(current_localized_time, first_tram_arrival_time)

        return self._format_waiting_time(first_tram_waiting_time_dict, line_id=line_id)

    def invoke(self, request):
        pass


class BearerAuth(requests.auth.AuthBase):
    def __init__(self, token):
        self.token = token

    def __call__(self, r):
        r.headers["authorization"] = "Bearer " + self.token
        return r
