from abc import ABCMeta, abstractmethod
from calendar import timegm
from datetime import datetime, timedelta

from jose import jwt

from apex_fastapi.auth.models import (
    AuthenticatedUser,
    BaseAccessTokenData,
    InternalTokenData,
    InternalTokenPayload,
)
from apex_fastapi.constants import INTERNAL_TOKEN_EXPIRE_MINUTES


class Authentication(metaclass=ABCMeta):
    def __init__(
        self,
        internal_token_secret_key: str,
        algorithm="HS256",
    ):
        self.internal_token_secret_key = internal_token_secret_key
        self.algorithm = algorithm

    def encode_internal_token(self, user: AuthenticatedUser):
        now = datetime.utcnow()
        expire = now + timedelta(minutes=INTERNAL_TOKEN_EXPIRE_MINUTES)
        payload = InternalTokenPayload(
            exp=timegm(expire.utctimetuple()),
            user_id=user.id,
            user=user.json(),
        )
        token = jwt.encode(
            payload.dict(),
            self.internal_token_secret_key,
            algorithm=self.algorithm,
        )
        return token

    def decode_internal_token(self, token: str) -> dict | None:
        return jwt.decode(
            token,
            self.internal_token_secret_key,
            algorithms=[self.algorithm],
        )

    def verify_internal_token(self, token: str) -> InternalTokenData | None:
        try:
            payload = self.decode_internal_token(token)
            if not payload:
                return None

            return InternalTokenData(
                user_id=payload.get("user_id"),
                exp=payload.get("exp"),
                token=token,
                user=AuthenticatedUser(**payload.get("user")),
            )
        except Exception as e:
            print("verify_internal_token", e)
            return None

    @abstractmethod
    async def verify_access_token(self, token: str) -> BaseAccessTokenData:
        ...
