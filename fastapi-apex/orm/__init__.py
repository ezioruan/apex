from tortoise import generate_config
from tortoise.contrib.fastapi import register_tortoise


def setup_db(app, db_url, modules, **kwargs):
    config = generate_config(db_url, app_modules=modules)
    config["use_tz"] = True
    register_tortoise(app, config=config, generate_schemas=False, **kwargs)
