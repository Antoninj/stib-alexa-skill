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
        """Set up test class with a new instance of token helper"""
        self.token_helper = TokenHelper()

    def test_get_valid_security_token(self):
        """Test retrieval of security token when token is still valid."""
        self.assertFalse(self.token_helper._security_token.is_token_expired())
        token = self.token_helper.get_security_bearer_token()
        self.assertIsNotNone(token)

    def test_get_expired_security_token(self):
        """Test auto generation of new token when token is expired."""
        self.token_helper._security_token.token_expiration_date = self.token_helper._security_token._get_expiration_date_as_unix_timestamp(
            1
        )
        time.sleep(5)
        self.assertTrue(self.token_helper._security_token.is_token_expired())
        token = self.token_helper.get_security_bearer_token()
        self.assertIsNotNone(token)


if __name__ == "__main__":
    unittest.main()
