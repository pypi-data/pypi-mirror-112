import kps_api
from common import connection_info

class UserModelKit():

    def __init__(self):
        self.user_running_tests = kps_api.User(name='userrunningtest', email=connection_info.USER_EMAIL, password='dummy', 
            role='INFRA_ADMIN', id=connection_info.USER_ID)
        # TODO: Need a way to query ProjectUserInfo and get the Id for PROJECT_ADMIN role
        self.user_project_role = '06f0af6a815765bb5e731bb24d091e9e'

    # model_id_1 and model_id_2 are short user-defined identifiers which will ensure unique id and name is given to the entity
    def get_data_models(self, model_id_1, model_id_2):
        user_model = kps_api.User(
                id='user{}{}'.format(model_id_1, model_id_2),
                name='user{}{}'.format(model_id_1, model_id_2), 
                email='user{}{}@ntnxsherlock.com'.format(model_id_1, model_id_2), 
                password='Test@123', 
                role='INFRA_ADMIN')
        return user_model
