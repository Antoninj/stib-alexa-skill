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

from ask_sdk_core.dispatch_components import AbstractExceptionHandler
from ask_sdk_core.handler_input import HandlerInput

from ...data import data
from ...service.exceptions import OpenDataServiceException
from ...client.token_helper import TokenException


logger = logging.getLogger("Lambda")


class GenericExceptionHandler(AbstractExceptionHandler):
    """
    Catch All Exception handler.
    This handler catches all kinds of exceptions and prints
    the stack trace on AWS Cloudwatch with the request envelope.
    """

    def can_handle(self, handler_input, exception):
        # type: (HandlerInput, Exception) -> bool

        return True

    def handle(self, handler_input, exception):
        # type: (HandlerInput, Exception) -> Response

        logger.error(exception, exc_info=True)
        _ = handler_input.attributes_manager.request_attributes["_"]
        session_attributes = handler_input.attributes_manager.session_attributes
        session_attributes["repeat_prompt"] = _(data.GENERIC_ERROR)
        handler_input.response_builder.speak(_(data.GENERIC_ERROR)).ask(
            _(data.GENERIC_ERROR_REPROMPT)
        )
        return handler_input.response_builder.response


class OpenDataAPIExceptionHandler(AbstractExceptionHandler):
    """
    Exception handler for Open Data API exceptions.
    """

    def can_handle(self, handler_input, exception):
        # type: (HandlerInput, OpenDataServiceException) -> bool

        return isinstance(exception, OpenDataServiceException) or isinstance(
            exception, TokenException
        )

    def handle(self, handler_input, exception):
        # type: (HandlerInput, e) -> Response

        logger.error(exception, exc_info=True)
        _ = handler_input.attributes_manager.request_attributes["_"]
        session_attributes = handler_input.attributes_manager.session_attributes
        session_attributes["repeat_prompt"] = _(data.OPEN_DATA_API_ERROR)
        handler_input.response_builder.speak(_(data.OPEN_DATA_API_ERROR_REPROMPT)).ask(
            _(data.OPEN_DATA_API_ERROR_REPROMPT)
        )
        return handler_input.response_builder.response
