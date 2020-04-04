# -*- coding: utf-8 -*-
from dataclasses import dataclass, field
from typing import List, Optional
from dataclasses_json import dataclass_json, LetterCase
from .passing_times import Destination
from enum import Enum
import pandas as pd

ROUTE_DATAPATH = "core/service/model/routes.txt"
STOP_DATAPATH = "core/service/model/stops.txt"
routes_df = pd.read_csv(ROUTE_DATAPATH)
stops_df = pd.read_csv(STOP_DATAPATH)


class RouteType(Enum):
    TRAMWAY = 0
    METRO = 1
    BUS = 3


@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass
class LinePoint:
    id: str = ""
    order: int = 0
    stop_name: str = ""

    def __post_init__(self):
        # todo: fix this... why the hell is there missing data in the first place?
        try:
            self.stop_name = stops_df[stops_df["stop_id"] == self.id].iloc[0][
                "stop_name"
            ]
        except:
            self.stop_name = ""


@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass
class LineDetails:
    destination: Optional[Destination] = None
    direction: str = ""
    line_id: str = ""
    points: List[LinePoint] = field(default_factory=list)
    route_type: Optional[RouteType] = None

    def __post_init__(self):
        self.route_type = RouteType(
            routes_df[routes_df["route_short_name"] == self.line_id].iloc[0][
                "route_type"
            ]
        )
