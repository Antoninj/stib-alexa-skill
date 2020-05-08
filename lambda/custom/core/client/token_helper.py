# -*- coding: utf-8 -*-

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

import calendar
import json
import logging
import os
from datetime import datetime, timedelta

import boto3
import requests
from botocore.exceptions import ClientError

logger = logging.getLogger("Lambda")


class TokenException(Exception):
    """Exception for token generation errors"""

    def __init__(self, msg, original_exception):
        super(TokenException, self).__init__(msg + (": %s" % original_exception))
        self.original_exception = original_exception


class TokenHelper:
    """Helper to manage OpenData API bearer token lifecycle."""

    def __init__(self):
        self.SECRET_NAME: str = os.environ["secret_name"]
        self.OPEN_DATA_API_ENDPOINT: str = os.environ["open_data_api_endpoint"]
        self.TOKEN_VALIDITY_TIME: str = os.environ["open_data_api_token_validity"]
        self.api_credentials: str = self._get_api_credentials_from_ssm()
        self.security_token: str = self._retrieve_api_access_token()
        self._set_token_expiration_date()

    def _set_token_expiration_date(self, token_validity_time: int = None) -> None:
        """Compute future expiration date of a token."""
        if not token_validity_time:
            token_validity_time = int(self.TOKEN_VALIDITY_TIME)
        future = datetime.utcnow() + timedelta(seconds=token_validity_time)
        self.token_expiration_date = calendar.timegm(future.utctimetuple())

    def _is_token_expired(self) -> bool:
        """Check validity of a token"""

        current_time = datetime.now()
        unix_timestamp = current_time.timestamp()
        return unix_timestamp > self.token_expiration_date

    def _get_api_credentials_from_ssm(self) -> str:
        """Get OpenData api credentials from AWS SSM Parameter Store (free stuff gooood)."""

        secret = None
        secret_name = self.SECRET_NAME
        region_name = "eu-west-1"

        # Create a SSM Parameter Store client
        session = boto3.session.Session()
        client = session.client(service_name="ssm", region_name=region_name)

        try:
            logger.info(
                "Getting secret value for secret [{}] from SSM parameter store".format(
                    secret_name
                )
            )
            get_secret_value_response = client.get_parameter(
                Name=secret_name, WithDecryption=True
            )
        except ClientError as e:
            raise e
        else:
            # Decrypts secret using the associated KMS CMK.
            secret = get_secret_value_response.get("Parameter").get("Value")

        return secret

    def _get_access_token(self, client_id: str, client_secret: str) -> str:
        """Get OpenData API access token."""

        request_url = self.OPEN_DATA_API_ENDPOINT + "/token"
        logger.info(
            "Getting access token for STIB open data api using token url: {} ".format(
                request_url
            )
        )
        client_auth = requests.auth.HTTPBasicAuth(client_id, client_secret)
        post_data = {"grant_type": "client_credentials"}
        try:
            response = requests.post(request_url, auth=client_auth, data=post_data)
            token_json = response.json()
            return token_json["access_token"]
        except Exception as e:
            raise TokenException("Problem generating new Open Data API token", e)

    def _retrieve_api_access_token(self) -> str:
        """Retrieve OpenData api bearer token."""

        stib_api_credentials = self.api_credentials
        # logger.debug("STIB API credentials {}".format(stib_api_credentials))
        api_credentials = json.loads(stib_api_credentials)
        client_id = api_credentials["key"]
        client_secret = api_credentials["secret"]
        access_token = self._get_access_token(client_id, client_secret)
        # logger.debug("STIB API access token [{}]".format(access_token))
        return access_token

    def get_security_token(self) -> str:
        """Retrieve OpenData api bearer token."""

        if not self._is_token_expired():
            return self.security_token
        else:
            logger.warning("Token expired... Getting new token")
            self.security_token = self._retrieve_api_access_token()
            self._set_token_expiration_date()
            return self.security_token
