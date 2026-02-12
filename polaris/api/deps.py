from polaris.db.session import get_db
from polaris.repositories.test_repository import TestRepository
from polaris.services.test_service import TestService
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession


def get_test_service(
    db: AsyncSession = Depends(get_db),
) -> TestService:
    repo = TestRepository(db)
    return TestService(repo)
