from typing import Generic, TypeVar, Type, List, Optional, Dict
from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from polaris.db.unit_of_work import UnitOfWork
from polaris.repositories.base_repository import BaseRepository
from polaris.db.base_model import BaseModel
from polaris.core.exceptions import NotFoundException
from polaris.core.events.registry import event_bus
from polaris.core.events.audit_event import AuditEvent
from polaris.core.roles import Role


ModelType = TypeVar("ModelType", bound=BaseModel)


class BaseService(Generic[ModelType]):

    def __init__(
        self,
        model: Type[ModelType],
        repository: Type[BaseRepository],
    ):
        self.model = model
        self.repository_class = repository

    def _repo(
        self,
        session: AsyncSession,
        tenant_id: UUID,
        role: Role,
    ):

        is_admin = role == Role.ADMIN

        return self.repository_class(
            self.model,
            session,
            tenant_id=tenant_id,
            is_admin=is_admin,
        )

    async def emit_audit(
        self,
        entity_id: UUID,
        action: str,
        performed_by: Optional[UUID] = None,
        metadata: Optional[Dict] = None,
    ):
        await event_bus.dispatch(
            AuditEvent(
                entity_name=self.model.__name__,
                entity_id=entity_id,
                action=action,
                performed_by=performed_by,
                metadata=metadata,
            )
        )

    async def get(
        self,
        session: AsyncSession,
        obj_id,
        tenant_id: UUID,
        role: Role,
    ):
        repo = self._repo(session, tenant_id, role)
        obj = await repo.get(obj_id)

        if not obj:
            raise NotFoundException()

        return obj

    async def list(
        self,
        session: AsyncSession,
        tenant_id: UUID,
        role: Role,
        skip: int = 0,
        limit: int = 20,
    ) -> List[ModelType]:

        repo = self._repo(session, tenant_id, role)
        return await repo.list(skip=skip, limit=limit)

    async def create(
        self,
        session: AsyncSession,
        obj_in: dict,
        tenant_id: UUID,
        role: Role,
        performed_by: Optional[UUID] = None,
    ):

        async with UnitOfWork(session):
            repo = self._repo(session, tenant_id, role)
            obj = await repo.create(obj_in)

        await self.emit_audit(
            entity_id=obj.id,
            action="CREATE",
            performed_by=performed_by,
            metadata=obj_in,
        )

        return obj
