from datetime import datetime, time as datetime_time, timedelta


def parse_waiting_times(json_payload, destination):
    passing_times = json_payload['points'][0]['passingTimes']
    str_expected_arrival_times = [passing_time['expectedArrivalTime'] for passing_time in passing_times if passing_time['destination']['fr'] == destination]
    expected_arrival_times = [datetime.fromisoformat(str_expected_arrival_time) for str_expected_arrival_time in str_expected_arrival_times]
    return expected_arrival_times


def compute_time_diff(start, end):
    if isinstance(start, datetime_time): # convert to datetime
        assert isinstance(end, datetime_time)
        start, end = [datetime.combine(datetime.min, t) for t in [start, end]]
    if start <= end: # e.g., 10:33:26-11:15:49
        return end - start
    else: # end < start e.g., 23:55:00-00:25:00
        end += timedelta(1) # +day
        assert end > start
        return end - start
