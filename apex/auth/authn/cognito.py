from httpx import ConnectError as HttpConnectionError
from jose import JWTError

from apex_fastapi.auth.errors import (
    AccessTokenVerificationException,
    cognito_connection_error,
    cognito_token_type_error,
    cognito_token_value_error,
)
from apex_fastapi.auth.models import CognitoAccessTokenData
from apex_fastapi.aws.cognito import (
    CognitoJWTException,
    CognitoSetting,
    CognitoTokenPayload,
    decode_cognito_jwt,
    get_cognito_public_keys,
)

from .authn import Authentication


class CognitoAuthentication(Authentication):
    def __init__(
        self,
        cognito_setting: CognitoSetting,
        internal_token_secret_key: str,
    ):
        self.cognito_setting = cognito_setting
        self._init_cognito()
        super().__init__(
            internal_token_secret_key=internal_token_secret_key,
        )

    def _init_cognito(self):
        try:
            print("Initializing cognito...")
            keys_url, keys = get_cognito_public_keys(
                region=self.cognito_setting.region,
                user_pool_id=self.cognito_setting.user_pool_id,
            )
            print(
                f"""[Initialize cognito] keys_url: {keys_url}
                keys: {keys}

                """
            )
        except Exception as e:
            print("Initializing cognito failed...")
            raise e

    def decode_access_token(self, token: str) -> CognitoTokenPayload:
        try:
            payload = decode_cognito_jwt(
                token=token,
                region=self.cognito_setting.region,
                user_pool_id=self.cognito_setting.user_pool_id,
                app_client_id=self.cognito_setting.app_client_id,
            )
            return CognitoTokenPayload(**payload)
        except TypeError:
            raise cognito_token_type_error
        except (ValueError, JWTError):
            raise cognito_token_value_error
        except HttpConnectionError:
            raise cognito_connection_error

    async def verify_access_token(self, token: str) -> CognitoAccessTokenData:
        try:
            payload = self.decode_access_token(token)
        except CognitoJWTException as e:
            raise AccessTokenVerificationException(str(e))

        return CognitoAccessTokenData(
            **payload.dict(),
            token=token,
            user_id=int(payload.username),
        )
