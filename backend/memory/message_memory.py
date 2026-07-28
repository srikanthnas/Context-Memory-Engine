from sqlalchemy.orm import Session

from database.models import Message
from embeddings.embedding_manager import EmbeddingManager
from retrieval.chroma_vector_store import ChromaVectorStore


class MessageMemory:
    """
    Retrieves conversation messages using:
    1. Recent messages
    2. Semantic search
    """

    vector_store = ChromaVectorStore()
    embedding_manager = EmbeddingManager()

    @staticmethod
    def get_recent_messages(
        db: Session,
        conversation_id: int,
        limit: int = 10,
    ):
        messages = (
            db.query(Message)
            .filter(Message.conversation_id == conversation_id)
            .order_by(Message.timestamp.desc())
            .limit(limit)
            .all()
        )

        return [
            {
                "id": message.id,
                "role": message.role,
                "content": message.content,
                "timestamp": message.timestamp.isoformat(),
            }
            for message in reversed(messages)
        ]

    @classmethod
    def search_relevant_messages(
        cls,
        query: str,
        user_id: int,
        top_k: int = 5,
    ):
        """
        Retrieve semantically relevant messages.
        """

        query_embedding = cls.embedding_manager.model.encode(query)

        results = cls.vector_store.search_messages(
            query_embedding=query_embedding,
            top_k=top_k,
            where={
                "user_id": user_id
            },
        )

        messages = []

        if results["documents"]:

            for document, metadata, distance in zip(
                results["documents"][0],
                results["metadatas"][0],
                results["distances"][0],
            ):

                messages.append(
                    {
                        "role": metadata.get("role", "unknown"),
                        "content": document,
                        "score": 1 - distance,
                        "metadata": metadata,
                    }
                )

        return messages