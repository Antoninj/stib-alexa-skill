from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Optional
from dataclasses_json import dataclass_json, LetterCase
from ..utils.time_utils import TimeUtils


@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass
class Message:
    fr: str = ""
    nl: str = ""


@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass
class Destination:
    fr: str = ""
    nl: str = ""


@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass
class PassingTime:
    destination: Optional[Destination] = None
    message: Optional[Message] = None
    line_id: str = ""
    expected_arrival_time: str = ""
    arriving_in_dict: dict = field(init=False, repr=False)
    formatted_waiting_time: str = field(init=False)

    def __post_init__(self):
        self.expected_arrival_time = datetime.fromisoformat(self.expected_arrival_time)
        current_localized_time = TimeUtils.get_current_localized_time()
        self.arriving_in_dict = TimeUtils.compute_time_diff(current_localized_time, self.expected_arrival_time)
        self.formatted_waiting_time = self._format_waiting_time()

    def __str__(self):
        return f'{self.arriving_in_dict}'

    def _format_waiting_time(self):
        formatted_waiting_time = "Le prochain tram {} en direction de {} passe dans {} minutes et {} secondes," \
                             " dépechez vous!".format(self.line_id,
                                                 self.destination.fr,
                                                 self.arriving_in_dict["minutes"],
                                                 self.arriving_in_dict["seconds"])
        return formatted_waiting_time


@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass
class PointPassingTimes:
    passing_times: List[PassingTime] = field(default_factory=list)
    point_id: str = ""
