# Copyright 2019-2020 Turner Broadcasting Inc. / WarnerMedia
# Copyright 2021 Chris Farris <chrisf@primeharbor.com>
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import boto3
from botocore.exceptions import ClientError
from boto3.dynamodb.conditions import Key
import json
import os
import logging

import logging
logger = logging.getLogger('antiope.AntiopeConfig')


class AntiopeConfig(object):
    """Class to represent an AWS Account """
    def __init__(self, config=None, SSMParam=None):
        """ Create a new object representing the AWS account specified by account_id """
        # Execute any parent class init()
        super(AntiopeConfig, self).__init__()

        # The following attributes are expected in the AntiopeConfig Object:
        # * account_table_name
        # * vpc_table_name
        # * role_name
        # * role_session_name
        # * antiope_bucket
        # * dynamodb (boto3 resource)
        # * account_table (dynamodb.Table resource)
        # * vpc_table (dynamodb.Table resource)

        if SSMParam is not None:
            try:
                client = boto3.client('ssm')
                response = client.get_parameter(Name=SSMParam)
                config = json.loads(response['Parameter']['Value'])  # config gets passed to the next conditional.
            except Exception as e:
                logger.critical(f"Failed to get Antiope Config from SSM Parameter Store: {e}")
                exit(1)

        if config is not None:
            try:
                self.account_table_name = config['account_table_name']
                self.vpc_table_name = config['vpc_table_name']
                self.role_name = config['role_name']
                self.role_session_name = config['role_session_name']
            except KeyError as e:
                logger.critical(f"AntiopeConfig passed a config that was missing a key: {e}")
                raise AntiopeDatabaseError(f"AntiopeConfig passed a config that was missing a key: {e}")
        else:
            # Assume things are in the environment
            # This is typical in the Antiope Lambda execution environment
            try:
                self.account_table_name = os.environ['ACCOUNT_TABLE']
                self.vpc_table_name = os.environ['VPC_TABLE']
                if 'ROLE_NAME' not in os.environ:
                    self.role_name = None
                else:
                    self.role_name = os.environ['ROLE_NAME']

                if 'ROLE_SESSION_NAME' not in os.environ:
                    self.role_session_name = "antiope"
                else:
                    self.role_session_name = os.environ['ROLE_SESSION_NAME']
            except KeyError as e:
                logger.critical(f"AntiopeConfig cannot find required key in environment: {e}")
                raise AntiopeDatabaseError(f"AntiopeConfig cannot find required key in environment: {e}")

        # # Save these as attributes
        self.dynamodb      = boto3.resource('dynamodb')
        self.account_table = self.dynamodb.Table(self.account_table_name)
        self.vpc_table     = self.dynamodb.Table(self.vpc_table_name)
        # TODO validate access & existence of these tables


#
# These are the common Exception Classes
#

class AntiopeAssumeRoleError(Exception):
    """raised when the AssumeRole Fails"""
    pass


class AntiopeDatabaseError(Exception):
    """raised when there are issues interacting with the Antiope DynamoDB Tables"""
    pass


class AccountUpdateError(Exception):
    """raised when an update to DynamoDB Fails"""
    pass


class AntiopeAccountLookupError(LookupError):
    """Raised when the Account requested is not in the database"""
    pass


class VPCLookupError(LookupError):
    '''Raised when the VPC requested is not in the database'''
    pass
