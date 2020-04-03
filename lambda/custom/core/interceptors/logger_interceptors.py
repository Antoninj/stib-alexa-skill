from ask_sdk_core.dispatch_components import (
    AbstractRequestInterceptor,
    AbstractResponseInterceptor,
)
from ask_sdk_core.handler_input import HandlerInput
import logging

from ask_sdk_model import Response

logger = logging.getLogger("Lambda")


# Request and Response Loggers
class RequestLogger(AbstractRequestInterceptor):
    """Log the request envelope."""

    def process(self, handler_input):
        # type: (HandlerInput) -> None
        logger.debug("Request Envelope: {}".format(handler_input.request_envelope))


class ResponseLogger(AbstractResponseInterceptor):
    """Log the response envelope."""

    def process(self, handler_input, response):
        # type: (HandlerInput, Response) -> None
        logger.debug("Response: {}".format(response))
