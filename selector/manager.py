from oslo_config import cfg
import oslo_messaging as messaging
import random

from openstack.nova import Nova
from openstack.metrics import Metric
from openstack import config

CONF = cfg.CONF

class SelectorManager(object):
    """ endpoints methods provided by controller service """
    def select(self, ctxt, host):
        """ select a vm in specific host and a dest host """
        nova = Nova()
        mtc = Metric()

        base_q = '''[{"field": "timestamp",
            "op": "ge",
            "value": "2016-01-20T04:30:00"},
            {"field": "timestamp",
            "op": "lt",
            "value": "2016-01-20T05:00:00"},
            {"field": "resource_id",
            "op": "eq",
            "value": "instance_id"}]'''

        instances = nova.getInstancesOnHost(host)
        cpu_avg = dict()

        for itnce in instances:
            query = base_q.replace('instance_id', itnce)
            cpu_avg[itnce] = mtc.getMeterStatistics("cpu_util", query)['avg']

	# NOTE change NOTE select most work heavy vm to migrate
	if cpu_avg:
            vm = max(cpu_avg, key=cpu_avg.get)
        else:
            vm = None

        # NOTE change NOTE select a host randomly
        hosts = nova.getComputeHosts()
        hosts.remove(host)
        dest = random.choice(hosts)
	print "select {0} on host {1} to migrate to {2}".format(vm, host, dest)

        return vm, dest

def start_selector():
    transport = messaging.get_transport(cfg.CONF)
    target = messaging.Target(topic=CONF.selector_topic, server='cs')
    endpoints = [
        SelectorManager(),
    ]
    server = messaging.get_rpc_server(transport, target, endpoints,
                                      executor='blocking')
    server.start()
    server.wait()

if __name__ == '__main__':
    try:
    	start_selector()
    except KeyboardInterrupt:
	print "\nselector service exiting..."
    #test_m = SelectorManager()
    #vm, dest= test_m.select({}, 'compute1')

