# coding: utf-8

"""
    KPS API reference.
    This is a wrapper on the Application API which provides easy functions to perform CRUD operations on the Application API.

"""

from __future__ import absolute_import

import logging
import uuid
import sys
logging.basicConfig( stream=sys.stderr, format='%(funcName)s:%(levelname)s:%(message)s', level=logging.DEBUG )

import kps_api
from kps_api.api.application_status_api import ApplicationStatusApi  # noqa: E501
from kps_api.rest import ApiException

from  kps_sdk import Auth
from common import connection_info

class ApplicationStatusEntityKit():

    def __init__(self):
        self.auth = Auth()
        self.configuration = self.auth.getAuthorizationHeader()
        self.authorization = self.configuration.get_api_key_with_prefix('Authorization')

        self.api_client = kps_api.ApiClient(configuration=self.configuration)
        self.api = kps_api.api.application_status_api.ApplicationStatusApi(api_client=self.api_client)  # noqa: E501

    def get_status(self, app_id=None):
        try:
            if app_id is not None:
                api_response = self.api.application_status_get_v2(
                    self.authorization, app_id)
            else:
                api_response = self.api.application_status_list_v2(self.authorization)
            logging.info("application_status_list_v2 API output: %s" % api_response)
            # returns ApplicationStatusListPayload object
            return api_response
        except ApiException as e:
            logging.error("Exception when calling ApplicationStatusApi->application_status_list/get_v2: %s", e)
            raise

