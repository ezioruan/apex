import enum


class HTTPError(enum.IntEnum):
    BAD_REQUEST = 400
    UNAUTHORIZED = 401
    FORBIDDEN = 403
    NOT_FOUND = 404
    INTERNAL_SERVER_ERROR = 500


class HTTPSuccess(enum.IntEnum):
    NO_CONTENT = 204
    CREATED = 201
    SUCCESS = 200
