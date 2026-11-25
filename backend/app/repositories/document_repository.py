from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import Session

from backend.app.models.document import Document


class DocumentRepository:

    @staticmethod
    def create(
        db: Session,
        document: Document,
    ) -> Document:
        try:
            db.add(document)
            db.commit()
            db.refresh(document)

            return document

        except Exception:
            db.rollback()
            raise

    @staticmethod
    def get_by_id(
        db: Session,
        document_id: UUID,
        tenant_id: UUID,
    ) -> Document | None:

        statement = select(Document).where(
            Document.id == document_id,
            Document.tenant_id == tenant_id,
        )

        return db.scalar(statement)

    @staticmethod
    def get_all(
        db: Session,
        tenant_id: UUID,
    ) -> list[Document]:

        statement = (
            select(Document)
            .where(Document.tenant_id == tenant_id)
            .order_by(Document.created_at.desc())
        )

        return list(db.scalars(statement).all())

    @staticmethod
    def update(
        db: Session,
        document: Document,
    ) -> Document:
        try:
            db.commit()
            db.refresh(document)

            return document

        except Exception:
            db.rollback()
            raise

    @staticmethod
    def delete(
        db: Session,
        document: Document,
    ) -> None:
        try:
            db.delete(document)
            db.commit()

        except Exception:
            db.rollback()
            raise