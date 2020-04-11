# -*- coding: utf-8 -*-
from dataclasses import dataclass, field
from typing import List, Optional
from dataclasses_json import dataclass_json, LetterCase
from .passing_times import Destination
from enum import Enum
import pandas as pd
import os

ROUTE_DATAPATH = os.path.dirname(os.path.abspath(__file__)) + "/routes.txt"
STOP_DATAPATH = os.path.dirname(os.path.abspath(__file__)) + "/stops.txt"
STOP_TRANSLATONS_DATAPATH = (
    os.path.dirname(os.path.abspath(__file__)) + "/translations.txt"
)

routes_df = pd.read_csv(ROUTE_DATAPATH)
stops_df = pd.read_csv(STOP_DATAPATH)
stops_translations_df = pd.read_csv(STOP_TRANSLATONS_DATAPATH)
# Todo: get rid of pandas/numpy dependency in this class


class RouteType(Enum):
    """STIB network route type enumeration."""

    TRAM = 0
    METRO = 1
    BUS = 3


@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass
class LinePoint:
    """Dataclass for a stop/point of a STIB line."""

    id: str = ""
    order: int = 0
    stop_name: str = ""
    stop_name_fr: str = ""
    stop_name_nl: str = ""

    def __post_init__(self):
        # todo: fix this... why the hell is there missing data in the first place?
        try:
            self.stop_name = stops_df[stops_df["stop_id"] == self.id].iloc[0][
                "stop_name"
            ]
            self.stop_name_fr = stops_translations_df[
                (stops_translations_df["trans_id"] == self.stop_name)
                & (stops_translations_df["lang"] == "fr")
            ].iloc[0]["translation"]
            self.stop_name_nl = stops_translations_df[
                (stops_translations_df["trans_id"] == self.stop_name)
                & (stops_translations_df["lang"] == "nl")
            ].iloc[0]["translation"]
        except:
            self.stop_name = "NOT FOUND"
            self.stop_name_fr = "NOT FOUND"
            self.stop_name_nl = "NOT FOUND"


@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass
class LineDetails:
    """Dataclass for details of a STIB line."""

    destination: Optional[Destination] = None
    direction: str = ""
    line_id: str = ""
    points: List[LinePoint] = field(default_factory=list)
    route_type: Optional[RouteType] = None

    def __post_init__(self):
        try:
            self.route_type = RouteType(
                routes_df[routes_df["route_short_name"] == self.line_id].iloc[0][
                    "route_type"
                ]
            )
        except:
            # Hardcode the route type if not defined... need to change this later
            self.route_type = RouteType(0)
