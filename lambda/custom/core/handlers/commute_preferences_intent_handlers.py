# -*- coding: utf-8 -*-
from ask_sdk_core.dispatch_components import AbstractRequestHandler
from ask_sdk_core.utils import is_intent_name
from ask_sdk_model.dialog_state import DialogState
from ask_sdk_model.dialog.delegate_directive import DelegateDirective
from ask_sdk_model.dialog.dynamic_entities_directive import *
from ask_sdk_model.er.dynamic import Entity, EntityValueAndSynonyms
import logging

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

        entity_value_and_synonyms = EntityValueAndSynonyms(value="LEGRAND")
        entity = Entity(id="1059", name=entity_value_and_synonyms)
        entities = [entity]
        entity_list_items = [EntityListItem(name="STOP_NAME", values=entities)]

        return (
            handler_input.response_builder.add_directive(
                DynamicEntitiesDirective(
                    update_behavior=UpdateBehavior.REPLACE, types=entity_list_items
                )
            )
            .add_directive(DelegateDirective())
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
        stop_id = slots["stop_id"].value
        # save slots into session attributes
        session_attr = handler_input.attributes_manager.session_attributes
        session_attr["favorite_line_id"] = line_id
        session_attr["favorite_stop_id"] = stop_id
        # save session attributes as persistent attributes
        handler_input.attributes_manager.persistent_attributes = session_attr
        handler_input.attributes_manager.save_persistent_attributes()

        speech = (
            "Très bien, je retiendrai que vous prenez la ligne {line_id} à l'arrêt {stop_id}"
            " lors de votre trajet quotidien".format(stop_id=stop_id, line_id=line_id)
        )
        handler_input.response_builder.speak(speech)
        return handler_input.response_builder.response
