# -*- coding: utf-8 -*-
import gettext
import logging
import os
import boto3

from ask_sdk_dynamodb.adapter import DynamoDbAdapter
from ask_sdk_core.skill_builder import CustomSkillBuilder

from core.handlers.get_arrival_times_intent_handler import *
from core.handlers.commute_preferences_intent_handler import *
from core.handlers.favorite_line_intent_handler import *
from core.handlers.favorite_stop_intent_handler import *

from core.handlers.launch_handler import LaunchRequestHandler
from core.handlers.common_handlers import *
from core.handlers.intent_reflector_handler import IntentReflectorHandler
from core.handlers.error_handler import ErrorHandler
from core.interceptors.i18_interceptor import LocalizationInterceptor
from core.interceptors.logger_interceptors import *
from core.client.stib_api_client import OpenDataAPIClient
from core.service.stib_service import OpenDataService
from core.data import data

# Environment variables definitions
ENVIRONMENT = os.environ["env"]
LOGGING_LEVEL = os.environ["log_level"]

# Logging configuration
logger = logging.getLogger("Lambda")
logger.setLevel(LOGGING_LEVEL)


def setup_skill_builder(service: OpenDataService) -> CustomSkillBuilder:
    """Helper method to create the custom skill builder instance."""

    logger.info("Setting up Custom Skill Builder with Dynamo DB persistence adapter...")
    dynamo_db_adapter = DynamoDbAdapter(
        table_name="DailyCommuteFavorites",
        partition_key_name="id",
        attribute_name="attributes",
        create_table=True,
        dynamodb_resource=boto3.resource("dynamodb"),
    )

    skill_builder = CustomSkillBuilder(persistence_adapter=dynamo_db_adapter)
    skill_builder.skill_id = "amzn1.ask.skill.789c381d-5f2c-469e-a888-ee60e260c9de"
    logger.info("Adding skill request handlers...")
    skill_builder.add_request_handler(LaunchRequestHandler())
    skill_builder.add_request_handler(GetArrivalTimesIntentHandler(service))
    skill_builder.add_request_handler(StartedInProgressFavoriteStopHandler())
    skill_builder.add_request_handler(CompletedFavoriteStopHandler())
    skill_builder.add_request_handler(StartedInProgressFavoriteLineHandler())
    skill_builder.add_request_handler(CompletedFavoriteLineHandler(service))
    # skill_builder.add_request_handler(HasLineIdCommutePreferencesHandler(service))
    # skill_builder.add_request_handler(StartedInProgressCommutePreferencesHandler())
    # skill_builder.add_request_handler(CompletedCommutePreferencesHandler())
    skill_builder.add_request_handler(HelpIntentHandler())
    skill_builder.add_request_handler(CancelOrStopIntentHandler())
    skill_builder.add_request_handler(SessionEndedRequestHandler())
    skill_builder.add_request_handler(IntentReflectorHandler())
    logger.info("Adding skill exception handler...")
    skill_builder.add_exception_handler(ErrorHandler())
    logger.info("Adding skill request interceptors...")
    skill_builder.add_global_request_interceptor(LocalizationInterceptor())
    skill_builder.add_global_request_interceptor(RequestLogger())
    logger.info("Adding skill response interceptors...")
    skill_builder.add_global_response_interceptor(ResponseLogger())
    return skill_builder


def local_test():
    """Perform some tests locally by bypassing lambda invocation."""

    # Test STIB API integration
    passing_times = stib_service.get_passing_times_for_stop_id_and_line_id()
    logger.info(passing_times[0].formatted_waiting_time)

    # Test i18n
    i18n = gettext.translation(
        "base", localedir="locales", languages=["fr-FR"], fallback=True
    )
    _ = i18n.gettext
    logger.info(_(data.STOP))


# Create new Open Data API client and service instances
logger.info("Setting up Open Data API service")
stib_service = OpenDataService(stib_api_client=OpenDataAPIClient())

# Set up the skill builder
sb = setup_skill_builder(service=stib_service)

local_test()

handler = sb.lambda_handler()


def handler():
    pass
