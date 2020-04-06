# -*- coding: utf-8 -*-
from typing import List, Optional

from ask_sdk_core.dispatch_components import AbstractRequestHandler
from ask_sdk_core.handler_input import HandlerInput
from ask_sdk_core.utils import (
    is_intent_name,
    get_slot_value,
    get_dialog_state,
    get_slot,
)
from ask_sdk_model import Response, Slot
from ask_sdk_model.dialog_state import DialogState
from ask_sdk_model.dialog.delegate_directive import DelegateDirective
import logging

logger = logging.getLogger("Lambda")


class StartedInProgressFavoriteStopHandler(AbstractRequestHandler):
    """
    Handler to delegate the favorite stop intent dialog to alexa
    """

    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool

        return (
            is_intent_name("SetFavoriteStopIntent")(handler_input)
            and get_dialog_state(handler_input) != DialogState.COMPLETED
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

        return (
            is_intent_name("SetFavoriteStopIntent")(handler_input)
            and get_dialog_state(handler_input) == DialogState.COMPLETED
        )

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        logger.debug("In CompletedFavoriteStopHandler")
        persistent_attributes = handler_input.attributes_manager.persistent_attributes
        session_attributes = handler_input.attributes_manager.session_attributes

        logger.debug("Slots %s", handler_input.request_envelope.request.intent.slots)

        # Todo: retrieve this properly via entity resolution results
        destination_name = get_slot_value(handler_input, "destination_name").upper()
        logger.debug("Destination: %s", destination_name)
        stop_name_slot = get_slot(handler_input, "stop_name")
        session_line_details = session_attributes["session_line_details"]
        success_slot_er_results = self._parse_successful_entity_resolution_results_for_slot(
            stop_name_slot
        )
        correct_slot_value = self._filter_correct_slot_value(
            success_slot_er_results, session_line_details, destination_name
        )
        logger.debug("Correct stop name slot value: %s", correct_slot_value)

        stop_id = correct_slot_value["id"]
        stop_name = correct_slot_value["stopName"]

        persistent_attributes["favorite_stop_id"] = stop_id
        line_id = persistent_attributes["favorite_line_id"]
        stib_transportation_type = persistent_attributes["favorite_transportation_type"]

        handler_input.attributes_manager.save_persistent_attributes()

        intent_complete_speech = (
            "Merci, vos préférences ont été correctement sauvegardées. Vous prenez donc le {} {} direction {}"
            " à l'arret {}".format(
                stib_transportation_type, line_id, destination_name, stop_name,
            )
        )

        return handler_input.response_builder.speak(intent_complete_speech).response

    @staticmethod
    def _parse_successful_entity_resolution_results_for_slot(
        slot: Optional[Slot],
    ) -> dict:
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
        slot_success_er_results: dict,
        serialized_line_details: List,
        destination_name: str,
    ) -> dict:
        correct_destination_line_details = list(
            filter(
                lambda line_detail: line_detail["destination"]["fr"]
                == destination_name,
                serialized_line_details,
            )
        )[-1]
        plausible_stop_ids = [
            item["value"]["id"] for item in slot_success_er_results["values"]
        ]
        correct_slot_value = list(
            filter(
                lambda point: point["id"] in plausible_stop_ids,
                correct_destination_line_details["points"],
            )
        )[-1]
        return correct_slot_value
