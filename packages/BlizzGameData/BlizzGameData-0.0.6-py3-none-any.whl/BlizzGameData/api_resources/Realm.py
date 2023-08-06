from .Resource import (
    Resource,
    execute_request
)


class Realm(Resource):
    def __init__(self, baseUrl, token):
        self.baseUrl = baseUrl
        self.realm_path = "/data/wow/realm"
        self.token = token

    def get(self, realmId, params={}):
        reqParams = {
            "url": f"{self.baseUrl}{self.realm_path}/{realmId}",
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
            "url": f"{self.baseUrl}{self.realm_path}/index",
            "params": params,
            "headers":{
                "Authorization": f"Bearer {self.token}"
            },
            "method": "GET" 
        }

        response = execute_request(reqParams)
        realms = response["realms"]
        for realm in realms:
            yield realm

