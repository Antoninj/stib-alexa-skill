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

import gettext

from ask_sdk_core.dispatch_components import AbstractRequestInterceptor
from ask_sdk_core.handler_input import HandlerInput
from ask_sdk_core.utils import get_locale
from aws_lambda_powertools.logging import Logger
from aws_lambda_powertools.tracing import Tracer

# Logging/tracing configuration
logger = Logger(service="i18n interceptor")
tracer = Tracer(service="i18n interceptor")


class LocalizationInterceptor(AbstractRequestInterceptor):
    """Request interceptor to handle multiple locales."""

    def process(self, handler_input):
        """Parse locale information and add i18n manager to the request attributes."""

        # type: (HandlerInput) -> None
        logger.debug("In LocalizationInterceptor")
        locale = get_locale(handler_input)
        logger.debug({"Locale": locale})
        i18n = gettext.translation(
            "base", localedir="core/locales/", languages=[locale], fallback=True
        )
        handler_input.attributes_manager.request_attributes["_"] = i18n.gettext
