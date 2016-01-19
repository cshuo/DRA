"""
openstack entity, including instances and compute hosts
"""
class Host(object):
    def __init__(self, hostName):
        self.hostName = hostName

    def getHostName(self):
        return self.hostName

class Instance:
    def __init__(self, id):
        self.id = id

    def getId(self):
        return self.id
