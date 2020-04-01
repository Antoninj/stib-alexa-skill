# -*- coding: utf-8 -*-
import gettext
import logging
import os

from ask_sdk_dynamodb.adapter import DynamoDbAdapter
from ask_sdk_core.skill_builder import CustomSkillBuilder
from ask_sdk_core.dispatch_components import (
    AbstractRequestHandler,
    AbstractRequestInterceptor,
)
from ask_sdk_core.dispatch_components import AbstractExceptionHandler
from ask_sdk_core.utils import is_request_type, is_intent_name
from ask_sdk_core.handler_input import HandlerInput
from ask_sdk_model import Response
from ask_sdk_model.dialog_state import DialogState
from ask_sdk_model.dialog.delegate_directive import DelegateDirective

from client.stib_api_client import OpenDataAPIClient
from service.stib_service import OpenDataService
from data import data

import boto3

# Environment variables definitions
ENVIRONMENT = os.environ["env"]
LOGGING_LEVEL = os.environ["log_level"]

# Logging config
logger = logging.getLogger("Lambda")
logger.setLevel(LOGGING_LEVEL)


class LaunchRequestHandler(AbstractRequestHandler):
    """Handler for Skill Launch."""

    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return is_request_type("LaunchRequest")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        logger.debug("In LaunchRequestHandler")
        _ = handler_input.attributes_manager.request_attributes["_"]

        speech = _(data.WELCOME)
        speech += " " + _(data.HELP)
        handler_input.response_builder.speak(speech)
        handler_input.response_builder.ask(_(data.GENERIC_REPROMPT))
        return handler_input.response_builder.response


class StartedInProgressCommutePreferencesHandler(AbstractRequestHandler):
    """
    Handler to delegate the commute preferences intent dialog to alexa
    """

    def can_handle(self, handler_input):
        return (
            is_intent_name("CaptureCommutePreferencesIntent")(handler_input)
            and handler_input.request_envelope.request.dialog_state
            != DialogState.COMPLETED
        )

    def handle(self, handler_input):
        logger.debug("In StartedInProgressCommutePreferencesHandler")
        logger.debug(
            "Dialog state %s", handler_input.request_envelope.request.dialog_state
        )
        return handler_input.response_builder.add_directive(
            DelegateDirective()
        ).response


class CompletedCommutePreferencesHandler(AbstractRequestHandler):
    """
    Handler for the commute preferences completed intent
    """

    def can_handle(self, handler_input):
        return (
            is_intent_name("CaptureCommutePreferencesIntent")(handler_input)
            and handler_input.request_envelope.request.dialog_state
            == DialogState.COMPLETED
        )

    def handle(self, handler_input):

        logger.debug("In CompletedCommutePreferencesHandler")
        logger.debug(
            "Dialog state %s", handler_input.request_envelope.request.dialog_state
        )
        slots = handler_input.request_envelope.request.intent.slots
        logger.debug("Slots %s", handler_input.request_envelope.request.intent.slots)
        # extract slot values
        line_id = slots["line_id"].value
        stop_id = slots["stop_id"].value
        logger.debug("Line id slot value:")
        logger.debug("Stop id slot value:")
        # save slots into session attributes
        session_attr = handler_input.attributes_manager.session_attributes
        session_attr["favorite_line_id"] = line_id
        session_attr["favorite_stop_id"] = stop_id
        # save session attributes as persistent attributes
        handler_input.attributes_manager.persistent_attributes = session_attr
        handler_input.attributes_manager.save_persistent_attributes()

        speech = (
            "Très bien, je retiendrai que vous prenez la ligne {line_id} à l'arrêt {stop_id}"
            " lors de votre trajet quotidien".format(stop_id=stop_id, line_id=line_id)
        )
        handler_input.response_builder.speak(speech)
        return handler_input.response_builder.response


class GetArrivalTimesIntentHandler(AbstractRequestHandler):
    """Handler for get arrival time Intent."""

    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool

        # Extract persistent attributes and check if they are all present
        attr = handler_input.attributes_manager.persistent_attributes
        attributes_are_present = (
            "favorite_stop_id" in attr and "favorite_line_id" in attr
        )

        return attributes_are_present and is_intent_name("GetArrivalTimesIntent")(
            handler_input
        )

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        logger.debug("In GetArrivalTimesIntentHandler")

        persistent_attributes = handler_input.attributes_manager.persistent_attributes
        logger.debug("Persistent attributes found: %s", persistent_attributes)
        favorite_stop_id = persistent_attributes["favorite_stop_id"]
        favorite_line_id = persistent_attributes["favorite_line_id"]
        passing_times = stib_service.get_passing_times_for_stop_id_and_line_id(
            stop_id=favorite_stop_id, line_id=favorite_line_id
        )
        if passing_times:
            speech_text = passing_times[0].formatted_waiting_time
        else:
            speech_text = (
                "Désolé, je n'ai pas trouvé d'informations pour le trajet demandé"
            )

        handler_input.response_builder.speak(speech_text).set_should_end_session(True)
        return handler_input.response_builder.response


class HelpIntentHandler(AbstractRequestHandler):
    """Handler for Help Intent."""

    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return is_intent_name("AMAZON.HelpIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        logger.debug("In HelpIntentHandler")
        _ = handler_input.attributes_manager.request_attributes["_"]

        handler_input.response_builder.speak(_(data.HELP)).ask(_(data.HELP))
        return handler_input.response_builder.response


class CancelOrStopIntentHandler(AbstractRequestHandler):
    """Single handler for Cancel and Stop Intent."""

    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return is_intent_name("AMAZON.CancelIntent")(handler_input) or is_intent_name(
            "AMAZON.StopIntent"
        )(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        logger.debug("In CancelOrStopIntentHandler")
        _ = handler_input.attributes_manager.request_attributes["_"]

        handler_input.response_builder.speak(_(data.STOP)).set_should_end_session(True)
        return handler_input.response_builder.response


class SessionEndedRequestHandler(AbstractRequestHandler):
    """Handler for Session End."""

    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return is_request_type("SessionEndedRequest")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        logger.debug("In SessionEndedRequestHandler")
        logger.debug(
            "Session ended with reason: {}".format(
                handler_input.request_envelope.request.reason
            )
        )
        return handler_input.response_builder.response


# The intent reflector is used for interaction model testing and debugging.
# It will simply repeat the intent the user said. You can create custom handlers
# for your intents by defining them above, then also adding them to the request
# handler chain below.
class IntentReflectorHandler(AbstractRequestHandler):
    """Handler for Hello World Intent."""

    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return is_request_type("IntentRequest")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        intent_name = handler_input.request_envelope.request.intent.name
        speech_text = ("You just triggered {}").format(intent_name)
        handler_input.response_builder.speak(speech_text).set_should_end_session(True)
        return handler_input.response_builder.response


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


class LocalizationInterceptor(AbstractRequestInterceptor):
    def process(self, handler_input):
        # type: (HandlerInput) -> None
        logger.debug("In LocalizationInterceptor")
        locale = handler_input.request_envelope.request.locale
        logger.debug("Locale is {}".format(locale))
        i18n = gettext.translation(
            "base", localedir="locales", languages=[locale], fallback=True
        )
        handler_input.attributes_manager.request_attributes["_"] = i18n.gettext


def setup_skill_builder():
    dynamo_db_adapter = DynamoDbAdapter(
        table_name="DailyCommuteFavorites",
        partition_key_name="id",
        attribute_name="attributes",
        create_table=True,
        dynamodb_resource=boto3.resource("dynamodb"),
    )

    skill_builder = CustomSkillBuilder(persistence_adapter=dynamo_db_adapter)
    skill_builder.add_request_handler(LaunchRequestHandler())
    skill_builder.add_request_handler(GetArrivalTimesIntentHandler())
    skill_builder.add_request_handler(StartedInProgressCommutePreferencesHandler())
    skill_builder.add_request_handler(CompletedCommutePreferencesHandler())
    skill_builder.add_request_handler(HelpIntentHandler())
    skill_builder.add_request_handler(CancelOrStopIntentHandler())
    skill_builder.add_request_handler(SessionEndedRequestHandler())
    skill_builder.add_request_handler(IntentReflectorHandler())
    # make sure IntentReflectorHandler is last so it doesn't override your custom intent handlers

    skill_builder.add_exception_handler(ErrorHandler())
    skill_builder.add_global_request_interceptor(LocalizationInterceptor())

    return skill_builder


def local_test():
    # Test STIB API integration
    passing_times = stib_service.get_passing_times_for_stop_id_and_line_id()
    logger.info(passing_times[0].formatted_waiting_time)

    # Test i18n
    i18n = gettext.translation(
        "base", localedir="locales", languages=["fr-FR"], fallback=True
    )
    _ = i18n.gettext
    logger.info(_(data.STOP))


# Set up the skill builder
sb = setup_skill_builder()

# Create new Open Data API client and service instances
stib_api_client = OpenDataAPIClient()
stib_service = OpenDataService(stib_api_client=stib_api_client)

# local_test()

handler = sb.lambda_handler()
