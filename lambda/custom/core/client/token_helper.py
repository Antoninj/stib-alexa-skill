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
import os
from datetime import datetime, timedelta, timezone

import boto3
import requests
from aws_lambda_powertools.logging import Logger
from aws_lambda_powertools.tracing import Tracer
from botocore.exceptions import ClientError

# Logging/tracing configuration
logger = Logger(service="Token helper")
tracer = Tracer(service="Token helper")


class TokenException(Exception):
    """Exception for token generation errors"""

    def __init__(self, msg, original_exception):
        super(TokenException, self).__init__(msg + (": %s" % original_exception))
        self.original_exception = original_exception


class SecurityToken:
    """Authentication token and expiration date access/management."""

    def __init__(self, token, token_validity_time: int = None):
        if token_validity_time:
            self.TOKEN_VALIDITY_TIME = token_validity_time
        else:
            self.TOKEN_VALIDITY_TIME = int(os.environ["open_data_api_token_validity"])

        self._bearer: str = token
        self._token_expiration_date = None
        self.token_expiration_date = self._get_expiration_date_as_unix_timestamp(
            validity_time=self.TOKEN_VALIDITY_TIME
        )

    @property
    def bearer(self):
        """Getter for bearer value."""
        return self._bearer

    @property
    def token_expiration_date(self):
        """Getter for token expiration date."""

        return self._token_expiration_date

    @token_expiration_date.setter
    def token_expiration_date(self, expiration_date: int) -> None:
        """Setter for token expiration date."""
        logger.info(
            {
                "operation": "Setting STIB API security token expiration date",
                "expiration_date": datetime.fromtimestamp(expiration_date),
            }
        )

        self._token_expiration_date = expiration_date

    @staticmethod
    def _get_expiration_date_as_unix_timestamp(validity_time: int) -> int:
        """Compute future expiration date of a token as a unix timestamp."""

        current_time = datetime.now(tz=timezone.utc)
        future_time = current_time + timedelta(seconds=validity_time)
        return calendar.timegm(future_time.utctimetuple())

    def is_token_expired(self) -> bool:
        """Check validity of a token."""

        current_time = datetime.now(tz=timezone.utc)
        unix_timestamp = current_time.timestamp()
        return unix_timestamp > self.token_expiration_date


class TokenHelper:
    """OpenData API authentication token lifecycle management helper class."""

    def __init__(self, token_validity_time: int = None):
        self.SECRET_NAME: str = os.environ["secret_name"]
        self.OPEN_DATA_API_ENDPOINT: str = os.environ["open_data_api_endpoint"]
        self._api_credentials: str = self._get_api_credentials_from_ssm()
        self._security_token: SecurityToken = SecurityToken(
            token=self._retrieve_api_access_token(),
            token_validity_time=token_validity_time,
        )

    @property
    def security_token(self):
        """Getter method for OpenData api bearer token."""

        if not self._security_token.is_token_expired():
            return self._security_token
        else:
            logger.warning("Token expired... Getting new token")
            self._security_token = SecurityToken(
                token=self._retrieve_api_access_token()
            )
            return self._security_token

    @tracer.capture_method
    def get_security_bearer_token(self) -> str:
        """Public method to access the OpenData API bearer token securely."""

        return self.security_token.bearer

    def _get_api_credentials_from_ssm(self) -> str:
        """Get OpenData api credentials from AWS SSM Parameter Store."""

        secret = None
        secret_name = self.SECRET_NAME
        region_name = "eu-west-1"

        # Create a SSM Parameter Store client
        session = boto3.session.Session()
        client = session.client(service_name="ssm", region_name=region_name)

        try:
            logger.info(
                {
                    "operation": "Getting secret value for secret from SSM parameter store",
                    "secret_name": secret_name,
                }
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

    @tracer.capture_method
    def _get_access_token(self, client_id: str, client_secret: str) -> str:
        """Get OpenData API access token."""

        request_url = self.OPEN_DATA_API_ENDPOINT + "/token"
        logger.info(
            {
                "operation": "Getting access token for STIB open data api",
                "token_url": request_url,
            }
        )
        client_auth = requests.auth.HTTPBasicAuth(client_id, client_secret)
        post_data = {"grant_type": "client_credentials"}
        try:
            with requests.post(
                request_url, auth=client_auth, data=post_data
            ) as response:
                response.raise_for_status()
                token_json = response.json()
                return token_json["access_token"]
        except requests.RequestException as error:
            raise TokenException("Problem generating new Open Data API token", error)

    def _retrieve_api_access_token(self) -> str:
        """Retrieve OpenData api bearer token."""

        stib_api_credentials = self._api_credentials
        api_credentials = json.loads(stib_api_credentials)
        client_id = api_credentials["key"]
        client_secret = api_credentials["secret"]
        access_token = self._get_access_token(client_id, client_secret)
        return access_token
