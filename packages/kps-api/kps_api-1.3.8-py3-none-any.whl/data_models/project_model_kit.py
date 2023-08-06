from data_models import BaseDataModel, CloudProfileModelKit, UserModelKit, ServiceDomainModelKit
import kps_api
from common import connection_info

class ProjectModelKit(BaseDataModel):
    
    def __init__(self):
        BaseDataModel.__init__(self)
        self.profile_model_kit = CloudProfileModelKit()
        self.user_model_kit = UserModelKit()
        self.sv_model_kit = ServiceDomainModelKit()

    # model_id_1 and model_id_2 are short user-defined identifiers which will ensure unique id and name is given to the entity
    def get_data_models(self, model_id_1, model_id_2):
        profile_model = self.profile_model_kit.get_data_models(model_id_1, model_id_2)
        user_model = self.user_model_kit.get_data_models(model_id_1, model_id_2)
        sv_prereq_models = self.sv_model_kit.get_data_models(model_id_1, model_id_2)

        project_model = kps_api.Project(
                cloud_credential_ids = [ profile_model.id ],
                description = 'My project for test',
                docker_profile_ids = [],
                edge_ids = [ sv_prereq_models['ServiceDomain'].id ],
                edge_selector_type = 'Explicit',
                edge_selectors = None,
                id = 'projid{}{}'.format(model_id_1, model_id_2),
                name = 'projname{}{}'.format(model_id_1, model_id_2),
                privileged = True,
                users = [])
        project_user_info = kps_api.ProjectUserInfo(user_id=user_model.id, 
            role_id=self.user_model_kit.user_project_role)
        current_user_info = kps_api.ProjectUserInfo(user_id=connection_info.USER_ID, 
            role_id=self.user_model_kit.user_project_role)
        project_model.users = [ project_user_info, current_user_info ]
        return { 'Project': project_model, 
                'CloudProfile': profile_model,
                'User': user_model,
                'ServiceDomain': sv_prereq_models['ServiceDomain'],
                'Category': sv_prereq_models['Category'] }

