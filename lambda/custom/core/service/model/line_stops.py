# -*- coding: utf-8 -*-
from dataclasses import dataclass, field
from typing import List, Optional
from dataclasses_json import dataclass_json, LetterCase
from .passing_times import Destination


@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass
class LinePoint:
    id: str = ""
    order: int = 0


@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass
class LineDetails:
    destination: Optional[Destination] = None
    direction: str = ""
    line_id: str = ""
    points: List[LinePoint] = field(default_factory=list)

    def __post_init__(self):
        pass
