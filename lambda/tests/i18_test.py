import unittest
import gettext
from ..custom.data import data


class TestI18n(unittest.TestCase):
    def setUp(self):
        i18n = gettext.translation(
            "base", localedir="locales", languages=["fr-FR"], fallback=True
        )
        self._ = i18n.gettext

    def test_translate_data(self):
        self.assertEqual(self._(data.STOP), "A la prochaine!")
