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

from typing import List, Optional, Dict

from ask_sdk_core.dispatch_components import AbstractRequestHandler
from ask_sdk_core.handler_input import HandlerInput
from ask_sdk_core.utils import (
    get_dialog_state,
    get_slot,
    get_slot_value,
    is_intent_name,
)
from ask_sdk_model import Response, Slot
from ask_sdk_model.dialog.delegate_directive import DelegateDirective
from ask_sdk_model.dialog_state import DialogState
from aws_lambda_powertools.logging import Logger
from aws_lambda_powertools.tracing import Tracer

from ...data import data

# Logging/tracing configuration
logger = Logger(service="Favorite stop intent handler")
tracer = Tracer(service="Favorite stop intent handler")


class StartedInProgressFavoriteStopHandler(AbstractRequestHandler):
    """
    Handler to delegate the favorite stop intent dialog to alexa
    """

    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool

        attr = handler_input.attributes_manager.session_attributes
        session_attributes_are_present = (
            "favorite_transportation_type" in attr and "favorite_line_id" in attr
        )
        return (
            is_intent_name("SetFavoriteStopIntent")(handler_input)
            and get_dialog_state(handler_input) != DialogState.COMPLETED
            and session_attributes_are_present
        )

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response

        logger.debug("In StartedInProgressFavoriteStopHandler")
        logger.debug(
            "Dialog state %s", handler_input.request_envelope.request.dialog_state
        )
        logger.debug("Slots %s", handler_input.request_envelope.request.intent.slots)

        return handler_input.response_builder.add_directive(
            DelegateDirective()
        ).response


class CompletedFavoriteStopHandler(AbstractRequestHandler):
    """
    Handler for the favorite stop completed intent
    """

    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool

        attr = handler_input.attributes_manager.session_attributes
        session_attributes_are_present = (
            "favorite_transportation_type" in attr and "favorite_line_id" in attr
        )
        return (
            is_intent_name("SetFavoriteStopIntent")(handler_input)
            and get_dialog_state(handler_input) == DialogState.COMPLETED
            and session_attributes_are_present
        )

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response

        logger.debug("In CompletedFavoriteStopHandler")

        # Boilerplate
        _ = handler_input.attributes_manager.request_attributes["_"]
        persistent_attributes = handler_input.attributes_manager.persistent_attributes
        session_attributes = handler_input.attributes_manager.session_attributes

        # Retrieve slot values
        logger.debug("Slots %s", handler_input.request_envelope.request.intent.slots)
        # Todo: retrieve this properly via entity resolution results
        destination_name = get_slot_value(handler_input, "destination_name")
        logger.debug("Destination: %s", destination_name)
        stop_name_slot = get_slot(handler_input, "stop_name")
        success_slot_er_results = self._parse_successful_entity_resolution_results_for_slot(
            stop_name_slot
        )
        session_line_details = session_attributes["session_line_details"]
        correct_slot_value = self._filter_correct_slot_value(
            success_slot_er_results, session_line_details, destination_name
        )
        logger.debug("Correct stop name slot value: %s", correct_slot_value)
        stop_id = correct_slot_value["id"]
        stop_name_fr = correct_slot_value["stopNameFr"]
        line_id = session_attributes["favorite_line_id"]
        stib_transportation_type = session_attributes["favorite_transportation_type"]

        # Update persistent attributes
        persistent_attributes["favorite_transportation_type"] = stib_transportation_type
        persistent_attributes["favorite_line_id"] = line_id
        persistent_attributes["favorite_line_destination"] = destination_name
        persistent_attributes["favorite_stop_id"] = stop_id
        persistent_attributes["favorite_stop_name"] = stop_name_fr
        handler_input.attributes_manager.save_persistent_attributes()

        # Prepare skill response
        speech = _(data.PREFERENCES_SAVED).format(
            stib_transportation_type, line_id, stop_name_fr, destination_name
        )
        reprompt_speech = _(data.SKILL_DESCRIPTION_WITH_PREFERENCES)
        speech += " " + reprompt_speech

        # Update repeat prompt
        session_attributes["repeat_prompt"] = reprompt_speech

        return (
            handler_input.response_builder.speak(speech).ask(reprompt_speech).response
        )

    @staticmethod
    def _parse_successful_entity_resolution_results_for_slot(
        slot: Optional[Slot],
    ) -> Dict:
        """Parse successful ER results."""

        entity_resolutions = {"values": [], "resolved": slot.value}
        success_entity_resolutions = [
            resolution_per_authority.values
            for resolution_per_authority in slot.resolutions.resolutions_per_authority
            if resolution_per_authority.status.code.value == "ER_SUCCESS_MATCH"
        ]
        flatten_success_entity_resolutions = [
            item.to_dict() for sublist in success_entity_resolutions for item in sublist
        ]
        entity_resolutions["values"] = flatten_success_entity_resolutions
        return entity_resolutions

    @staticmethod
    def _filter_correct_slot_value(
        slot_success_er_results: Dict,
        serialized_line_details: List,
        destination_name: str,
    ) -> Dict:
        """Find correct stop name based on ER results and destination slot value."""

        correct_destination_line_details = [
            line_detail
            for line_detail in serialized_line_details
            if line_detail["destination"]["fr"] == destination_name.upper()
        ][-1]

        plausible_stop_ids = [
            item["value"]["id"] for item in slot_success_er_results["values"]
        ]
        correct_slot_value = [
            point
            for point in correct_destination_line_details["points"]
            if point["id"] in plausible_stop_ids
        ][-1]
        return correct_slot_value
