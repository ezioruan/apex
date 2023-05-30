## apex_fastapi Framework

This repo contains some extra steup for an FastAPI project
- fastapi_plus : create fast app with some default settings and handlers
- logger_plus : logger setup for fastapi, tortoise , aws and etc.
- schema_plus : Base module for schema
- settings : Env base settings


### Test
1. Run `docker-compose up -d` in the test folder.
2. Copy the `test.env` file to `.env` and fill in or change the values.
3. Run `export $(cat .env | xargs)` to set the environment variables.
4. Run `pytest` in the root folder.


### Shell
1. Instantiate class object `ShellCommand`
2. Run the instance
```
# utils/cli.py
shell = ShellCommand(
    db_url=settings.DATABASE_URL,
    models=settings.APPLICATION_MODELS,
    )
# run shell()
```
