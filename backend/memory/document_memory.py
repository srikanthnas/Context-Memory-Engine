"""
Document Memory

Retrieves the most relevant document chunks for a user.
"""

from sqlalchemy.orm import Session

from database.models import Document
from embeddings.embedding_manager import EmbeddingManager
from retrieval.chroma_vector_store import ChromaVectorStore
from memory.memory_metadata import MemoryMetadata


class DocumentMemory:
    """
    Retrieves semantically relevant document chunks for a user.
    """

    @staticmethod
    def get_documents(
        db: Session,
        user_id: int,
        query: str,
        top_k: int = 3,
    ):
        embedding_manager = EmbeddingManager()
        vector_store = ChromaVectorStore()

        query_embedding = embedding_manager.embed_text(query)

        results = vector_store.search(
            query_embedding=query_embedding,
            top_k=top_k,
            where={"user_id": user_id},
        )

        documents = results.get("documents", [[]])[0]
        metadatas = results.get("metadatas", [[]])[0]

        relevant_chunks = []

        for text, metadata in zip(documents, metadatas):
            document = (
                db.query(Document)
                .filter(
                    Document.id == metadata["document_id"],
                    Document.user_id == user_id,
                )
                .first()
            )

            if document:
                metadata = MemoryMetadata.touch(metadata)

                relevant_chunks.append(
                    {
                        "document_id": document.id,
                        "filename": document.filename,
                        "chunk": text,
                        "metadata": metadata,
                    }
                )

        return relevant_chunks