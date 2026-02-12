from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base_class import Base
from app.db.base_model import BaseModel


class TestModel(Base, BaseModel):
    __tablename__ = "test_models"

    name: Mapped[str] = mapped_column(String, nullable=False)
