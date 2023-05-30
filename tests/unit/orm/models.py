from tortoise import fields

from apex_fastapi.orm.models import BaseModel, EncryptedField


class User(BaseModel):
    name = fields.CharField(max_length=50)
    email = EncryptedField()
