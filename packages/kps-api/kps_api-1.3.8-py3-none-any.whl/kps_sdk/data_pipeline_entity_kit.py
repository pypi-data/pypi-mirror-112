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
from kps_api.api.data_pipeline_api import DataPipelineApi  # noqa: E501
from kps_api.rest import ApiException
from kps_sdk import Auth, DataSourceEntityKit, ProjectEntityKit

class DataPipelineEntityKit():

    def __init__(self):
        self.auth = Auth()
        self.configuration = self.auth.getAuthorizationHeader()
        self.authorization = self.configuration.get_api_key_with_prefix('Authorization')

        self.api_client = kps_api.ApiClient(configuration=self.configuration)
        self.api = kps_api.api.data_pipeline_api.DataPipelineApi(api_client=self.api_client)  # noqa: E501
        self.data_source_entity_kit = DataSourceEntityKit()
        self.project_entity_kit = ProjectEntityKit()

    def create(self, data_pipeline, data_source, project, cloud_profile, user, service_domain, category, node):
        try:
            _ = self.project_entity_kit.create(project, user, cloud_profile, service_domain, category)
            _, data_source = self.data_source_entity_kit.create(data_source, node)
            api_response = self.api.data_pipeline_create(data_pipeline, self.authorization)
            logging.info("DataPipeline created: id: %s", api_response.id)
            return api_response
        except ApiException as e:
            logging.error("Exception when calling DataPipelineApi->data_pipeline_create: %s",e)
            raise

    def delete(self, data_pipeline_id, data_source_id, project_id, cloud_profile_id, 
                user_id, service_domain_id, node_id, category_id):
        try:
            api_response = self.api.data_pipeline_delete(data_pipeline_id, self.authorization)
            logging.info("DataPipeline deleted: id: %s", api_response.id)
            _ = self.data_source_entity_kit.delete(data_source_id, node_id, self.authorization)
            _ = self.project_entity_kit.delete(project_id, user_id, cloud_profile_id, service_domain_id, category_id)
            return api_response
        except ApiException as e:
            logging.error("Exception when calling DataPipelineApi->data_pipeline_delete: %s",e)
            raise

    def get(self, data_pipeline_name=None):

        try:
            if data_pipeline_name is not None:
                # int | 0-based index of the page to fetch results. (optional)
                page_index = 0
                page_size = 100  # int | Item count of each page. (optional)
                # order_by = ['order_by_example'] # list[str] | Specify result order. Zero or more entries with format: &ltkey> [desc] where orderByKeys lists allowed keys in each response. (optional)
                # str | Specify result filter. Format is similar to a SQL WHERE clause. For example, to filter object by name with prefix foo, use: name LIKE 'foo%'. Supported filter keys are the same as order by keys. (optional)
                filter = "name = \'%s\'" % data_pipeline_name

                api_response = self.api.data_pipeline_list(
                    self.authorization, page_index=page_index, page_size=page_size, filter=filter)
            else:
                api_response = self.api.data_pipeline_list(
                    self.authorization)
                logging.info("data_pipeline_list API output: %s" % api_response)
                # returns DataSourceListPayload object
            return api_response
        except ApiException as e:
            logging.error("Exception when calling DataPipelineApi->data_pipeline_list: %s",e)
            raise
    
    def get_by_id(self, data_pipeline_id):
        try:
            api_response = self.api.data_pipeline_get(data_pipeline_id, self.authorization)
            return api_response
        except ApiException as e:
            logging.error("Exception when calling DataPipelineApi->data_pipeline_get: %s", e)
            raise

    def update(self, data_pipeline):
        try:
            api_response = self.api.data_pipeline_update(data_pipeline, self.authorization, data_pipeline.id)
            return api_response
        except ApiException as e:
            logging.error("Exception when calling DataPipelineApi->data_pipeline_update: %s", e)
            raise

    def get_node_containers(self, data_pipeline_id, node_id):
        try:
            api_response = self.api.get_data_pipeline_containers(data_pipeline_id, node_id, self.authorization)
            return api_response
        except ApiException as e:
            logging.error("Exception when calling DataPipelineApi->get_data_pipeline_containers: %s", e)
            raise

    def get_by_project(self, project_id):
        try:
            api_response = self.api.project_get_data_pipelines(project_id, self.authorization)
            return api_response
        except ApiException as e:
            logging.error("Exception when calling DataPipelineApi->project_get_data_pipelines: %s", e)
            raise

