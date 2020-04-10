from ask_sdk_core.dispatch_components import AbstractRequestHandler
from ask_sdk_core.handler_input import HandlerInput
from ask_sdk_core.utils import is_intent_name
from requests import Response
import logging


logger = logging.getLogger("Lambda")


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
        handler_input.response_builder.speak(repeat_text)
        return handler_input.response_builder.response
