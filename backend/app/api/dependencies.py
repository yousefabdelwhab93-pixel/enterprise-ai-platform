from fastapi import Depends
from sqlalchemy.orm import Session

from backend.app.core.config import Settings, settings
from backend.app.core.database import SessionLocal
from uuid import UUID

from fastapi import HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from backend.app.core.security import decode_access_token
from backend.app.models.user import User
from sqlalchemy import select
from backend.app.core.permissions import Permission
from backend.app.core.role_permissions import has_permission

def get_settings() -> Settings:
    return settings


def get_app_name(app_settings: Settings = Depends(get_settings)):
    return app_settings.APP_NAME


def get_db():
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()


security = HTTPBearer()


def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db),
):
    token = credentials.credentials

    try:
        payload = decode_access_token(token)

        user_id = UUID(payload["sub"])
        tenant_id = UUID(payload["tenant_id"])

    except (ValueError, KeyError, TypeError):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

    user = db.scalar(
        select(User).where(
            User.id == user_id,
            User.tenant_id == tenant_id,
            User.is_active.is_(True),
        )
    )

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found or inactive",
            headers={"WWW-Authenticate": "Bearer"},
        )

    return user

def require_tenant_access(
    tenant_id: UUID,
    current_user: User = Depends(get_current_user),
):
    if current_user.tenant_id != tenant_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied to this tenant",
        )

    return current_user 

def require_permission(permission: Permission):

    def permission_checker(
        current_user = Depends(get_current_user)
    ):

        if not has_permission(current_user.role, permission):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You don't have permission to perform this action"
            )

        return current_user

    return permission_checker
