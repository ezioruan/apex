import os

from apex_fastapi.settings.base_settings import EnvBaseSettings
from apex_fastapi.settings.test_settings import TestSettings


def test_base_settings_from_env_file():
    settings = EnvBaseSettings()
    assert settings


def test_base_settings_overwride_from_env_var():
    new_project_name = "new project name"
    os.environ["PROJECT_NAME"] = new_project_name
    settings = EnvBaseSettings()
    assert settings
    assert settings.PROJECT_NAME == new_project_name


def test_test_settings_from_env_file():
    settings = TestSettings()
    assert settings
