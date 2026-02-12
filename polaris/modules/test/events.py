from dataclasses import dataclass
from uuid import UUID
from polaris.core.events.base import DomainEvent


@dataclass
class TestCreatedEvent(DomainEvent):
    test_id: UUID
    name: str
