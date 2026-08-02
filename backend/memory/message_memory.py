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
        """
        Retrieve the most recent messages from SQLite.
        """

        messages = (
            db.query(Message)
            .filter(
                Message.conversation_id == conversation_id
            )
            .order_by(
                Message.timestamp.desc()
            )
            .limit(limit)
            .all()
        )

        return [
            {
                "id": message.id,
                "conversation_id": message.conversation_id,
                "role": message.role,
                "content": message.content,
                "timestamp": message.timestamp.isoformat(),
                "importance": message.importance,
                "access_count": message.access_count,
                "last_accessed": (
                    message.last_accessed.isoformat()
                    if message.last_accessed
                    else None
                ),
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
        Retrieve semantically relevant messages
        from ChromaDB.
        """

        query_embedding = (
            cls.embedding_manager.model.encode(query)
        )

        results = cls.vector_store.search_messages(
            query_embedding=query_embedding,
            top_k=top_k,
            where={
                "user_id": user_id
            },
        )

        messages = []

        documents = results.get(
            "documents",
            [[]],
        )[0]

        metadatas = results.get(
            "metadatas",
            [[]],
        )[0]

        distances = results.get(
            "distances",
            [[]],
        )[0]

        for document, metadata, distance in zip(
            documents,
            metadatas,
            distances,
        ):

            # Message ID stored in Chroma metadata
            message_id = metadata.get("message_id")

            messages.append(
                {
                    "id": message_id,
                    "conversation_id": metadata.get(
                        "conversation_id"
                    ),
                    "role": metadata.get(
                        "role",
                        "unknown",
                    ),
                    "content": document,
                    "distance": distance,
                    "score": 1 / (1 + distance),
                    "metadata": metadata,
                }
            )

        return messages