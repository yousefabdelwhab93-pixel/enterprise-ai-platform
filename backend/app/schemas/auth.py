from uuid import UUID

from pydantic import BaseModel


class LoginRequest(BaseModel):
    tenant_id: UUID
    email: str
    password: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"