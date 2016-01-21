from oslo_config import cfg
import oslo_messaging as messaging

from openstack import config

CONF = cfg.CONF

class SelectorAPI(object):
    """
    client side for selector rpc api
    """
    def __init__(self):
        self.transport = messaging.get_transport(cfg.CONF)
        self.target = messaging.Target(topic=CONF.selector_topic)
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
	    return None, None

if __name__ == '__main__':
    print CONF.selector_topic
