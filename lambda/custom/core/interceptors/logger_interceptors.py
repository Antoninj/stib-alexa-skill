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

from ask_sdk_core.dispatch_components import (AbstractRequestInterceptor,
                                              AbstractResponseInterceptor)
from ask_sdk_core.handler_input import HandlerInput
from ask_sdk_model import Response
from aws_lambda_powertools.logging import Logger
from aws_lambda_powertools.tracing import Tracer

# Logging/tracing configuration
logger = Logger(service="Logger interceptor")
tracer = Tracer(service="Logger interceptor")


class RequestLoggerInterceptor(AbstractRequestInterceptor):
    """Request Interceptor for logging purposes."""

    def process(self, handler_input):
        """Log the request envelope."""

        # type: (HandlerInput) -> None
        logger.debug({"Request Envelope": handler_input.request_envelope})


class ResponseLoggerInterceptor(AbstractResponseInterceptor):
    """Response Interceptor for logging purposes."""

    def process(self, handler_input, response):
        """Log the response envelope."""

        # type: (HandlerInput, Response) -> None
        logger.debug({"Response": response})
