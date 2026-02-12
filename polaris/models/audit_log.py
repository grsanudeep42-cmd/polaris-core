from sqlalchemy import String, JSON
from sqlalchemy.orm import Mapped, mapped_column
from uuid import UUID

from polaris.db.base_model import BaseModel


class AuditLog(BaseModel):
    __tablename__ = "audit_logs"

    entity_name: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    entity_id: Mapped[UUID] = mapped_column(
        nullable=False,
        index=True,
    )

    action: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
    )

    performed_by: Mapped[UUID] = mapped_column(
        nullable=True,
    )

    metadata: Mapped[dict] = mapped_column(
        JSON,
        nullable=True,
    )
