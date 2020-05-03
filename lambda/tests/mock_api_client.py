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

import os

from ask_sdk_model.services import ApiClient, ApiClientResponse
import json


PASSING_TIME_BY_POINT_SUFFIX = "/OperationMonitoring/4.0/PassingTimeByPoint/"
PASSING_TIME_BY_POINT_SUCCESS_API_RESPONSE = (
    '{"points": [{"passingTimes": [{"destination": {"fr": "WTC / GLIBERT", "nl": "WTC / GLIBERT"}, '
    '"expectedArrivalTime": "2021-03-30T11:15:00+01:00", "lineId": "93"},'
    ' {"destination": {"fr": "WTC / GLIBERT", "nl": "WTC / GLIBERT"},'
    ' "expectedArrivalTime": "2021-03-30T11:24:00+01:00", "lineId": "93"}], "pointId": "1059"}]}'
)
STOPS_BY_LINE_SUFFIX = "/NetworkDescription/1.0/PointByLine/"
STOPS_BY_LINE_SUCCESS_API_RESPONSE = (
    '{"lines": [{"destination": {"fr": "LEGRAND", "nl": "LEGRAND"}, '
    '"direction": "Suburb",'
    '"lineId": "93",'
    '"points": [{"id": "5400", "order": 1},'
    '{"id": "5402", "order": 2},'
    '{"id": "5399F", "order": 3},'
    '{"id": "5403", "order": 4},'
    '{"id": "5010", "order": 5},'
    '{"id": "6501", "order": 6},'
    '{"id": "6505", "order": 7},'
    '{"id": "6504", "order": 8},'
    '{"id": "4130F", "order": 9},'
    '{"id": "6100", "order": 10},'
    '{"id": "6122", "order": 11},'
    '{"id": "1073", "order": 12},'
    '{"id": "6103F", "order": 13},'
    '{"id": "6178", "order": 14},'
    '{"id": "5762", "order": 15},'
    '{"id": "1646F", "order": 16},'
    '{"id": "6012G", "order": 17},'
    '{"id": "6412F", "order": 18},'
    '{"id": "6014", "order": 19},'
    '{"id": "6437F", "order": 20},'
    '{"id": "6308F", "order": 21},'
    '{"id": "6309F", "order": 22},'
    '{"id": "6310F", "order": 23},'
    '{"id": "6311", "order": 24},'
    '{"id": "6312", "order": 25},'
    '{"id": "6313", "order": 26},'
    '{"id": "6314", "order": 27},'
    '{"id": "5405", "order": 28},'
    '{"id": "5406", "order": 29},'
    '{"id": "5404", "order": 30},'
    '{"id": "5408", "order": 31},'
    '{"id": "5409", "order": 32},'
    '{"id": "1047F", "order": 33}]},'
    '{"destination": {"fr": "STADE", "nl": "STADION"},'
    '"direction": "City",'
    '"lineId": "93",'
    '"points": [{"id": "1059", "order": 1},'
    '{"id": "5466", "order": 2},'
    '{"id": "5467", "order": 3},'
    '{"id": "5475", "order": 4},'
    '{"id": "5469", "order": 5},'
    '{"id": "5470", "order": 6},'
    '{"id": "6361", "order": 7},'
    '{"id": "6352", "order": 8},'
    '{"id": "6353F", "order": 9},'
    '{"id": "6354", "order": 10},'
    '{"id": "6355F", "order": 11},'
    '{"id": "6356F", "order": 12},'
    '{"id": "6357F", "order": 13},'
    '{"id": "6434F", "order": 14},'
    '{"id": "6359F", "order": 15},'
    '{"id": "6413F", "order": 16},'
    '{"id": "6066G", "order": 17},'
    '{"id": "1644F", "order": 18},'
    '{"id": "6177", "order": 19},'
    '{"id": "6179", "order": 20},'
    '{"id": "6168F", "order": 21},'
    '{"id": "1076", "order": 22},'
    '{"id": "6174F", "order": 23},'
    '{"id": "6171", "order": 24},'
    '{"id": "4126F", "order": 25},'
    '{"id": "6172", "order": 26},'
    '{"id": "6552", "order": 27},'
    '{"id": "6553", "order": 28},'
    '{"id": "5081F", "order": 29},'
    '{"id": "5471", "order": 30},'
    '{"id": "5398F", "order": 31},'
    '{"id": "5472", "order": 32},'
    '{"id": "5474", "order": 33}]}]}'
)


class BinaryMockResponse:
    def __init__(self, binary_content):
        self.content = binary_content

    def content(self):
        return self.content


class JsonMockResponse:
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
        url = request.url
        if PASSING_TIME_BY_POINT_SUFFIX in url:
            mock_api_response = JsonMockResponse(
                json.loads(PASSING_TIME_BY_POINT_SUCCESS_API_RESPONSE), "200"
            )
        elif STOPS_BY_LINE_SUFFIX in url:
            mock_api_response = JsonMockResponse(
                json.loads(STOPS_BY_LINE_SUCCESS_API_RESPONSE), "200"
            )
        else:
            with open(
                os.path.dirname(os.path.dirname(__file__)) + "/tests/gtfs.zip", "rb"
            ) as gtfs_zip_file:
                data = gtfs_zip_file.read()
            mock_api_response = BinaryMockResponse(binary_content=data)

        api_client_response = ApiClientResponse(body=mock_api_response)
        return api_client_response
