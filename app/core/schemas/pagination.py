from pydantic import BaseModel


class PaginationMeta(BaseModel):
    total: int
    limit: int
    offset: int
