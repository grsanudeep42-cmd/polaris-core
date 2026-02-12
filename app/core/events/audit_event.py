from dataclasses import dataclass
from uuid import UUID
from typing import Optional, Dict

from app.core.events.base import DomainEvent


@dataclass
class AuditEvent(DomainEvent):
    entity_name: str
    entity_id: UUID
    action: str
    performed_by: Optional[UUID]
    metadata: Optional[Dict]
