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
from ask_sdk_core.utils import is_request_type
from ask_sdk_core.handler_input import HandlerInput
from ask_sdk_model import Response

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

        session_attributes["repeat_prompt"] = reprompt

        handler_input.response_builder.speak(speech)
        handler_input.response_builder.ask(reprompt)
        return handler_input.response_builder.response
