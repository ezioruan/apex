from fastapi import Depends, FastAPI, status
from fastapi.exceptions import HTTPException
from fastapi.security import OAuth2PasswordRequestForm

from apex_fastapi.auth import AuthEndpoint, TokenResponse
from apex_fastapi.constants import SWAGGER_LOGIN_URL


def setup_swagger(
    app: FastAPI,
    auth_endpoint: AuthEndpoint,
    login_url=SWAGGER_LOGIN_URL,
):
    async def login(input: OAuth2PasswordRequestForm = Depends()):
        try:
            return await auth_endpoint.token(
                input.username,
                input.password,
            )
        except Exception as e:
            print("Swagger login", e)
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=str(e),
            )

    app.add_api_route(
        path=login_url,
        methods=["post"],
        endpoint=login,
        response_model=TokenResponse,
    )
