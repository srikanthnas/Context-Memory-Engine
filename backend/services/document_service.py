import os
import shutil
from pathlib import Path
from retrieval.document_retriever import DocumentRetriever
from embeddings.embedding_manager import EmbeddingManager
from retrieval.chroma_vector_store import ChromaVectorStore

from fastapi import UploadFile
from sqlalchemy.orm import Session

from database.models import Document

UPLOAD_FOLDER = Path("uploads")
UPLOAD_FOLDER.mkdir(exist_ok=True)


class DocumentService:

    @staticmethod
    def upload_document(
        db: Session,
        user_id: int,
        file: UploadFile,
    ):

        file_path = UPLOAD_FOLDER / file.filename

        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        document = Document(
            user_id=user_id,
            filename=file.filename,
            filepath=str(file_path),
        )

        db.add(document)
        db.commit()
        db.refresh(document)
        try:
    # Extract and chunk the document
            chunks = DocumentRetriever.retrieve(
                filepath=document.filepath,
                chunk_size=500,
            )

            # Generate embeddings with metadata
            embedding_manager = EmbeddingManager()

            embedded_chunks = embedding_manager.embed_document_chunks(
                chunks,
                document_id=document.id,
                user_id=document.user_id,
                filename=document.filename,
            )

            # Store in ChromaDB
            vector_store = ChromaVectorStore()
            vector_store.add_documents(embedded_chunks)

            print(
                f"Indexed {len(embedded_chunks)} chunks "
                f"for {document.filename}"
            )

        except Exception as e:
            print(f"Indexing failed: {e}")

        return document