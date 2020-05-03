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

import csv
import io
import logging
from typing import List, Optional
from enum import Enum

from dataclasses import dataclass, field
from dataclasses_json import dataclass_json, LetterCase

from .passing_times import Destination

logger = logging.getLogger("Lambda")

NOT_FOUND = "NOT FOUND"


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
        self.stop_name = self.set_generic_stop_name(stops_csv_file)
        self.stop_name_fr = self.set_stop_name_fr(translations_csv_file)
        self.stop_name_nl = self.set_stop_name_nl(translations_csv_file)

    def set_generic_stop_name(self, stops_csv_file: io.BytesIO) -> str:
        reader = csv.reader(stops_csv_file.getvalue().decode("utf-8").splitlines())
        for stop_info in reader:
            if stop_info[0] == self.id:
                return stop_info[2]
        return NOT_FOUND

    def set_stop_name_fr(self, translations_csv_file: io.BytesIO) -> str:
        reader = csv.reader(
            translations_csv_file.getvalue().decode("utf-8").splitlines()
        )
        for translation_info in reader:
            if translation_info[0] == self.stop_name and translation_info[2] == "fr":
                return translation_info[1]
        return NOT_FOUND

    def set_stop_name_nl(self, translations_csv_file: io.BytesIO) -> str:
        reader = csv.reader(
            translations_csv_file.getvalue().decode("utf-8").splitlines()
        )
        for translation_info in reader:
            if translation_info[0] == self.stop_name and translation_info[2] == "nl":
                return translation_info[1]
        return NOT_FOUND


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
        reader = csv.reader(routes_csv_file.getvalue().decode("utf-8").splitlines())
        for route_info in reader:
            if route_info[1] == self.line_id:
                self.route_type = RouteType(int(route_info[4]))

        # Hardcode the route type if not defined... need to change this later
        if not self.route_type:
            self.route_type = RouteType(1)
