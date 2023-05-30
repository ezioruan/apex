from apex_fastapi.auth.models import (
    AuthenticatedUser,
    BaseAccessTokenData,
    TokenResponse,
)
from apex_fastapi.auth.utils import call_service, create_token_header


class AuthEndpoint:
    def __init__(
        self,
        root: str,
        token_url="/api/v1/auth/token",
        user_info_url: str = "/api/v1/auth/token/user",
        verify_token_url: str = "/api/v1/auth/token",
    ):
        self.root = root
        self.token_url = f"{self.root}{token_url}"
        self.user_info_url = f"{self.root}{user_info_url}"
        self.verify_token_url = f"{self.root}{verify_token_url}"

    async def _request(
        self,
        url: str,
        method: str = "get",
        access_token: str | None = None,
        data=None,
        json=None,
    ):
        headers = {}
        if access_token:
            headers.update(**create_token_header(access_token))

        return await call_service(
            service_name="AuthService",
            url=url,
            method=method,
            headers=headers,
            data=data,
            json=json,
        )

    async def token(self, email: str, password: str) -> TokenResponse:
        data = await self._request(
            self.token_url,
            method="post",
            json={"email": email, "password": password},
        )
        return TokenResponse(**data.data)

    async def verify_token(self, token: str) -> BaseAccessTokenData:
        data = await self._request(self.verify_token_url, access_token=token)
        return BaseAccessTokenData(**data.data)

    async def user_info(
        self,
        access_token: str,
        user_id: int,
    ) -> AuthenticatedUser:
        data = await self._request(
            self.user_info_url,
            access_token=access_token,
        )
        return AuthenticatedUser(**data.data)
