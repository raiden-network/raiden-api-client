from typing import Any


class RaidenAPIWrapperException(Exception):
    pass


class RaidenAPIException(RaidenAPIWrapperException):
    def __int__(self, error_messages: Any):
        self.error_messages = error_messages


class InvalidAPIResponse(RaidenAPIWrapperException):
    """The response was not valid json"""
