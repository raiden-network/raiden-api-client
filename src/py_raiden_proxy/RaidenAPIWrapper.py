from json import JSONDecodeError

import requests
from typing import List
from attrdict import AttrDict
from py_raiden_proxy.exceptions.exceptions import RaidenAPIException, RaidenAPIConflictException, \
    InvalidAPIResponse
from requests import RequestException


class RaidenAPIWrapper:
    def __init__(self, ip, port, version="v1"):
        self.api = f"http://{ip}:{port}/api/{version}/"
        self.headers = {'Content-Type': 'application/json', }

    def get_channels(self) -> List[AttrDict]:
        res = requests.get(f"{self.api}channels")
        return self.handle_response(res)

    def get_address(self) -> AttrDict:
        res = requests.get(f"{self.api}address")
        return self.handle_response(res)

    def get_payments(self, target=None, token=None) -> List[AttrDict]:
        # Query all payments
        if None not in (target, token):
            res = requests.get(f"{self.api}payments/{token}/{target}")
        # Query payments with specific partner and token
        else:
            res = requests.get(f"{self.api}payments")
        return self.handle_response(res)

    def open_channel(self, target, deposit, token, settle_timeout=500) -> AttrDict:
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
        return self.handle_response(res)

    def fund_channel(self, target, deposit, token) -> AttrDict:
        json_data = {"total_deposit": deposit}

        res = requests.patch(
            f"{self.api}channels/{token}/{target}",
            headers=self.headers,
            json=json_data,
            timeout=600,
        )

        return self.handle_response(res)

    def transfer(self, target, amount, token, identifier=None, ) -> AttrDict:
        json_data = {'amount': amount, }

        if identifier:
            json_data['identifier'] = identifier

        res = requests.post(
            f"{self.api}payments/{token}/{target}",
            headers=self.headers,
            json=json_data
        )

        return self.handle_response(res)

    def handle_response(self, response):

        try:
            response_json = response.json()
        except JSONDecodeError:
            raise InvalidAPIResponse()

        # For some get endpoints the result will be a list of jsons
        if isinstance(response_json, list):
            decoded_response = []
            for item in response_json:
                decoded_response.append(AttrDict(item))
        # If it's a single dict
        else:
            decoded_response = AttrDict(response_json)

        # Successful request
        if 199 < response.status_code < 300:
            return decoded_response

        # Raise Exception if request wasn't successful
        try:
            response.raise_for_status()
        except RequestException as ex:
            if response.status_code == 409:
                raise RaidenAPIConflictException(decoded_response["errors"],
                                                 response.status_code) from ex
            else:
                raise RaidenAPIException(decoded_response["errors"], response.status_code) from ex
