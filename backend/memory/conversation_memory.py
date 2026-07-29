from sqlalchemy.orm import Session

from database.models import Conversation
from embeddings.embedding_manager import EmbeddingManager
from retrieval.chroma_vector_store import ChromaVectorStore


class ConversationMemory:
    """
    Retrieves semantically relevant conversations for a user.
    """

    def __init__(self):
        self.embedding_manager = EmbeddingManager()
        self.vector_store = ChromaVectorStore()

    def get_recent_conversations(
        self,
        db: Session,
        user_id: int,
        prompt: str,
        limit: int = 5,
    ):
        """
        Retrieve conversations using semantic similarity.
        """

        query_embedding = self.embedding_manager.embed_text(prompt)

        results = self.vector_store.search_conversations(
            query_embedding=query_embedding,
            top_k=limit,
            where={"user_id": user_id},
        )

        conversations = []

        if (
            results["ids"]
            and len(results["ids"][0]) > 0
        ):
            metadata_list = results["metadatas"][0]

            for metadata in metadata_list:

                conversation = (
                    db.query(Conversation)
                    .filter(
                        Conversation.id
                        == metadata["conversation_id"]
                    )
                    .first()
                )

                if conversation:
                    conversations.append(
                        {
                            "id": conversation.id,
                            "title": conversation.title,
                            "created_at": conversation.created_at.isoformat(),
                        }
                    )

        return conversations