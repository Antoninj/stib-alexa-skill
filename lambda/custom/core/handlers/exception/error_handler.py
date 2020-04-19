import logging

from ask_sdk_core.dispatch_components import AbstractExceptionHandler
from ask_sdk_core.handler_input import HandlerInput

from ...data import data

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
        _ = handler_input.attributes_manager.request_attributes["_"]
        session_attributes = handler_input.attributes_manager.session_attributes
        session_attributes["repeat_prompt"] = _(data.ERROR)
        handler_input.response_builder.speak(_(data.ERROR)).ask(_(data.ERROR_REPROMPT))
        return handler_input.response_builder.response
