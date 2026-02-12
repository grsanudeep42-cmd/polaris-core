from abc import ABC, abstractmethod
from polaris.core.events.base import DomainEvent


class EventHandler(ABC):

    @abstractmethod
    async def handle(self, event: DomainEvent) -> None:
        pass
