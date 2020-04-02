# -*- coding: utf-8 -*-
from ask_sdk_core.dispatch_components import AbstractRequestHandler
from ask_sdk_core.utils import is_request_type, is_intent_name
from ask_sdk_core.handler_input import HandlerInput
from ask_sdk_model import Response
import logging
from ..data import data

logger = logging.getLogger("Lambda")


class HelpIntentHandler(AbstractRequestHandler):
    """Handler for Help Intent."""

    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return is_intent_name("AMAZON.HelpIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        logger.debug("In HelpIntentHandler")
        _ = handler_input.attributes_manager.request_attributes["_"]

        handler_input.response_builder.speak(_(data.HELP)).ask(_(data.HELP))
        return handler_input.response_builder.response


class CancelOrStopIntentHandler(AbstractRequestHandler):
    """Single handler for Cancel and Stop Intent."""

    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return is_intent_name("AMAZON.CancelIntent")(handler_input) or is_intent_name(
            "AMAZON.StopIntent"
        )(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        logger.debug("In CancelOrStopIntentHandler")
        _ = handler_input.attributes_manager.request_attributes["_"]

        handler_input.response_builder.speak(_(data.STOP)).set_should_end_session(True)
        return handler_input.response_builder.response


class SessionEndedRequestHandler(AbstractRequestHandler):
    """Handler for Session End."""

    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return is_request_type("SessionEndedRequest")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        logger.debug("In SessionEndedRequestHandler")
        logger.debug(
            "Session ended with reason: {}".format(
                handler_input.request_envelope.request.reason
            )
        )
        return handler_input.response_builder.response
