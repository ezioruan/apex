from apex_fastapi.utils.cli import ShellCommand

from .settings import settings

shell = ShellCommand(
    db_url=settings.DATABASE_URL, models=settings.APPLICATION_MODULES
)
