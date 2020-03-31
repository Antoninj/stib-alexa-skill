from ask_sdk_model.services import ApiClient, ApiClientResponse
import json

SUCCESS_API_RESPONSE = (
    '{"points": [{"passingTimes": [{"destination": {"fr": "WTC / GLIBERT", "nl": "WTC / GLIBERT"}, '
    '"expectedArrivalTime": "2021-03-30T11:15:00+01:00", "lineId": "93"},'
    ' {"destination": {"fr": "WTC / GLIBERT", "nl": "WTC / GLIBERT"},'
    ' "expectedArrivalTime": "2021-03-30T11:24:00+01:00", "lineId": "93"}], "pointId": "1059"}]}'
)


class MockResponse:
    def __init__(self, json_data, status_code):
        self.json_data = json_data
        self.status_code = status_code

    def json(self):
        return self.json_data


class MockAPIClient(ApiClient):
    """Mock STIB API client object to facilitate unit testing of the service layer."""

    def __init__(self):
        pass

    def invoke(self, request):
        mock_api_response = MockResponse(json.loads(SUCCESS_API_RESPONSE), "200")
        apiClientResponse = ApiClientResponse(body=mock_api_response)
        return apiClientResponse
