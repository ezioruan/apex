from apex_fastapi.settings.base_settings import EnvBaseSettings
from functools import lru_cache
from pydantic import HttpUrl


class Settings(EnvBaseSettings):
    PROJECT_NAME: str = "Sample Service"
    SECRET_KEY: str
    USER_SERVICES_URL: HttpUrl = None

    APPLICATION_MODULES: list[str] = [
        "app.auth.models",
        "app.item.models",
    ]


@lru_cache
def get_settings():
    return Settings()


settings = get_settings()
