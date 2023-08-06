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
from kps_api.api.application_api import ApplicationApi  # noqa: E501
from kps_api.rest import ApiException

from kps_sdk import Auth, ProjectEntityKit
from common import connection_info

class ApplicationEntityKit():

    def __init__(self):
        self.auth = Auth()
        self.configuration = self.auth.getAuthorizationHeader()
        self.authorization = self.configuration.get_api_key_with_prefix('Authorization')
        self.project = ProjectEntityKit()
        self.api_client = kps_api.ApiClient(configuration=self.configuration)
        self.api = kps_api.api.application_api.ApplicationApi(api_client=self.api_client)  # noqa: E501

    def create(self, application, project, user, cloud_profile, service_domain, category):
        try:
            api_response = self.project.create(project, user, cloud_profile, service_domain, category)
        except ApiException as e:
            logging.error("Exception while creating project or its dependencies: %s", e)
            raise  
        try:
            api_response = self.api.application_create_v2(application, self.authorization)
            logging.info("Application created: id: %s", api_response.id)
            return api_response
        except ApiException as e:
            logging.error("Exception when calling ApplicationApi->application_create_v2: %s", e)
            raise

    def delete(self, app_id, project_id, user_id, profile_id, service_domain_id, category_id):
        try:
            app_api_response = self.api.application_delete_v2(self.authorization, app_id)
            logging.info("Application deleted: id: %s", app_api_response.id)
        except ApiException as e:
            logging.error("Exception when calling ApplicationApi->application_delete_v2: %s", e)
        try:
            _ = self.project.delete(project_id, user_id, profile_id, service_domain_id, category_id)
        except ApiException as e:
            logging.error("Exception while deleting project or its dependencies: %s", e)
        return app_api_response

    def update(self, application_object):
        try:
            api_response = self.api.application_update_v3(application_object, self.authorization, application_object.id)
            return api_response
        except ApiException as e:
            logging.error("Exception when calling ApplicationApi->application_update_v3: %s", e)
            raise

    def get(self, app_name=None):
        try:
            if app_name is not None:
                # int | 0-based index of the page to fetch results. (optional)
                page_index = 0
                page_size = 30000  # int | Item count of each page. (optional)
                # order_by = [] # list[str] | Specify result order. Zero or more entries with format: &ltkey> [desc] where orderByKeys lists allowed keys in each response. (optional)
                # str | Specify result filter. Format is similar to a SQL WHERE clause. For example, to filter object by name with prefix foo, use: name LIKE 'foo%'. Supported filter keys are the same as order by keys. (optional)
                filter = "name = \'%s\'" % app_name

                api_response = self.api.application_list_v2(
                    self.authorization, page_index=page_index, page_size=page_size, filter=filter)
            else:
                api_response = self.api.application_list_v2(self.authorization)
            # returns ApplicationListResponsePayload object
            return api_response
        except ApiException as e:
            logging.error("Exception when calling ApplicationApi->application_list_v2: %s", e)
            raise

    def get_by_id(self, app_id):
        try:
            api_response = self.api.application_get_v2(self.authorization, app_id)
            # returns ApplicationV2 object
            return api_response
        except ApiException as e:
            logging.error("Exception when calling ApplicationApi->application_get_v2: %s", e)
            raise

    def get_by_project(self, project_id):
        try:
            api_response = self.api.project_get_applications_v2(self.authorization, project_id)
            # returns ApplicationListResponsePayload object
            return api_response
        except ApiException as e:
            logging.error("Exception when calling ApplicationApi->project_get_applications_v2: %s", e)
            raise

    def get_status(self, app_id=None):
        try:
            if app_id is not None:
                api_response = self.api.application_status_get_v2(
                    self.authorization, app_id)
            else:
                api_response = self.api.application_status_list_v2(self.authorization)
            logging.info("application_status_list_v2 API output: %s" % api_response)
            # returns ApplicationStatusListPayload object
            return api_response
        except ApiException as e:
            logging.error("Exception when calling ApplicationStatusApi->application_status_list/get_v2: %s", e)
            raise

