from enum import IntEnum


class UserStatus(IntEnum):
    FORBID = 0
    ACTIVE = 1
    MODIFY_PWD = 2


class RequestMethod(IntEnum):
    GET = 0
    POST = 1
    PUT = 2
    PATCH = 3
    DELETE = 4
