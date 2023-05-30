from fastapi import APIRouter, Depends
from apex_fastapi.schema_plus.response import Response
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from .schemas import LoginRequest, TokenResponse
from apex_fastapi.fastapi_plus.utils import json_response
from .service import AuthService

auth_service = AuthService()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/v1/auth/swagger/token")

router = APIRouter(
    prefix="/auth",
    tags=["auth"],
)


@router.post("/swagger/token", response_model=TokenResponse)
async def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
):
    token = await auth_service.login(form_data.username, form_data.password)
    return token


@router.post("/login", response_model=Response[TokenResponse])
async def login(request: LoginRequest):
    token = await auth_service.login(request.username, request.password)
    return json_response(data=token)
