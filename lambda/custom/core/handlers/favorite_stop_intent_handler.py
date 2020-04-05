# -*- coding: utf-8 -*-
from ask_sdk_core.dispatch_components import AbstractRequestHandler
from ask_sdk_core.handler_input import HandlerInput
from ask_sdk_core.utils import is_intent_name, get_slot_value, get_dialog_state
from ask_sdk_model import Response
from ask_sdk_model.dialog_state import DialogState
from ask_sdk_model.dialog.delegate_directive import DelegateDirective
import logging

logger = logging.getLogger("Lambda")


class StartedInProgressFavoriteStopHandler(AbstractRequestHandler):
    """
    Handler to delegate the favorite line intent dialog to alexa
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
    Handler for the favorite line completed intent
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
        slots = handler_input.request_envelope.request.intent.slots
        logger.debug("Slots %s", handler_input.request_envelope.request.intent.slots)

        # Get intent slots value
        destination_name = get_slot_value(handler_input, "destination_name")
        stop_name = get_slot_value(handler_input, "stop_name")

        # Retrieve session attributes
        session_attr = handler_input.attributes_manager.session_attributes
        session_line_details = session_attr["session_line_details"]

        # save session attributes as persistent attributes
        # handler_input.attributes_manager.persistent_attributes = session_attr
        # handler_input.attributes_manager.save_persistent_attributes()

        intent_complete_speech = (
            "Merci, vos préférences ont été correctement sauvegardées."
        )

        return handler_input.response_builder.speak(intent_complete_speech).response
