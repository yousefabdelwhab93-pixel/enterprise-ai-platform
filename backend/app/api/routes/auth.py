from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from backend.app.core.security import verify_password, create_access_token
from backend.app.models.user import User
from backend.app.models.tenant import Tenant
from backend.app.schemas.auth import LoginRequest, TokenResponse
from backend.app.api.dependencies import get_db, get_current_user
from backend.app.schemas.user import UserResponse

router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post("/login", response_model=TokenResponse)
def login(
    login_data: LoginRequest,
    db: Session = Depends(get_db),
):
    # Check if tenant exists and is active
    tenant = db.scalar(
        select(Tenant).where(
            Tenant.id == login_data.tenant_id,
            Tenant.is_active.is_(True),
        )
    )

    if not tenant:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
        )

    # Find user inside the tenant
    user = db.scalar(
        select(User).where(
            User.tenant_id == login_data.tenant_id,
            User.email == login_data.email.lower().strip(),
            User.is_active.is_(True),
        )
    )

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
        )

    # Verify password
    if not verify_password(login_data.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
        )

    # Generate JWT
    access_token = create_access_token(
        data={
            "sub": str(user.id),
            "tenant_id": str(user.tenant_id),
            "role": user.role,
        }
    )

    return {
        "access_token": access_token,
        "token_type": "bearer",
    }

@router.get("/me", response_model=UserResponse)
def get_me(
    current_user: User = Depends(get_current_user),
):
    return current_user