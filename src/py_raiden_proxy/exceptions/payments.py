from typing import Any

from py_raiden_proxy.exceptions.base import RaidenAPIConflictException


class NoRoute(RaidenAPIConflictException):
    def __int__(self, error_messages: Any):
        super().__init__(error_messages)
