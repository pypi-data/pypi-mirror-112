from data_models import BaseDataModel, ProjectModelKit
import kps_api

class ApplicationModelKit(BaseDataModel):

    def __init__(self):
        BaseDataModel.__init__(self)
        self.project = ProjectModelKit()
        self.yaml_filename="../common/flask-web-server.yaml"

    def get_data_models(self, api_name, test_name):
        project_model = self.project.get_data_models(api_name, test_name)
        with open(self.yaml_filename, "r") as yamlFile:
            app_manifest = yamlFile.read()
        application_model = kps_api.ApplicationV2(
                id = 'appid{}{}'.format(api_name, test_name),
                name = 'appname{}{}'.format(api_name, test_name),
                description = 'Application for testing {}: {}'.format(api_name, test_name),
                project_id = project_model['Project'].id,
                app_manifest = app_manifest)
        return { 'Application': application_model,
                'Project': project_model['Project'], 
                'CloudProfile': project_model['CloudProfile'],
                'User': project_model['User'],
                'ServiceDomain': project_model['ServiceDomain'],
                'Category': project_model['Category'] }
