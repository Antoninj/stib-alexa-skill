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

import time
import unittest
from ..custom.core.client.token_helper import TokenHelper


class TestTokenHelper(unittest.TestCase):
    def setUp(self):
        self.token_helper = TokenHelper()

    def test_get_valid_security_token(self):
        self.assertFalse(self.token_helper._is_token_expired())
        token = self.token_helper.get_security_token()
        self.assertIsNotNone(token)

    def test_get_expired_security_token(self):
        self.token_helper._set_token_expiration_date(token_validity_time=1)
        time.sleep(5)
        self.assertTrue(self.token_helper._is_token_expired())
        token = self.token_helper.get_security_token()
        self.assertIsNotNone(token)


if __name__ == "__main__":
    unittest.main()
