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

from datetime import datetime
from typing import List, Optional

from dataclasses import dataclass, field
from dataclasses_json import dataclass_json, LetterCase

from ..utils.time_utils import TimeUtils


@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass
class Message:
    """Message dataclass."""

    fr: str = ""
    nl: str = ""


@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass
class Destination:
    """Destination dataclass."""

    fr: str = ""
    nl: str = ""


@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass
class PassingTime:
    """Dataclass for the passing/arrival time at a STIB stop/point."""

    destination: Optional[Destination] = None
    message: Optional[Message] = None
    line_id: str = ""
    expected_arrival_time: str = ""
    arriving_in_dict: dict = field(init=False, repr=False)

    def __post_init__(self):
        self.expected_arrival_time = datetime.fromisoformat(self.expected_arrival_time)
        current_localized_time = TimeUtils.get_current_localized_time()
        self.arriving_in_dict = TimeUtils.compute_time_diff(
            current_localized_time, self.expected_arrival_time
        )

    def __str__(self):
        return self._format_waiting_time()

    def _format_waiting_time(self) -> str:
        """Format waiting time in human readable form."""
        # Todo : Improve this to handle all cases

        if self.arriving_in_dict["days"] > 0:
            formatted_waiting_time = "{} jours, {} heures, {} minutes et {} secondes.".format(
                self.arriving_in_dict["days"],
                self.arriving_in_dict["hours"],
                self.arriving_in_dict["minutes"],
                self.arriving_in_dict["seconds"],
            )
        elif self.arriving_in_dict["hours"] > 0:
            formatted_waiting_time = "{} heures, {} minutes et {} secondes.".format(
                self.arriving_in_dict["hours"],
                self.arriving_in_dict["minutes"],
                self.arriving_in_dict["seconds"],
            )
        elif self.arriving_in_dict["minutes"] > 0:
            formatted_waiting_time = "{} minutes et {} secondes".format(
                self.arriving_in_dict["minutes"], self.arriving_in_dict["seconds"]
            )
        else:
            formatted_waiting_time = "{} secondes".format(
                self.arriving_in_dict["seconds"]
            )
        return formatted_waiting_time


@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass
class PointPassingTimes:
    """Dataclass for a list of passing/arrival times at a STIB stop/point."""

    passing_times: List[PassingTime] = field(default_factory=list)
    point_id: str = ""
