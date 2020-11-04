import pytest
from py_raiden_proxy.RaidenAPIWrapper import RaidenAPIWrapper
from py_raiden_proxy.exceptions.exceptions import ConflictError, NotFoundError

URL = "localhost"
PORT = "5001"
TOKEN = "0x3ed0DaEDC3217615bde34FEDd023bC81ae49251B"
TARGET = "0x1F916ab5cf1B30B22f24Ebf435f53Ee665344Acf"  # Raiden Hub
OFFLINE_TARGET = "0xA547D39D21ab29eC7b79DAe974b24e72f9BD352E"  # Raiden Hub
WRONG_FORMATED_TARGET = "0x000000000000000000000000000000000000000"

rdn = RaidenAPIWrapper(ip=URL, port=PORT, default_token=TOKEN)


class TestTransfer:
    def test_not_found_error(self):
        with pytest.raises(NotFoundError):
            rdn.transfer(amount=1, target=WRONG_FORMATED_TARGET)

    def test_conflict_error(self):
        with pytest.raises(ConflictError):
            rdn.transfer(amount=1, target=OFFLINE_TARGET)
