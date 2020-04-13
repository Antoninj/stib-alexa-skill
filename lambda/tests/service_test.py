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
