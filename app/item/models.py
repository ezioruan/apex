from tortoise import fields

from apex_fastapi.orm.models import BaseModel


class Item(BaseModel):
    name = fields.CharField(max_length=64)
    description = fields.CharField(max_length=255)
    user_id = fields.IntField(null=True)

    class Mata:
        table = "item"
