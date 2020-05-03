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

import unittest
from .mock_api_client import MockAPIClient
from ..custom.core.service.stib_service import OpenDataService


class TestStibAPIService(unittest.TestCase):
    def setUp(self):
        self.stib_service = OpenDataService(MockAPIClient())

    def test_get_passing_times_for_stop_id_and_line_id(self):
        passing_times = self.stib_service.get_passing_times_for_stop_id_and_line_id(
            stop_id="1059", line_id="93"
        )
        self.assertIsNotNone(passing_times)

    def test_get_stops_by_line_id(self):
        line_details = self.stib_service.get_stops_by_line_id(line_id="93")
        self.assertIsNotNone(line_details)


if __name__ == "__main__":
    unittest.main()
