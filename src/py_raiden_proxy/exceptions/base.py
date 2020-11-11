from typing import Any


class RaidenAPIWrapperException(Exception):
    pass


class RaidenAPIException(RaidenAPIWrapperException):
    def __int__(self, error_messages: Any, status_code: int):
        self.error_messages = error_messages
        self.status_code = status_code


class RaidenAPIConflictException(RaidenAPIException):
    """Response statuscode was 409"""
    def __int__(self, error_messages: Any):
        super().__init__(error_messages, 409)


class InvalidAPIResponse(RaidenAPIWrapperException):
    """The response was not valid json"""

