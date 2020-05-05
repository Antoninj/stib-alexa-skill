# -*- coding: utf-8 -*-

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
import logging
import os
import boto3

from ask_sdk_dynamodb.adapter import DynamoDbAdapter
from ask_sdk_core.skill_builder import CustomSkillBuilder

from core.handlers.custom.get_arrival_times_intent_handler import *
from core.handlers.custom.commute_preferences_intent_handler import *
from core.handlers.custom.favorite_line_intent_handler import *
from core.handlers.custom.favorite_stop_intent_handler import *
from core.handlers.custom.save_trip_preferences_intent_handler import (
    SaveTripPreferencesHandler,
)
from core.handlers.launch_handler import LaunchRequestHandler
from core.handlers.amazon.common_intents_handlers import *
from core.handlers.amazon.repeat_intent_handler import RepeatHandler
from core.handlers.amazon.fallback_intent_handler import FallBackHandler
from core.handlers.amazon.intent_reflector_handler import IntentReflectorHandler
from core.handlers.exception.error_handler import ErrorHandler
from core.interceptors.i18_interceptor import LocalizationInterceptor
from core.interceptors.logger_interceptors import (
    RequestLoggerInterceptor,
    ResponseLoggerInterceptor,
)
from core.client.stib_api_client import OpenDataAPIClient
from core.service.stib_service import OpenDataService
from core.data import data

# Environment variables definitions
ENVIRONMENT = os.environ["env"]
LOGGING_LEVEL = os.environ["log_level"]
DYNAMO_DB_TABLE_NAME = os.environ["dynamo_db_table_name"]

# Logging configuration
logger = logging.getLogger("Lambda")
logger.setLevel(LOGGING_LEVEL)


def setup_skill_builder(service: OpenDataService) -> CustomSkillBuilder:
    """Helper method to create the custom skill builder instance."""

    logger.info("Setting up Custom Skill Builder with Dynamo DB persistence adapter...")
    dynamo_db_adapter = DynamoDbAdapter(
        table_name=DYNAMO_DB_TABLE_NAME,
        partition_key_name="id",
        attribute_name="attributes",
        create_table=True,
        dynamodb_resource=boto3.resource("dynamodb"),
    )

    skill_builder = CustomSkillBuilder(persistence_adapter=dynamo_db_adapter)
    # skill_builder.skill_id = "amzn1.ask.skill.789c381d-5f2c-469e-a888-ee60e260c9de"
    logger.info("Adding skill request handlers...")
    skill_builder.add_request_handler(LaunchRequestHandler())
    skill_builder.add_request_handler(SaveTripPreferencesHandler())
    skill_builder.add_request_handler(GetArrivalTimesNoPrefsIntentHandler())
    skill_builder.add_request_handler(GetArrivalTimesIntentHandler(service))
    skill_builder.add_request_handler(StartedInProgressFavoriteStopHandler())
    skill_builder.add_request_handler(CompletedFavoriteStopHandler())
    skill_builder.add_request_handler(StartedInProgressFavoriteLineHandler())
    skill_builder.add_request_handler(CompletedFavoriteLineHandler(service))
    skill_builder.add_request_handler(YesIntentHandler())
    skill_builder.add_request_handler(NoIntentHandler())
    skill_builder.add_request_handler(HelpIntentHandler())
    skill_builder.add_request_handler(CancelOrStopIntentHandler())
    skill_builder.add_request_handler(RepeatHandler())
    skill_builder.add_request_handler(FallBackHandler())
    skill_builder.add_request_handler(SessionEndedRequestHandler())
    skill_builder.add_request_handler(IntentReflectorHandler())
    logger.info("Adding skill exception handler...")
    skill_builder.add_exception_handler(ErrorHandler())
    logger.info("Adding skill request interceptors...")
    skill_builder.add_global_request_interceptor(LocalizationInterceptor())
    skill_builder.add_global_request_interceptor(RequestLoggerInterceptor())
    logger.info("Adding skill response interceptors...")
    skill_builder.add_global_response_interceptor(ResponseLoggerInterceptor())
    return skill_builder


# Create new Open Data API client and service instances
logger.info("Launching skill in %s environment", ENVIRONMENT)
logger.info("Setting up Open Data API service")
stib_service = OpenDataService(stib_api_client=OpenDataAPIClient())

# Set up the skill builder and lambda handler
sb = setup_skill_builder(service=stib_service)
handler = sb.lambda_handler()
