from sqlalchemy.ext.asyncio import AsyncSession
from polaris.models.test_model import TestModel
from polaris.repositories.base_repository import BaseRepository


class TestRepository(BaseRepository[TestModel]):

    def __init__(self, db: AsyncSession):
        super().__init__(TestModel, db)
