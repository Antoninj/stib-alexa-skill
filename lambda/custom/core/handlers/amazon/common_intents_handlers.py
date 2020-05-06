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
from ask_sdk_core.handler_input import HandlerInput
from ask_sdk_core.utils import is_intent_name, is_request_type
from ask_sdk_model import Response

from ...data import data

logger = logging.getLogger("Lambda")


class YesIntentHandler(AbstractRequestHandler):
    """Single handler for Yes Intent."""

    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        _ = handler_input.attributes_manager.request_attributes["_"]
        session_attributes = handler_input.attributes_manager.session_attributes

        return session_attributes["repeat_prompt"] == _(
            data.ASK_FOR_PREFERENCES_REPROMPT
        ) and is_intent_name("AMAZON.YesIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response

        logger.debug("In YesIntentHandler")
        _ = handler_input.attributes_manager.request_attributes["_"]
        session_attributes = handler_input.attributes_manager.session_attributes

        speech = _(data.ELLICIT_LINE_PREFERENCES)
        reprompt = _(data.ELLICIT_LINE_PREFERENCES_REPROMPT)
        session_attributes["repeat_prompt"] = reprompt

        handler_input.response_builder.speak(speech)
        handler_input.response_builder.ask(reprompt)
        return handler_input.response_builder.response


class NoIntentHandler(AbstractRequestHandler):
    """Single handler for No Intent."""

    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool

        return is_intent_name("AMAZON.NoIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response

        logger.debug("In NoIntentHandler")
        _ = handler_input.attributes_manager.request_attributes["_"]
        handler_input.response_builder.speak(_(data.STOP)).set_should_end_session(True)
        return handler_input.response_builder.response


class HelpIntentHandler(AbstractRequestHandler):
    """Handler for Help Intent."""

    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool

        return is_intent_name("AMAZON.HelpIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response

        logger.debug("In HelpIntentHandler")
        _ = handler_input.attributes_manager.request_attributes["_"]

        session_attributes = handler_input.attributes_manager.session_attributes
        speech = _(data.HELP)
        session_attributes["repeat_prompt"] = speech

        handler_input.response_builder.speak(speech).ask(_(data.HELP_REPROMPT))
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
