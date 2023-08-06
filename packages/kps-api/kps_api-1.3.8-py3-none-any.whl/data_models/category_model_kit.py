from data_models import BaseDataModel
import kps_api

class CategoryModelKit(BaseDataModel):

    def __init__(self):
        BaseDataModel.__init__(self)

    # model_id_1 and model_id_2 are short user-defined identifiers which will ensure unique id and name is given to the entity
    def get_data_models(self, model_id_1, model_id_2):
        category_model = kps_api.Category(
                id = 'catid{}{}'.format(model_id_1, model_id_2),
                name = 'catname{}{}'.format(model_id_1, model_id_2),
                purpose = 'Category for testing {}: {}'.format(model_id_1, model_id_2),
                values = [ 'value1', 'value2' ])
        return category_model
