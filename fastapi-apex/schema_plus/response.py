from typing import Generic, TypeVar

from pydantic import Field
from pydantic.generics import GenericModel

from apex_fastapi.constants import HTTPMessage

T = TypeVar("T")


class Response(GenericModel, Generic[T]):
    code: int = Field(
        default=0,
        title="code",
        description="""
        The code represents whether the operation was successful or not
        1: 0 means no error is the default state
        2: three-digit number in 400-500, which is an error of HTTP.
            At this time, it is the same as http status_code.
        3: four-digit number, means is a business logic error.
            At this time, the http status_code will be 200.
        """,
    )
    message: str = Field(
        default=HTTPMessage.SUCCESS.value,
        title="description",
        description="""
        Intuitive error message uppercase and underline
        example: USER_NOT_ACTIVE, USER_EXPIRED
                         """,
    )
    data: T = Field(
        default=None,
        title="data",
        description="""
                   """,
    )


class InternalServiceResponse(GenericModel, Generic[T]):
    service_name: str
    url: str = ""
    code: int = 0
    message: str = HTTPMessage.SUCCESS.value
    data: T = None


class ListData(GenericModel, Generic[T]):
    total: int | None = Field(
        default=None, title="total", description="The records count"
    )
    rows: list[T] = Field(
        default=None, title="rows", description="The data list"
    )


class PaginationData(GenericModel, Generic[T]):
    total: int | None = Field(
        default=None, title="total", description="The records count"
    )
    page_number: int | None = Field(
        default=None, title="page_number", description="page size from 1"
    )
    page_size: int | None = Field(
        default=None, title="page_size", description="row size for a page"
    )
    rows: list[T] | T = Field(
        default=None, title="rows", description="The data list"
    )
