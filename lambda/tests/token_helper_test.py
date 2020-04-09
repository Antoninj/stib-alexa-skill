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
