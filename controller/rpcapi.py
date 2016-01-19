from oslo_config import cfg
import oslo_messaging as messaging
import logging

'''
CONF = cfg.CONF
rpcapi_opt = [
    cfg.StrOpt('controller_topic',
               default='controller_topic',
               help='the topic that controller service listen on')
]
CONF.register_opts(rpcapi_opt)
'''

LOG = logging.getLogger(__name__)

class ControllerAPI(object):
    def __init__(self):
        self.transport = messaging.get_transport(cfg.CONF)
        self.target = messaging.Target(topic='controller')
        self._client = messaging.RPCClient(self.transport, self.target)

    def migrate(self, vm_id, dest_host):
        try:
            self._client.cast(ctxt={}, method='migrate', vm=vm_id, dest=dest_host)
        except:
            LOG.error('failed to deliver migrate marshling msg!!')
