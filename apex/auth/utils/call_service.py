import httpx
from fastapi import status

from apex_fastapi.constants import BusinessCode
from apex_fastapi.fastapi_plus.exceptions import InternalServiceInvocationException
from apex_fastapi.schema_plus.response import InternalServiceResponse


async def call_service(
    service_name: str,
    url: str,
    method: str = "get",
    headers: dict[str, str] | None = None,
    data: dict | None = None,
    json: dict | None = None,
    params: dict | None = None,
    files=None,
):
    async with httpx.AsyncClient() as client:
        try:
            resp = await client.request(
                method=method,
                url=url,
                headers=headers,
                data=data,
                json=json,
                params=params,
                files=files,
                follow_redirects=True,
            )
            resp_data = InternalServiceResponse(
                **resp.json(),
                url=url,
                service_name=service_name,
            )

            if resp.status_code != status.HTTP_200_OK:
                raise InternalServiceInvocationException(
                    service_name=service_name,
                    url=url,
                    message=resp_data.message,
                    detail=resp_data,
                    code=resp.status_code,
                )

            if resp_data.code != BusinessCode.NO_ERROR:
                raise InternalServiceInvocationException(
                    service_name=service_name,
                    url=url,
                    message=resp_data.message,
                    detail=resp_data,
                    code=resp_data.code,
                )

            return resp_data
        except InternalServiceInvocationException as e:
            raise e
        except Exception as e:
            raise InternalServiceInvocationException(
                service_name=service_name,
                url=url,
                message=str(e),
                detail=str(e),
            )
