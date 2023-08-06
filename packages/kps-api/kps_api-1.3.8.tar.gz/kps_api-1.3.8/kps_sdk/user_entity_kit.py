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
from kps_api.rest import ApiException
from kps_sdk import Auth
from common import connection_info

class UserEntityKit():

    def __init__(self):
        self.auth = Auth()
        self.configuration = self.auth.getAuthorizationHeader()
        self.authorization = self.configuration.get_api_key_with_prefix('Authorization')

        self.api_client = kps_api.ApiClient(configuration=self.configuration)

    def create(self, user):
        try:
            header_params = {}
            # HTTP header `Accept`
            header_params['Accept'] = self.api_client.select_header_accept(['application/json'])  # noqa: E501

            # HTTP header `Content-Type`
            header_params['Content-Type'] = self.api_client.select_header_content_type(['application/json'])  # noqa: E501

            header_params['Authorization'] = self.authorization
            auth_settings = [ 'BearerToken' ]
            body_params = {
                "id": user.id,
                "name": user.name,
                "email": user.email,
                "password": user.password,
                "role": user.role,
            }
            api_response = self.api_client.call_api(
                '/v1/users', 'POST',
                {},
                {},
                header_params,
                auth_settings=auth_settings,
                body=body_params,
                response_type='str')
            logging.info("User created: response: %s", api_response)
            return api_response
        except ApiException as e:
            logging.error("Exception when calling user api create: %s",e)
            raise

    def delete(self, user_id):
        try:
            header_params = {}
            header_params['Authorization'] = self.authorization
            auth_settings = [ 'BearerToken' ]
            delete_url = '/v1/users/' + user_id
            api_response = self.api_client.call_api(
                delete_url, 'DELETE',
                {},
                {},
                header_params,
                auth_settings=auth_settings,
                response_type='str')
            logging.info("User deleted: response: %s", api_response)
            return api_response
        except ApiException as e:
            logging.error("Exception when calling user api delete %s",e)
            raise

    def get(self):
        try:
            header_params = {}
            header_params['Authorization'] = self.authorization
            auth_settings = [ 'BearerToken' ]
            get_url = '/v1/users/' 
            api_response = self.api_client.call_api(
                get_url, 'GET',
                {},
                {},
                header_params,
                auth_settings=auth_settings,
                response_type='str')
            return api_response
        except ApiException as e:
            logging.error("Exception when calling user api get %s",e)
            raise

