from sqlalchemy.ext.asyncio import AsyncSession
from app.models.test_model import TestModel
from app.repositories.base_repository import BaseRepository


class TestRepository(BaseRepository[TestModel]):

    def __init__(self, db: AsyncSession):
        super().__init__(TestModel, db)
