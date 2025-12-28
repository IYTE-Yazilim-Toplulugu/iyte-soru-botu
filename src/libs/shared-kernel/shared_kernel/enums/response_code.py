from enum import Enum


class ResponseCode(Enum):
    SUCCESS = 0
    INTERNAL_ERROR = 1
    BAD_REQUEST = 2
    UNAUTHENTICATED = 3
    UNAUTHORIZED = 4
    NOT_FOUND = 5
    EXISTS = 6
    FORBIDDEN = 7
    SERVICE_SPECIFIED = 8
