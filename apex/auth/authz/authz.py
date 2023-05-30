from fastapi import Request

from apex_fastapi.auth.endpoint import AuthEndpoint
from apex_fastapi.auth.errors import must_be_internal_call_error, permission_error
from apex_fastapi.auth.models import (
    AuthenticatedUser,
    BaseAccessTokenData,
    InternalTokenData,
)
from apex_fastapi.constants import FULL_ACCESS_PERMISSION
from apex_fastapi.fastapi_plus.exceptions import InternalServiceInvocationException


class Authorization:
    from apex_fastapi.auth.authn import Authentication

    _user: AuthenticatedUser | None = None

    def __init__(
        self,
        request: Request,
        access_token: str,
        user_id: str,
        authn: Authentication,
        internal_token_data: InternalTokenData | None = None,
        endpoint: AuthEndpoint | None = None,
        ip_whitelist: list[str] | None = None,
    ):
        self.request = request
        self.access_token = access_token
        self.internal_token = None
        self.user_id = user_id
        self._endpoint = endpoint
        self._authn = authn
        self._ip_whitelist = ip_whitelist or []

        self.internal_token_data = internal_token_data
        self.access_token_data = BaseAccessTokenData(
            token=access_token,
            user_id=user_id,
        )
        if internal_token_data:
            self.internal_token = internal_token_data.token
            self.user_id = internal_token_data.user_id
            self._user = internal_token_data.user

    async def _get_authenticated_user(self) -> AuthenticatedUser:
        if self._user:
            user = self._user
        else:
            user = await self._endpoint.user_info(
                self.access_token,
                self.user_id,
            )

        if not user:
            raise InternalServiceInvocationException(
                service_name="AuthService",
                message="No user information found!",
            )

        return user

    def check_permission(
        self,
        user: AuthenticatedUser,
        permission: str | None = None,
    ):
        if permission:
            full_access_permission = (
                f"{'.'.join(permission.split('.')[:2])}."
                f"{FULL_ACCESS_PERMISSION}"
            )
            if (permission not in user.permissions) or (
                full_access_permission not in user.permissions
            ):
                raise permission_error

    def must_be_internal_call(self):
        if not self.internal_token:
            raise must_be_internal_call_error

    async def user(self, permission: str | None = None) -> AuthenticatedUser:
        user = await self._get_authenticated_user()

        def store_user():
            self._user = user
            self.internal_token = self._authn.encode_internal_token(user)

        client_host = self.request.client.host
        if self._ip_whitelist and client_host in self._ip_whitelist:
            store_user()
            return user

        # check permission
        self.check_permission(user=user, permission=permission)

        store_user()
        return user
