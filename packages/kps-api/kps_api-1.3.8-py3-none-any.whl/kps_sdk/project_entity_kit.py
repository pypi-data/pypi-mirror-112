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
from kps_api.api.project_api import ProjectApi  # noqa: E501
from kps_api.rest import ApiException

from kps_sdk import Auth, UserEntityKit, CloudProfileEntityKit, ServiceDomainEntityKit
from common import connection_info

class ProjectEntityKit():

    def __init__(self):
        self.auth = Auth()
        self.configuration = self.auth.getAuthorizationHeader()
        self.authorization = self.configuration.get_api_key_with_prefix('Authorization')
        self.api_client = kps_api.ApiClient(configuration=self.configuration)
        self.api = kps_api.api.project_api.ProjectApi(api_client=self.api_client)  # noqa: E501
        self.user_entity_kit = UserEntityKit()
        self.cloud_profile_entity_kit = CloudProfileEntityKit()
        self.service_domain_entity_kit = ServiceDomainEntityKit()

    def create(self, project, user, cloud_profile, service_domain, category):
        try:
            # create a cloud profile, user, service domain with a new category. Provide these as input to the new project creation
            # add the user running tests also to the project
            profile = self.cloud_profile_entity_kit.create_aws_profile(cloud_profile)
            if profile is not None and profile.id is not None and profile.id != project.cloud_credential_ids[0]:
                project.cloud_credential_ids = [ profile.id ]
            _ = self.user_entity_kit.create(user) 
            sv_api_response = self.service_domain_entity_kit.create(service_domain, category)
            if sv_api_response is not None and sv_api_response.id is not None and sv_api_response.id != project.edge_ids[0]:
                    project.edge_ids = [ service_domain.id ]
            api_response = self.api.project_create_v2(project, self.authorization)
            logging.info("Project created: id: %s", api_response.id)
            return api_response, project
        except ApiException as e:
            logging.error("Exception when calling ProjectApi->project_create_v2: %s",e)
            raise

    def delete(self, project_id, user_id, cloud_profile_id, service_domain_id, category_id):
        try:
            _ = self.cloud_profile_entity_kit.delete(cloud_profile_id)
        except ApiException as e:
            logging.error("Exception when calling CloudProfile delete: %s",e)
        try:
            _ = self.user_entity_kit.delete(user_id)
        except ApiException as e:
            logging.error("Exception when calling User delete: %s",e)
        try:
            _ = self.service_domain_entity_kit.delete(service_domain_id, category_id)
        except ApiException as e:
            logging.error("Exception when calling ServiceDomain delete: %s",e)
        try:
            api_response = self.api.project_delete_v2(project_id, self.authorization)
            logging.info("Project deleted: id: %s", api_response.id)
            return api_response
        except ApiException as e:
            logging.error("Exception when calling ProjectApi->project_delete_v2: %s",e)
            raise

    def get(self, project_name=None):

        try:
            if project_name is not None:
                # int | 0-based index of the page to fetch results. (optional)
                page_index = 0
                page_size = 100  # int | Item count of each page. (optional)
                # order_by = ['order_by_example'] # list[str] | Specify result order. Zero or more entries with format: &ltkey> [desc] where orderByKeys lists allowed keys in each response. (optional)
                # str | Specify result filter. Format is similar to a SQL WHERE clause. For example, to filter object by name with prefix foo, use: name LIKE 'foo%'. Supported filter keys are the same as order by keys. (optional)
                filter = "name = \'%s\'" % project_name

                api_response = self.api.project_list_v2(
                    self.authorization, page_index=page_index, page_size=page_size, filter=filter)
            else:
                api_response = self.api.project_list_v2(
                    self.authorization)
                logging.info("project_list API output: %s" % api_response)
                # returns ProjectListPayload object
            return api_response
        except ApiException as e:
            logging.error("Exception when calling ProjectApi->project_list_v2: %s",e)
            raise
    
    def get_by_id(self, project_id):
        try:
            api_response = self.api.project_get_v2(project_id, self.authorization)
            return api_response
        except ApiException as e:
            logging.error("Exception when calling ProjectApi->project_get_v2: %s", e)
            raise

    def update(self, project):
        try:
            api_response = self.api.project_update_v3(project, self.authorization, project.id)
            return api_response
        except ApiException as e:
            logging.error("Exception when calling ProjectApi->project_update_v3: %s", e)
            raise

