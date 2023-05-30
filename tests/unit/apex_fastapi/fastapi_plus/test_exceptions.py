import enum

from apex_fastapi.fastapi_plus.errors import HTTPError
from apex_fastapi.fastapi_plus.exceptions import APPException, HTTPException


class ErrorTest1(enum.IntEnum):
    TEST_ERROR = 1


def test_APPException():
    try:
        raise APPException(ErrorTest1.TEST_ERROR)
    except APPException as e:
        assert e.code == ErrorTest1.TEST_ERROR
        assert e.message == ErrorTest1.TEST_ERROR.name
        print("e", e)


def test_HTTPException():
    try:
        raise HTTPException(HTTPError.UNAUTHORIZED)
    except HTTPException as e:
        assert e.code == HTTPError.UNAUTHORIZED
        assert e.message == HTTPError.UNAUTHORIZED.name
        print("e", e)
