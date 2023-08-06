import json
from pathlib import Path
from ..Battlenet import (
    Battlenet,
    Token
)
 
import logging

log = logging.getLogger("")


class FsTokenCache:
    def __init__(self, region, basePath):
        self.region = region
        self.basePath = Path(basePath).joinpath(region)

        if not self.basePath.exists():
            #self.basePath.mkdir(exist_ok=True, parents=True)
            log.info(f"Created folder {self.basePath}")

    def retrieveToken(self):  # user param to get specific token from user
        token_path = self.basePath.joinpath("token.json")
        if token_path.exists():
            with token_path.open() as token_file:
                token_json = token_file.read()
                if not token_json == "":
                    token_data = json.loads(token_json)
                    log.info(f"Retrieved token {token_path}")
                    return Token(**token_data)

    def saveToken(self, token):
        token_path = self.basePath.joinpath("token.json")
        token_dict = {
            "access_token": token.access_token,
            "token_type": token.token_type,
            "expires_in": token.expires_in,
            "sub": token.sub
        }
        """
        token_path.touch()
        with token_path.open("w+") as token_file:
            token_file.write(json.dumps(token_dict))
            log.info(f"Saved token to {token_path}")
        """

class OauthBattlenet:
    def __init__(self, token_cache, client_id, secret):
        # retrieves token from custom storage of battlenet
        self.region = token_cache.region
        self.client = client_id
        self.secret = secret
        self.BattlenetClient = Battlenet(self.region, client_id, secret)
        self.token_cache = token_cache

    def get_authorized_token(self):
        current_token = self.token_cache.retrieveToken()
        if self.BattlenetClient.validate_token(current_token):
            return current_token

        new_token = self.BattlenetClient.application_authentication()
        self.token_cache.saveToken(new_token)
        return new_token
