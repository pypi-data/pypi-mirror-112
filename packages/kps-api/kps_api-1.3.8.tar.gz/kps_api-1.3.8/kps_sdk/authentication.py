from __future__ import print_function
import kps_api
from kps_api.rest import ApiException
import unittest
import logging
import sys
from common import connection_info

logging.basicConfig( stream=sys.stderr, format='%(funcName)s:%(levelname)s:%(message)s', level=logging.DEBUG )

class Auth():

    Token = 'None'

    def __init__(self):
    
        self.configuration = kps_api.Configuration()
        self.configuration.host = connection_info.KPS_ENDPOINT
        self.api_client = kps_api.ApiClient(configuration=self.configuration)

        # create an instance of the API class
        self.api_instance = kps_api.AuthApi(api_client=self.api_client)

    def loginUsingAuthTag(self, userEmail, userPwd):

        try:
            # Lets the user log in.
            self.request = kps_api.Credential(userEmail, userPwd)
            api_response = self.api_instance.login_call_v2(self.request)

            # Configure API key authorization: BearerToken
            self.configuration.api_key['Authorization'] = api_response.token
            # Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
            self.configuration.api_key_prefix['Authorization'] = 'Bearer'
            self.configuration.debug = False

            return self.configuration, api_response.token

        except ApiException as e:
            logging.error("Exception when calling AuthApi->login_call_v2: %s", e)
            raise

    def getAuthorizationHeader(self):
        self.configuration.api_key['Authorization'] = Auth.Token
        self.configuration.api_key_prefix['Authorization'] = 'Bearer'
        return self.configuration

    
