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
from kps_api.api.service_domain_api import ServiceDomainApi  # noqa: E501
from kps_api.rest import ApiException

from kps_sdk import Auth, CategoryEntityKit
from common import connection_info

class ServiceDomainEntityKit():

    def __init__(self):
        self.auth = Auth()
        self.configuration = self.auth.getAuthorizationHeader()
        self.authorization = self.configuration.get_api_key_with_prefix('Authorization')

        self.api_client = kps_api.ApiClient(configuration=self.configuration)
        self.api = kps_api.api.service_domain_api.ServiceDomainApi(api_client=self.api_client)  # noqa: E501
        self.category_entity_kit = CategoryEntityKit()

    def create(self, service_domain, category):
        try:
            _ = self.category_entity_kit.create(category)
            category_info = kps_api.CategoryInfo(id=category.id, value=category.values[0])
            service_domain.labels = [ category_info ]
            api_response = self.api.service_domain_create(service_domain, self.authorization)
            logging.info("ServiceDomain created: id: %s", api_response.id)
            return api_response
        except ApiException as e:
            logging.error("Exception when calling ServiceDomainApi->service_domain_create: %s",e)
            raise

    def delete(self, service_domain_id, category_id):
        try:
            _ = self.category_entity_kit.delete(category_id)
        except ApiException as e:
            logging.error("Exception when calling Category delete: %s",e)
        try:
            api_response = self.api.service_domain_delete(service_domain_id, self.authorization)
            logging.info("ServiceDomain deleted: id: %s", api_response.id)
            return api_response
        except ApiException as e:
            logging.error("Exception when calling ServiceDomainApi->service_domain_delete: %s",e)
            raise

    def update(self, service_domain):
        try:
            api_response = self.api.service_domain_update(service_domain, self.authorization, service_domain.id)
            return api_response
        except ApiException as e:
            logging.error("Exception when calling ServiceDomainApi->service_domain_update: %s",e)
            raise

    def get(self, service_domain_name=None):

        try:
            if service_domain_name is not None:
                # int | 0-based index of the page to fetch results. (optional)
                page_index = 0
                page_size = 100  # int | Item count of each page. (optional)
                # order_by = ['order_by_example'] # list[str] | Specify result order. Zero or more entries with format: &ltkey> [desc] where orderByKeys lists allowed keys in each response. (optional)
                # str | Specify result filter. Format is similar to a SQL WHERE clause. For example, to filter object by name with prefix foo, use: name LIKE 'foo%'. Supported filter keys are the same as order by keys. (optional)
                filter = "name = \'%s\'" % service_domain_name

                api_response = self.api.service_domain_list(
                    self.authorization, page_index=page_index, page_size=page_size, filter=filter)
            else:
                api_response = self.api.service_domain_list(
                    self.authorization)
            logging.info("service_domain_list API output: %s" % api_response)
            return api_response
        except ApiException as e:
            logging.error("Exception when calling Api->service_domain_list: %s",e)
            raise

    def get_by_id(self, service_domain_id):
        try:
            api_response = self.api.service_domain_get(service_domain_id, self.authorization)
            return api_response
        except ApiException as e:
            logging.error("Exception when calling ServiceDomainApi->service_domain_get: %s", e)
            raise

    def get_by_project(self, project_id):
        try:
            api_response = self.api.project_get_service_domains(project_id, self.authorization)
            return api_response
        except ApiException as e:
            logging.error("Exception when calling ServiceDomainApi->project_get_service_domain: %s", e)
            raise

    def get_nodes(self, service_domain_id):
        try:
            api_response = self.api.service_domain_get_nodes(service_domain_id, self.authorization)
            return api_response
        except ApiException as e:
            logging.error("Exception when calling ServiceDomainApi->service_domain_get_nodes: %s", e)
            raise
    
    def get_nodes_info(self, service_domain_id):
        try:
            api_response = self.api.service_domain_get_nodes_info(service_domain_id, self.authorization)
            return api_response
        except ApiException as e:
            logging.error("Exception when calling ServiceDomainApi->service_domain_get_nodesinfo: %s", e)
            raise
    
    def get_effective_profile(self, service_domain_id):
        try:
            api_response = self.api.service_domain_get_effective_profile(service_domain_id, self.authorization)
            return api_response
        except ApiException as e:
            logging.error("Exception when calling ServiceDomainApi->service_domain_get_effective_profile: %s", e)
            raise

