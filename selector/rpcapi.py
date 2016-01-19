from oslo_config import cfg
import oslo_messaging as messaging
import logging

'''
CONF = cfg.CONF
rpcapi_opt = [
    cfg.StrOpt('selector_topic',
               default='selector_topic',
               help='the topic that selector_topic service listen on')
]
CONF.register_opts(rpcapi_opt)
'''

LOG = logging.getLogger(__name__)

class SelectorAPI(object):
    def __init__(self):
        self.transport = messaging.get_transport(cfg.CONF)
        self.target = messaging.Target(topic='selector')
        self._client = messaging.RPCClient(self.transport, self.target)

    def select(self, host):
        """
        select a vm on specific host to migrate to another host
        return: selected vm and dest_host
        """
        try:
            vm, dest = self._client.call(ctxt={}, method='select', host=host)
	    return vm, dest
        except:
            print "exception occur"
