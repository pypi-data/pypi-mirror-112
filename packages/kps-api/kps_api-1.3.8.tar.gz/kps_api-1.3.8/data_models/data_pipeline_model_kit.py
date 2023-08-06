from data_models import BaseDataModel, DataSourceModelKit, CloudProfileModelKit, ProjectModelKit
import kps_api

class DataPipelineModelKit(BaseDataModel):
    
    def __init__(self):
        BaseDataModel.__init__(self)
        self.data_source_model_kit = DataSourceModelKit()
        self.cloud_profile_model_kit = CloudProfileModelKit()
        self.project_model_kit = ProjectModelKit()

    # model_id_1 and model_id_2 are short user-defined identifiers which will ensure unique id and name is given to the entity
    def get_data_models(self, model_id_1, model_id_2):
        data_source_prereq_models = self.data_source_model_kit.get_data_models(
            model_id_1, model_id_2)
        project_prereq_models = self.project_model_kit.get_data_models(model_id_1, model_id_2)
        retention_info_model = kps_api.RetentionInfo(limit=3600, type='Time')
        project_prereq_models['ServiceDomain'] = data_source_prereq_models['ServiceDomain']
        project_prereq_models['Category'] = data_source_prereq_models['Category']
        data_pipeline_model = kps_api.DataPipeline(
            aws_cloud_region = 'us-west-2',
            aws_stream_type = 'S3',
            cloud_creds_id = project_prereq_models['CloudProfile'].id,
            cloud_type = 'AWS',
            data_retention = [ retention_info_model ],
            data_type = 'Image',
            description = 'Data pipeline for test',
            destination = 'Cloud',
            enable_sampling = False,
            id = 'dpid{}{}'.format(model_id_1, model_id_2),
            name = 'dpname{}{}'.format(model_id_1, model_id_2),
            origin = 'Data Source',
            origin_selectors = data_source_prereq_models['DataSource'].selectors,
            project_id = project_prereq_models['Project'].id,
            transformation_args_list = [],
            size = 1)
        return {'DataPipeline': data_pipeline_model, 
                'DataSource': data_source_prereq_models['DataSource'],
                'Project': project_prereq_models['Project'],
                'ServiceDomain': project_prereq_models['ServiceDomain'],
                'Node': data_source_prereq_models['Node'],
                'Category': project_prereq_models['Category'],
                'CloudProfile': project_prereq_models['CloudProfile'],
                'User': project_prereq_models['User']
                }

