from data_models import BaseDataModel, ServiceDomainModelKit
import kps_api

class NodeModelKit(BaseDataModel):

    def __init__(self):

        BaseDataModel.__init__(self)
        
        self.ip = 11
        self.node_name_to_update = "mynodetoupdate"
        self.updated_description = "Updated node for test"
        self.node_serial_to_update = "MyUpdatedNodeSerial"
        self.node_version_onboard = "1"
        self.node_ssh_onboard = "sshkey"
        self.is_master = True
        self.is_worker = True

        self.node_role = kps_api.NodeRole(master=True, worker=True)
        self.sv_model_kit = ServiceDomainModelKit()

    # Please pass the name of API being tested and name of the test as parameters
    # These will be used to generate unique id and name for the new entity
    # Pass service_domain_id for creating a node in an existing service domain. 
    # Do not pass it if a new service domain needs to be created for the new node. 
    def get_data_models(self, api_name, test_name, service_domain_id = None):
        testdata_model = kps_api.Node(id = 'nodeid{}{}'.format(api_name, test_name),
            name = 'nodename{}{}'.format(api_name, test_name),
            description = 'Node for {} API {} method test'.format(api_name, test_name),
            serial_number = 'nodeserial{}{}'.format(api_name, test_name),
            ip_address = '10.1.10.{}'.format(self.ip),
            gateway='10.1.10.1',
            subnet='255.255.255.0',
            role=self.node_role,
            svc_domain_id = "tobereplaced")
        self.ip = self.ip + 1
        if service_domain_id is None:
            prereq_models = self.sv_model_kit.get_data_models(api_name, test_name)
            testdata_model.svc_domain_id = prereq_models['ServiceDomain'].id
            return { 'Node': testdata_model, 
                 'ServiceDomain': prereq_models['ServiceDomain'], 
                 'Category': prereq_models['Category'] }
        else:
            testdata_model.svc_domain_id = service_domain_id
            return { 'Node': testdata_model }
