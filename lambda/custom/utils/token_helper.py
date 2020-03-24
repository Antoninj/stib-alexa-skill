import logging
import os
import json
import calendar
from datetime import datetime, timedelta

import boto3
from botocore.exceptions import ClientError
import base64
import requests

logger = logging.getLogger("Lambda")


class TokenHelper:
    def __init__(self):
        self.SECRET_NAME = os.environ['secret_name']
        self.OPEN_DATA_API_ENDPOINT = os.environ['open_data_api_endpoint']
        self.TOKEN_VALIDITY_TIME = os.environ['open_data_api_token_validity']
        self.token_expiration_date = self.compute_token_expiration_date(self.TOKEN_VALIDITY_TIME)
        self.api_credentials = self._get_api_credentials()
        self.security_token = self._retrieve_api_access_token()

    @staticmethod
    def _compute_token_expiration_date(token_validity_time):
        future = datetime.utcnow() + timedelta(seconds=int(token_validity_time))
        return calendar.timegm(future.utctimetuple())

    def _is_token_expired(self):
        current_time = datetime.now()
        unix_timestamp = current_time.timestamp()
        return unix_timestamp > self.token_expiration_date

    def _get_api_credentials(self):
        """Get OpenData api credentials from secret manager."""

        secret = None
        secret_name = self.SECRET_NAME
        region_name = "eu-west-1"

        # Create a Secrets Manager client
        session = boto3.session.Session()
        client = session.client(
            service_name='secretsmanager',
            region_name=region_name
        )

        # In this sample we only handle the specific exceptions for the 'GetSecretValue' API.
        # See https://docs.aws.amazon.com/secretsmanager/latest/apireference/API_GetSecretValue.html
        # We rethrow the exception by default.

        try:
            logger.info("Getting secret value for secret '{}' from secret manager".format(secret_name))
            get_secret_value_response = client.get_secret_value(
                SecretId=secret_name
            )
        except ClientError as e:
            if e.response['Error']['Code'] == 'DecryptionFailureException':
                # Secrets Manager can't decrypt the protected secret text using the provided KMS key.
                # Deal with the exception here, and/or rethrow at your discretion.
                raise e
            elif e.response['Error']['Code'] == 'InternalServiceErrorException':
                # An error occurred on the server side.
                # Deal with the exception here, and/or rethrow at your discretion.
                raise e
            elif e.response['Error']['Code'] == 'InvalidParameterException':
                # You provided an invalid value for a parameter.
                # Deal with the exception here, and/or rethrow at your discretion.
                raise e
            elif e.response['Error']['Code'] == 'InvalidRequestException':
                # You provided a parameter value that is not valid for the current state of the resource.
                # Deal with the exception here, and/or rethrow at your discretion.
                raise e
            elif e.response['Error']['Code'] == 'ResourceNotFoundException':
                # We can't find the resource that you asked for.
                # Deal with the exception here, and/or rethrow at your discretion.
                raise e
        else:
            # Decrypts secret using the associated KMS CMK.
            # Depending on whether the secret is a string or binary, one of these fields will be populated.
            if 'SecretString' in get_secret_value_response:
                secret = get_secret_value_response['SecretString']
            else:
                secret = base64.b64decode(get_secret_value_response['SecretBinary'])

        return secret

    def _get_access_token(self, client_id, client_secret):
        """Get OpenData access token."""

        request_url = self.OPEN_DATA_API_ENDPOINT + "/token"
        logger.info("Getting access token for STIB open data api using token url: {} ".format(request_url))
        client_auth = requests.auth.HTTPBasicAuth(client_id, client_secret)
        post_data = {"grant_type": "client_credentials"}
        response = requests.post(request_url,
                                 auth=client_auth,
                                 data=post_data)
        token_json = response.json()
        return token_json["access_token"]

    def _retrieve_api_access_token(self):
        """Retrieve STIB api bearer token."""

        stib_api_credentials = self.api_credentials
        logger.debug("STIB API credentials {}".format(stib_api_credentials))

        api_credentials = json.loads(stib_api_credentials)
        client_id = api_credentials['key']
        client_secret = api_credentials['secret']

        access_token = self._get_access_token(client_id, client_secret)
        logger.debug("STIB API access token {}".format(access_token))
        return access_token

    def get_security_token(self):
        if not self._is_token_expired():
            return self.security_token
        else:
            logger.warning("Token expired... Getting new token")
            self.security_token = self._retrieve_api_access_token()
            new_token_expiration_date = self._compute_token_expiration_date(self.TOKEN_VALIDITY_TIME)
            self.token_expiration_date = new_token_expiration_date
            return self.security_token


