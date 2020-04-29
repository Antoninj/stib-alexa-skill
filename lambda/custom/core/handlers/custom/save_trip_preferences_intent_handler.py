# -*- coding: utf-8 -*-

#   Copyright 2020 Antonin Jousson
#
#  Licensed under the Apache License, Version 2.0 (the "License").
#  You may not use this file except in compliance with the License.
#  A copy of the License is located at
#
#  http://aws.amazon.com/apache2.0/
#
#  or in the "license" file accompanying this file. This file is
#  distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS
#  OF ANY KIND, either express or implied. See the License for the
#  specific language governing permissions and limitations under the
#  License.

import logging

from ask_sdk_core.dispatch_components import AbstractRequestHandler
from ask_sdk_core.utils import is_request_type, is_intent_name
from ask_sdk_core.handler_input import HandlerInput
from ask_sdk_model import Response

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
