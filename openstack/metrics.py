from openstack.base_service import OpenstackService
from openstack import conf
from utils.http_util import OpenstackRestful


class Metric(OpenstackService):

    def __init__(self):

        OpenstackService.__init__(self)
        self.restful = OpenstackRestful(self.tokenId)


    def getAllMeters(self):
        url = "%s/v2/meters" % conf.CEILOMETER_URL
        result = self.restful.getResult(url)
        return result

    def getAllResources(self):
        url = "%s/v2/resources" % conf.CEILOMETER_URL
        result = self.restful.getResult(url)
        return result

    def getMeter(self, meter_name, queryFilter):
        url = "%s/v2/meters/%s" % (conf.CEILOMETER_URL, meter_name)

        #transfer str to list
        queryFilter = eval(queryFilter)
        print queryFilter

        params = ""
        for queryItem in queryFilter:
            param = ""
            for key in queryItem:
                param += "&q.%s=%s" % (key, queryItem[key])
            params += param

        url = url + "?" + params

        result = self.restful.getResult(url)
        return result[0]


    def getMeterStatistics(self, meter_name, queryFilter, groupby = None, period = None, aggregate = None):
        url = "%s/v2/meters/%s/statistics" % (conf.CEILOMETER_URL, meter_name)

        #transfer str to list
        queryFilter = eval(queryFilter)

        params = ""
        for queryItem in queryFilter:
            param = ""
            for key in queryItem:
                param += "&q.%s=%s" % (key, queryItem[key])
            params += param

        url = url + "?" + params

        result = self.restful.getResult(url)
        return result[0]


if __name__=="__main__":

    ceilometerTest = Metric()

    q = '''[{"field": "timestamp",
    "op": "ge",
    "value": "2016-01-17T12:00:00"},
    {"field": "timestamp",
    "op": "lt",
    "value": "2016-01-17T13:00:00"},
    {"field": "resource_id",
    "op": "eq",
    "value": "8387a836-1a28-4061-8c25-e5a57ff170e8"}]'''

    print ceilometerTest.getMeterStatistics("cpu_util", q)
