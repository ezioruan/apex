from apex_fastapi.settings.base_settings import EnvBaseSettings


class Settings(EnvBaseSettings):
    APPLICATION_MODULES: list[str] = [
        "apex_fastapi.orm.test_models",
    ]
    BUCKET_NAME: str
    PRESIGNED_URL: str


settings = Settings()
