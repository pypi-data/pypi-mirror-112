import kps_api

class ServiceDomainInfoModelKit():

    def __init__(self):
        self.sv_info_update = kps_api.ServiceDomainInfo(
                id = 'tobereplaced',
                svc_domain_id = 'tobereplaced',
                artifacts = {},
                features = kps_api.Features(
                    download_and_upgrade = True,
                    high_mem_alert = False,
                    multi_node_aware = True,
                    remote_ssh = False,
                    url_upgrade = False
                    )
                )


