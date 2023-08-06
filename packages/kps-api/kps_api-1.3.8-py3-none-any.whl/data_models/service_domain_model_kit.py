import kps_api
from data_models import BaseDataModel, CategoryModelKit

class ServiceDomainModelKit(BaseDataModel):

    def __init__(self):
        BaseDataModel.__init__(self)
        self.ip = 101
        self.category_model_kit = CategoryModelKit()

    # model_id_1 and model_id_2 are short user-defined identifiers which will ensure unique id and name is given to the entity
    def get_data_models(self, model_id_1, model_id_2):
        category_model_kit_model = self.category_model_kit.get_data_models(model_id_1, model_id_2)
        sv_model = kps_api.ServiceDomain(
                id = 'svid{}{}'.format(model_id_1, model_id_2), 
                name = 'svname{}{}'.format(model_id_1, model_id_2),
                description = 'Test service domain for {} {}'.format(model_id_1, model_id_2),
                env = "'{\"MYVAR1\":\"MYVALUE1\",\"MYVAR2\",\"MYVALUE2\"}'",
                labels = [],
                virtual_ip = '10.1.10.{}'.format(self.ip),
                profile = kps_api.ServiceDomainProfile(enable_ssh=False, privileged=True, ingress_type='Traefik')
                )
        self.ip = self.ip + 1
        return { 'ServiceDomain': sv_model, 'Category': category_model_kit_model }

    
