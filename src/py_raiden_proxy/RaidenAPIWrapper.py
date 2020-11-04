from json import JSONDecodeError

import requests
from attrdict import AttrDict
from py_raiden_proxy.exceptions.exceptions import RaidenAPIException, RaidenAPIConflictException
from requests import RequestException


class RaidenAPIWrapper:
    def __init__(self, ip, port, version="v1"):
        self.api = f"http://{ip}:{port}/api/{version}/"
        self.headers = {'Content-Type': 'application/json', }

    def open_channel(self, target, deposit, token, settle_timeout=500):
        json_data = {
            "partner_address": target,
            "settle_timeout": settle_timeout,
            "token_address": token,
            "total_deposit": deposit
        }

        res = requests.put(
            f"{self.api}channels",
            headers=self.headers,
            json=json_data,
            timeout=600
        )
        return self.check_http_code(res)

    def fund_channel(self, target, deposit, token):
        json_data = {"total_deposit": deposit}

        res = requests.patch(
            f"{self.api}channels/{token}/{target}",
            headers=self.headers,
            json=json_data,
            timeout=600,
        )

        return self.check_http_code(res)

    def transfer(self, target, amount, token, identifier=None, ):
        json_data = {'amount': amount, }

        if identifier:
            json_data['identifier'] = identifier

        res = requests.post(
            f"{self.api}payments/{token}/{target}",
            headers=self.headers,
            json=json_data
        )

        return self.check_http_code(res)

    def check_http_code(self, response):
        try:
            decoded_response = AttrDict(response.json())
        except (KeyError, JSONDecodeError):
            raise RaidenAPIException()

        # Successful request
        if 199 < response.status_code < 300:
            return decoded_response

        # Raise Exception if request wasn't successful
        try:
            response.raise_for_status()
        except RequestException as ex:
            if response.status_code == 409:
                raise RaidenAPIConflictException(decoded_response["errors"], response.status_code) from ex
            else:
                raise RaidenAPIException(decoded_response["errors"], response.status_code) from ex
