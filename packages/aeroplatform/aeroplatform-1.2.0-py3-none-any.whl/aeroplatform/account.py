import requests
import os
import json
import logging
import configparser
import boto3
import sys

from pathlib import Path
from enum import Enum
from . import ROOT_DIR

logging.basicConfig(stream=sys.stdout, level=os.environ.get('LOGLEVEL', 'INFO').upper())

logging.getLogger('boto3').setLevel(logging.CRITICAL)
logging.getLogger('botocore').setLevel(logging.CRITICAL)
logging.getLogger('s3transfer').setLevel(logging.CRITICAL)
logging.getLogger('urllib3').setLevel(logging.CRITICAL)

logger = logging.getLogger(__name__)

json_config = json.load(open(os.path.join(ROOT_DIR, "config.json"), "r"))

BASE_URL = json_config['BASE_API_URL']
CLIENT_ID = json_config['USER_POOL_CLIENT_ID']
PROVISION_URL = f"{BASE_URL}/compute/config"

class ComputeStatus():

    NO_VALUE = 0
    INIT = 1
    CREATING = 2
    CREATED = 3
    FAILED = 4

class Account():

    def __init__(self, email, password):

        self.email = email
        self.password = password

        self.user_home = str(Path.home())


    def provision(self, is_first_provision):
        data = dict(
            company="solo",
            project="default"
        )
        logger.debug("provision()")
        logger.debug(data)
        r = requests.post(PROVISION_URL,
            json=data,
            headers = {
                "x-api-key": self.auth_token
            }
        )
        logger.debug(r.status_code)
        
        if r.status_code == 202:
            return ComputeStatus.INIT
        elif r.status_code == 207:
            return ComputeStatus.CREATING
        elif r.status_code != 200:
            raise Exception(r.status_code, r.text)

        response_data = r.json()

        if is_first_provision:
            self.login()

        response_data['config']['AERO_ID_TOKEN'] = self.id_token

        # Create Metaflow directory
        if not os.path.exists(f"{self.user_home}/.metaflowconfig"):
            os.mkdir(f"{self.user_home}/.metaflowconfig")

        with open(f"{self.user_home}/.metaflowconfig/config.json", 'w', encoding='utf-8') as f:
            json.dump(response_data['config'], f, ensure_ascii=False, indent=4)

        return ComputeStatus.CREATED
        
    def login(self):

        self.auth_token, self.id_token = self._login()


    def create(self):

        outcome = self._create_account(self.email, self.password)

        return outcome
    
    def _hash(self, password):

        return sha256(password.strip()).hexdigest()

    def _create_account(cls, email, password):

        data = dict(
            username=email, 
            password=password
        )
        logger.debug("_create_account()")
        logger.debug(data)
        logger.info("Signup is currently not supported on the CLI")

        return True

    def _login(self):

        cognito = boto3.client('cognito-idp', region_name='eu-west-1')

        logger.debug("_login()")
        response = cognito.initiate_auth(
            AuthFlow="USER_PASSWORD_AUTH",
            AuthParameters={
                "USERNAME": self.email,
                "PASSWORD": self.password
            },
            ClientId=CLIENT_ID
        )
        logger.debug(response)

        if 'AuthenticationResult' not in response:
            raise Exception("Error logging in")

        logger.debug(response['AuthenticationResult']['AccessToken'])

        return response['AuthenticationResult']['AccessToken'], response['AuthenticationResult']['IdToken']
