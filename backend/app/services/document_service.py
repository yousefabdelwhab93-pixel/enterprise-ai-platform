from uuid import UUID

from sqlalchemy.orm import Session

from backend.app.models.document import Document
from backend.app.repositories.document_repository import DocumentRepository
from backend.app.schemas.document import DocumentCreate, DocumentUpdate


class DocumentService:

    @staticmethod
    def create_document(
        db: Session,
        document_data: DocumentCreate,
        tenant_id: UUID,
        uploaded_by: UUID,
        storage_path: str,
    ) -> Document:

        document = Document(
            tenant_id=tenant_id,
            uploaded_by=uploaded_by,
            filename=document_data.filename,
            file_type=document_data.file_type,
            file_size=document_data.file_size,
            storage_path=storage_path,
        )

        return DocumentRepository.create(db, document)

    @staticmethod
    def get_document(
        db: Session,
        document_id: UUID,
        tenant_id: UUID,
    ) -> Document | None:

        return DocumentRepository.get_by_id(
            db=db,
            document_id=document_id,
            tenant_id=tenant_id,
        )

    @staticmethod
    def get_all_documents(
        db: Session,
        tenant_id: UUID,
    ) -> list[Document]:

        return DocumentRepository.get_all(
            db=db,
            tenant_id=tenant_id,
        )

    @staticmethod
    def update_document(
        db: Session,
        document_id: UUID,
        tenant_id: UUID,
        document_data: DocumentUpdate,
    ) -> Document | None:

        document = DocumentRepository.get_by_id(
            db=db,
            document_id=document_id,
            tenant_id=tenant_id,
        )

        if document is None:
            return None

        update_data = document_data.model_dump(exclude_unset=True)

        for field, value in update_data.items():
            setattr(document, field, value)

        return DocumentRepository.update(db, document)

    @staticmethod
    def delete_document(
        db: Session,
        document_id: UUID,
        tenant_id: UUID,
    ) -> bool:

        document = DocumentRepository.get_by_id(
            db=db,
            document_id=document_id,
            tenant_id=tenant_id,
        )

        if document is None:
            return False

        DocumentRepository.delete(db, document)

        return True