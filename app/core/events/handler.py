from abc import ABC, abstractmethod
from app.core.events.base import DomainEvent


class EventHandler(ABC):

    @abstractmethod
    async def handle(self, event: DomainEvent) -> None:
        pass
