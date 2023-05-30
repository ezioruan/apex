from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from apex_fastapi.fastapi_plus.exceptions import HTTPException
from apex_fastapi.fastapi_plus.errors import HTTPError
from .settings import settings
from .constants import ALGORITHM

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/v1/auth/swagger/token")


def parse_jwt_data(token: str) -> int:
    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[ALGORITHM]
        )
        user_id: str = payload.get("sub")
        if user_id is None:
            raise HTTPException(HTTPError.UNAUTHORIZED)
    except JWTError:
        raise HTTPException(HTTPError.UNAUTHORIZED)
    return int(user_id)


async def get_user_id(token: str = Depends(oauth2_scheme)) -> int:
    user_id = parse_jwt_data(token)
    return user_id
