#   Copyright 2020 Antonin Jousson
#
#  Licensed under the Apache License, Version 2.0 (the "License").
#  You may not use this file except in compliance with the License.
#  A copy of the License is located at
#
#  http://aws.amazon.com/apache2.0/
#
#  or in the "license" file accompanying this file. This file is
#  distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS
#  OF ANY KIND, either express or implied. See the License for the
#  specific language governing permissions and limitations under the
#  License.

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
