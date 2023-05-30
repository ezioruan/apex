from fastapi import status
from fastapi.responses import ORJSONResponse, Response

from apex_fastapi.constants import BusinessCode, HTTPMessage
from apex_fastapi.schema_plus.response import InternalServiceResponse
from apex_fastapi.schema_plus.response import Response as ContentResponse


def json_response(
    *,
    code=BusinessCode.NO_ERROR,
    status_code=status.HTTP_200_OK,
    data: list | dict,
    message=HTTPMessage.SUCCESS.value,
    headers: dict | None = None,
) -> Response:
    dict_func = getattr(data, "dict", None)
    if dict_func and callable(dict_func):
        data = data.dict()
    print("Response message", f"({code}) {message}")
    resp = ORJSONResponse(
        status_code=status_code,
        content=ContentResponse(
            code=code,
            message=message,
            data=data,
        ).dict(),
        headers=headers,
    )
    return resp


def internal_service_json_response(
    *,
    service_name: str,
    url: str = "",
    code=BusinessCode.NO_ERROR,
    status_code=status.HTTP_200_OK,
    data: list | dict,
    detail: list | dict | None = None,
    message=HTTPMessage.SUCCESS.value,
) -> Response:
    dict_func = getattr(data, "dict", None)
    if dict_func and callable(dict_func):
        data = data.dict()
    print(f"[Internal] {service_name} response: ({code}) {message}")
    return ORJSONResponse(
        status_code=status_code,
        content=InternalServiceResponse(
            service_name=service_name,
            code=code,
            message=message,
            url=url,
            data=data,
            detail=detail,
        ).dict(),
    )


def transform_internal_service_error_response(
    *,
    err: InternalServiceResponse,
) -> Response:
    print(f"{err.service_name} response: ({err.code}) {err.message}")
    return ORJSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content=ContentResponse(
            code=err.code,
            message=err.message,
            data=None,
        ).dict(),
    )


def exception_convert(err: dict) -> str:
    loc, msg, error_type = err["loc"], err["msg"], err["type"]
    error_types = error_type.split(".")
    etype, tag = error_types[0], ".".join(error_types[1:])
    filtered_loc = loc[1:] if loc[0] in ("body", "query", "path") else loc
    field_string = ".".join(filtered_loc)
    if etype == "value_error":
        if tag == "missing":
            return f"{field_string} is required"
        elif tag == "extra":
            return f"{field_string} is unexpected"
        elif str(tag).startswith("url"):
            return f"{field_string} is not a valid url"
        elif tag == "tuple.length":
            return (
                f'{field_string} must be {err["ctx"]["limit_value"]} '
                f"characters long"
            )
        elif tag == "any_str.min_length":
            return (
                f"{field_string} must be longer than "
                f'{err["ctx"]["limit_value"]}'
            )
        elif tag == "any_str.max_length":
            return (
                f"{field_string} cant be longer than "
                f'{err["ctx"]["limit_value"]}'
            )
        if msg:
            return f"{field_string} error: {msg}"
        return f"{field_string} type error"
    elif etype == "type_error":
        if tag == "not_none":
            return f"{field_string} is not None"
        elif tag == "enum":
            return f"{field_string} is not a valid enumeration member"
        elif tag in ("bool", "byte", "dict"):
            return f"{field_string} value is not a valid {tag} type"
        return f"{field_string} value is not a valid {tag}"
    return f"{field_string} {etype} error: {msg}"
