from pydantic import EmailStr, Field, validator
from tortoise.contrib.pydantic import pydantic_model_creator

from apex_fastapi.orm.test_models import User
from apex_fastapi.schema_plus.models import BaseModel


class UserCreateRequest(BaseModel):
    name: str = Field(min_length=5)
    email: EmailStr

    @validator("name")
    def name_must_alphanumeric(cls, v):
        if not v.isalnum():
            raise ValueError("must be alphanumeric")
        return v

    @validator("name")
    def name_must_longger_than_5digits(cls, v):
        if not len(v) > 5:
            raise ValueError("must longer than 5")
        return v


UserResponse = pydantic_model_creator(User)
