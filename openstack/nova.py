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

        result = self.restful.getResult(url)
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
    def liveMigration(instanceId, hostName):
        ssh_controller = SshTool(conf.CONTROLLER_HOST, 22,
                                  conf.HOST_ROOT_USERNAME,
                                  conf.HOST_ROOT_PASSWORD)

        cmd_migrate = "nova %s live-migration --block-migrate %s %s" \
		      % (conf.PARAMS, instanceId, hostName)
        ssh_controller.remote_cmd(cmd_migrate)
        ssh_controller.close()

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
    #for instance in instances:
    #    print instance.getId()

    #nova.liveMigration('8387a836-1a28-4061-8c25-e5a57ff170e8', "compute2")


    ##host = Host("compute1", conf.COMPUTE1_HOST)
    #
    ##Nova.liveMigration(instances[0], host)
    #hosts = nova.getHosts()
    #for host in hosts:
    #    print host.getHostName()
    print nova.getInstancesOnHost('compute2')[0]
