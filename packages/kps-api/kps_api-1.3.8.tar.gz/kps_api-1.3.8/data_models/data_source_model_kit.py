from data_models import BaseDataModel, NodeModelKit
import kps_api

class DataSourceModelKit(BaseDataModel):
    
    def __init__(self):
        BaseDataModel.__init__(self)
        self.node_model_kit = NodeModelKit()

    # model_id_1 and model_id_2 are short user-defined identifiers which will ensure unique id and name is given to the entity
    def get_data_models(self, model_id_1, model_id_2):
        prereq_models = self.node_model_kit.get_data_models(model_id_1, model_id_2)
        data_field = kps_api.DataSourceFieldInfoV2(topic="rtsp://myrtspurl:554",
            name = "datafield1")
        selector = kps_api.DataSourceFieldSelector(id = prereq_models['Category'].id, 
            scope = [ data_field.name ], 
            value = prereq_models['Category'].values[0])
        data_source_model = kps_api.DataSource(
            auth_type = "PASSWORD",
            connection = 'Secure',
            edge_id = prereq_models['Node'].id,
            id = "dsid{}{}".format(model_id_1, model_id_2),
            name = "dsname{}{}".format(model_id_1, model_id_2),
            protocol = "RTSP",
            type = "Sensor",
            fields = [ data_field ],
            selectors = [ selector ],
            ifc_info = None)
        return { 'DataSource': data_source_model,
                'Node': prereq_models['Node'],
                'ServiceDomain': prereq_models['ServiceDomain'],
                'Category': prereq_models['Category'] }

