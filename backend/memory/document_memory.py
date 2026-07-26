"""
Document Memory

Retrieves document memory for a user.
"""

from sqlalchemy.orm import Session

from database.models import Document
from retrieval.document_retriever import DocumentRetriever


class DocumentMemory:
    """
    Retrieves document memory for a user.
    """

    @staticmethod
    def get_documents(
        db: Session,
        user_id: int,
        chunk_size: int = 500,
    ):
        documents = (
            db.query(Document)
            .filter(Document.user_id == user_id)
            .all()
        )

        results = []

        for document in documents:
            try:
                chunks = DocumentRetriever.retrieve(
                    filepath=document.filepath,
                    chunk_size=chunk_size,
                )

                results.append(
                    {
                        "id": document.id,
                        "filename": document.filename,
                        "filepath": document.filepath,
                        "chunks": chunks,
                    }
                )

            except Exception:
                # Skip unreadable or unsupported documents
                continue

        return results