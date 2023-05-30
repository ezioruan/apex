from apex_fastapi.auth.endpoint import AuthEndpoint
from apex_fastapi.auth.errors import AccessTokenVerificationException
from apex_fastapi.auth.models import BaseAccessTokenData
from apex_fastapi.fastapi_plus.exceptions import InternalServiceInvocationException

from .authn import Authentication


class UserServiceAuthentication(Authentication):
    def __init__(self, internal_token_secret_key: str, endpoint: AuthEndpoint):
        self.endpoint = endpoint
        super().__init__(
            internal_token_secret_key=internal_token_secret_key,
        )

    async def verify_access_token(self, token: str) -> BaseAccessTokenData:
        try:
            return await self.endpoint.verify_token(token)
        except InternalServiceInvocationException as e:
            raise AccessTokenVerificationException(e.message)
        except Exception as e:
            raise AccessTokenVerificationException(str(e))
