from typing import List
from fastapi import Depends

from app.core.roles import Role
from app.core.auth_context import AuthContext
from app.core.security import get_current_user
from app.core.exceptions import ApiException


def require_roles(allowed_roles: List[Role]):
    async def role_dependency(
        current_user: AuthContext = Depends(get_current_user),
    ) -> AuthContext:

        # Admin override
        if current_user.role == Role.ADMIN:
            return current_user

        if current_user.role not in allowed_roles:
            raise ApiException(
                status_code=403,
                detail="Insufficient permissions",
                error_code="FORBIDDEN",
            )

        return current_user

    return role_dependency
