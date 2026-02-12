from datetime import datetime
from uuid import uuid4
from dataclasses import dataclass, field


@dataclass
class DomainEvent:
    event_id: str = field(default_factory=lambda: str(uuid4()))
    occurred_at: datetime = field(default_factory=datetime.utcnow)
