from apex_fastapi.schema_plus.response import Response, T

from .errors import HTTPError, HTTPSuccess


class UnauthorizedResponse(Response):
    code: int = HTTPError.UNAUTHORIZED
    message: str = HTTPError.UNAUTHORIZED.name
    data: T = {}


class BadRequestResponse(Response):
    code: int = HTTPError.BAD_REQUEST
    message: str = HTTPError.BAD_REQUEST.name
    data: T = {}


class ForbiddenResponse(Response):
    code: int = HTTPError.FORBIDDEN
    message: str = HTTPError.FORBIDDEN.name
    data: T = {}


class NotFoundResponse(Response):
    code: int = HTTPError.NOT_FOUND
    message: str = HTTPError.NOT_FOUND.name
    data: T = {}


class InternalServerErrorResponse(Response):
    code: int = HTTPError.INTERNAL_SERVER_ERROR
    message: str = HTTPError.INTERNAL_SERVER_ERROR.name
    data: T = {}


class NotContentResponse(Response):
    code: int = HTTPSuccess.NO_CONTENT
    message: str = HTTPSuccess.NO_CONTENT.name
    data: T = {}


class CreatedResponse(Response):
    code: int = HTTPSuccess.CREATED
    message: str = HTTPSuccess.CREATED.name
    data: T = {}


responses = {
    201: {"model": CreatedResponse},
    400: {"model": UnauthorizedResponse},
    401: {"model": BadRequestResponse},
    403: {"model": ForbiddenResponse},
    404: {"model": NotFoundResponse},
    500: {"model": InternalServerErrorResponse},
}
