from oslo_config import cfg
import oslo_messaging as messaging

from controller.rpcapi import ControllerAPI
from selector.rpcapi import SelectorAPI

def trigger_sche():
    # busy host choosed to re schedule
    busy_host = 'compute2'

    select_api = SelectorAPI()
    controller_api = ControllerAPI()
    # selected vm to migrate to dest
    vm, dest = select_api.select(busy_host)
    print vm, dest
    controller_api.migrate(vm, dest)

def test_sel():
    transport = messaging.get_transport(cfg.CONF)
    target = messaging.Target(topic='selector')
    client = messaging.RPCClient(transport, target)
    
    vm, dest = client.call(ctxt={}, method='select', host='compute2')
    print vm, dest


if __name__ == '__main__':
    trigger_sche()
