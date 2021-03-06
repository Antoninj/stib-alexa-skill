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

import sys
import unittest

from lex_bot_tester.aws.alexa.alexaskilltest import AlexaSkillTest

verbose = True


class StibScheduleTestSuite(AlexaSkillTest):
    """ Skill integration tests"""

    def test_save_trip_preferences_intent(self):
        """
        Test generated by urutu on 2020-03-29 11:52:47
        """

        skill_name = "STIB-MIVB network"
        intent = "SaveTripPreferencesIntent"
        conversation = [
            {
                "slot": None,
                "text": "alexa open stib schedule and modify my preferences",
                "prompt": None,
            }
        ]
        simulation_result = self.conversation_text(
            skill_name, intent, conversation, verbose=verbose
        )
        # self.assertSimulationResultIsCorrect(simulation_result, verbose=verbose)

    def test_next_tram_intent(self):
        """
        Test generated by urutu on 2020-03-29 11:52:47
        """
        skill_name = "STIB-MIVB network"
        intent = "GetArrivalTimesIntent"
        conversation = [
            {
                "slot": None,
                "text": "alexa ask stib schedule when is the next tram",
                "prompt": None,
            }
        ]
        simulation_result = self.conversation_text(
            skill_name, intent, conversation, verbose=verbose
        )

    def test_set_favorite_line_intent(self):
        """
        Test generated by urutu on 2020-05-06 09:34:55
        """

        skill_name = "STIB-MIVB network"
        intent = "SetFavoriteLineIntent"
        conversation = [
            {"slot": None, "text": "alexa open stib schedule", "prompt": None},
            {
                "slot": "line_id",
                "text": "the tram one thousand fifty nine",
                "prompt": "Which line do you usually travel on?",
            },
        ]
        simulation_result = self.conversation_text(
            skill_name, intent, conversation, verbose=verbose
        )
        self.assertSimulationResultIsCorrect(simulation_result, verbose=verbose)

    def test_set_favorite_stop_intent(self):
        """
        Test generated by urutu on 2020-05-06 09:34:55
        """

        skill_name = "STIB-MIVB network"
        intent = "SetFavoriteStopIntent"
        conversation = [
            {"slot": None, "text": "alexa open stib schedule", "prompt": None},
            {
                "slot": "destination_name",
                "text": "towards STADE",
                "prompt": "In which direction are you travelling?",
            },
            {
                "slot": "stop_name",
                "text": "legrand",
                "prompt": "Great! What's your stop name?",
            },
        ]
        simulation_result = self.conversation_text(
            skill_name, intent, conversation, verbose=verbose
        )
        self.assertSimulationResultIsCorrect(simulation_result, verbose=verbose)


if __name__ == "__main__":
    verbose = "-v" in sys.argv or "--verbose" in sys.argv
    unittest.main()
