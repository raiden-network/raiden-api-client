import pytest
from py_raiden_proxy.exceptions import RaidenAPIException, RaidenAPIConflictException, \
    InvalidAPIResponse
from py_raiden_proxy.wrapper import RaidenAPIWrapper
from requests.models import Response

URL = "localhost"
PORT = "5001"
TOKEN = "0x3ed0DaEDC3217615bde34FEDd023bC81ae49251B"
TARGET = "0x1F916ab5cf1B30B22f24Ebf435f53Ee665344Acf"  # Raiden Hub
OFFLINE_TARGET = "0xA547D39D21ab29eC7b79DAe974b24e72f9BD352E"  # Raiden Hub
WRONG_FORMATED_TARGET = "0x000000000000000000000000000000000000000"

rdn = RaidenAPIWrapper(ip=URL, port=PORT)


def default_response():
    res = Response()
    res._content = b'{"value": "Some value"}'
    res.status_code = 200
    return res


class TestHandleResponse:

    def test_error_status_codes(self):
        res = default_response()
        res._content = b'{"errors": "Some Error"}'
        for status_code in [402, 403, 404, 409, 500, 501, 503]:
            res.status_code = status_code
            if status_code == 409:
                with pytest.raises(RaidenAPIConflictException):
                    rdn._handle_response(res)

            else:
                with pytest.raises(RaidenAPIException):
                    rdn._handle_response(res)

    def test_expected_status_codes(self):
        res = default_response()
        for status_code in [200, 201]:
            res.status_code = status_code
            assert rdn._handle_response(res)["value"] == "Some value"

    def test_attrdict_response(self):
        res = default_response()
        assert rdn._handle_response(res).value == "Some value"

    def test_list_of_attrdict_response(self):
        res = default_response()
        res._content = b'[{"value1": "Some value"}, {"value2": "Another value"}]'
        assert rdn._handle_response(res)[0].value1 == "Some value"
        assert rdn._handle_response(res)[1].value2 == "Another value"

    def test_list_of_string_response(self):
        res = default_response()
        res._content = b'["string1", "string2"]'
        assert rdn._handle_response(res)[0] == "string1"
        assert rdn._handle_response(res)[1] == "string2"

    def test_invalid_api_response(self):
        res = default_response()
        res._content = b'not valid json'
        with pytest.raises(InvalidAPIResponse):
            rdn._handle_response(res)


class TestRequests:
    def __int__(self):
        self.api = "http://{URL}:{PORT}/api/v1/"



