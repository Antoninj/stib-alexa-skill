# -*- coding: utf-8 -*-
from ask_sdk_core.dispatch_components import AbstractRequestHandler
from ask_sdk_core.utils import is_request_type
from ask_sdk_core.handler_input import HandlerInput
from ask_sdk_model import Response
import logging
from ..data import data

logger = logging.getLogger("Lambda")


class LaunchRequestHandler(AbstractRequestHandler):
    """Handler for Skill Launch."""

    # Todo: Make this two different launch handlers

    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool

        return is_request_type("LaunchRequest")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response

        logger.debug("In LaunchRequestHandler")
        _ = handler_input.attributes_manager.request_attributes["_"]
        persistent_attributes = handler_input.attributes_manager.persistent_attributes
        session_attributes = handler_input.attributes_manager.session_attributes

        logger.debug(persistent_attributes)

        if not persistent_attributes:
            speech = _(data.WELCOME_NEW_USER)
            speech += " " + _(data.SKILL_DESCRIPTION_WITHOUT_PREFERENCES)
            speech += " " + _(data.ASK_FOR_PREFERENCES)
            reprompt = _(data.ASK_FOR_PREFERENCES_REPROMPT)
        else:
            speech = _(data.WELCOME_RETURNING_USER)
            speech += " " + _(data.SKILL_DESCRIPTION_WITH_PREFERENCES)
            reprompt = _(data.SKILL_DESCRIPTION_WITH_PREFERENCES_REPROMPT)

        session_attributes["repeat_prompt"] = speech

        handler_input.response_builder.speak(speech)
        handler_input.response_builder.ask(reprompt)
        return handler_input.response_builder.response
