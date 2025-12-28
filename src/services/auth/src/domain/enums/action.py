from enum import Enum


class Action(Enum):

    LOGIN_SUCCESS = 1
    LOGIN_FAILED = 2
    PASSWORD_CHANGE = 3
    LOGOUT = 4
    ACCOUNT_LOCKED = 5
