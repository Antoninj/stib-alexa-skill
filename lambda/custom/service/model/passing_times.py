from dataclasses import dataclass, field
from typing import List, Optional

from dataclasses_json import dataclass_json, LetterCase


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

@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass
class PointPassingTimes:
    passing_times: List[PassingTime] = field(default_factory=list)
    point_id: str = ""

