from fastapi import APIRouter, Depends

from apex_fastapi.schema_plus.response import Response, ListData
from apex_fastapi.fastapi_plus.utils import json_response
from .schemas import ItemRequest, ItemResponse
from .service import ItemService

from app.dependencies import get_user_id

item_service = ItemService()

router = APIRouter(
    prefix="/items",
    tags=["items"],
)


@router.post("/", response_model=Response[ItemResponse])
async def create_item(
    request: ItemRequest, user_id: int = Depends(get_user_id)
):
    data = await item_service.add_item(user_id, request)
    return json_response(data=data)


@router.get("/", response_model=Response[ListData[ItemResponse]])
async def get_items(user_id: int = Depends(get_user_id)):
    data = await item_service.get_items(user_id)
    return json_response(data=data)


@router.get("/{item_id}", response_model=Response[ItemResponse])
async def get_item(item_id: int, user_id: int = Depends(get_user_id)):
    data = await item_service.get_item(user_id, item_id)
    return json_response(data=data)
