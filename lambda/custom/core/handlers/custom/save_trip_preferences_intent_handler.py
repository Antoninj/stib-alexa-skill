# -*- coding: utf-8 -*-
from ask_sdk_core.dispatch_components import AbstractRequestHandler
from ask_sdk_core.utils import is_request_type, is_intent_name
from ask_sdk_core.handler_input import HandlerInput
from ask_sdk_model import Response
import logging
from ...data import data

logger = logging.getLogger("Lambda")


class SaveTripPreferencesHandler(AbstractRequestHandler):
    """Single handler for save trip preferences Intent."""

    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool

        return is_intent_name("SaveTripPreferencesIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response

        logger.debug("In SaveTripPreferencesHandler")

        # Boilerplate
        _ = handler_input.attributes_manager.request_attributes["_"]
        session_attributes = handler_input.attributes_manager.session_attributes

        # Prepare skill response
        speech = _(data.ELLICIT_LINE_PREFERENCES)
        reprompt = _(data.ELLICIT_LINE_PREFERENCES_REPROMPT)

        # Update repeat prompt
        session_attributes["repeat_prompt"] = speech

        handler_input.response_builder.speak(speech)
        handler_input.response_builder.ask(reprompt)
        return handler_input.response_builder.response
