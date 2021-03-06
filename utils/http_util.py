import urllib2
import urllib
import requests
import json

class OpenstackRestful:

    def __init__(self, tokenId):
        self.tokenId = tokenId

    def getResult(self, url, postData = None):
	if postData:
	    print "post req"
	    data = urllib.urlencode(postData)
            serverRequest = urllib2.Request(url, data)
        else:
	    print "get req"
            serverRequest = urllib2.Request(url)
        serverRequest.add_header("Content-type", "application/json")
        serverRequest.add_header("X-Auth-Token", self.tokenId)

        response = urllib2.urlopen(serverRequest)
        result = json.loads(response.read())
        return result

    def get_req(self, url):
	headers = {'Content-type': 'application/json', 'X-Auth-Token': self.tokenId}
        result = requests.get(url, headers=headers).json()
	return result

    def post_req(self, url, post_data):
	headers = {'Content-type': 'application/json', 'X-Auth-Token': self.tokenId}
	requests.post(url, json=post_data, headers=headers)
