from uuid import UUID, uuid4

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from backend.app.api.dependencies import (
    get_db,
    get_current_user,
    require_permission,
)
from backend.app.core.permissions import Permission
from backend.app.models.user import User
from backend.app.schemas.document import (
    DocumentCreate,
    DocumentUpdate,
    DocumentResponse,
)
from backend.app.services.document_service import DocumentService


router = APIRouter(
    prefix="/documents",
    tags=["Documents"],
)


# =========================
# CREATE DOCUMENT
# =========================

@router.post(
    "/",
    response_model=DocumentResponse,
    status_code=status.HTTP_201_CREATED,
    dependencies=[
        Depends(require_permission(Permission.DOCUMENTS_CREATE))
    ],
)
def create_document(
    document_data: DocumentCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    # Generate a unique temporary storage path
    unique_id = uuid4()

    storage_path = (
        f"pending/{current_user.tenant_id}/{unique_id}/"
        f"{document_data.filename}"
    )

    document = DocumentService.create_document(
        db=db,
        document_data=document_data,
        tenant_id=current_user.tenant_id,
        uploaded_by=current_user.id,
        storage_path=storage_path,
    )

    return document


# =========================
# GET ALL DOCUMENTS
# =========================

@router.get(
    "/",
    response_model=list[DocumentResponse],
    dependencies=[
        Depends(require_permission(Permission.DOCUMENTS_READ))
    ],
)
def get_all_documents(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    documents = DocumentService.get_all_documents(
        db=db,
        tenant_id=current_user.tenant_id,
    )

    return documents


# =========================
# GET DOCUMENT BY ID
# =========================

@router.get(
    "/{document_id}",
    response_model=DocumentResponse,
    dependencies=[
        Depends(require_permission(Permission.DOCUMENTS_READ))
    ],
)
def get_document_by_id(
    document_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    document = DocumentService.get_document(
        db=db,
        document_id=document_id,
        tenant_id=current_user.tenant_id,
    )

    if document is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Document not found.",
        )

    return document


# =========================
# UPDATE DOCUMENT
# =========================

@router.patch(
    "/{document_id}",
    response_model=DocumentResponse,
    dependencies=[
        Depends(require_permission(Permission.DOCUMENTS_UPDATE))
    ],
)
def update_document(
    document_id: UUID,
    document_data: DocumentUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    document = DocumentService.update_document(
        db=db,
        document_id=document_id,
        tenant_id=current_user.tenant_id,
        document_data=document_data,
    )

    if document is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Document not found.",
        )

    return document


# =========================
# DELETE DOCUMENT
# =========================

@router.delete(
    "/{document_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[
        Depends(require_permission(Permission.DOCUMENTS_DELETE))
    ],
)
def delete_document(
    document_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    deleted = DocumentService.delete_document(
        db=db,
        document_id=document_id,
        tenant_id=current_user.tenant_id,
    )

    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Document not found.",
        )

    return None