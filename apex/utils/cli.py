import asyncio

from tortoise import Tortoise


class TortoiseOrmSettingsInvalid(Exception):
    pass


class DependenciesNotFound(Exception):
    pass


class ShellCommand:
    def __init__(self, db_url: str, models: list[str]):
        """
        db_url: mysql://root:123456@127.0.0.1:3306/db_expenses?charset=utf8mb4
        models: ['aerich.models', 'app.expenses.models' ]
        """
        if not db_url or not models:
            raise TortoiseOrmSettingsInvalid(
                "Tortoise-orm db_url or register modules invalid "
            )
        self.db_url = db_url
        self.models = models

    def __call__(self, *args, **kwargs):
        try:
            from IPython import embed
        except ImportError:
            raise DependenciesNotFound(
                "Can not import necessary dependencies."
            )

        asyncio.run(
            Tortoise.init(db_url=self.db_url, modules={"models": self.models})
        )
        embed(using="asyncio")
