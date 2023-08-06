from data_models import BaseDataModel
import kps_api

class CloudProfileModelKit(BaseDataModel):

    def __init__(self):
        BaseDataModel.__init__(self)

    # model_id_1 and model_id_2 are short user-defined identifiers which will ensure unique id and name is given to the entity
    def get_data_models(self, model_id_1, model_id_2):
        profile_model = kps_api.CloudProfile(id='cfid{}{}'.format(model_id_1, model_id_2),
                name='CF{}{}'.format(model_id_1, model_id_2),
                type='AWS',
                description='My cloud profile',
                aws_credential=kps_api.AWSCredential(access_key='MyAwsAccessKey', secret='MyAwsSecretKey'))
        return profile_model

