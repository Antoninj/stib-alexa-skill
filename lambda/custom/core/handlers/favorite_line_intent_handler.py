# -*- coding: utf-8 -*-
from ask_sdk_core.dispatch_components import AbstractRequestHandler
from ask_sdk_core.handler_input import HandlerInput
from ask_sdk_core.utils import is_intent_name, get_dialog_state, get_slot_value
from ask_sdk_model import Response
from ask_sdk_model.dialog_state import DialogState
from ask_sdk_model.dialog.delegate_directive import DelegateDirective
from ask_sdk_model.dialog.dynamic_entities_directive import *
from ask_sdk_model.er.dynamic import (
    Entity,
    EntityValueAndSynonyms,
    EntityListItem,
    UpdateBehavior,
)
from typing import List
from ..service.model.line_stops import LineDetails
import logging

logger = logging.getLogger("Lambda")


class StartedInProgressFavoriteLineHandler(AbstractRequestHandler):
    """
    Handler to delegate the favorite line intent dialog to alexa
    """

    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool

        return (
            is_intent_name("SetFavoriteLineIntent")(handler_input)
            and get_dialog_state(handler_input) != DialogState.COMPLETED
        )

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response

        logger.debug("In StartedInProgressFavoriteLineHandler")
        logger.debug(
            "Dialog state %s", handler_input.request_envelope.request.dialog_state
        )
        logger.debug("Slots %s", handler_input.request_envelope.request.intent.slots)

        return handler_input.response_builder.add_directive(
            DelegateDirective()
        ).response


class CompletedFavoriteLineHandler(AbstractRequestHandler):
    """
    Handler for the favorite line completed intent
    """

    def __init__(self, service):
        self.stib_service = service

    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool

        return (
            is_intent_name("SetFavoriteLineIntent")(handler_input)
            and get_dialog_state(handler_input) == DialogState.COMPLETED
        )

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response

        logger.debug("In CompletedFavoriteLineHandler")
        logger.debug("Slots %s", handler_input.request_envelope.request.intent.slots)

        # Get list of valid stops for given line
        line_id = get_slot_value(handler_input, "line_id")
        line_details = self.stib_service.get_stops_by_line_id(line_id)
        logger.debug(line_details)

        # Hardcode dynamic entities value for now
        stop_entity_value_and_synonyms = EntityValueAndSynonyms(value="ABBAYE")
        stop_entity = Entity(id="5466", name=stop_entity_value_and_synonyms)
        destination_entity_value_and_synonyms = EntityValueAndSynonyms(value="STADE")
        destination_entity = Entity(
            id="5474", name=destination_entity_value_and_synonyms
        )
        entity_list_items = [
            EntityListItem(name="STOP_NAME", values=[stop_entity]),
            EntityListItem(name="DESTINATION_NAME", values=[destination_entity]),
        ]

        # Retrieve transportation_type
        stib_transportation_type = line_details[0].route_type.name.lower()
        logger.debug("Transportation type: %s", stib_transportation_type)

        # save slots into session attributes
        session_attr = handler_input.attributes_manager.session_attributes
        session_attr["favorite_line_id"] = line_id
        session_attr["favorite_transportation_type"] = stib_transportation_type

        # save session attributes as persistent attributes
        handler_input.attributes_manager.persistent_attributes = session_attr
        handler_input.attributes_manager.save_persistent_attributes()

        # save line details into session attributes
        session_attr["session_line_details"] = [
            line_detail.to_dict() for line_detail in line_details
        ]

        stop_name_elicitation_speech = "Dans quelle direction allez vous?"
        reprompt_speech = "Dans quelle direction prenez vous le {} {}?".format(
            stib_transportation_type, line_id
        )

        return (
            handler_input.response_builder.add_directive(
                DynamicEntitiesDirective(
                    update_behavior=UpdateBehavior.REPLACE, types=entity_list_items
                )
            )
            .speak(stop_name_elicitation_speech)
            .ask(reprompt_speech)
            .response
        )

    def _build_entity_list_items_from_line_details(
        self, line_details: List[LineDetails]
    ):
        pass
