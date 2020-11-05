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

    def get_channels(self, token=None, partner=None) -> List[AttrDict]:
        if token:
            res = requests.get(f"{self.api}channels/{token}")
        elif token and partner:
            res = requests.get(f"{self.api}channels/{token}/{partner}")
        else:
            res = requests.get(f"{self.api}channels")
        return self.handle_response(res)

    def get_token_network(self, token=None):
        if token:
            res = requests.get(f"{self.api}tokens/{token}")
        else:
            res = requests.get(f"{self.api}tokens")
        return self.handle_response(res)

    def get_raiden_version(self):
        res = requests.get(f"{self.api}version")
        return self.handle_response(res)

    def get_address(self) -> AttrDict:
        res = requests.get(f"{self.api}address")
        return self.handle_response(res)

    def get_payments(self, partner=None, token=None) -> List[AttrDict]:
        # Query all payments
        if None not in (partner, token):
            res = requests.get(f"{self.api}payments/{token}/{partner}")
        # Query payments with specific partner and token
        else:
            res = requests.get(f"{self.api}payments")
        return self.handle_response(res)

    def get_pending_transfer(self, token=None, partner=None):
        if token:
            res = requests.get(f"{self.api}pending_transfers/{token}")
        elif token and partner:
            res = requests.get(f"{self.api}pending_transfers/{token}/{partner}")
        else:
            res = requests.get(f"{self.api}pending_transfers")
        return self.handle_response(res)

    def get_connections(self):
        res = requests.get(f"{self.api}connections")
        return self.handle_response(res)

    def get_node_status(self):
        res = requests.get(f"{self.api}status")
        return self.handle_response(res)

    def leave_token_network(self, token):
        res = requests.delete(f"{self.api}connections/{token}")
        return self.handle_response(res)

    def register_token(self, token):
        res = requests.put(f"{self.api}tokens/{token}")
        return self.handle_response(res)

    def open_channel(self, partner, deposit, token, settle_timeout=500) -> AttrDict:
        json_data = {
            "partner_address": partner,
            "settle_timeout": settle_timeout,
            "token_address": token,
            "total_deposit": deposit,
        }

        res = requests.put(
            f"{self.api}channels",
            headers=self.headers,
            json=json_data,
            timeout=600
        )
        return self.handle_response(res)

    def fund_channel(self, partner, deposit, token) -> AttrDict:
        json_data = {"total_deposit": deposit,}

        res = requests.patch(
            f"{self.api}channels/{token}/{partner}",
            headers=self.headers,
            json=json_data,
            timeout=600,
        )

        return self.handle_response(res)

    def transfer(self, partner, amount, token, identifier=None, ) -> AttrDict:
        json_data = {'amount': amount, }

        if identifier:
            json_data['identifier'] = identifier

        res = requests.post(
            f"{self.api}payments/{token}/{partner}",
            headers=self.headers,
            json=json_data,
        )

        return self.handle_response(res)

    def mint_tokens(self, token, receiver, amount):
        test_api = self.api + "_testing/"
        json_data = {
            "to": receiver,
            "value": amount,
        }
        res = requests.post(
            f"{test_api}tokens/{token}/mint",
            headers=self.headers,
            json=json_data,
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
                decoded_response.append(self.attrdict_me(item))
        # If it's a single dict
        else:
            decoded_response = self.attrdict_me(response_json)

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

    def attrdict_me(self, object):
        try:
            result = AttrDict(object)
        except ValueError:
            result = object
        return result
