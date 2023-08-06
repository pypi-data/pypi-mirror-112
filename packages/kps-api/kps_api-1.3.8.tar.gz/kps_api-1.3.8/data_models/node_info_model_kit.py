from data_models import BaseDataModel

class NodeInfoModelKit(BaseDataModel):

    def __init__(self):

        BaseDataModel.__init__(self)
        
        self.connected = True
        self.cpu_usage = "1.6"
        self.healthy = True
        self.kube_version = "v1.15.5"
        self.memory_free_KB = "29264264"
        self.node_build_num = "2.1.13.1450"
        self.node_version = "704350000"  
        self.num_cpu = "8"
        self.onboarded = True
        self.os_version = "CentOS Linux release 7.6.1810 (Core)"
        self.storage_free_KB = "35926992"
        self.total_memory_KB = "32779072"
        self.total_storage_KB = "52401156"
