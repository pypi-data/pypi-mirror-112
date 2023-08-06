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
from kps_api.api.ml_model_status_api import MLModelStatusApi
from kps_api.rest import ApiException
from kps_sdk import Auth
from common import connection_info

class MLModelStatusEntityKit():

    def __init__(self):
        self.auth = Auth()
        self.configuration = self.auth.getAuthorizationHeader()
        self.authorization = self.configuration.get_api_key_with_prefix('Authorization')

        self.api_client = kps_api.ApiClient(configuration=self.configuration)
        self.api = kps_api.api.ml_model_status_api.MLModelStatusApi(api_client=self.api_client)  # noqa: E501

    def list(self, ml_model_name=None):
        try:
            if ml_model_name is not None:
                # int | 0-based index of the page to fetch results. (optional)
                page_index = 0
                page_size = 30000  # int | Item count of each page. (optional)
                # order_by = [] # list[str] | Specify result order. Zero or more entries with format: &ltkey> [desc] where orderByKeys lists allowed keys in each response. (optional)
                # str | Specify result filter. Format is similar to a SQL WHERE clause. For example, to filter object by name with prefix foo, use: name LIKE 'foo%'. Supported filter keys are the same as order by keys. (optional)
                filter = "name = \'%s\'" % ml_model_name

                api_response = self.api.m_l_model_status_list(
                    self.authorization, page_index=page_index, page_size=page_size, filter=filter)
            else:
                api_response = self.api.m_l_model_status_list(self.authorization)
            return api_response
        except ApiException as e:
            logging.error("Exception when calling MLModelApi->m_l_model_status_list: %s", e)
            raise

    def get_by_id(self, ml_model_id):
        try:
            api_response = self.api.m_l_model_status_get(ml_model_id, self.authorization)
            return api_response
        except ApiException as e:
            logging.error("Exception when calling MLModelApi->m_l_model_status_get: %s", e)
            raise


