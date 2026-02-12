from typing import Type, TypeVar, List

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db
from app.core.schemas.response import ResponseEnvelope
from app.core.schemas.pagination import PaginationMeta
from app.core.dependencies.pagination import pagination_params
from app.repositories.base_repository import BaseRepository
from app.db.base_class import Base


ModelType = TypeVar("ModelType", bound=Base)


def create_crud_router(
    model: Type[ModelType],
    create_schema: Type,
    response_schema: Type,
) -> APIRouter:

    router = APIRouter()

    # -----------------------
    # CREATE
    # -----------------------
    @router.post(
        "/",
        response_model=ResponseEnvelope[response_schema],
    )
    async def create_item(
        payload: create_schema, # type: ignore
        db: AsyncSession = Depends(get_db),
    ):
        repo = BaseRepository(model, db)

        obj = await repo.create(**payload.model_dump())
        await db.commit()

        return ResponseEnvelope.success_response(data=obj)

    # -----------------------
    # LIST
    # -----------------------
    @router.get(
        "/",
        response_model=ResponseEnvelope[List[response_schema]],
    )
    async def list_items(
        db: AsyncSession = Depends(get_db),
        pagination: dict = Depends(pagination_params),
    ):
        repo = BaseRepository(model, db)

        items = await repo.list(
            limit=pagination["limit"],
            offset=pagination["offset"],
        )
        total = await repo.count()

        meta = PaginationMeta(
            total=total,
            limit=pagination["limit"],
            offset=pagination["offset"],
        )

        return ResponseEnvelope.success_response(
            data=items,
            meta=meta.model_dump(),
        )

    return router
