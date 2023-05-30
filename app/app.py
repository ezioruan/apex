from apex_fastapi.fastapi_plus import create_app
from apex_fastapi.orm import setup_db

from .api import v1
from .logger import logger
from .settings import settings

modules = {"models": settings.APPLICATION_MODULES}


app = create_app(
    cors_origins=settings.CORS_ORIGINS,
    title=settings.PROJECT_NAME,
    # openapi_url=f"{settings.API_V1_STR}/openapi.json",
)

setup_db(app, db_url=settings.DATABASE_URL, modules=modules)


app.include_router(v1.router)
logger.info("start server")
