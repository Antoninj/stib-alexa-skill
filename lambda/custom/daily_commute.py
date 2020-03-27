# -*- coding: utf-8 -*-

import logging
import os

from ask_sdk_dynamodb.adapter import DynamoDbAdapter
from ask_sdk_core.skill_builder import CustomSkillBuilder

from ask_sdk_core.dispatch_components import AbstractRequestHandler
from ask_sdk_core.dispatch_components import AbstractExceptionHandler
from ask_sdk_core.utils import is_request_type, is_intent_name
from ask_sdk_core.handler_input import HandlerInput
from ask_sdk_model import Response

from client.stib_api_client import OpenDataAPIClient
from service.stib_service import OpenDataService

import boto3

# Environment variables definitions
ENVIRONMENT = os.environ['env']
LOGGING_LEVEL = os.environ['log_level']

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
        logger.info("In LaunchRequestHandler")
        speech_text = "Welcome, you can ask when is the next tram."
        handler_input.response_builder.speak(speech_text).ask(speech_text)
        return handler_input.response_builder.response


class NextTramIntentHandler(AbstractRequestHandler):
    """Handler for Next Tram Intent."""

    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool

        # extract persistent attributes and check if they are all present
        attr = handler_input.attributes_manager.persistent_attributes
        attributes_are_present = ("favorite_stop_id" in attr and "favorite_line_id" in attr)

        return attributes_are_present and is_intent_name("NextTramIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        logger.info("In NextTramIntentHandler")

        logger.info("Retrieving favorite line and stop from dynamo DB...")
        persistent_attributes = handler_input.attributes_manager.persistent_attributes
        logger.info("Persistent attributes found: %s", persistent_attributes)
        favorite_stop_id = persistent_attributes['favorite_stop_id']
        favorite_line_id = persistent_attributes['favorite_line_id']

        logger.info("Getting waiting times for line %s at stop %s", favorite_line_id, favorite_stop_id)

        speech_text = stib_service.get_waiting_times_for_stop_id_and_line_id(stop_id=favorite_stop_id,
                                                                             line_id=favorite_line_id)

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
        speech_text = "You can ask when is the next tram! How can I help?"
        handler_input.response_builder.speak(speech_text).ask(speech_text)
        return handler_input.response_builder.response


class CancelOrStopIntentHandler(AbstractRequestHandler):
    """Single handler for Cancel and Stop Intent."""

    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return (is_intent_name("AMAZON.CancelIntent")(handler_input) or
                is_intent_name("AMAZON.StopIntent")(handler_input))

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        logger.debug("In CancelOrStopIntentHandler")
        speech_text = "Goodbye!"
        handler_input.response_builder.speak(speech_text)
        return handler_input.response_builder.response


class SessionEndedRequestHandler(AbstractRequestHandler):
    """Handler for Session End."""

    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return is_request_type("SessionEndedRequest")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        logger.debug("In SessionEndedRequestHandler")
        logger.debug("Session ended with reason: {}".format(
            handler_input.request_envelope.request.reason))
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
        speech_text = "Sorry, I couldn't understand what you said. Please try again."
        handler_input.response_builder.speak(speech_text).ask(speech_text)
        return handler_input.response_builder.response


def setup_skill_builder():
    dynamo_db_adapter = DynamoDbAdapter(table_name="DailyCommuteFavorites", partition_key_name="id",
                                        attribute_name="attributes", create_table=True,
                                        dynamodb_resource=boto3.resource("dynamodb"))
    skill_builder = CustomSkillBuilder(persistence_adapter=dynamo_db_adapter)
    skill_builder.add_request_handler(LaunchRequestHandler())
    skill_builder.add_request_handler(NextTramIntentHandler())
    skill_builder.add_request_handler(HelpIntentHandler())
    skill_builder.add_request_handler(CancelOrStopIntentHandler())
    skill_builder.add_request_handler(SessionEndedRequestHandler())
    skill_builder.add_request_handler(
        IntentReflectorHandler())  # make sure IntentReflectorHandler is last so it doesn't override your custom intent handlers

    skill_builder.add_exception_handler(ErrorHandler())

    return skill_builder


### Set up the skill builder
sb = setup_skill_builder()

### Create Open Data STIB API client and service instances
stib_api_client = OpenDataAPIClient()
stib_service = OpenDataService(stib_api_client=stib_api_client)

# waiting_time = stib_service.get_waiting_times_for_stop_id_and_line_id()
# logger.info(waiting_time)

handler = sb.lambda_handler()
