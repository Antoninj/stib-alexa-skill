# -*- coding: utf-8 -*-

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

from datetime import datetime, time as datetime_time, timedelta
from typing import Dict

import pytz


class TimeUtils:
    """Utility class for time manipulation methods (anti-pythonic I know)."""

    @staticmethod
    def get_current_localized_time():
        """Define method here."""

        current_time_utc = datetime.utcnow()
        return pytz.utc.localize(current_time_utc)

    @staticmethod
    def compute_time_diff(start, end) -> Dict:
        """I need to implement this differently."""

        if isinstance(start, datetime_time):  # convert to datetime
            assert isinstance(end, datetime_time)
            start, end = [datetime.combine(datetime.min, t) for t in [start, end]]
        if start <= end:  # e.g., 10:33:26-11:15:49
            return TimeUtils._convert_timedelta(end - start)
        else:  # end < start e.g., 23:55:00-00:25:00
            end += timedelta(1)  # +day

            assert end > start
            return TimeUtils._convert_timedelta(end - start)

    @staticmethod
    def _convert_timedelta(duration) -> Dict:
        """Define method here."""

        duration_dict = {}
        days, seconds = duration.days, duration.seconds
        duration_dict["days"] = days
        hours = seconds // 3600
        minutes = (seconds % 3600) // 60
        seconds = seconds % 60
        duration_dict["hours"] = hours
        duration_dict["minutes"] = minutes
        duration_dict["seconds"] = seconds

        return duration_dict
