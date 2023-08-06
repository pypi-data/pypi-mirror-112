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
from kps_api.api.service_instance_api import ServiceInstanceApi  # noqa: E501
from kps_api.rest import ApiException

from kps_sdk import Auth, ProjectEntityKit
from common import connection_info

class ServiceInstanceEntityKit():

    def __init__(self):
        self.auth = Auth()
        self.configuration = self.auth.getAuthorizationHeader()
        self.authorization = self.configuration.get_api_key_with_prefix('Authorization')

        self.api_client = kps_api.ApiClient(configuration=self.configuration)
        self.api = kps_api.api.service_instance_api.ServiceInstanceApi(api_client=self.api_client)  # noqa: E501
        self.project = ProjectEntityKit()

    def create(self, service_instance, project, user, cloud_profile, service_domain, category):
        try:
            project_api_response, project_created = self.project.create(project, user, cloud_profile, service_domain, category)
            if service_instance.scope == 'PROJECT' and service_instance.scope_id != project_api_response.id:
                service_instance.scope_id = project_api_response.id
            api_response = self.api.service_instance_create(service_instance, self.authorization)
            logging.info("ServiceInstance created: id: %s", api_response.id)
            return api_response, project_created
        except ApiException as e:
            logging.error("Exception when calling ServiceInstanceApi->service_instance_create: %s",e)
            raise

    def delete(self, service_instance_id, project_id, user_id, profile_id, service_domain_id, category_id):
        api_response = None
        try:
            api_response = self.api.service_instance_delete(service_instance_id, self.authorization)
            logging.info("ServiceInstance deleted: id: %s", api_response.id)
        except ApiException as e:
            logging.error("Exception when calling ServiceInstanceApi->service_instance_delete: %s",e)
        try:
            api_response = self.project.delete(project_id, user_id, profile_id, service_domain_id, category_id)
            return api_response
        except ApiException as e:
            logging.error("Exception when calling Project Entity Kit delete: %s",e)
            raise

    def update(self, service_instance):
        try:
            api_response = self.api.service_instance_update(service_instance, self.authorization, service_instance.id)
            return api_response
        except ApiException as e:
            logging.error("Exception when calling ServiceInstanceApi->service_instance_update: %s",e)
            raise

    def get(self, service_instance_name=None):

        try:
            if service_instance_name is not None:
                # int | 0-based index of the page to fetch results. (optional)
                page_index = 0
                page_size = 100  # int | Item count of each page. (optional)
                # order_by = ['order_by_example'] # list[str] | Specify result order. Zero or more entries with format: &ltkey> [desc] where orderByKeys lists allowed keys in each response. (optional)
                # str | Specify result filter. Format is similar to a SQL WHERE clause. For example, to filter object by name with prefix foo, use: name LIKE 'foo%'. Supported filter keys are the same as order by keys. (optional)
                filter = "name = \'%s\'" % service_instance_name

                api_response = self.api.service_instance_list(
                    self.authorization, page_index=page_index, page_size=page_size, filter=filter)
            else:
                api_response = self.api.service_instance_list(
                    self.authorization)
                logging.info("service_instance_list API output: %s" % api_response)
            return api_response
        except ApiException as e:
            logging.error("Exception when calling Api->service_instance_list: %s",e)
            raise

    def get_by_id(self, service_instance_id):
        try:
            api_response = self.api.service_instance_get(service_instance_id, self.authorization)
            return api_response
        except ApiException as e:
            logging.error("Exception when calling ServiceInstanceApi->service_instance_get: %s", e)
            raise

    def get_status_by_id(self, service_instance_id):
        try:
            api_response = self.api.service_instance_status_list(service_instance_id, self.authorization)
            logging.info("service_instance_status_list API output: %s" % api_response)
            return api_response
        except ApiException as e:
            logging.error("Exception when calling Api->service_instance_status_list: %s",e)
            raise
