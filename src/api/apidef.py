import requests
from .websocket import *
from src.utils.errors import (FallbackError, BadRequestError, UnsupportedActionError, BadParamError, BadHandlerError, InternalHandlerError)

class API:
    def http_communication(self, url, data, timeout=10):
        headers = {'Content-Type': 'application/json'}
        response = requests.post(url, headers=headers, data=json.dumps(data), timeout=timeout)
        return response.json()

    def websocket_communication(self, url, data):
        ws = websocket.create_connection(url)
        ws.send(json.dumps(data))
        result = ws.recv()
        return json.loads(result)
    def handle_error(self, error):
        if isinstance(error, FallbackError):
            # Handle FallbackError
            pass
        elif isinstance(error, BadRequestError):
            # Handle BadRequestError
            pass
        elif isinstance(error, UnsupportedActionError):
            # Handle UnsupportedActionError
            pass
        elif isinstance(error, BadParamError):
            # Handle BadParamError
            pass
        elif isinstance(error, BadHandlerError):
            # Handle BadHandlerError
            pass
        elif isinstance(error, InternalHandlerError):
            # Handle InternalHandlerError
            pass
        else:
            # Handle other errors
            pass
