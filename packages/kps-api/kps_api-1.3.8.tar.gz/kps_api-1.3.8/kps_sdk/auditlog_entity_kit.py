# coding: utf-8

"""
    KPS API reference.
    This is a wrapper on the AuditLog API which provides easy functions to perform GET request

"""

from __future__ import absolute_import

import logging
import uuid
import sys
logging.basicConfig( stream=sys.stderr, format='%(funcName)s:%(levelname)s:%(message)s', level=logging.DEBUG )

import kps_api
from kps_api.api.auditlog_api import AuditlogApi  # noqa: E501
from kps_api.rest import ApiException

from kps_sdk import Auth
from common import connection_info

class AuditLogEntityKit():

    def __init__(self):
        self.auth = Auth()
        self.configuration = self.auth.getAuthorizationHeader()
        self.authorization = self.configuration.get_api_key_with_prefix('Authorization')

        self.api_client = kps_api.ApiClient(configuration=self.configuration)
        self.api = kps_api.api.auditlog_api.AuditlogApi(api_client=self.api_client)  # noqa: E501

    def get(self):

        try:
            #page_index = 0
            #page_size = 10  # int | Item count of each page. (optional)
            #api_response = self.api.query_audit_logs_v2(
            #    self.authorization, page_index=page_index, page_size=page_size)
            api_response = self.api.query_audit_logs_v2(self.authorization)
            logging.info("AuditLog API output: %s" % api_response)
            # returns AuditLogPayload object
            return api_response
        except ApiException as e:
            logging.error("Exception when calling AuditLogApi->auditlogs: %s",e)
            raise

