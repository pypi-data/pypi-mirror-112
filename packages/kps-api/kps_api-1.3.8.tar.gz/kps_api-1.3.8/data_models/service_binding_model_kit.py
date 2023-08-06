import kps_api
from data_models import BaseDataModel, ProjectModelKit
import logging
import sys
logging.basicConfig( stream=sys.stderr, format='%(funcName)s:%(levelname)s:%(message)s', level=logging.DEBUG )

class ServiceBindingModelKit(BaseDataModel):

    def __init__(self):
        BaseDataModel.__init__(self)
        self.project_model_kit = ProjectModelKit()

    # api_name and test_name are short user-defined identifiers which will ensure unique id and name is given to the entity
    def get_data_models(self, api_name, test_name, sv_class):
        project_model = self.project_model_kit.get_data_models(api_name, test_name)
        sv_binding_model = kps_api.ServiceBinding(
                id = 'svbindingid{}{}'.format(api_name, test_name), 
                name = 'svbindingname{}{}'.format(api_name, test_name),
                description = 'Test service binding for {} {}'.format(api_name, test_name),
                svc_class_id = sv_class.id,
                min_svc_domain_version = sv_class.min_svc_domain_version,
                svc_version = sv_class.svc_version,
                type = sv_class.type,
                scope = sv_class.scope
                )
        if sv_class.scope == 'PROJECT':
            sv_binding_model.bind_resource = kps_api.ServiceBindingResource(id = project_model['Project'].id,
                type = kps_api.ServiceBindingResourceType.PROJECT)
        elif sv_class.scope == 'SERVICEDOMAIN':
            sv_binding_model.bind_resource = kps_api.ServiceBindingResource(id = project_model['ServiceDomain'].id,
                type = kps_api.ServiceBindingResourceType.SERVICEDOMAIN)
        return { 'ServiceBinding': sv_binding_model, 'Project': project_model }

    
