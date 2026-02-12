import logging
from sqlalchemy.ext.asyncio import AsyncSession

from polaris.core.events.handler import EventHandler
from polaris.core.events.audit_event import AuditEvent
from polaris.db.session import AsyncSessionLocal
from polaris.models.audit_log import AuditLog


logger = logging.getLogger(__name__)


class AuditEventHandler(EventHandler):

    async def handle(self, event: AuditEvent) -> None:

        async with AsyncSessionLocal() as session:
            audit = AuditLog(
                entity_name=event.entity_name,
                entity_id=event.entity_id,
                action=event.action,
                performed_by=event.performed_by,
                metadata=event.metadata,
            )

            session.add(audit)
            await session.commit()
