from fastapi import Request
from fastapi.security.utils import get_authorization_scheme_param

from apex_fastapi.auth.errors import no_auth_error
from apex_fastapi.constants import (
    ACCESS_TOKEN_HEADER_KEY,
    TOKEN_HEADER_VALUE_PREFIX,
)


def create_token_header(
    token,
    key=ACCESS_TOKEN_HEADER_KEY,
    prefix=TOKEN_HEADER_VALUE_PREFIX,
):
    return {key: f"{prefix} {token}"}


def get_token_from_headers(
    request: Request,
    key: str = ACCESS_TOKEN_HEADER_KEY,
    prefix: str = TOKEN_HEADER_VALUE_PREFIX,
    auto_error: bool = True,
) -> str | None:
    authorization: str = request.headers.get(key)
    scheme, token = get_authorization_scheme_param(authorization)
    if not authorization or scheme.lower() != prefix.lower():
        if auto_error:
            raise no_auth_error
        else:
            return None
    return token
