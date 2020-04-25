# -*- coding: utf-8 -*-
import csv
import io
import logging
from typing import List, Optional
from enum import Enum

from dataclasses import dataclass, field
from dataclasses_json import dataclass_json, LetterCase

from .passing_times import Destination

logger = logging.getLogger("Lambda")


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

    def set_stop_names(
        self, stops_csv_file: io.BytesIO, translations_csv_file: io.BytesIO
    ):
        # todo: fix this... why the hell is there missing data in the first place?
        try:
            reader = csv.reader(stops_csv_file.getvalue().decode("utf-8").splitlines())
            for stop_info in reader:
                if stop_info[0] == self.id:
                    self.stop_name = stop_info[2]

            reader = csv.reader(
                translations_csv_file.getvalue().decode("utf-8").splitlines()
            )
            for translation_info in reader:
                if (
                    translation_info[0] == self.stop_name
                    and translation_info[2] == "fr"
                ):
                    self.stop_name_fr = translation_info[1]
                if (
                    translation_info[0] == self.stop_name
                    and translation_info[2] == "nl"
                ):
                    self.stop_name_nl = translation_info[1]
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

    def set_route_type(self, routes_csv_file: io.BytesIO):
        try:
            reader = csv.reader(routes_csv_file.getvalue().decode("utf-8").splitlines())
            for route_info in reader:
                if route_info[1] == self.line_id:
                    self.route_type = RouteType(int(route_info[4]))
        except:
            # Hardcode the route type if not defined... need to change this later
            self.route_type = RouteType(1)
