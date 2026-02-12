from dataclasses import dataclass
from uuid import UUID
from app.core.events.base import DomainEvent


@dataclass
class TestCreatedEvent(DomainEvent):
    test_id: UUID
    name: str
