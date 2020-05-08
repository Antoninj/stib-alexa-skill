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

from ask_sdk_core.dispatch_components import AbstractRequestHandler
from ask_sdk_core.utils import is_intent_name
from ask_sdk_model.dialog.delegate_directive import DelegateDirective
from ask_sdk_model.dialog.dynamic_entities_directive import *
from ask_sdk_model.dialog_state import DialogState
from ask_sdk_model.er.dynamic import (Entity, EntityListItem,
                                      EntityValueAndSynonyms, UpdateBehavior)

logger = logging.getLogger("Lambda")


class StartedInProgressCommutePreferencesHandler(AbstractRequestHandler):
    """
    Handler to delegate the commute preferences intent dialog to alexa
    """

    def can_handle(self, handler_input):
        return (
            is_intent_name("CaptureCommutePreferencesIntent")(handler_input)
            and handler_input.request_envelope.request.dialog_state
            != DialogState.COMPLETED
        )

    def handle(self, handler_input):
        logger.debug("In StartedInProgressCommutePreferencesHandler")
        logger.debug(
            "Dialog state %s", handler_input.request_envelope.request.dialog_state
        )
        logger.debug("Slots %s", handler_input.request_envelope.request.intent.slots)

        return handler_input.response_builder.add_directive(
            DelegateDirective()
        ).response


class HasLineIdCommutePreferencesHandler(AbstractRequestHandler):
    """
    Handler to delegate the commute preferences intent dialog to alexa
    """

    def __init__(self, service):
        self.stib_service = service

    def can_handle(self, handler_input):
        return (
            is_intent_name("CaptureCommutePreferencesIntent")(handler_input)
            and handler_input.request_envelope.request.dialog_state
            != DialogState.COMPLETED
            and handler_input.request_envelope.request.intent.slots["line_id"].value
            and not handler_input.request_envelope.request.intent.slots[
                "stop_name"
            ].value
        )

    def handle(self, handler_input):
        logger.debug("In HasLineIdCommutePreferencesHandler")
        logger.debug(
            "Dialog state %s", handler_input.request_envelope.request.dialog_state
        )
        slots = handler_input.request_envelope.request.intent.slots
        logger.debug("Slots %s", handler_input.request_envelope.request.intent.slots)

        # Get list of valid stops for given line
        line_id = slots["line_id"].value
        line_details = self.stib_service.get_stops_by_line_id(line_id)
        logger.debug(line_details)

        entity_value_and_synonyms = EntityValueAndSynonyms(value="ABBAYE")
        entity = Entity(id="5466", name=entity_value_and_synonyms)
        entities = [entity]
        entity_list_items = [EntityListItem(name="STOP_NAME", values=entities)]

        stop_name_elicitation_speech = "Quel est le nom de votre arrêt?"
        reprompt_speech = "Quel est votre arrêt?"
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


class CompletedCommutePreferencesHandler(AbstractRequestHandler):
    """
    Handler for the commute preferences completed intent
    """

    def can_handle(self, handler_input):
        return (
            is_intent_name("CaptureCommutePreferencesIntent")(handler_input)
            and handler_input.request_envelope.request.dialog_state
            == DialogState.COMPLETED
        )

    def handle(self, handler_input):
        logger.debug("In CompletedCommutePreferencesHandler")
        logger.debug(
            "Dialog state %s", handler_input.request_envelope.request.dialog_state
        )
        slots = handler_input.request_envelope.request.intent.slots
        logger.debug("Slots %s", handler_input.request_envelope.request.intent.slots)
        # extract slot values
        line_id = slots["line_id"].value
        stop_name = slots["stop_name"].value
        # save slots into session attributes
        session_attr = handler_input.attributes_manager.session_attributes
        session_attr["favorite_line_id"] = line_id
        session_attr["favorite_stop_id"] = stop_name
        # save session attributes as persistent attributes
        handler_input.attributes_manager.persistent_attributes = session_attr
        handler_input.attributes_manager.save_persistent_attributes()

        speech = (
            "Très bien, je retiendrai que vous prenez la ligne {line_id} à l'arrêt {stop_id}"
            " lors de votre trajet quotidien".format(stop_id=stop_name, line_id=line_id)
        )
        handler_input.response_builder.speak(speech)
        return handler_input.response_builder.response
