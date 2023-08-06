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
from kps_api.api.node_info_api import NodeInfoApi  # noqa: E501
from kps_api.rest import ApiException
from kps_sdk import Auth

from common import connection_info

class NodeInfoEntityKit():

    def __init__(self):
        self.auth = Auth()
        self.configuration = self.auth.getAuthorizationHeader()
        self.authorization = self.configuration.get_api_key_with_prefix('Authorization')

        self.api_client = kps_api.ApiClient(configuration=self.configuration)
        self.api = kps_api.api.node_info_api.NodeInfoApi(api_client=self.api_client)  # noqa: E501


    def update(self, updated_info, node_id):
        try:
            api_response = self.api.node_info_update(updated_info, self.authorization, node_id)
            return api_response
        except ApiException as e:
            logging.error("Exception when calling NodeInfoApi->node_info_update: %s", e)
            raise

    def list(self):
        try:
            api_response = self.api.node_info_list(self.authorization)
            return api_response
        except ApiException as e:
            logging.error("Exception when calling NodeInfoApi->node_info_list: %s", e)
            raise

    def get_by_id(self, node_id):
        try:
            api_response = self.api.node_info_get(node_id, self.authorization)
            return api_response
        except ApiException as e:
            logging.error("Exception when calling NodeInfoApi->node_info_get: %s", e)
            raise

    def get_by_project(self, project_id):
        try:
            api_response = self.api.project_get_nodes_info(project_id, self.authorization)
            return api_response
        except ApiException as e:
            logging.error("Exception when calling NodeInfoApi->project_get_node_infos: %s", e)
            raise

