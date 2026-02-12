from sqlalchemy import String, Enum
from sqlalchemy.orm import Mapped, mapped_column

from polaris.db.base_model import BaseModel
from polaris.core.roles import Role


class User(BaseModel):
    __tablename__ = "users"

    email: Mapped[str] = mapped_column(
        String(255),
        unique=True,
        nullable=False,
        index=True,
    )

    full_name: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    role: Mapped[Role] = mapped_column(
        Enum(Role, name="role_enum"),
        default=Role.USER,
        nullable=False,
    )
