import requests


class Resource:
    def __init__(self):
        pass

    def get(self, source_id, params):
        raise Exception("Resource get not implemented")
    
    def index(self, params):
        raise Exception("Resource index not implemented")


def execute_request(reqData):
    httpReq = requests.request(**reqData)
    try:
        httpReq.raise_for_status()
        #log.info(f"{reqData['method']} {reqData['url']}")
        response = httpReq.json()
        return response
    except Exception as e:
        print(e)
        print(httpReq.text)