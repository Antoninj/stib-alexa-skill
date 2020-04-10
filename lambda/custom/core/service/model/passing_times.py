# -*- coding: utf-8 -*-
from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Optional
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
        # self.formatted_waiting_time = self._format_waiting_time()

    def __str__(self):
        return self._format_waiting_time()

    def _format_waiting_time(self) -> str:
        """Format waiting time in human readable form."""

        formatted_waiting_time = "Le prochain tram {} en direction de {} passe dans {} minutes et {} secondes.".format(
            self.line_id,
            self.destination.fr,
            self.arriving_in_dict["minutes"],
            self.arriving_in_dict["seconds"],
        )
        return formatted_waiting_time


@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass
class PointPassingTimes:
    """Dataclass for a list of passing/arrival times at a STIB stop/point."""

    passing_times: List[PassingTime] = field(default_factory=list)
    point_id: str = ""
