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
from kps_api.api.category_api import CategoryApi  # noqa: E501
from kps_api.rest import ApiException

from kps_sdk import Auth
from common import connection_info

class CategoryEntityKit():

    def __init__(self):
        self.auth = Auth()
        self.configuration = self.auth.getAuthorizationHeader()
        self.authorization = self.configuration.get_api_key_with_prefix('Authorization')

        self.api_client = kps_api.ApiClient(configuration=self.configuration)
        self.api = kps_api.api.category_api.CategoryApi(api_client=self.api_client)  # noqa: E501

    def create(self, category):
        try:
            api_response = self.api.category_create_v2(category, self.authorization)
            logging.info("Category created: id: %s", api_response.id)
            return api_response
        except ApiException as e:
            logging.error("Exception when calling CategoryApi->category_create_v2: %s",e)
            raise

    def delete(self, category_id):
        try:
            api_response = self.api.category_delete_v2(category_id, self.authorization)
            logging.info("Category deleted: id: %s", api_response.id)
            return api_response
        except ApiException as e:
            logging.error("Exception when calling CategoryApi->category_delete_v2: %s",e)
            raise

    def get(self):
        try:
            api_response = self.api.category_list_v2(self.authorization)
            logging.info("category_list API output: %s" % api_response)
            return api_response
        except ApiException as e:
            logging.error("Exception when calling CategoryApi->category_list_v2: %s",e)
            raise

    def get_by_id(self, category_id):
        try:
            api_response = self.api.category_get_v2(category_id, self.authorization)
            return api_response
        except ApiException as e:
            logging.error("Exception when calling CategoryApi->category_get_v2: %s", e)
            raise


