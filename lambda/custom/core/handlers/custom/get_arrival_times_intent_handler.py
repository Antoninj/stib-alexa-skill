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

from typing import List, Optional
import logging

from ask_sdk_core.dispatch_components import AbstractRequestHandler
from ask_sdk_core.handler_input import HandlerInput
from ask_sdk_core.utils import is_intent_name
from ask_sdk_model import Response

from ...data import data
from ...service.model.passing_times import PassingTime

logger = logging.getLogger("Lambda")


class GetArrivalTimesNoPrefsIntentHandler(AbstractRequestHandler):
    """Handler for get arrival time Intent: no available preferences scenario."""

    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool

        # Extract persistent attributes and check if they are all present
        attr = handler_input.attributes_manager.persistent_attributes
        attributes_are_present = (
            "favorite_stop_id" in attr and "favorite_line_id" in attr
        )
        return not attributes_are_present and is_intent_name("GetArrivalTimesIntent")(
            handler_input
        )

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response

        logger.debug("In GetArrivalTimesNoPrefsIntentHandler")
        _ = handler_input.attributes_manager.request_attributes["_"]
        session_attributes = handler_input.attributes_manager.session_attributes

        # Prepare skill response
        speech = _(data.WELCOME_NEW_USER)
        speech += " " + _(data.SKILL_DESCRIPTION_WITHOUT_PREFERENCES)
        speech += " " + _(data.ASK_FOR_PREFERENCES)
        reprompt = _(data.ASK_FOR_PREFERENCES_REPROMPT)
        session_attributes["repeat_prompt"] = reprompt

        handler_input.response_builder.speak(speech)
        handler_input.response_builder.ask(reprompt)
        return handler_input.response_builder.response


class GetArrivalTimesIntentHandler(AbstractRequestHandler):
    """Handler for get arrival time Intent: happy flow scenario."""

    def __init__(self, service):
        self.stib_service = service

    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool

        # Extract required persistent attributes and check if they are all defined
        attr = handler_input.attributes_manager.persistent_attributes
        attributes_are_present = (
            "favorite_stop_id" in attr and "favorite_line_id" in attr
        )
        return attributes_are_present and is_intent_name("GetArrivalTimesIntent")(
            handler_input
        )

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response

        logger.debug("In GetArrivalTimesIntentHandler")

        # Boilerplate
        _ = handler_input.attributes_manager.request_attributes["_"]
        persistent_attributes = handler_input.attributes_manager.persistent_attributes
        session_attributes = handler_input.attributes_manager.session_attributes

        # Retrieve user preferences from persistent storage
        logger.debug("Slots: %s", handler_input.request_envelope.request.intent.slots)
        logger.debug("Persistent attributes: %s", persistent_attributes)
        favorite_stop_id = persistent_attributes["favorite_stop_id"]
        favorite_line_id = persistent_attributes["favorite_line_id"]
        favorite_transportation_type = persistent_attributes[
            "favorite_transportation_type"
        ]

        # Call STIB API to retrieve arrival times
        # Todo: Add try/except statements for error handling
        passing_times: Optional[
            List[PassingTime]
        ] = self.stib_service.get_passing_times_for_stop_id_and_line_id(
            stop_id=favorite_stop_id, line_id=favorite_line_id
        )
        logger.debug(passing_times)

        # Prepare skill response
        speech_text = self._format_waiting_times(
            passing_times=passing_times,
            transportation_type=favorite_transportation_type,
            translate=_,
        )
        speech_text += " " + _(data.FAREWELL)

        # Update repeat prompt
        session_attributes["repeat_prompt"] = speech_text

        handler_input.response_builder.speak(speech_text).set_should_end_session(True)
        return handler_input.response_builder.response

    @staticmethod
    def _format_waiting_times(
        passing_times: List[PassingTime], transportation_type: str, translate
    ) -> str:
        """Define method here."""
        if len(passing_times) == 2:
            formatted_waiting_times = (
                GetArrivalTimesIntentHandler._format_first_waiting_time(
                    passing_times[0], transportation_type, translate=translate
                )
                + " "
                + GetArrivalTimesIntentHandler._format_second_waiting_time(
                    passing_times[1], translate=translate
                )
            )
        elif len(passing_times) == 1:
            formatted_waiting_times = GetArrivalTimesIntentHandler._format_first_waiting_time(
                passing_times[0], transportation_type, translate=translate
            )
        else:
            formatted_waiting_times = translate(data.NO_INFORMATION_FOUND)
        return formatted_waiting_times

    @staticmethod
    def _format_first_waiting_time(
        passing_time: PassingTime, transportation_type: str, translate
    ) -> str:
        """Define method here."""
        logger.debug(passing_time.arriving_in_dict)
        formatted_waiting_time = translate(data.FIRST_ARRIVAL_TIME_INFO).format(
            transportation_type,
            passing_time.line_id,
            passing_time.destination.fr.lower(),
            passing_time.format_waiting_time(translate=translate),
        )
        return formatted_waiting_time

    @staticmethod
    def _format_second_waiting_time(passing_time: PassingTime, translate) -> str:
        """Define method here."""
        formatted_waiting_time = translate(data.SECOND_ARRIVAL_TIME_INFO).format(
            passing_time.format_waiting_time(translate=translate)
        )
        return formatted_waiting_time
