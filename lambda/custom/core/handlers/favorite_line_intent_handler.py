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
        # Todo: Add try/catch statements for error handling
        line_id = get_slot_value(handler_input, "line_id")
        line_details = self.stib_service.get_stops_by_line_id(line_id)
        logger.debug(line_details)

        entity_list_items = self._build_entity_list_items_from_line_details(
            line_details
        )

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

        # save line details into session attributes for later use
        session_attr["session_line_details"] = [
            line_detail.to_dict() for line_detail in line_details
        ]

        destinations = [line_detail.destination.fr for line_detail in line_details]

        destination_elicitation_speech = "C'est noté. Dans quelle direction prenez vous le {} {}, {} ou {}?".format(
            stib_transportation_type, line_id, *destinations
        )
        reprompt_speech = "Dans quelle direction allez vous, {} ou {}?".format(
            *destinations
        )

        return (
            handler_input.response_builder.add_directive(
                DynamicEntitiesDirective(
                    update_behavior=UpdateBehavior.REPLACE, types=entity_list_items
                )
            )
            .speak(destination_elicitation_speech)
            .ask(reprompt_speech)
            .response
        )

    @staticmethod
    def _build_entity_list_items_from_line_details(
        line_details: List[LineDetails],
    ) -> List[EntityListItem]:
        """
        Create list of dynamic entity items from line details
        """

        # todo: refine this to add try/catch statements and validations
        points = line_details[0].points + line_details[1].points
        destinations = [line.destination for line in line_details]

        stop_entities = [
            Entity(id=point.id, name=EntityValueAndSynonyms(value=point.stop_name))
            for point in points
        ]
        destination_entities = [
            Entity(id=destination.fr, name=EntityValueAndSynonyms(value=destination.fr))
            for destination in destinations
        ]
        entity_list_items = [
            EntityListItem(name="STOP_NAME", values=stop_entities),
            EntityListItem(name="DESTINATION_NAME", values=destination_entities),
        ]
        return entity_list_items
