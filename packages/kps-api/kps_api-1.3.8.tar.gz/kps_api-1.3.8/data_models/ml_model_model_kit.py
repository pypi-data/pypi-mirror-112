from data_models import BaseDataModel
import kps_api

class MLModelModelKit(BaseDataModel):

    def __init__(self):

        BaseDataModel.__init__(self)

    def get_data_models(self, api_name, test_name, framework_type):
        testdata_model = kps_api.MLModel(id = 'mlmodelid{}{}'.format(api_name, test_name),
            name = 'mlmodelname{}{}'.format(api_name, test_name),
            description = 'ML Model for {} API {} method test'.format(api_name, test_name),
            framework_type = framework_type,
            project_id = 'tobereplaced')
        return { 'MLModel': testdata_model }
