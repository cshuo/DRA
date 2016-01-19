from oslo_config import cfg
import oslo_messaging as messaging
import logging
import random

from openstack.nova import Nova
from openstack.metrics import Metric


'''
CONF = cfg.CONF
rpcapi_opt = [
    cfg.StrOpt('selector_topic',
               default='selector_topic',
               help='the topic that select service listen on')
]
CONF.register_opts(rpcapi_opt)
'''

LOG = logging.getLogger(__name__)

class SelectorManager(object):
    """ endpoints methods provided by controller service """
    def select(self, ctxt, host):
        """ select a vm in specific host and a dest host """
        nova = Nova()
        mtc = Metric()

        base_q = '''[{"field": "timestamp",
            "op": "ge",
            "value": "2016-01-17T12:00:00"},
            {"field": "timestamp",
            "op": "lt",
            "value": "2016-01-17T13:00:00"},
            {"field": "resource_id",
            "op": "eq",
            "value": "instance_id"}]'''

        instances = nova.getInstancesOnHost(host)
        cpu_avg = dict()

        for itnce in instances:
            query = base_q.replace('instance_id', itnce)
            cpu_avg[itnce] = mtc.getMeterStatistics("cpu_util", query)['avg']

        vm = max(cpu_avg, key=cpu_avg.get)

        # select a host randomly
        hosts = nova.getComputeHosts()
        hosts.remove(host)
        dest = random.choice(hosts)
	print "select {0} on host {1} to migrate to {2}".format(vm, host, dest)

        return vm, dest

def start_selector():
    transport = messaging.get_transport(cfg.CONF)
    target = messaging.Target(topic='selector', server='cs')
    endpoints = [
        SelectorManager(),
    ]
    server = messaging.get_rpc_server(transport, target, endpoints,
                                      executor='blocking')
    server.start()
    server.wait()

if __name__ == '__main__':
    start_selector()
