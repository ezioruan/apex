from .models import Item
from .schemas import ItemRequest, ItemResponse, ItemsResponse
from apex_fastapi.schema_plus.response import ListData


class ItemService:
    async def add_item(
        self, user_id: int, request: ItemRequest
    ) -> ItemResponse:
        item = Item(**request.dict())
        item.user_id = user_id
        await Item.save(item)
        return await ItemResponse.from_tortoise_orm(item)

    async def get_items(self, user_id: int) -> ListData[ItemResponse]:
        queryset = Item.filter(user_id=user_id).order_by("-id").all()
        rows = await ItemsResponse.from_queryset(queryset)
        return ListData[ItemsResponse](rows=rows, total=len(rows.__root__))

    async def get_item(self, user_id: int, item_id: int) -> ItemResponse:
        queryset = Item.filter(user_id=user_id, id=item_id).first()
        return await ItemResponse.from_queryset_single(queryset)
