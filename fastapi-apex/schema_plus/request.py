from apex_fastapi.schema_plus.models import BaseModel


class PaginationRequest(BaseModel):
    page_number: int
    page_size: int
