import traceback

from fastapi import Depends, FastAPI, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.openapi.docs import get_redoc_html, get_swagger_ui_html
from fastapi.openapi.utils import get_openapi
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from starlette.exceptions import HTTPException as StarletteHTTPException
from starlette.middleware.cors import CORSMiddleware

from .deps import get_basic_auth_deps
from .exceptions import (
    APPException,
    HTTPException,
    InternalServiceInvocationException,
)
from .utils import (
    exception_convert,
    internal_service_json_response,
    json_response,
)


def health():
    return json_response(data={})


async def catch_exceptions_middleware(request: Request, call_next):
    try:
        return await call_next(request)
    except Exception as ex:
        # TODO add sentry
        full_message = traceback.format_exc()
        print(full_message)
        return json_response(
            code=500, status_code=500, data=None, message=str(ex)
        )


def create_app(cors_origins=None, *args, **kwargs):
    app = FastAPI(
        *args,
        **kwargs,
    )

    @app.exception_handler(APPException)
    async def app_exception_handler(request: Request, exc: APPException):
        print("app_exception_handler")
        return json_response(
            code=exc.code,
            status_code=200,
            data=None,
            message=exc.message,
        )

    @app.exception_handler(HTTPException)
    async def http_exception_handler(request: Request, exc: HTTPException):
        print("http_exception_handler")
        return json_response(
            code=exc.code,
            status_code=exc.code,
            data=None,
            message=exc.message,
        )

    @app.exception_handler(StarletteHTTPException)
    async def starlette_http_exception_handler(
        request: Request, exc: StarletteHTTPException
    ):
        print("starlette_http_exception_handler", exc.headers)
        return json_response(
            code=exc.status_code,
            status_code=exc.status_code,
            data=None,
            message=exc.detail,
            headers=exc.headers,
        )

    @app.exception_handler(InternalServiceInvocationException)
    async def internal_service_invocation_exception_handler(
        request: Request, exc: InternalServiceInvocationException
    ):
        print("internal_service_invocation_exception_handler")
        return internal_service_json_response(
            service_name=exc.service_name,
            code=exc.code or -1,
            url=exc.url,
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            data=None,
            message=exc.message,
            detail=exc.detail,
        )

    @app.exception_handler(RequestValidationError)
    async def validation_exception_handler(
        request: Request, exc: RequestValidationError
    ):
        print("validation_exception_handler")
        reformatted_message = list()
        for pydantic_error in exc.errors():
            reformatted_message.append(exception_convert(pydantic_error))
        print("join response...", reformatted_message)
        return json_response(
            code=status.HTTP_400_BAD_REQUEST,
            status_code=status.HTTP_400_BAD_REQUEST,
            data=None,
            message=",".join(reformatted_message),
        )

    # Set all CORS enabled origins
    if cors_origins:
        app.add_middleware(
            CORSMiddleware,
            allow_origins=[str(origin) for origin in cors_origins],
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )

    app.middleware("http")(catch_exceptions_middleware)
    app.add_api_route("/health", health, include_in_schema=False)
    return app


def setup_basic_auth_for_docs(
    app: FastAPI,
    username: str,
    password: str,
    docs_url: str = "/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
):
    get_current_username = get_basic_auth_deps(username, password)

    @app.get(docs_url, include_in_schema=False)
    async def get_swagger_documentation(
        username: str = Depends(get_current_username),
    ):
        return get_swagger_ui_html(openapi_url="/openapi.json", title="docs")

    @app.get(redoc_url, include_in_schema=False)
    async def get_redoc_documentation(
        username: str = Depends(get_current_username),
    ):
        return get_redoc_html(openapi_url="/openapi.json", title="docs")

    @app.get(openapi_url, include_in_schema=False)
    async def openapi(username: str = Depends(get_current_username)):
        return get_openapi(
            title=app.title, version=app.version, routes=app.routes
        )
