import json

import requests

from loguru import logger

from .config import BASE_URL_PRODUCTION, DEFAULT_HTTP_TIME
from .exception import ApiException, ConnectionException

class Request(object):
    def __init__(self, headers=None, timeout=DEFAULT_HTTP_TIME, session=None):
        self.session = None
        self.timeout = timeout
        self.headers = headers
        self.session = session

    def request(self, method, url, params=None, data=None, headers=None):
        headers = self.headers if headers is None else headers
        try:
            caller = self.session or requests
            response = caller.request(
                method=method,
                url=url,
                params=params,
                data=data,
                headers=headers,
                timeout=self.timeout,
            )
        except requests.exceptions.RequestException as e:
            message = ["An error occurred connecting to Optimus."]
            if (
                not url
                or not url.startswith(BASE_URL_PRODUCTION)
            ):
                message.append("The host may be misconfigured or unavailable.")
            # TODO: add contact
            message.append("Contact us for assistance.")
            message.append("")
            message.append(str(e))
            raise ConnectionException("\n".join(message))
        return self._handle_response(response)

    @staticmethod
    def _handle_response(response):
        status_code = response.status_code
        is_success = 200 <= status_code <= 299
        if status_code == 204:
            response_json = None
        else:
            try:
                response_json = json.loads(response.text)
            except ValueError:
                response_json = {"message": response.text}
                status_code = 500 if is_success else status_code
        
        response_json["x-request-id"] = response.headers.get("x-request-id") or ""
      
        if is_success:
            return response_json
                  
        raise ApiException(response_json, status_code)

    def get(self, url, params=None, data=None, headers=None):
        return self.request("get", url=url, params=params, data=data, headers=headers)

    def post(self, url, params=None, data=None, headers=None):
        return self.request("post", url=url, params=params, data=data, headers=headers)

    def put(self, url, params=None, data=None, headers=None):
        return self.request("put", url=url, params=params, data=data, headers=headers)

    def delete(self, url, params=None, data=None, headers=None):
        return self.request("delete", url=url, params=params, data=data, headers=headers)
