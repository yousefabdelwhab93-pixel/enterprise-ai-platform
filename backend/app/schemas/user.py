from uuid import UUID
from datetime import datetime

from pydantic import BaseModel, ConfigDict


# =========================
# CREATE USER
# =========================

class UserCreate(BaseModel):
    tenant_id: UUID
    full_name: str
    email: str
    password: str


# =========================
# UPDATE USER
# =========================

class UserUpdate(BaseModel):
    full_name: str | None = None
    email: str | None = None
    role: str | None = None
    is_active: bool | None = None


# =========================
# USER RESPONSE
# =========================

class UserResponse(BaseModel):
    id: UUID
    tenant_id: UUID
    full_name: str
    email: str
    role: str
    is_active: bool
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)