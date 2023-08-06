import kps_api
from data_models import BaseDataModel, ProjectModelKit

class ServiceInstanceModelKit(BaseDataModel):

    def __init__(self):
        BaseDataModel.__init__(self)
        self.project_model_kit = ProjectModelKit()

    # api_name and test_name are short user-defined identifiers which will ensure unique id and name is given to the entity
    def get_data_models(self, api_name, test_name, sv_class):
        project_model = self.project_model_kit.get_data_models(api_name, test_name)
        sv_model = kps_api.ServiceInstance(
                id = 'svinstid{}{}'.format(api_name, test_name), 
                name = 'svinstname{}{}'.format(api_name, test_name),
                description = 'Test service instance for {} {}'.format(api_name, test_name),
                svc_class_id = sv_class.id,
                min_svc_domain_version = sv_class.min_svc_domain_version,
                scope = sv_class.scope,
                svc_version = sv_class.svc_version,
                type = sv_class.type
                )
        if sv_class.scope == 'PROJECT':
            sv_model.scope_id = project_model['Project'].id
        elif sv_class.scope == 'SERVICEDOMAIN':
            sv_model.scope_id = project_model['ServiceDomain'].id
        return { 'ServiceInstance': sv_model, 'Project': project_model }

    
