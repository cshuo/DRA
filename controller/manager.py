from oslo_config import cfg
import oslo_messaging as messaging
import logging

from openstack.nova import Nova
from openstack import config


CONF = cfg.CONF
LOG = logging.getLogger(__name__)

class ControllerManager(object):
    """ endpoints methods provided by controller service """

    def migrate(self, ctxt, vm, dest):
        """ live migrate a vm to dest """
	print "migrate {0} to {1}".format(vm, dest)
        Nova().liveMigrate(vm, dest)

def start_controller():
    transport = messaging.get_transport(cfg.CONF)
    target = messaging.Target(topic=CONF.controller_topic, server='cshuo')
    endpoints = [
        ControllerManager(),
    ]
    server = messaging.get_rpc_server(transport, target, endpoints,
                                      executor='blocking')
    server.start()
    server.wait()

if __name__ == '__main__':
    try:
    	start_controller()
    except KeyboardInterrupt:
	print "\ncontroller service exiting..."
