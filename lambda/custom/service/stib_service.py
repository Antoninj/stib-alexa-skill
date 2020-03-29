# -*- coding: utf-8 -*-
import logging
from ask_sdk_model.services import ApiClientRequest, ApiClient
from .model.passing_times import PointPassingTimes

logger = logging.getLogger("Lambda")


class OpenDataService:
    DEFAULT_STOP_ID = "1059"
    DEFAULT_LINE_ID = "93"
    PASSING_TIME_BY_POINT_SUFFIX = "/OperationMonitoring/4.0/PassingTimeByPoint/"

    def __init__(self, stib_api_client: ApiClient):
        self.api_client = stib_api_client

    @staticmethod
    def _get_max_line_passing_times(line_passing_times: [], max_passing_times=2):
        if line_passing_times and (len(line_passing_times) >= max_passing_times):
            return line_passing_times[:max_passing_times]
        else:
            return line_passing_times

    def _get_passing_times_for_line_id(self, point_passing_times: [], line_id):
        if point_passing_times:
            passing_times = point_passing_times[0].passing_times
            line_passing_times = [passing_time for passing_time in passing_times if
                                  passing_time.line_id == line_id]
            max_line_id_passing_times = self._get_max_line_passing_times(line_passing_times)
            return max_line_id_passing_times
        else:
            return point_passing_times

    def get_passing_times_for_stop_id_and_line_id(self, stop_id=DEFAULT_STOP_ID, line_id=DEFAULT_LINE_ID,
                                                  lang: str = 'fr'):
        request_url = self.PASSING_TIME_BY_POINT_SUFFIX + stop_id
        api_request = ApiClientRequest(url=request_url, method='GET')
        response = self.api_client.invoke(api_request)
        raw_passages = response.body.json()
        point_passing_times = PointPassingTimes.schema().load(raw_passages['points'], many=True)

        return self._get_passing_times_for_line_id(point_passing_times, line_id)
