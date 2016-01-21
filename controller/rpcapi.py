from oslo_config import cfg
import oslo_messaging as messaging
import logging

from openstack import config

CONF = cfg.CONF
LOG = logging.getLogger(__name__)

class ControllerAPI(object):
    """
    client side for controller rpc api
    """
    def __init__(self):
        self.transport = messaging.get_transport(cfg.CONF)
        self.target = messaging.Target(topic=CONF.controller_topic)
        self._client = messaging.RPCClient(self.transport, self.target)

    def migrate(self, vm_id, dest_host):
        try:
            self._client.cast(ctxt={}, method='migrate', vm=vm_id, dest=dest_host)
        except:
            LOG.error('failed to deliver migrate marshling msg!!')
