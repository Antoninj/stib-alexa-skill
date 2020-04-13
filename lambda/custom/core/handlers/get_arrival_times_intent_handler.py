# -*- coding: utf-8 -*-
from ask_sdk_core.dispatch_components import AbstractRequestHandler
from ask_sdk_core.handler_input import HandlerInput
from ask_sdk_core.utils import is_intent_name
from ask_sdk_model import Response

import logging
from ..data import data

logger = logging.getLogger("Lambda")


class GetArrivalTimesNoPrefsIntentHandler(AbstractRequestHandler):
    """Handler for get arrival time Intent."""

    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool

        # Extract persistent attributes and check if they are all present
        attr = handler_input.attributes_manager.persistent_attributes
        attributes_are_present = (
            "favorite_stop_id" in attr and "favorite_line_id" in attr
        )

        return not attributes_are_present and is_intent_name("GetArrivalTimesIntent")(
            handler_input
        )

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response

        logger.debug("In GetArrivalTimesNoPrefsIntentHandler")
        _ = handler_input.attributes_manager.request_attributes["_"]

        speech = _(data.WELCOME_NEW_USER)
        speech += " " + _(data.SKILL_DESCRIPTION_WITHOUT_PREFERENCES)
        speech += " " + _(data.ASK_FOR_PREFERENCES)
        reprompt = _(data.ASK_FOR_PREFERENCES_REPROMPT)

        handler_input.response_builder.speak(speech)
        handler_input.response_builder.ask(reprompt)
        return handler_input.response_builder.response


class GetArrivalTimesIntentHandler(AbstractRequestHandler):
    """Handler for get arrival time Intent."""

    def __init__(self, service):
        self.stib_service = service

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
        _ = handler_input.attributes_manager.request_attributes["_"]
        persistent_attributes = handler_input.attributes_manager.persistent_attributes
        session_attributes = handler_input.attributes_manager.session_attributes
        logger.debug("Slots: %s", handler_input.request_envelope.request.intent.slots)
        logger.debug("Persistent attributes: %s", persistent_attributes)
        favorite_stop_id = persistent_attributes["favorite_stop_id"]
        favorite_line_id = persistent_attributes["favorite_line_id"]
        favorite_transportation_type = persistent_attributes[
            "favorite_transportation_type"
        ]
        passing_times = self.stib_service.get_passing_times_for_stop_id_and_line_id(
            stop_id=favorite_stop_id, line_id=favorite_line_id
        )
        if len(passing_times) == 2:
            speech_text = self._format_waiting_times(
                passing_times, favorite_transportation_type
            )
            speech_text += " " + _(data.FAREWELL)
        elif len(passing_times) == 1:
            speech_text = self._format_first_waiting_time(
                passing_times, favorite_transportation_type
            )
            speech_text += " " + _(data.FAREWELL)
        else:
            speech_text = (
                "Désolé, je n'ai pas trouvé d'informations pour le trajet demandé"
            )
        session_attributes["repeat_prompt"] = speech_text
        handler_input.response_builder.speak(speech_text).set_should_end_session(True)
        return handler_input.response_builder.response

    @staticmethod
    def _format_waiting_times(passing_times, transportation_type: str) -> str:
        """Define method here."""

        formatted_waiting_times = GetArrivalTimesIntentHandler._format_first_waiting_time(
            passing_times[0], transportation_type
        ) + GetArrivalTimesIntentHandler._format_second_waiting_time(
            passing_times[1]
        )

        return formatted_waiting_times

    @staticmethod
    def _format_first_waiting_time(passing_time, transportation_type: str) -> str:
        """Define method here."""
        logger.debug(passing_time.arriving_in_dict)
        lower_case_destination = passing_time.destination.fr.lower()
        formatted_waiting_time = "Le prochain {} {} en direction de {} passe dans {} minutes et {} secondes.".format(
            transportation_type,
            passing_time.line_id,
            lower_case_destination,
            passing_time.arriving_in_dict["minutes"],
            passing_time.arriving_in_dict["seconds"],
        )
        return formatted_waiting_time

    @staticmethod
    def _format_second_waiting_time(passing_time) -> str:
        """Define method here."""

        formatted_waiting_time = " Le suivant passe dans {} minutes et {} secondes.".format(
            passing_time.arriving_in_dict["minutes"],
            passing_time.arriving_in_dict["seconds"],
        )
        return formatted_waiting_time
