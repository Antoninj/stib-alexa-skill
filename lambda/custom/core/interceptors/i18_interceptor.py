from ask_sdk_core.dispatch_components import AbstractRequestInterceptor
from ask_sdk_core.handler_input import HandlerInput
from ask_sdk_core.utils import get_locale

import logging
import gettext

logger = logging.getLogger("Lambda")


class LocalizationInterceptor(AbstractRequestInterceptor):
    """Define class here."""

    def process(self, handler_input):
        # type: (HandlerInput) -> None
        logger.debug("In LocalizationInterceptor")
        locale = get_locale(handler_input)
        logger.debug("Locale is {}".format(locale))
        i18n = gettext.translation(
            "base", localedir="../locales", languages=[locale], fallback=True
        )
        handler_input.attributes_manager.request_attributes["_"] = i18n.gettext
