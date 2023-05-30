import logging
import sys

from apex_fastapi.constants import LogLevel


def setup_logger(
    name: str, level: LogLevel, debug_sql: bool = False
) -> logging.Logger:

    print("setup_logger", level, level.name)

    logging.basicConfig(level=level.value)
    logger = logging.getLogger(name)
    fmt = logging.Formatter(
        fmt="%(asctime)s - %(name)s:%(lineno)d - %(levelname)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )
    sh = logging.StreamHandler(sys.stdout)
    sh.setLevel(level.value)
    sh.setFormatter(fmt)

    # will print debug sql
    if debug_sql:
        logger_db_client = logging.getLogger("db_client")
        logger_db_client.setLevel(logging.DEBUG)
        logger_db_client.addHandler(sh)

        logger_tortoise = logging.getLogger("tortoise")
        logger_tortoise.setLevel(logging.DEBUG)
        logger_tortoise.addHandler(sh)

    return logger
