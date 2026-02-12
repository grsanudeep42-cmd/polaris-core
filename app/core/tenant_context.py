from uuid import UUID
from pydantic import BaseModel


class TenantContext(BaseModel):
    tenant_id: UUID
