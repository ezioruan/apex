import secrets

from pydantic import (
    AnyHttpUrl,
    BaseSettings,
    HttpUrl,
    IPvAnyNetwork,
    validator,
)

from apex_fastapi.constants import LogLevel


class EnvBaseSettings(BaseSettings):
    ENV: str = "dev"
    PROJECT_NAME: str

    SECRET_KEY: str = secrets.token_urlsafe(32)
    # 60 minutes * 24 hours * 8 days = 8 days
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 8
    SERVER_NAME: str
    SERVER_HOST: str
    SERVER_PORT: int

    # CORS_ORIGINS is a JSON-formatted list of origins
    # e.g: '[ "http://localhost:4200", "http://localhost:3000", \
    # "http://localhost:8080", "http://local.dockertoolbox.tiangolo.com"]'
    CORS_ORIGINS: list[AnyHttpUrl] = []

    # MYSQL Database URL
    DATABASE_URL: str | None = None
    TEST_DATABASE_URL: str | None = None

    # Debug SQL
    DEBUG_SQL: bool | None = None

    # Logger Level
    LOG_LEVEL: LogLevel | None = "INFO"



    AUTH_IP_WHITELIST: list[IPvAnyNetwork] = []
    # http basic auth
    BASIC_AUTH_USERNAME: str | None = None
    BASIC_AUTH_PASSWORD: str | None = None


    @validator("CORS_ORIGINS", pre=True)
    def assemble_cors_origins(cls, v: str | list[str]) -> list[str] | str:
        if isinstance(v, str) and not v.startswith("["):
            return [i.strip() for i in v.split(",")]
        elif isinstance(v, (list, str)):
            return v
        raise ValueError(v)


    @validator("LOG_LEVEL", pre=True)
    def assemble_log_level(cls, v: str) -> str | None:
        level = LogLevel[v]
        if not level:
            raise ValueError(v)
        return level

    class Config:
        env_file = ".env"
        case_sensitive = True
