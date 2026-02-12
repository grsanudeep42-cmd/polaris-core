from fastapi import Header
from uuid import UUID

from app.core.exceptions import ApiException
from app.core.tenant_context import TenantContext


async def get_current_tenant(
    x_tenant_id: UUID | None = Header(default=None),
) -> TenantContext:

    if not x_tenant_id:
        raise ApiException(
            status_code=400,
            detail="Tenant ID missing",
            error_code="TENANT_REQUIRED",
        )

    return TenantContext(tenant_id=x_tenant_id)
