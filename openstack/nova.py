import urllib2
import json
from openstack.base_service import OpenstackService
from utils.http_util import OpenstackRestful
from utils.ssh_util import SshTool
from openstack import conf


class Nova(OpenstackService):

    def __init__(self):
        OpenstackService.__init__(self)
        self.restful = OpenstackRestful(self.tokenId)


    def liveMigrate(self, instance_id, host):
        url = "{base}/v2/{tenant}/servers/{instance}/action".format(base=conf.NOVA_URL,
		tenant=self.tenantId, instance=instance_id)
        values = {"os-migrateLive":{"block_migration": "true", "host":host, 'disk_over_commit':"false"}}
        self.restful.post_req(url, values)

    def evacuteServer(self, src, dest):
        url = "{base}/v2/{tenant}/servers/{instance}/action".format(base=conf.NOVA_URL,
		tenant=self.tenantId, instance=instance_id)
	

    def stopInstance(self, instance_id):
        url = "{base}/v2/{tenant}/servers/{instance}/action".format(base=conf.NOVA_URL,
		tenant=self.tenantId, instance=instance_id)
	values = {"os-stop": 'null'}
	self.restful.post_req(url, values)
     
    def startInstance(self, instance_id):
        url = "{base}/v2/{tenant}/servers/{instance}/action".format(base=conf.NOVA_URL,
		tenant=self.tenantId, instance=instance_id)
	values = {"os-start": 'null'}
	self.restful.post_req(url, values)

    def getInstances(self):
	""" get all instances belong to a tenant """
        url = "%s/v2/%s/servers" % (conf.NOVA_URL, self.tenantId)

        result = self.restful.getResult(url)
        servers = result['servers']

        instances = []
        for i in range(len(servers)):
            instances.append(servers[i]['id'])

        return instances

    def getInstancesOnHost(self, host):
        url = "%s/v2/%s/servers?host=%s" % (conf.NOVA_URL, self.tenantId, host)

        result = self.restful.get_req(url)
        servers = result['servers']

        instances = []
        for i in range(len(servers)):
            instances.append(servers[i]['id'])

        return instances


    def getComputeHosts(self):
        url = "%s/v2/%s/os-hosts" % (conf.NOVA_URL, self.tenantId)

        result = self.restful.getResult(url)

        hostsList = result['hosts']
        hosts = []
        for host in hostsList:
            if host['service'] == 'compute':
                hosts.append(host['host_name'])

        return hosts


    @staticmethod
    def liveMigrateAll(src_host, dest_host):
        ssh_controller = SshTool(conf.CONTROLLER_HOST, 22,
                                  conf.HOST_ROOT_USERNAME,
                                  conf.HOST_ROOT_PASSWORD)

        cmd_migrate = "nova host-evacuate-live --target-host {dest} \
                      --block-migrate {src}".format(src=src_host, dest=dest_host)
        ssh_controller.remote_cmd(cmd_migrate)
        ssh_controller.close()


if __name__ == "__main__":
    nova = Nova()
    #instances = nova.getInstances()
    #print nova.getInstancesOnHost('compute1')[0]
    #nova.liveMigrate('8387a836-1a28-4061-8c25-e5a57ff170e8', 'compute1')
    nova.startInstance('8387a836-1a28-4061-8c25-e5a57ff170e8')

