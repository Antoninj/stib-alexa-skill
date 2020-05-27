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

from ask_sdk_core.dispatch_components import AbstractRequestHandler
from ask_sdk_core.handler_input import HandlerInput
from ask_sdk_core.utils import is_intent_name
from aws_lambda_powertools.logging import Logger
from aws_lambda_powertools.tracing import Tracer
from requests import Response

# Logging/tracing configuration
logger = Logger(service="Repeat Amazon handler")
tracer = Tracer(service="Repeat Amazon handler")


class RepeatHandler(AbstractRequestHandler):
    """Handler for Repeat Intent."""

    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool

        return is_intent_name("AMAZON.RepeatIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response

        logger.debug("In RepeatIntentHandler")

        session_attributes = handler_input.attributes_manager.session_attributes
        # Get last prompt from session attributes
        repeat_text = session_attributes["repeat_prompt"]

        handler_input.response_builder.speak(repeat_text).set_should_end_session(False)
        return handler_input.response_builder.response
