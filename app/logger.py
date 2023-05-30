import logging
from .settings import settings
from apex_fastapi.logger_plus import setup_logger


logger: logging.Logger = setup_logger(
    settings.SERVER_NAME, settings.LOG_LEVEL, settings.DEBUG_SQL
)
