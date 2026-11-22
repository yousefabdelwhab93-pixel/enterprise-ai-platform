import uuid
from datetime import datetime

from sqlalchemy import (
    String,
    Boolean,
    DateTime,
    ForeignKey,
    UniqueConstraint,
    func,
)
from sqlalchemy.orm import Mapped, mapped_column

from backend.app.core.database import Base


class User(Base):
    __tablename__ = "users"

    __table_args__ = (
        UniqueConstraint(
            "tenant_id",
            "email",
            name="uq_user_tenant_email",
        ),
    )

    # Primary Key
    id: Mapped[uuid.UUID] = mapped_column(
        primary_key=True,
        default=uuid.uuid4,
    )

    # Tenant Relationship (Foreign Key)
    tenant_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("tenants.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    # User Information
    full_name: Mapped[str] = mapped_column(
        String(150),
        nullable=False,
    )

    email: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    # Hashed Password
    password_hash: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    # User Role
    role: Mapped[str] = mapped_column(
        String(50),
        default="user",
        server_default="user",
        nullable=False,
    )

    # Account Status
    is_active: Mapped[bool] = mapped_column(
        Boolean,
        default=True,
        server_default="true",
        nullable=False,
    )

    # Creation Timestamp
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )