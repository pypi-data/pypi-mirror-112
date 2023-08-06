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
from common import connection_info
logging.basicConfig( stream=sys.stderr, format='%(funcName)s:%(levelname)s:%(message)s', level=logging.DEBUG )

import kps_api
from kps_api.api.data_source_api import DataSourceApi  # noqa: E501
from kps_api.rest import ApiException
from kps_sdk import Auth, NodeEntityKit

class DataSourceEntityKit():

    def __init__(self):
        self.auth = Auth()
        self.configuration = self.auth.getAuthorizationHeader()
        self.authorization = self.configuration.get_api_key_with_prefix('Authorization')

        self.api_client = kps_api.ApiClient(configuration=self.configuration)
        self.api = kps_api.api.data_source_api.DataSourceApi(api_client=self.api_client)  # noqa: E501
        self.node_entity_kit = NodeEntityKit()

    def create(self, data_source, node, service_domain=None, category=None):
        try:
            if service_domain is not None and category is not None:
                api_response = self.node_entity_kit.create(node, service_domain, category)
                data_source.edge_id = node.svc_domain_id
            else:
                api_response = self.node_entity_kit.create(node)
                logging.info("Node creation response: id: %s", api_response.id)
                data_source.edge_id = node.svc_domain_id
            logging.info("Creating data source with these details: %s", data_source)
            api_response = self.api.data_source_create_v2(data_source, self.authorization)
            logging.info("DataSource created: id: %s", api_response.id)
            return api_response, data_source
        except ApiException as e:
            logging.error("Exception when calling DataSourceApi->data_source_create_v2: %s",e)
            raise

    def delete(self, data_source_id, node_id, service_domain_id=None, category_id=None):
        try:
            api_response = self.api.data_source_delete_v2(data_source_id, self.authorization)
            logging.info("DataSource deleted: id: %s", api_response.id)
            _ = self.node_entity_kit.delete(node_id, service_domain_id, category_id)
            return api_response
        except ApiException as e:
            logging.error("Exception when calling DataSourceApi->data_source_delete_v2: %s",e)
            raise

    def get(self, data_source_name=None):

        try:
            if data_source_name is not None:
                # int | 0-based index of the page to fetch results. (optional)
                page_index = 0
                page_size = 100  # int | Item count of each page. (optional)
                # order_by = ['order_by_example'] # list[str] | Specify result order. Zero or more entries with format: &ltkey> [desc] where orderByKeys lists allowed keys in each response. (optional)
                # str | Specify result filter. Format is similar to a SQL WHERE clause. For example, to filter object by name with prefix foo, use: name LIKE 'foo%'. Supported filter keys are the same as order by keys. (optional)
                filter = "name = \'%s\'" % data_source_name

                api_response = self.api.data_source_list_v2(
                    self.authorization, page_index=page_index, page_size=page_size, filter=filter)
            else:
                api_response = self.api.data_source_list_v2(
                    self.authorization)
                logging.info("data_source_list API output: %s" % api_response)
                # returns DataSourceListPayload object
            return api_response
        except ApiException as e:
            logging.error("Exception when calling DataSourceApi->data_source_list_v2: %s",e)
            raise
    
    def get_by_id(self, data_source_id):
        try:
            api_response = self.api.data_source_get_v2(data_source_id, self.authorization)
            return api_response
        except ApiException as e:
            logging.error("Exception when calling DataSourceApi->data_source_get_v2: %s", e)
            raise

    def update(self, data_source):
        try:
            api_response = self.api.data_source_update_v3(data_source, self.authorization, data_source.id)
            return api_response
        except ApiException as e:
            logging.error("Exception when calling DataSourceApi->data_source_update_v3: %s", e)
            raise

    def get_artifacts(self, data_source_id):
        try:
            api_response = self.api.data_source_get_artifact_v2(data_source_id, self.authorization)
            return api_response
        except ApiException as e:
            logging.error("Exception when calling DataSourceApi->data_source_get_artifact_v2: %s", e)
            raise

    def get_by_node(self, node_id):
        try:
            api_response = self.api.edge_get_datasources_v2(node_id, self.authorization)
            return api_response
        except ApiException as e:
            logging.error("Exception when calling DataSourceApi->edge_get_datasources_v2: %s", e)
            raise

