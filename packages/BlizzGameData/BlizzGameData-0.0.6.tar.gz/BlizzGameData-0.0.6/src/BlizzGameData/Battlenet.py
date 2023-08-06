import logging
import requests
from dataclasses import dataclass

log = logging.getLogger("debug")


def makeRequest(reqData):
    resource_request = requests.request(**reqData)
    try:
        resource_request.raise_for_status()
        log.info(f"{reqData['method']} {reqData['url']}")
        return resource_request.json()
    except Exception as e:
        print(e)


@dataclass
class Token:
    access_token: str
    token_type: str
    expires_in: int
    sub: str


class Battlenet:
    def __init__(self, region, client_id, secret):
        self.client = client_id
        self.secret = secret
        self.region = region
        self.baseUrl = f"https://{region}.battle.net"

        # paths
        self.token_path = "/oauth/token"
        self.token_validation_path = "/oauth/check_token"

    def application_authentication(self):
        reqData = {
            "url": f"{self.baseUrl}{self.token_path}",
            "files": {
                "grant_type": (None, "client_credentials")
            },
            "auth": (self.client, self.secret),
            "method": "POST"
        }

        token_data = makeRequest(reqData)
        if token_data:
            return Token(**token_data)

    def user_authentication(self):
        raise Exception("Authorization code flow not implemented")

    def validate_token(self, token):
        if token == None:
            return None

        reqData = {
            "url": f"{self.baseUrl}{self.token_validation_path}",
            "data": {
                ":region": self.region,
                "token": token.access_token
            },
            "method": "POST"
        }

        token_validation = makeRequest(reqData)
        if token_validation:
            return token_validation
