from datetime import datetime

from pydantic import EmailStr, HttpUrl, Json

from apex_fastapi.schema_plus.models import BaseModel

from .constants import UserPhaseType, UserScopeType, UserType


class AuthenticatedUser(BaseModel):
    id: int
    firstname: str
    lastname: str
    email: EmailStr
    avatar: str | None = None
    client_id: int
    user_type: UserType
    scope: UserScopeType
    user_phase: UserPhaseType
    has_mfa: bool
    archived_at: datetime | None = None
    created_at: datetime
    updated_at: datetime
    roles: list[int] = []
    permissions: list[str] = []
    resource_policies: dict[str, dict] = {}


class TokenRequest(BaseModel):
    email: EmailStr
    password: str

    class Config:
        schema_extra = {
            "example": {
                "email": "test@join.com",
                "password": "Qu8l1ty!",
            },
        }


class TokenResponse(BaseModel):
    id_token: str
    access_token: str
    refresh_token: str
    token_type: str


class BaseAccessTokenData(BaseModel):
    token: str
    user_id: int


class CognitoAccessTokenData(BaseAccessTokenData):
    cognito_id: str
    event_id: str
    token_use: str
    scope: str
    auth_time: int
    iss: HttpUrl
    exp: int
    iat: int
    jti: str
    client_id: str


class InternalTokenPayload(BaseModel):
    user_id: int
    exp: int
    user: Json


class InternalTokenData(BaseModel):
    token: str
    user_id: int
    exp: int
    user: AuthenticatedUser
