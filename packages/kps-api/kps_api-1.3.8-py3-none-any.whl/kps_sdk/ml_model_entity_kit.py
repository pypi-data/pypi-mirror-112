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
from kps_api.api.ml_model_api import MLModelApi  # noqa: E501
from kps_api.rest import ApiException
from kps_sdk import Auth
from common import connection_info

class MLModelEntityKit():

    def __init__(self):
        self.auth = Auth()
        self.configuration = self.auth.getAuthorizationHeader()
        self.authorization = self.configuration.get_api_key_with_prefix('Authorization')

        self.api_client = kps_api.ApiClient(configuration=self.configuration)
        self.api = kps_api.api.ml_model_api.MLModelApi(api_client=self.api_client)  # noqa: E501

    # create a new ML Model in the default project
    def create(self, ml_model):
        try:
            api_response = self.api.m_l_model_create(ml_model, self.authorization)
            logging.info("ML Model created: id: %s", api_response.id)
            return api_response
        except Exception as e:
            logging.error("Exception when calling MLModelApi->m_l_model_create: %s", e)
            raise

    # Delete an ML model
    def delete(self, ml_model_id):
        try:
            api_response = self.api.m_l_model_delete(ml_model_id, self.authorization)
            logging.info("ML Model deleted: id: %s", api_response.id)
            return api_response
        except ApiException as e:
            logging.error("Exception when calling MLModelApi->m_l_model_delete: %s", e)
            raise

    def update(self, ml_model_to_update):
        try:
            api_response = self.api.m_l_model_update(ml_model_to_update, 
                self.authorization, ml_model_to_update.id)
            logging.info("ML Model updated: id: %s", api_response.id)
            return api_response
        except ApiException as e:
            logging.error("Exception when calling MLModelApi->m_l_model_update: %s", e)
            raise

    def list(self, ml_model_name=None):
        try:
            if ml_model_name is not None:
                # int | 0-based index of the page to fetch results. (optional)
                page_index = 0
                page_size = 30000  # int | Item count of each page. (optional)
                # order_by = [] # list[str] | Specify result order. Zero or more entries with format: &ltkey> [desc] where orderByKeys lists allowed keys in each response. (optional)
                # str | Specify result filter. Format is similar to a SQL WHERE clause. For example, to filter object by name with prefix foo, use: name LIKE 'foo%'. Supported filter keys are the same as order by keys. (optional)
                filter = "name = \'%s\'" % ml_model_name

                api_response = self.api.m_l_model_list(
                    self.authorization, page_index=page_index, page_size=page_size, filter=filter)
            else:
                api_response = self.api.m_l_model_list(self.authorization)
            return api_response
        except ApiException as e:
            logging.error("Exception when calling MLModelApi->m_l_model_list: %s", e)
            raise

    def get_by_id(self, ml_model_id):
        try:
            api_response = self.api.m_l_model_get(ml_model_id, self.authorization)
            return api_response
        except ApiException as e:
            logging.error("Exception when calling MLModelApi->m_l_model_get: %s", e)
            raise

    def get_by_project(self, project_id):
        try:
            api_response = self.api.project_get_ml_models(project_id, self.authorization)
            return api_response
        except ApiException as e:
            logging.error("Exception when calling MLModelApi->project_get_m_l_models: %s", e)
            raise

    def create_version(self, ml_model_id, model_version, payload):
        try:
            api_response = self.api.m_l_model_version_create(payload, 
                self.authorization, model_version, ml_model_id)
            logging.info("ML Model version %s created: id: %s", model_version, api_response.id)
            return api_response
        except ApiException as e:
            logging.error("Exception when calling MLModelApi->m_l_model_version_create: %s", e)
            raise

    def delete_version(self, ml_model_id, model_version):
        try:
            api_response = self.api.m_l_model_version_delete(ml_model_id, model_version, self.authorization)
            logging.info("ML Model version %s deleted: id: %s", model_version, api_response.id)
            return api_response
        except ApiException as e:
            logging.error("Exception when calling MLModelApi->m_l_model_version_delete: %s", e)
            raise

    def update_version(self, ml_model_id, model_version):
        try:
            api_response = self.api.m_l_model_version_update(ml_model_id, model_version, self.authorization)
            logging.info("ML Model version %s updated: id: %s", model_version, api_response.id)
            return api_response
        except ApiException as e:
            logging.error("Exception when calling MLModelApi->m_l_model_version_update: %s", e)
            raise

    def get_version_presigned_url(self, ml_model_id, model_version, expiration_in_minutes=None):
        try:
            api_response = self.api.m_l_model_version_url_get(ml_model_id, model_version, self.authorization)
            logging.info("ML Model id: %s: version presigned url: %s", ml_model_id, api_response.url)
            return api_response
        except ApiException as e:
            logging.error("Exception when calling MLModelApi->m_l_model_version_update: %s", e)
            raise

