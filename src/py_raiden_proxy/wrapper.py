from json import JSONDecodeError
import re

import requests
from enum import Enum
from typing import List
from attrdict import AttrDict
from py_raiden_proxy.exceptions import (
    RaidenAPIException,
    RaidenAPIConflictException,
    InvalidAPIResponse,
)
from requests import RequestException


HEX_ADDRESS_REGEX = r'(0x)[a-fA-F0-9]{40}'
REGEX_404_NO_CHANNEL = re.compile(f"^Channel with partner '{HEX_ADDRESS_REGEX}' for token '{HEX_ADDRESS_REGEX}' could not be found.$")


def attrdict_me(object):
    try:
        result = AttrDict(object)
    except ValueError:
        result = object
    return result


def exception_matches(ex, status_code, error_message_regexes=None):
    if not isinstance(ex, RaidenAPIException):
        return False
    # unfortunately, the attributes are not directly accessible in exceptions, but
    # are simply stored in a list
    ex_error_messages, ex_status_code = ex.args
    if ex_status_code == status_code:
        if error_message_regexes:
            # not CPU critical, don't compile to piped regex
            for error_message in ex_error_messages:
                if any(regex.match(error_message) for regex in error_message_regexes):
                    return True
        else:
            return True
    return False


class RaidenAPIWrapper:
    def __init__(self, ip, port, version="v1"):
        self.api = f"http://{ip}:{port}/api/{version}/"
        self.headers = {'Content-Type': 'application/json', }

    def get_channels(self, token=None, partner=None) -> List[AttrDict]:
        if token and partner:
            res = requests.get(f"{self.api}channels/{token}/{partner}")
        elif token:
            res = requests.get(f"{self.api}channels/{token}")
        else:
            res = requests.get(f"{self.api}channels")
        try:
            handled_response = self._handle_response(res)
        except RaidenAPIException as ex:
            if exception_matches(ex, 404, [REGEX_404_NO_CHANNEL]):
                handled_response = []
            else:
                raise ex
        if partner and not token:
            return [channel for channel in handled_response if channel.partner_address == partner]
        else:
            return handled_response

    def get_token_network(self, token=None):
        if token:
            res = requests.get(f"{self.api}tokens/{token}")
        else:
            res = requests.get(f"{self.api}tokens")
        return self._handle_response(res)

    def get_raiden_version(self):
        res = requests.get(f"{self.api}version")
        return self._handle_response(res)

    def get_address(self) -> AttrDict:
        res = requests.get(f"{self.api}address")
        return self._handle_response(res)

    def get_payments(self, partner=None, token=None) -> List[AttrDict]:
        # Query all payments
        if None not in (partner, token):
            res = requests.get(f"{self.api}payments/{token}/{partner}")
        # Query payments with specific partner and token
        else:
            res = requests.get(f"{self.api}payments")
        return self._handle_response(res)

    def get_pending_transfer(self, token=None, partner=None):
        if token:
            res = requests.get(f"{self.api}pending_transfers/{token}")
        elif token and partner:
            res = requests.get(f"{self.api}pending_transfers/{token}/{partner}")
        else:
            res = requests.get(f"{self.api}pending_transfers")
        return self._handle_response(res)

    def get_connections(self):
        res = requests.get(f"{self.api}connections")
        return self._handle_response(res)

    def get_node_status(self):
        res = requests.get(f"{self.api}status")
        return self._handle_response(res)

    def leave_token_network(self, token):
        res = requests.delete(f"{self.api}connections/{token}")
        return self._handle_response(res)

    def register_token(self, token):
        res = requests.put(f"{self.api}tokens/{token}")
        return self._handle_response(res)

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
        return self._handle_response(res)

    def fund_channel(self, partner, deposit, token) -> AttrDict:
        json_data = {"total_deposit": deposit,}

        res = requests.patch(
            f"{self.api}channels/{token}/{partner}",
            headers=self.headers,
            json=json_data,
            timeout=600,
        )

        return self._handle_response(res)

    def transfer(self, partner, amount, token, identifier=None, ) -> AttrDict:
        json_data = {'amount': amount, }

        if identifier:
            json_data['identifier'] = identifier

        res = requests.post(
            f"{self.api}payments/{token}/{partner}",
            headers=self.headers,
            json=json_data,
        )

        return self._handle_response(res)

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
        return self._handle_response(res)


    def _handle_response(self, response):
        try:
            response_json = response.json()
        except JSONDecodeError:
            raise InvalidAPIResponse()

        # For some get endpoints the result will be a list of jsons
        if isinstance(response_json, list):
            decoded_response = []
            for item in response_json:
                decoded_response.append(attrdict_me(item))
        # If it's a single dict
        else:
            decoded_response = attrdict_me(response_json)

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
