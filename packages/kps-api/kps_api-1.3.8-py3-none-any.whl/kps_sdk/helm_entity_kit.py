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
from kps_api.api.helm_api import HelmApi  # noqa: E501
from kps_api.rest import ApiException
from kps_sdk import Auth, ProjectEntityKit, NodeEntityKit, NodeInfoEntityKit
from common import connection_info

class HelmEntityKit():

    def __init__(self):
        self.auth = Auth()
        self.configuration = self.auth.getAuthorizationHeader()
        self.authorization = self.configuration.get_api_key_with_prefix('Authorization')

        self.api_client = kps_api.ApiClient(configuration=self.configuration)
        self.api = kps_api.api.helm_api.HelmApi(api_client=self.api_client)  # noqa: E501
        self.project = ProjectEntityKit()
        self.node = NodeEntityKit()
        self.node_info = NodeInfoEntityKit()

    # create a new Helm App in a new project
    def create(self, chart, values, application, project, user, cloud_profile, service_domain, category, nodes):
        # create project, user, cloud profile, service domain and category
        try:
            api_response = self.project.create(project, user, cloud_profile, service_domain, category)
        except ApiException as e:
            logging.error("Exception while creating project or its dependencies: %s", e)
            raise
        # create nodes in the service domain and set the service domain version to v2.1.0
        # Helm app requires Kafka service to be enabled which can be done only for service domain versions above 2.0.0
        try:
            api_response = self.node.create(nodes[0])
            node_id = api_response.id
            logging.info("Node id: %s", node_id)
            api_response = self.node.create(nodes[1])
            logging.info("Node id: %s", api_response.id)
            api_response = self.node.create(nodes[2])
            logging.info("Node id: %s", api_response.id)
            logging.info("Done with node creation")
        except Exception as e:
            logging.error("Exception while creating nodes: %s", e)
            # Not raising the exception since NodeInfo Update returns an error which is a known issue
            # raise
        logging.info("Now calling helm app create")
        try:
            api_response = self.api.helm_application_create(chart=chart, values=values,
                application=application, url="testurl", authorization=self.authorization)
            logging.info("Helm application created: id: %s", api_response.id)
            return api_response
        except Exception as e:
            logging.error("Exception when calling HelmApi->helm_application_create: %s", e)
            raise

    def update(self, chart, values, application, application_id):
        try:
            api_response = self.api.helm_application_update(chart=chart, values=values,
                application=application, authorization=self.authorization,
                url="testurl", id=application_id)
            logging.info("Helm Application updated: id: %s", application_id)
            return api_response
        except ApiException as e:
            logging.error("Exception when calling HelmApi->helm_application_update: %s", e)
            raise

    def create_template(self, chart, values, release, namespace):
        try:
            api_response = self.api.helm_template(chart=chart, values=values,
                release=release, namespace=namespace,
                url="testurl", authorization=self.authorization)
            logging.info("Helm template created with the following metadata %s", api_response.metadata)
            return api_response
        except ApiException as e:
            logging.error("Exception when calling HelmApi->helm_template: %s", e)
            raise

