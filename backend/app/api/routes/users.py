from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from uuid import UUID
from backend.app.schemas.user import UserCreate, UserResponse, UserUpdate

from backend.app.api.dependencies import get_db
from backend.app.core.security import hash_password
from backend.app.models.tenant import Tenant
from backend.app.models.user import User
from backend.app.schemas.user import UserCreate, UserResponse


router = APIRouter(
    prefix="/users",
    tags=["Users"],
)


@router.post(
    "/",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_user(
    user_data: UserCreate,
    db: Session = Depends(get_db),
):
    # Check if tenant exists and is active
    tenant_statement = select(Tenant).where(
        Tenant.id == user_data.tenant_id,
        Tenant.is_active.is_(True),
    )

    tenant = db.scalar(tenant_statement)

    if tenant is None:
        raise HTTPException(
            status_code=404,
            detail="Active tenant not found.",
        )

    # Hash the password
    hashed_password = hash_password(user_data.password)

    # Create user
    new_user = User(
        tenant_id=user_data.tenant_id,
        full_name=user_data.full_name,
        email=user_data.email.strip().lower(),
        password_hash=hashed_password,
    )

    # Save to database
    db.add(new_user)

    try:
        db.commit()
        db.refresh(new_user)

        return new_user

    except IntegrityError:
        db.rollback()

        raise HTTPException(
            status_code=409,
            detail="User with this email already exists in this tenant.",
        )


@router.get(
    "/",
    response_model=list[UserResponse],
)
def get_all_users(
    tenant_id: UUID,
    include_inactive: bool = False,
    db: Session = Depends(get_db),
):
    # Check if tenant exists and is active
    tenant_statement = select(Tenant).where(
        Tenant.id == tenant_id,
        Tenant.is_active.is_(True),
    )

    tenant = db.scalar(tenant_statement)

    if tenant is None:
        raise HTTPException(
            status_code=404,
            detail="Active tenant not found.",
        )

    # Get users belonging to this tenant
    statement = select(User).where(
        User.tenant_id == tenant_id
    )

    # Return active users only by default
    if not include_inactive:
        statement = statement.where(
            User.is_active.is_(True)
        )

    users = db.scalars(statement).all()

    return users

@router.get("/{user_id}", response_model=UserResponse)
def get_user_by_id(
    user_id: UUID,
    tenant_id: UUID,
    db: Session = Depends(get_db),
):
    statement = select(User).where(
        User.id == user_id,
        User.tenant_id == tenant_id,
        User.is_active.is_(True),
    )

    user = db.scalar(statement)

    if user is None:
        raise HTTPException(
            status_code=404,
            detail="User not found.",
        )

    return user


@router.patch("/{user_id}", response_model=UserResponse)
def update_user(
    user_id: UUID,
    tenant_id: UUID,
    user_data: UserUpdate,
    db: Session = Depends(get_db),
):
    statement = select(User).where(
        User.id == user_id,
        User.tenant_id == tenant_id,
        User.is_active.is_(True),
    )

    user = db.scalar(statement)

    if user is None:
        raise HTTPException(
            status_code=404,
            detail="User not found.",
        )

    update_data = user_data.model_dump(exclude_unset=True)

    if "email" in update_data:
        update_data["email"] = update_data["email"].strip().lower()

    for field, value in update_data.items():
        setattr(user, field, value)

    try:
        db.commit()
        db.refresh(user)
        return user

    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=409,
            detail="User with this email already exists in this tenant.",
        )


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(
    user_id: UUID,
    tenant_id: UUID,
    db: Session = Depends(get_db),
):
    statement = select(User).where(
        User.id == user_id,
        User.tenant_id == tenant_id,
        User.is_active.is_(True),
    )

    user = db.scalar(statement)

    if user is None:
        raise HTTPException(
            status_code=404,
            detail="User not found.",
        )

    user.is_active = False

    db.commit()

    return None