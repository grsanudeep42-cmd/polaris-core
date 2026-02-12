from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db
from app.services.test_service import TestService
from app.schemas.test_schema import TestCreate, TestResponse

from app.core.schemas.response import ResponseEnvelope
from app.core.schemas.pagination import PaginationMeta
from app.core.dependencies.pagination import PaginationParams, pagination_params
from app.models.test_model import TestModel
from app.schemas.test_schema import TestCreate, TestResponse
from app.core.crud.router_factory import create_crud_router
from app.db.session import get_session
from app.core.response import ResponseEnvelope
from app.core.permissions import require_roles
from app.core.roles import Role
from app.core.auth_context import AuthContext

router = APIRouter()

router = create_crud_router(
    model=TestModel,
    create_schema=TestCreate,
    response_schema=TestResponse,
)

@router.post(
    "/",
    response_model=ResponseEnvelope[TestResponse],
)
async def create_test(
    payload: TestCreate,
    db: AsyncSession = Depends(get_db),
):
    service = TestService(db)
    result = await service.create_test(payload)

    return ResponseEnvelope.success_response(data=result)


@router.get(
    "/",
    response_model=ResponseEnvelope[List[TestResponse]],
)
async def list_tests(
    db: AsyncSession = Depends(get_db),
    pagination: PaginationParams = Depends(pagination_params),
):
    service = TestService(db)

    items, total = await service.list_tests(
        limit=pagination.limit,
        offset=pagination.offset,
    )

    meta = PaginationMeta(
        total=total,
        limit=pagination.limit,
        offset=pagination.offset,
    )

    return ResponseEnvelope.success_response(
        data=items,
        meta=meta.model_dump(),
    )

@router.get(
    "/secure-data",
    dependencies=[Depends(require_roles([Role.CLIENT, Role.FREELANCER]))],
)
async def secure_endpoint(
    session: AsyncSession = Depends(get_session),
):
    return ResponseEnvelope(
        success=True,
        message="Access granted",
    )