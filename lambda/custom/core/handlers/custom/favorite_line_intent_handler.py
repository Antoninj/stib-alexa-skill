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

import logging
import uuid
from typing import List, Optional

from ask_sdk_core.dispatch_components import AbstractRequestHandler
from ask_sdk_core.handler_input import HandlerInput
from ask_sdk_core.utils import get_dialog_state, get_slot_value, is_intent_name
from ask_sdk_model import Response
from ask_sdk_model.dialog.delegate_directive import DelegateDirective
from ask_sdk_model.dialog.dynamic_entities_directive import *
from ask_sdk_model.dialog_state import DialogState
from ask_sdk_model.er.dynamic import (
    Entity,
    EntityListItem,
    EntityValueAndSynonyms,
    UpdateBehavior,
)

from ...data import data
from ...service.model.line_stops import LineDetails

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
        # Boilerplate
        _ = handler_input.attributes_manager.request_attributes["_"]
        session_attributes = handler_input.attributes_manager.session_attributes

        # Retrieve slot values
        logger.debug("Slots %s", handler_input.request_envelope.request.intent.slots)
        line_id = get_slot_value(handler_input, "line_id")

        # Call STIB API to retrieve line details
        line_details: Optional[
            List[LineDetails]
        ] = self.stib_service.get_stops_by_line_id(line_id)
        logger.debug(line_details)

        # Save line details into session attributes for later use
        session_attributes["session_line_details"] = [
            line_detail.to_dict() for line_detail in line_details
        ]

        # Retrieve destinations from line details
        destinations = [line_detail.destination.fr for line_detail in line_details]
        # Retrieve transportation_type from line details
        stib_transportation_type = line_details[0].route_type.name.lower()
        logger.debug("Transportation type: %s", stib_transportation_type)

        # Save attributes as session attributes
        session_attributes["favorite_line_id"] = line_id
        session_attributes["favorite_transportation_type"] = stib_transportation_type

        # Prepare skill response
        speech = _(data.ELLICIT_DESTINATION_PREFERENCES).format(
            stib_transportation_type, line_id, *destinations
        )
        reprompt_speech = _(data.ELLICIT_DESTINATION_PREFERENCES_REPROMPT).format(
            *destinations
        )
        # Update repeat prompt
        session_attributes["repeat_prompt"] = reprompt_speech

        # Build entity list items to update model using dynamic entities
        entity_list_items = self._build_entity_list_items_from_line_details(
            line_details
        )
        return (
            handler_input.response_builder.add_directive(
                DynamicEntitiesDirective(
                    update_behavior=UpdateBehavior.REPLACE, types=entity_list_items
                )
            )
            .speak(speech)
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

        points = line_details[0].points + line_details[1].points
        destinations = [line.destination for line in line_details]
        stop_entities = [
            Entity(id=point.id, name=EntityValueAndSynonyms(value=point.stop_name_fr))
            for point in points
        ]
        # Todo: use destination stop id instead of generated ID
        destination_entities = [
            Entity(
                id=str(uuid.uuid4()), name=EntityValueAndSynonyms(value=destination.fr)
            )
            for destination in destinations
        ]
        entity_list_items = [
            EntityListItem(name="STOP_NAME", values=stop_entities),
            EntityListItem(name="DESTINATION_NAME", values=destination_entities),
        ]
        return entity_list_items
