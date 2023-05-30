from pydantic import Field, HttpUrl

from apex_fastapi.schema_plus.models import BaseModel


class CognitoSetting(BaseModel):
    region: str
    user_pool_id: str
    app_client_id: str
    app_client_secret_key: str


class CognitoTokenPayload(BaseModel):
    origin_jti: str
    cognito_id: str = Field(alias="sub")
    event_id: str
    token_use: str
    scope: str
    auth_time: int
    iss: HttpUrl
    exp: int
    iat: int
    jti: str
    client_id: str
    username: str


class CognitoAuthenticationResult(BaseModel):
    IdToken: str
    AccessToken: str
    RefreshToken: str
    ExpiresIn: int
    TokenType: str


class CognitoRefreshTokenResult(BaseModel):
    IdToken: str
    AccessToken: str
    ExpiresIn: int
    TokenType: str


class CognitoGetUserAttribute(BaseModel):
    Name: str
    Value: str


class CognitoGetUserResult(BaseModel):
    Sub: str
    Email: str
    Username: str
    UserAttributes: list[CognitoGetUserAttribute]
