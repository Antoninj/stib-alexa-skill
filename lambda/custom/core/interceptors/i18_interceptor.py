from ask_sdk_core.dispatch_components import AbstractRequestInterceptor
from ask_sdk_core.handler_input import HandlerInput
import logging
import gettext

logger = logging.getLogger("Lambda")


class LocalizationInterceptor(AbstractRequestInterceptor):
    def process(self, handler_input):
        # type: (HandlerInput) -> None
        logger.debug("In LocalizationInterceptor")
        locale = handler_input.request_envelope.request.locale
        logger.debug("Locale is {}".format(locale))
        i18n = gettext.translation(
            "base", localedir="../locales", languages=[locale], fallback=True
        )
        handler_input.attributes_manager.request_attributes["_"] = i18n.gettext
