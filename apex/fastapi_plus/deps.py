import secrets

from fastapi import Depends, HTTPException, Query, Request, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials

from apex_fastapi.schema_plus.request import PaginationRequest


def get_pagination_query(
    page_number: int = Query(default=1),
    page_size: int = Query(default=10),
):
    return PaginationRequest(
        page_number=page_number,
        page_size=page_size,
    )


class Pagination:
    def __init__(
        self,
        request: Request,
        page_number: int = Query(default=1, ge=1),
        page_size: int = Query(default=10, ge=1),
        pagable: bool = Query(default=True),
    ):
        self.request = request
        self.pagable = pagable

        self.page_number = page_number
        self.page_size = page_size

        self.limit = page_size
        self.offset = (page_number - 1) * page_size

    def dict(self):
        return self.__dict__


def get_basic_auth_deps(username: str, password: str):
    security = HTTPBasic()

    def get_current_username(
        credentials: HTTPBasicCredentials = Depends(security),
    ):
        correct_username = secrets.compare_digest(
            credentials.username, username
        )
        correct_password = secrets.compare_digest(
            credentials.password, password
        )
        if not (correct_username and correct_password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect email or password",
                headers={"WWW-Authenticate": "Basic"},
            )

        return credentials.username

    return get_current_username
