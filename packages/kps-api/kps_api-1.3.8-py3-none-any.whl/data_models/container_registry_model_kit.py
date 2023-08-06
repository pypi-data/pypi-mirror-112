from data_models import BaseDataModel, CloudProfileModelKit
import kps_api
from common import connection_info

class ContainerRegistryModelKit(BaseDataModel):
    
    def __init__(self):
        BaseDataModel.__init__(self)
        self.cloud_profile_model_kit = CloudProfileModelKit()
    
    # model_id_1 and model_id_2 are short user-defined identifiers which will ensure unique id and name is given to the entity
    def get_data_models(self, model_id_1, model_id_2):
        cloud_profile_model = self.cloud_profile_model_kit.get_data_models(model_id_1, model_id_2)
        cloud_profile_info = kps_api.CloudProfileInfo(cloud_profile_model.id)
        container_registry_info = kps_api.ContainerRegistryInfo(email = connection_info.NUTANIX_EMAIL, user_name=connection_info.NUTANIX_USER_NAME, pwd="dummy")
        container_registry_model = kps_api.ContainerRegistryV2(
                description = 'My container registry',
                id = 'contregid{}{}'.format(model_id_1, model_id_2),
                name = 'contregname{}{}'.format(model_id_1, model_id_2),
                server = 'https://sherlockdev.dkr.ecr.region.amazonaws.com',
                type='AWS',
                cloud_profile_info=cloud_profile_info,
                container_registry_info=container_registry_info)
        return container_registry_model, cloud_profile_model

