from .Resource import (
    Resource,
    execute_request
)


class ConnectedRealm(Resource):
    def __init__(self, baseUrl, token):
        super().__init__()
        self.baseUrl = baseUrl
        self.token = token
        self.connected_realm_path = "/data/wow/connected-realm"
        
    def get(self, connected_realm_id, params={}):
        reqParams = {
            "url": f"{self.baseUrl}{self.connected_realm_path}/{connected_realm_id}",
            "params": params,
            "headers":{
                "Authorization": f"Bearer {self.token}"
            },
            "method": "GET" 
        }

        response = execute_request(reqParams)
        return response

    def index(self, params={}):
        reqParams = {
            "url": f"{self.baseUrl}{self.connected_realm_path}/index",
            "params": params,
            "headers":{
                "Authorization": f"Bearer {self.token}"
            },
            "method": "GET"
        }

        response = execute_request(reqParams)
        for url in response["connected_realms"]:
            baseUrl = url["href"].split("?")[0]
            index = baseUrl.split("/")[-1]
            url["id"] = index
            yield url

