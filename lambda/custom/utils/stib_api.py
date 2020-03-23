import requests
import os
import logging

logger = logging.getLogger("Lambda")


class OpenDataAPI:
    default_stop_id = "1047"

    def __init__(self, token_helper):
        self.OPEN_DATA_API_ENDPOINT = os.environ['open_data_api_endpoint']
        self.token_helper = token_helper
        if self.token_helper is not None:
            self.api_bearer_token = self.token_helper.retrieve_stib_api_access_token()

    def get_waiting_times_for_stop_id(self, stop_id=default_stop_id):
        open_data_api_waiting_time_endpoint = self.OPEN_DATA_API_ENDPOINT + "/OperationMonitoring/4.0/PassingTimeByPoint/"
        request_url = open_data_api_waiting_time_endpoint + stop_id
        response = requests.get(request_url, auth=BearerAuth(self.api_bearer_token))

        return response.json()


class BearerAuth(requests.auth.AuthBase):
    def __init__(self, token):
        self.token = token

    def __call__(self, r):
        r.headers["authorization"] = "Bearer " + self.token
        return r



