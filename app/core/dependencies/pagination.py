from fastapi import Query
from pydantic import BaseModel, Field


class PaginationParams(BaseModel):
    limit: int = Field(10, ge=1, le=100)
    offset: int = Field(0, ge=0)


def pagination_params(
    limit: int = Query(10, ge=1, le=100),
    offset: int = Query(0, ge=0),
) -> PaginationParams:
    return PaginationParams(limit=limit, offset=offset)
