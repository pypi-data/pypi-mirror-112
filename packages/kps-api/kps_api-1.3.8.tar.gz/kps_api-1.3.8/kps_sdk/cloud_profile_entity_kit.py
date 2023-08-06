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
from kps_api.api.cloud_profile_api import CloudProfileApi  # noqa: E501
from kps_api.rest import ApiException

from kps_sdk import Auth
from common import connection_info

class CloudProfileEntityKit():

    def __init__(self):
        self.auth = Auth()
        self.configuration = self.auth.getAuthorizationHeader()
        self.authorization = self.configuration.get_api_key_with_prefix('Authorization')

        self.api_client = kps_api.ApiClient(configuration=self.configuration)
        self.api = kps_api.api.cloud_profile_api.CloudProfileApi(api_client=self.api_client)  # noqa: E501

    def create_aws_profile(self, profile):
        try:
            api_response = self.api.cloud_profile_create(profile, self.authorization)
            logging.info("CloudProfile created: id: %s", api_response.id)
            return api_response
        except ApiException as e:
            logging.error("Exception when calling CloudProfileApi->cloud_profile_create: %s", e)
            raise


    def delete(self, profile_id):

        try:
            api_response = self.api.cloud_profile_delete(profile_id, self.authorization)
            logging.info("CloudProfile deleted: id: %s", api_response.id)
            return api_response
        except ApiException as e:
            logging.error("Exception when calling CloudProfileApi->cloud_profile_delete: %s", e)
            raise

    def update(self, profile):
        try:
            api_response = self.api.cloud_profile_update(profile, self.authorization, profile.id)
            return api_response
        except ApiException as e:
            logging.error("Exception when calling CloudProfileApi->cloud_profile_update: %s", e)
            raise

    def list(self, profile_name=None):
        try:
            if profile_name is not None:
                # int | 0-based index of the page to fetch results. (optional)
                page_index = 0
                page_size = 30000  # int | Item count of each page. (optional)
                # order_by = [] # list[str] | Specify result order. Zero or more entries with format: &ltkey> [desc] where orderByKeys lists allowed keys in each response. (optional)
                # str | Specify result filter. Format is similar to a SQL WHERE clause. For example, to filter object by name with prefix foo, use: name LIKE 'foo%'. Supported filter keys are the same as order by keys. (optional)
                filter = "name = \'%s\'" % profile_name

                api_response = self.api.cloud_profile_list(
                    self.authorization, page_index=page_index, page_size=page_size, filter=filter)
            else:
                api_response = self.api.cloud_profile_list(self.authorization)
            return api_response
        except ApiException as e:
            logging.error("Exception when calling CloudProfileApi->cloud_profile_list: %s", e)
            raise

    def get_by_id(self, profile_id):
        try:
            api_response = self.api.cloud_profile_get(profile_id, self.authorization)
            return api_response
        except ApiException as e:
            logging.error("Exception when calling CloudProfileApi->cloud_profile_get: %s", e)
            raise

    def get_by_project(self, project_id):
        try:
            api_response = self.api.project_get_cloud_profiles(project_id, self.authorization)
            return api_response
        except ApiException as e:
            logging.error("Exception when calling CloudProfileApi->project_get_cloud_profiles: %s", e)
            raise

