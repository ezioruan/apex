import asyncio
import os

import boto3
import pytest
from fastapi import Depends
from httpx import AsyncClient
from moto import mock_s3
from tortoise import Tortoise, generate_config

from apex_fastapi.auth import (
    AuthEndpoint,
    apex_fastapiBearer,
    UserServiceAuthentication,
)
from apex_fastapi.constants import LogLevel
from apex_fastapi.fastapi_plus import create_app
from apex_fastapi.logger_plus import setup_logger
from apex_fastapi.orm import setup_db
from apex_fastapi.router import setup_upload
from apex_fastapi.swagger import setup_swagger

from .settings import settings

modules = {"models": settings.APPLICATION_MODULES}


@pytest.fixture
def aws_credentials():
    """Mocked AWS Credentials for moto."""
    os.environ["AWS_ACCESS_KEY_ID"] = "testing"
    os.environ["AWS_SECRET_ACCESS_KEY"] = "testing"
    os.environ["AWS_SECURITY_TOKEN"] = "testing"
    os.environ["AWS_SESSION_TOKEN"] = "testing"


@pytest.fixture
def s3_client(aws_credentials):
    with mock_s3():
        conn = boto3.client("s3", region_name="us-east-1")
        yield conn


async def init_db(db_url) -> None:
    config = generate_config(db_url, app_modules=modules)
    config["use_tz"] = True
    await Tortoise.init(
        config=config,
    )


@pytest.fixture(scope="session")
async def app():
    app = create_app()
    auth_endpoint = AuthEndpoint(root=settings.USER_SERVICE_URL)
    authentication = UserServiceAuthentication(
        endpoint=auth_endpoint,
        internal_token_secret_key=settings.INTERNAL_TOKEN_SECRET_KEY,
    )
    auth_schema = apex_fastapiBearer(
        ip_whitelist=settings.AUTH_IP_WHITELIST,
        authn=authentication,
        endpoint=auth_endpoint,
    )
    setup_db(app, settings.DATABASE_URL, modules)
    setup_swagger(app, AuthEndpoint("http://test"))
    setup_upload(
        app,
        bucket_name=settings.BUCKET_NAME,
        dependencies=[Depends(auth_schema)],
        presigned_url=settings.PRESIGNED_URL,
    )
    return app


@pytest.fixture(scope="session")
async def db():
    db = await init_db(settings.DATABASE_URL)
    print("db", db)
    yield db


@pytest.fixture(scope="session")
async def client(app):
    async with AsyncClient(app=app, base_url="http://test") as client:
        print("Client is ready")
        yield client


async def init(db_url: str):
    pass


@pytest.fixture(scope="session")
def anyio_backend():
    return "asyncio"


@pytest.fixture(scope="session")
def event_loop():
    return asyncio.get_event_loop()


@pytest.fixture(autouse=True)
async def initialize_tests():
    print("initialize_tests settings", settings)
    setup_logger("test", LogLevel.DEBUG, True)
    yield
