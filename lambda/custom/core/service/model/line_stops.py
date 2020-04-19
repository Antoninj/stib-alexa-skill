# -*- coding: utf-8 -*-
import os
from typing import List, Optional
from enum import Enum

from dataclasses import dataclass, field
from dataclasses_json import dataclass_json, LetterCase
import pandas as pd

from .passing_times import Destination


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

    def set_stop_names(self, stops_df, stops_translations_df):
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

    def set_route_type(self, routes_df):
        try:
            self.route_type = RouteType(
                routes_df[routes_df["route_short_name"] == self.line_id].iloc[0][
                    "route_type"
                ]
            )
        except:
            # Hardcode the route type if not defined... need to change this later
            self.route_type = RouteType(1)
