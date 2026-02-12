from typing import Generic, TypeVar, Type, Optional, List
from uuid import UUID
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from polaris.db.base_model import BaseModel
from polaris.core.exceptions import VersionMismatchException


ModelType = TypeVar("ModelType", bound=BaseModel)


class BaseRepository(Generic[ModelType]):

    def __init__(
        self,
        model: Type[ModelType],
        session: AsyncSession,
        tenant_id: Optional[UUID] = None,
        is_admin: bool = False,
    ):
        self.model = model
        self.session = session
        self.tenant_id = tenant_id
        self.is_admin = is_admin

    def _tenant_filter(self, stmt):
        if self.is_admin:
            return stmt

        if self.tenant_id:
            return stmt.where(self.model.tenant_id == self.tenant_id)

        return stmt

    async def get(self, obj_id) -> Optional[ModelType]:
        stmt = select(self.model).where(
            self.model.id == obj_id,
            self.model.is_deleted.is_(False),
        )

        stmt = self._tenant_filter(stmt)

        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def list(
        self,
        skip: int = 0,
        limit: int = 20,
    ) -> List[ModelType]:

        stmt = (
            select(self.model)
            .where(self.model.is_deleted.is_(False))
            .offset(skip)
            .limit(limit)
        )

        stmt = self._tenant_filter(stmt)

        result = await self.session.execute(stmt)
        return result.scalars().all()

    async def create(self, obj_in: dict) -> ModelType:
        db_obj = self.model(**obj_in)

        if self.tenant_id:
            db_obj.tenant_id = self.tenant_id

        self.session.add(db_obj)
        return db_obj

    async def update(
        self,
        db_obj: ModelType,
        obj_in: dict,
        expected_version: int,
    ) -> ModelType:

        if db_obj.version != expected_version:
            raise VersionMismatchException()

        for field, value in obj_in.items():
            setattr(db_obj, field, value)

        db_obj.version += 1
        return db_obj

    async def soft_delete(
        self,
        db_obj: ModelType,
        expected_version: int,
    ) -> ModelType:

        if db_obj.version != expected_version:
            raise VersionMismatchException()

        db_obj.is_deleted = True
        db_obj.version += 1
        return db_obj
