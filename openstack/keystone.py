import requests

class Authentication:
    def __init__(self):
        self.tokenId=None
        self.tenantId=None

    def tokenGet(self, host, tenant, user, passwd):
	url = "{0}/v2.0/tokens".format(host)
	headers = {"Content-type":"application/json"}
	data = {'auth': {'tenantName': tenant,
			 'passwordCredentials': {'username': user, 'password':passwd}}}
	info = requests.post(url, json=data, headers=headers).json()

        self.tokenId = info["access"]["token"]["id"]
        self.tenantId = info["access"]["token"]["tenant"]["id"]

    def getTokenId(self):
        return self.tokenId

    def getTenantId(self):
        return self.tenantId

if __name__=="__main__":
    auth = Authentication()
    auth.tokenGet("http://20.0.1.11:35357", "admin", "admin", "cshuo")
    print auth.getTenantId()
    print auth.getTokenId()
