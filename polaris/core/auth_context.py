from uuid import UUID
from pydantic import BaseModel
from polaris.core.roles import Role


class AuthContext(BaseModel):
    user_id: UUID
    role: Role
