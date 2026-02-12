from uuid import UUID
from pydantic import BaseModel
from app.core.roles import Role


class AuthContext(BaseModel):
    user_id: UUID
    role: Role
