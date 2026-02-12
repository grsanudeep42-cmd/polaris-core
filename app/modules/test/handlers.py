import logging
from app.core.events.handler import EventHandler
from app.modules.test.events import TestCreatedEvent


logger = logging.getLogger(__name__)


class TestCreatedHandler(EventHandler):

    async def handle(self, event: TestCreatedEvent) -> None:
        logger.info(
            f"Test created with ID {event.test_id} "
            f"and name {event.name}"
        )
