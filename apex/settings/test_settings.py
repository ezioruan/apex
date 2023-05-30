from .base_settings import EnvBaseSettings


class TestSettings(EnvBaseSettings):
    class Config:
        env_file = ".test.env"
        case_sensitive = True
