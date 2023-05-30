from enum import IntEnum


class AuthError(IntEnum):
    USER_NOT_FOUND = 10001
    PASSWORD_NOT_EQUAL = 10002
