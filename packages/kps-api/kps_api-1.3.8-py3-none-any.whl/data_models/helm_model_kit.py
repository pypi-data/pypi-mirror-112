import kps_api
from data_models import BaseDataModel, ProjectModelKit, NodeModelKit
import json

class HelmModelKit(BaseDataModel):

    def __init__(self):
        BaseDataModel.__init__(self)
        self.project_model_kit = ProjectModelKit()
        self.node_model_kit = NodeModelKit()

    # api_name and test_name are short user-defined identifiers which will ensure unique id and name is given to the entity
    def get_data_models(self, api_name, test_name):
        project_model = self.project_model_kit.get_data_models(api_name, test_name)
        # Need application model in the following format. 
        # {"edgeIds":["24628f35-3957-4c86-a63f-646ae3a20838"],"excludeEdgeIds":[],"edgeSelectors":[],
        # "name":"mynewk8sapp","appManifest":"","tenantId":"tenant-id-waldot","description":"TEST",
        # "projectId":"c8f0a2e0-2b56-4c28-8569-4e71b7f96318","packagingType":"helm" }
        application_model = { 'id': 'helmappid{}{}'.format(api_name, test_name),
            'name': 'helmappname{}{}'.format(api_name, test_name),
            'description': 'Helm app for testing {} {}'.format(api_name, test_name),
            'edgeIds': [ project_model['ServiceDomain'].id ],
            'projectId': project_model['Project'].id,
            'packagingType': 'helm' }
        app_json = json.dumps(application_model)
        chart_data = './mytestchart-0.1.0.tgz'
        values = './values.yaml'
        # get 3 node models for creating a multi-node service domain
        node_model_1 = self.node_model_kit.get_data_models(api_name, test_name + '1', project_model['ServiceDomain'].id)
        node_model_2 = self.node_model_kit.get_data_models(api_name, test_name + '2', project_model['ServiceDomain'].id)
        node_model_3 = self.node_model_kit.get_data_models(api_name, test_name + '3', project_model['ServiceDomain'].id)
        return { 'Application': app_json,
            'Project': project_model['Project'],
            'User': project_model['User'],
            'CloudProfile': project_model['CloudProfile'],
            'ServiceDomain': project_model['ServiceDomain'],
            'Category': project_model['Category'],
            'Chart': chart_data,
            'Values': values,
            'Nodes': [ node_model_1['Node'], node_model_2['Node'], node_model_3['Node'] ] }

    def get_template_model(self):
        chart_data = './woodkraft-apps.tgz'
        values = './values.yaml'
        release = '2'
        namespace = 'mynamespace'
        return { 'Chart': chart_data,
            'Values': values,
            'Release': release,
            'Namespace': namespace }

    
