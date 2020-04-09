import os
import unittest
import gettext

from ..custom.core.data import data


class TestI18n(unittest.TestCase):

    LOCALE_DIR = os.path.dirname(os.path.dirname(__file__)) + "/custom/core/locales/"

    def setUp(self):
        i18n = gettext.translation(
            "base", localedir=self.LOCALE_DIR, languages=["en-US"]
        )
        self._ = i18n.gettext

    def test_translate_data(self):
        print(self._(data.STOP))
        self.assertEqual(self._(data.STOP), "Bye bye!")
