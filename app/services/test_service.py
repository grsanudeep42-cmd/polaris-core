from sqlalchemy.ext.asyncio import AsyncSession
from app.repositories.test_repository import TestRepository
from app.schemas.test_schema import TestCreate


class TestService:

    def __init__(self, db: AsyncSession):
        self.repo = TestRepository(db)

    async def create_test(self, payload: TestCreate):
        obj = await self.repo.create(name=payload.name)
        await self.repo.db.commit()
        await self.repo.db.refresh(obj)
        return obj

    async def list_tests(self, limit: int, offset: int):
        items = await self.repo.list(limit=limit, offset=offset)
        total = await self.repo.count()
        return items, total
