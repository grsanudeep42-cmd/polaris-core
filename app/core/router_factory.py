from typing import Type, List

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db
from app.core.schemas.response import ResponseEnvelope
from app.core.schemas.pagination import PaginationMeta
from app.core.dependencies.pagination import pagination_params
from app.core.exceptions import ApiException


def create_crud_router(
    model,
    create_schema,
    response_schema,
    service_class,
):
    router = APIRouter()

    # CREATE
    @router.post(
        "/",
        response_model=ResponseEnvelope[response_schema],
    )
    async def create_item(
        payload: create_schema, # type: ignore
        db: AsyncSession = Depends(get_db),
    ):
        service = service_class(db)
        result = await service.create(payload)

        return ResponseEnvelope.success_response(data=result)

    # LIST
    @router.get(
        "/",
        response_model=ResponseEnvelope[List[response_schema]],
    )
    async def list_items(
        db: AsyncSession = Depends(get_db),
        pagination: dict = Depends(pagination_params),
    ):
        service = service_class(db)

        items, total = await service.list(
            limit=pagination["limit"],
            offset=pagination["offset"],
        )

        meta = PaginationMeta(
            total=total,
            limit=pagination["limit"],
            offset=pagination["offset"],
        )

        return ResponseEnvelope.success_response(
            data=items,
            meta=meta.model_dump(),
        )

    # GET BY ID
    @router.get(
        "/{item_id}",
        response_model=ResponseEnvelope[response_schema],
    )
    async def get_item(
        item_id: int,
        db: AsyncSession = Depends(get_db),
    ):
        service = service_class(db)
        item = await service.get(item_id)

        if not item:
            raise ApiException(status_code=404, detail="Item not found")

        return ResponseEnvelope.success_response(data=item)

    # UPDATE
    @router.put(
        "/{item_id}",
        response_model=ResponseEnvelope[response_schema],
    )
    async def update_item(
        item_id: int,
        payload: create_schema, # type: ignore
        db: AsyncSession = Depends(get_db),
    ):
        service = service_class(db)
        item = await service.update(item_id, payload)

        if not item:
            raise ApiException(status_code=404, detail="Item not found")

        return ResponseEnvelope.success_response(data=item)

    # DELETE
    @router.delete(
        "/{item_id}",
        response_model=ResponseEnvelope[bool],
    )
    async def delete_item(
        item_id: int,
        db: AsyncSession = Depends(get_db),
    ):
        service = service_class(db)
        deleted = await service.delete(item_id)

        if not deleted:
            raise ApiException(status_code=404, detail="Item not found")

        return ResponseEnvelope.success_response(data=True)

    return router
