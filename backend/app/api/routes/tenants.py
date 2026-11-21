from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from uuid import UUID

from backend.app.api.dependencies import get_db
from backend.app.models.tenant import Tenant
from backend.app.schemas.tenant import (
    TenantCreate,
    TenantUpdate,
    TenantResponse,
)


router = APIRouter(
    prefix="/tenants",
    tags=["Tenants"],
)


# =========================
# CREATE TENANT
# =========================

@router.post(
    "/",
    response_model=TenantResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_tenant(
    tenant_data: TenantCreate,
    db: Session = Depends(get_db),
):
    tenant = Tenant(
        name=tenant_data.name,
        slug=tenant_data.slug,
    )

    try:
        db.add(tenant)
        db.commit()
        db.refresh(tenant)

        return tenant

    except IntegrityError:
        db.rollback()

        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="A tenant with this slug already exists.",
        )


# =========================
# GET ALL TENANTS
# =========================

@router.get(
    "/",
    response_model=list[TenantResponse],
)
def get_all_tenants(
    include_inactive: bool = False,
    db: Session = Depends(get_db),
):
    statement = select(Tenant)

    if not include_inactive:
        statement = statement.where(
            Tenant.is_active.is_(True)
        )

    tenants = db.scalars(statement).all()

    return tenants


# =========================
# GET TENANT BY ID
# =========================

@router.get(
    "/{tenant_id}",
    response_model=TenantResponse,
)
def get_tenant_by_id(
    tenant_id: UUID,
    db: Session = Depends(get_db),
):
    statement = select(Tenant).where(
        Tenant.id == tenant_id
    )

    tenant = db.scalar(statement)

    if tenant is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Tenant not found.",
        )

    return tenant


# =========================
# UPDATE TENANT
# =========================

@router.patch(
    "/{tenant_id}",
    response_model=TenantResponse,
)
def update_tenant(
    tenant_id: UUID,
    tenant_data: TenantUpdate,
    db: Session = Depends(get_db),
):
    statement = select(Tenant).where(
        Tenant.id == tenant_id
    )

    tenant = db.scalar(statement)

    if tenant is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Tenant not found.",
        )

    update_data = tenant_data.model_dump(
        exclude_unset=True
    )

    for field, value in update_data.items():
        setattr(tenant, field, value)

    try:
        db.commit()
        db.refresh(tenant)

        return tenant

    except IntegrityError:
        db.rollback()

        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Update conflicts with existing data.",
        )


# =========================
# DELETE TENANT (SOFT DELETE)
# =========================

@router.delete(
    "/{tenant_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_tenant(
    tenant_id: UUID,
    db: Session = Depends(get_db),
):
    statement = select(Tenant).where(
        Tenant.id == tenant_id
    )

    tenant = db.scalar(statement)

    if tenant is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Tenant not found.",
        )

    tenant.is_active = False

    db.commit()

    return None