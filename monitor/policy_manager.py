from oslo_config import cfg
import oslo_messaging as messaging
import time

from controller.rpcapi import ControllerAPI
from selector.rpcapi import SelectorAPI
from openstack.nova import Nova

def trigger_sche(host):
    """ trigger controller to conduct migrate operation """
    # busy host choosed to re schedule
    select_api = SelectorAPI()
    controller_api = ControllerAPI()
    # selected vm to migrate to dest
    vm, dest = select_api.select(host)
    if vm:
    	controller_api.migrate(vm, dest)
	time.sleep(120)

def monitor():
    """ monitor host status to decide whether resource reallocation """
    nova = Nova()
    while 1:
    	hosts = nova.getComputeHosts()
        for h in hosts:
	    sttcs = nova.hypervisorDetail(h)
	    if float(sttcs['mem_used']) / sttcs['mem_total'] > 0.3:
		print "host busy", ",migrate vm from ", h
	        trigger_sche(h)
	time.sleep(10)

if __name__ == '__main__':
    print "monitoring service start..."
    try:
        monitor()
    except KeyboardInterrupt:
	print "\nexiting..."
