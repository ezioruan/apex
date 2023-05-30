from tortoise import fields
from apex_fastapi.orm.models import BaseModel


class User(BaseModel):
    name = fields.CharField(max_length=50)
    email = fields.CharField(max_length=50, unique=True)
    password = fields.CharField(max_length=50)

    class Mata:
        table = "user"
