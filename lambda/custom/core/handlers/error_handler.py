from ask_sdk_core.dispatch_components import AbstractExceptionHandler
from ask_sdk_core.handler_input import HandlerInput
import logging

logger = logging.getLogger("Lambda")


# Generic error handling to capture any syntax or routing errors. If you receive an error
# stating the request handler chain is not found, you have not implemented a handler for
# the intent being invoked or included it in the skill builder below.
class ErrorHandler(AbstractExceptionHandler):
    """Catch-all exception handler, log exception and
    respond with custom message.
    """

    def can_handle(self, handler_input, exception):
        # type: (HandlerInput, Exception) -> bool
        return True

    def handle(self, handler_input, exception):
        # type: (HandlerInput, Exception) -> Response
        logger.error(exception, exc_info=True)
        speech_text = "Désolé, je n'ai pas compris votre requête. Pouvez vous répeter s'il vous plait."
        handler_input.response_builder.speak(speech_text).ask(speech_text)
        return handler_input.response_builder.response
