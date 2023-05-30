from apex_fastapi.auth.utils import call_service, create_token_header
from apex_fastapi.constants import INTERNAL_AUTHORIZATION_HEADER_KEY


class Endpoint:
    def __init__(self, name: str, root: str):
        self.name = name
        self.root = root

    def _create_headers(self, headers, auth=None):
        if not auth:
            return headers

        if not headers:
            headers = {}

        if auth.access_token:
            headers.update(**create_token_header(auth.access_token))

        if auth.internal_token:
            headers.update(
                **create_token_header(
                    auth.internal_token,
                    key=INTERNAL_AUTHORIZATION_HEADER_KEY,
                )
            )

        return headers

    async def __call__(
        self,
        url: str,
        method: str = "get",
        auth=None,  # Authorization
        headers: dict[str, str] | None = None,
        data: dict | None = None,
        json: dict | None = None,
        params: dict | None = None,
        files=None,
    ):
        resp = await call_service(
            service_name=self.name,
            method=method,
            url=f"{self.root}{url}",
            data=data,
            json=json,
            params=params,
            files=files,
            headers=self._create_headers(headers, auth),
        )
        return resp.data
