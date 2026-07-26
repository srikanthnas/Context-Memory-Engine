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
        print(f"Found {len(documents)} document(s) for user {user_id}")

        for doc in documents:
            print(
                f"id={doc.id}, "
                f"user_id={doc.user_id}, "
                f"filename={doc.filename}, "
                f"filepath={doc.filepath}"
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

            except Exception as e:
                print(f"Error processing {document.filename}: {e}")
                raise

        return results