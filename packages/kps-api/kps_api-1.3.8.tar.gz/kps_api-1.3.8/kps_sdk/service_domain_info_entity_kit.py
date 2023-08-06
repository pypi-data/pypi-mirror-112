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
from kps_api.api.service_domain_info_api import ServiceDomainInfoApi  # noqa: E501
from kps_api.rest import ApiException
from kps_sdk import Auth
from common import connection_info

class ServiceDomainInfoEntityKit():

    def __init__(self):
        self.auth = Auth()
        self.configuration = self.auth.getAuthorizationHeader()
        self.authorization = self.configuration.get_api_key_with_prefix('Authorization')

        self.api_client = kps_api.ApiClient(configuration=self.configuration)
        self.api = kps_api.api.service_domain_info_api.ServiceDomainInfoApi(api_client=self.api_client)  # noqa: E501

    def update(self, service_domain_info):
        try:
            api_response = self.api.service_domain_info_update(service_domain_info, self.authorization, service_domain_info.id)
            return api_response
        except ApiException as e:
            logging.error("Exception when calling ServiceDomainInfoApi->service_domain_info_update: %s",e)
            raise

    def get(self):

        try:
           api_response = self.api.service_domain_info_list(self.authorization)
           logging.info("service_domain_info_list API output: %s" % api_response)
           return api_response
        except ApiException as e:
           logging.error("Exception when calling Api->service_domain_info_list: %s",e)
           raise

    def get_by_id(self, service_domain_id):
        try:
            api_response = self.api.service_domain_info_get(service_domain_id, self.authorization)
            return api_response
        except ApiException as e:
            logging.error("Exception when calling ServiceDomainInfoApi->service_domain_info_get: %s", e)
            raise

    def get_by_project(self, project_id):
        try:
            api_response = self.api.project_get_service_domains_info(project_id, self.authorization)
            return api_response
        except ApiException as e:
            logging.error("Exception when calling ServiceDomainInfoApi->project_get_service_domain_info: %s", e)
            raise

