from fastapi import Depends, Header
from uuid import UUID

from polaris.core.auth_context import AuthContext
from polaris.core.roles import Role
from polaris.core.exceptions import ApiException


async def get_current_user(
    x_user_id: UUID | None = Header(default=None),
    x_user_role: str | None = Header(default=None),
) -> AuthContext:
    """
    Temporary header-based auth for development.
    Replace with JWT verification later.
    """

    if not x_user_id or not x_user_role:
        raise ApiException(
            status_code=401,
            detail="Unauthorized",
            error_code="UNAUTHORIZED",
        )

    try:
        role = Role(x_user_role)
    except ValueError:
        raise ApiException(
            status_code=403,
            detail="Invalid role",
            error_code="INVALID_ROLE",
        )

    return AuthContext(
        user_id=x_user_id,
        role=role,
    )
