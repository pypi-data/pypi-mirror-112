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
from kps_api.api.service_class_api import ServiceClassApi  # noqa: E501
from kps_api.rest import ApiException

from kps_sdk import Auth
from common import connection_info

class ServiceClassEntityKit():
    def __init__(self):
        self.auth = Auth()
        self.configuration = self.auth.getAuthorizationHeader()
        self.authorization = self.configuration.get_api_key_with_prefix('Authorization')

        self.api_client = kps_api.ApiClient(configuration=self.configuration)
        self.api = kps_api.api.service_class_api.ServiceClassApi(api_client=self.api_client)  # noqa: E501

    def get(self, service_class_type=None):
        try:
            if service_class_type is not None:
                # int | 0-based index of the page to fetch results. (optional)
                page_index = 0
                page_size = 100  # int | Item count of each page. (optional)
                # order_by = ['order_by_example'] # list[str] | Specify result order. Zero or more entries with format: &ltkey> [desc] where orderByKeys lists allowed keys in each response. (optional)
                # str | Specify result filter. Format is similar to a SQL WHERE clause. For example, to filter object by name with prefix foo, use: name LIKE 'foo%'. Supported filter keys are the same as order by keys. (optional)
                filter = "type = \'%s\'" % service_class_type

                api_response = self.api.service_class_list(
                    self.authorization, page_index=page_index, page_size=page_size, filter=filter)
            else:
                api_response = self.api.service_class_list(self.authorization)
            logging.info("service_class_list API output: %s" % api_response)
            return api_response
        except ApiException as e:
            logging.error("Exception when calling Api->service_class_list: %s",e)
            raise

    def get_by_id(self, service_class_id):
        try:
            api_response = self.api.service_class_get(service_class_id, self.authorization)
            return api_response
        except ApiException as e:
            logging.error("Exception when calling ServiceClassApi->service_class_get: %s", e)
            raise

