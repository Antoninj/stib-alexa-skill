import unittest
from .mock_api_client import MockAPIClient
from ..custom.service.stib_service import OpenDataService


class TestStibAPIService(unittest.TestCase):
    def setUp(self):
        self.stib_service = OpenDataService(MockAPIClient())

    def test_get_passing_times_for_stop_id_and_line_id(self):
        passing_times = self.stib_service.get_passing_times_for_stop_id_and_line_id()
        self.assertIsNotNone(passing_times)


if __name__ == "__main__":
    unittest.main()
