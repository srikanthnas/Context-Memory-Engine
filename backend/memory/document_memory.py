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

        # Generate embedding for the user's query
        query_embedding = embedding_manager.embed_text(query)

        # Search document chunks belonging only to this user
        results = vector_store.search(
            query_embedding=query_embedding,
            top_k=top_k,
            where={"user_id": user_id},
        )

        documents = results.get("documents", [[]])[0]
        metadatas = results.get("metadatas", [[]])[0]

        relevant_chunks = []

        # Keeps track of documents already updated during
        # this retrieval request.
       

        for text, metadata in zip(documents, metadatas):

            document = (
                db.query(Document)
                .filter(
                    Document.id == metadata["document_id"],
                    Document.user_id == user_id,
                )
                .first()
            )

            if not document:
                continue

            metadata = MemoryMetadata.touch(metadata)

            # Update adaptive-memory information only once
            # per unique document, not once per chunk.
           

            relevant_chunks.append(
                {
                    "document_id": document.id,
                    "filename": document.filename,
                    "chunk": text,
                    "metadata": metadata,
                    "importance": document.importance,
                    "access_count": document.access_count,
                    "last_accessed": (
                        document.last_accessed.isoformat()
                        if document.last_accessed
                        else None
                    ),
                }
            )

        return relevant_chunks