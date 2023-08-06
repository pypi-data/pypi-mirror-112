# coding: utf-8

"""
    KPS API reference.
    This is a wrapper on the Application API which provides easy functions to perform CRUD operations on the Application API.

"""

from __future__ import absolute_import

import logging
import uuid
import sys
import json
logging.basicConfig( stream=sys.stderr, format='%(funcName)s:%(levelname)s:%(message)s', level=logging.DEBUG )

import kps_api
from kps_api.api.container_registry_api import ContainerRegistryApi  # noqa: E501
from kps_api.rest import ApiException

from kps_sdk import Auth, UserEntityKit, CloudProfileEntityKit
from common import connection_info

class ContainerRegistryEntityKit():

    def __init__(self):
        self.auth = Auth()
        self.configuration = self.auth.getAuthorizationHeader()
        self.authorization = self.configuration.get_api_key_with_prefix('Authorization')

        self.api_client = kps_api.ApiClient(configuration=self.configuration)
        self.api = kps_api.api.container_registry_api.ContainerRegistryApi(api_client=self.api_client)  # noqa: E501
        self.cloud_profile_entity_kit = CloudProfileEntityKit()

    def create(self, container_registry, cloud_profile):
        try:
            # create a cloud profile and container registry
            profile = self.cloud_profile_entity_kit.create_aws_profile(cloud_profile)
            container_registry.cloud_credential_id = [ profile.id ]
            api_response = self.api.container_registry_create_v2(container_registry, self.authorization)
            logging.info("ContainerRegistry created: id: %s", api_response.id)
            return api_response, container_registry, profile
        except ApiException as e:
            logging.error("Exception when calling ContainerRegistryApi->container_registry_create_v2: %s",e)
            return None, container_registry, cloud_profile

    def delete(self, container_registry_id, cloud_profile_id):
        try:
            _ = self.cloud_profile_entity_kit.delete(cloud_profile_id)
            api_response = self.api.container_registry_delete_v2(container_registry_id, self.authorization)
            logging.info("ContainerRegistry deleted: id: %s", api_response.id)
            return api_response
        except ApiException as e:
            logging.error("Exception when calling ContainerRegistryApi->container_registry_delete_v2: %s",e)
            raise

    def get(self, container_registry_name=None):

        try:
            if container_registry_name is not None:
                # int | 0-based index of the page to fetch results. (optional)
                page_index = 0
                page_size = 100  # int | Item count of each page. (optional)
                # order_by = ['order_by_example'] # list[str] | Specify result order. Zero or more entries with format: &ltkey> [desc] where orderByKeys lists allowed keys in each response. (optional)
                # str | Specify result filter. Format is similar to a SQL WHERE clause. For example, to filter object by name with prefix foo, use: name LIKE 'foo%'. Supported filter keys are the same as order by keys. (optional)
                filter = "name = \'%s\'" % container_registry_name

                api_response = self.api.container_registry_list_v2(
                    self.authorization, page_index=page_index, page_size=page_size, filter=filter)
            else:
                api_response = self.api.container_registry_list_v2(
                    self.authorization)
                logging.info("container_registry_list API output: %s" % api_response)
                # returns ProjectListPayload object
            return api_response
        except ApiException as e:
            logging.error("Exception when calling ContainerRegistryApi->container_registry_list_v2: %s",e)
            raise
    
    def get_by_id(self, container_registry_id):
        try:
            api_response = self.api.container_registry_get_v2(container_registry_id, self.authorization)
            return api_response
        except ApiException as e:
            logging.error("Exception when calling ContainerRegistryApi->container_registry_get_v2: %s", e)
            raise

    def update(self, container_registry):
        try:
            api_response = self.api.container_registry_update_v2(container_registry, self.authorization, container_registry.id)
            return api_response
        except ApiException as e:
            logging.error("Exception when calling ContainerRegistryApi->container_registry_update_v2: %s", e)
            raise
    
    def get_by_project(self, project_id):
        try:
            api_response = self.api.project_get_container_registries_v2(project_id, self.authorization)
            return api_response
        except ApiException as e:
            logging.error("Exception when calling ContainerRegistryApi->project_get_container_registries_v2: %s", e)
            raise

