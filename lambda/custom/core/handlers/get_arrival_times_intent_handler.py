# -*- coding: utf-8 -*-
from ask_sdk_core.dispatch_components import AbstractRequestHandler
from ask_sdk_core.utils import is_intent_name
import logging

logger = logging.getLogger("Lambda")


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

        logger.debug("Slots: %s", handler_input.request_envelope.request.intent.slots)
        persistent_attributes = handler_input.attributes_manager.persistent_attributes
        logger.debug("Persistent attributes: %s", persistent_attributes)
        favorite_stop_id = persistent_attributes["favorite_stop_id"]
        favorite_line_id = persistent_attributes["favorite_line_id"]
        passing_times = self.stib_service.get_passing_times_for_stop_id_and_line_id(
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
