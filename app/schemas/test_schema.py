from pydantic import BaseModel
from uuid import UUID


class TestBase(BaseModel):
    name: str


class TestCreate(TestBase):
    pass


class TestUpdate(TestBase):
    version: int


class TestResponse(TestBase):
    id: UUID
    version: int

    class Config:
        from_attributes = True
