from .models import Item
from apex_fastapi.schema_plus.models import BaseModel
from tortoise.contrib.pydantic import (
    pydantic_model_creator,
    pydantic_queryset_creator,
)


class ItemRequest(BaseModel):
    name: str
    description: str


ItemResponse = pydantic_model_creator(Item)
ItemsResponse = pydantic_queryset_creator(Item)
