from __future__ import annotations

import base64
import json
import os
from json import JSONDecodeError

from tortoise import BaseDBAsyncClient, fields, timezone
from tortoise.exceptions import OperationalError
from tortoise.fields.base import Field
from tortoise.models import Model

from .manager import EnabledObjectManager


class BaseModel(Model):
    id = fields.IntField(pk=True)
    created_at = fields.DatetimeField(auto_now_add=True)
    updated_at = fields.DatetimeField(auto_now=True)
    deleted_at = fields.DatetimeField(null=True, default=None)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.Meta.manager = EnabledObjectManager(self)
        self._meta.manager = EnabledObjectManager(self)

    async def delete(self, using_db: BaseDBAsyncClient | None = None) -> None:
        """
        Set deleted_at to current time to mark the object as deleted

        :param using_db: Specific DB connection to use instead of default bound

        :raises OperationalError: If object has never been persisted.
        """
        self.deleted_at = timezone.now()
        await self.save(
            force_update=True, update_fields=["deleted_at"], using_db=using_db
        )

    async def force_delete(
        self, using_db: BaseDBAsyncClient | None = None
    ) -> None:
        """
        Deletes the current model object.

        :param using_db: Specific DB connection to use instead of default bound

        :raises OperationalError: If object has never been persisted.
        """
        db = using_db or self._choose_db(True)
        if not self._saved_in_db:
            raise OperationalError("Can't delete unpersisted record")
        await self._pre_delete(db)
        await db.executor_class(model=self.__class__, db=db).execute_delete(
            self
        )
        await self._post_delete(db)

    class Meta:
        abstract = True
        ordering = ["-id"]
        manager = EnabledObjectManager()

    class PydanticMeta:
        exclude = ("deleted_at",)

