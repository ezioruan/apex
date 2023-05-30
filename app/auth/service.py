from datetime import datetime, timedelta
from .models import User
from .errors import AuthError
from jose import jwt
import hashlib
from apex_fastapi.fastapi_plus.exceptions import APPException
from app.constants import ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES
from app.settings import settings
from app.logger import logger


class AuthService:
    def verify_password(self, plain_password, hashed_password):
        password_hash = hashlib.md5(plain_password.encode("utf-8")).hexdigest()
        return password_hash == hashed_password

    async def login(self, username: str, password: str):
        user = await User.filter(email=username).first()
        if not user:
            raise APPException(AuthError.USER_NOT_FOUND)
        if not self.verify_password(password, user.password):
            raise APPException(AuthError.PASSWORD_NOT_EQUAL)
        logger.info("AuthService login success for user %s", username)
        access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = self.create_access_token(
            data={"sub": str(user.id)}, expires_delta=access_token_expires
        )
        return {"access_token": access_token, "token_type": "bearer"}

    def create_access_token(
        self, data: dict, expires_delta: timedelta | None = None
    ):
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(minutes=15)
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(
            to_encode, settings.SECRET_KEY, algorithm=ALGORITHM
        )
        return encoded_jwt
