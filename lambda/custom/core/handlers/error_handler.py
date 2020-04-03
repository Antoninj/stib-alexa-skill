from ask_sdk_core.dispatch_components import AbstractExceptionHandler
from ask_sdk_core.handler_input import HandlerInput
import logging

logger = logging.getLogger("Lambda")


class ErrorHandler(AbstractExceptionHandler):
    """Catch All Exception handler.
    This handler catches all kinds of exceptions and prints
    the stack trace on AWS Cloudwatch with the request envelope."""

    def can_handle(self, handler_input, exception):
        # type: (HandlerInput, Exception) -> bool
        return True

    def handle(self, handler_input, exception):
        # type: (HandlerInput, Exception) -> Response
        logger.error(exception, exc_info=True)
        speech_text = "Désolé, je n'ai pas compris votre requête. Pouvez vous répeter s'il vous plait."
        handler_input.response_builder.speak(speech_text).ask(speech_text)
        return handler_input.response_builder.response
