from uuid import UUID
from datetime import datetime

from pydantic import (
    BaseModel,
    ConfigDict,
    Field,
    model_validator,
)


# =========================
# CREATE DOCUMENT
# =========================

class DocumentCreate(BaseModel):
    filename: str = Field(
        min_length=1,
        max_length=255,
    )

    file_type: str = Field(
        min_length=1,
        max_length=100,
    )

    file_size: int = Field(
        ge=0,
    )


# =========================
# UPDATE DOCUMENT
# =========================

class DocumentUpdate(BaseModel):
    is_active: bool | None = None

    @model_validator(mode="after")
    def validate_update(self):
        if not self.model_fields_set:
            raise ValueError("At least one field must be provided.")

        if self.is_active is None:
            raise ValueError("is_active cannot be null.")

        return self


# =========================
# DOCUMENT RESPONSE
# =========================

class DocumentResponse(BaseModel):
    id: UUID
    tenant_id: UUID
    uploaded_by: UUID | None

    filename: str
    file_type: str
    file_size: int

    storage_path: str
    status: str
    is_active: bool

    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)