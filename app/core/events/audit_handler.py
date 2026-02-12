import logging
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.events.handler import EventHandler
from app.core.events.audit_event import AuditEvent
from app.db.session import AsyncSessionLocal
from app.models.audit_log import AuditLog


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
