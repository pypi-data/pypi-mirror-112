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
from kps_api.api.node_api import NodeApi  # noqa: E501
from kps_api.rest import ApiException
from kps_sdk import Auth, ServiceDomainEntityKit
from common import connection_info

class NodeEntityKit():

    def __init__(self):
        self.auth = Auth()
        self.configuration = self.auth.getAuthorizationHeader()
        self.authorization = self.configuration.get_api_key_with_prefix('Authorization')

        self.api_client = kps_api.ApiClient(configuration=self.configuration)
        self.api = kps_api.api.node_api.NodeApi(api_client=self.api_client)  # noqa: E501
        self.service_domain = ServiceDomainEntityKit()

    # create a new node. Pass the service domain and category if these objects do not exist
    # For adding a new node to an existing service domain, pass service domain and category as None
    def create(self, node, service_domain=None, category=None):
        try:
            if service_domain is not None and category is not None:
                api_response = self.service_domain.create(service_domain, category)
                if api_response is not None and api_response.id is not None and api_response.id != node.svc_domain_id:
                    node.svc_domain_id = api_response.id
            api_response = self.api.node_create(node, self.authorization)
            logging.info("Node created: id: %s", api_response.id)
            return api_response
        except ApiException as e:
            logging.error("Exception when calling NodeApi->node_create: %s", e)
            raise

    # Delete a node and optionally its parent service domain and category
    def delete(self, node_id, svc_domain_id=None, category_id=None):
        try:
            node_api_response = ''
            if node_id != svc_domain_id:
                node_api_response = self.api.node_delete(node_id, self.authorization)
                logging.info("Node deleted: id: %s", node_api_response.id)
            if svc_domain_id is not None and category_id is not None:
                svc_api_response = self.service_domain.delete(svc_domain_id, category_id)
            return node_api_response
        except ApiException as e:
            logging.error("Exception when calling NodeApi->node_delete: %s", e)
            raise

    def update(self, node_to_update):
        try:
            api_response = self.api.node_update(node_to_update, self.authorization, node_to_update.id)
            return api_response
        except ApiException as e:
            logging.error("Exception when calling NodeApi->node_update: %s", e)
            raise

    def onboard(self, node_onboard_info):
        try:
            self.api.node_onboarded(node_onboard_info)
        except ApiException as e:
            logging.error("Exception when calling NodeApi->node_onboarded: %s", e)
            raise

    def list(self, node_name=None):
        try:
            if node_name is not None:
                # int | 0-based index of the page to fetch results. (optional)
                page_index = 0
                page_size = 30000  # int | Item count of each page. (optional)
                # order_by = [] # list[str] | Specify result order. Zero or more entries with format: &ltkey> [desc] where orderByKeys lists allowed keys in each response. (optional)
                # str | Specify result filter. Format is similar to a SQL WHERE clause. For example, to filter object by name with prefix foo, use: name LIKE 'foo%'. Supported filter keys are the same as order by keys. (optional)
                filter = "name = \'%s\'" % node_name

                api_response = self.api.node_list(
                    self.authorization, page_index=page_index, page_size=page_size, filter=filter)
            else:
                api_response = self.api.node_list(self.authorization)
            return api_response
        except ApiException as e:
            logging.error("Exception when calling NodeApi->node_list: %s", e)
            raise

    def get_by_id(self, node_id):
        try:
            api_response = self.api.node_get(node_id, self.authorization)
            return api_response
        except ApiException as e:
            logging.error("Exception when calling NodeApi->node_get: %s", e)
            raise

    def get_by_project(self, project_id):
        try:
            api_response = self.api.project_get_nodes(project_id, self.authorization)
            return api_response
        except ApiException as e:
            logging.error("Exception when calling NodeApi->project_get_nodes: %s", e)
            raise

