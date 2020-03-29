import sys
import unittest

from lex_bot_tester.aws.alexa.alexaskilltest import AlexaSkillTest

verbose = True


class StibScheduleTestSuite(AlexaSkillTest):

    def test_next_tram_intent(self):
        """
        Test generated by urutu on 2020-03-29 11:52:47
        """
        skill_name = 'STIB schedule'
        intent = 'NextTramIntent'
        conversation = [{'slot': None, 'text': 'ask stib schedule when is the next tram', 'prompt': None}]
        simulation_result = self.conversation_text(skill_name, intent, conversation, verbose=verbose)
        #self.assertSimulationResultIsCorrect(simulation_result, verbose=verbose)


    def test_help_intent(self):
        """
        Test generated by urutu on 2020-03-29 11:52:47
        """
        skill_name = 'STIB schedule'
        intent = 'AMAZON.HelpIntent'
        conversation = [{'slot': None, 'text': 'ask stib schedule help', 'prompt': None}]
        simulation_result = self.conversation_text(skill_name, intent, conversation, verbose=verbose)
        #self.assertSimulationResultIsCorrect(simulation_result, verbose=verbose)


if __name__ == '__main__':
    verbose = '-v' in sys.argv or '--verbose' in sys.argv
    unittest.main()