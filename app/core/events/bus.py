from typing import Type, Dict, List, Callable
import logging

from app.core.events.base import DomainEvent
from app.core.events.handler import EventHandler


logger = logging.getLogger(__name__)


class EventBus:

    def __init__(self):
        self._handlers: Dict[
            Type[DomainEvent],
            List[EventHandler],
        ] = {}

    def register(
        self,
        event_type: Type[DomainEvent],
        handler: EventHandler,
    ) -> None:

        if event_type not in self._handlers:
            self._handlers[event_type] = []

        self._handlers[event_type].append(handler)

        logger.info(
            f"Registered handler {handler.__class__.__name__} "
            f"for event {event_type.__name__}"
        )

    async def dispatch(self, event: DomainEvent) -> None:

        handlers = self._handlers.get(type(event), [])

        if not handlers:
            logger.debug(
                f"No handlers registered for event {type(event).__name__}"
            )
            return

        for handler in handlers:
            try:
                await handler.handle(event)
            except Exception as e:
                logger.exception(
                    f"Error handling event {type(event).__name__}: {str(e)}"
                )
