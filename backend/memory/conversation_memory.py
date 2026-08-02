from sqlalchemy.orm import Session

from database.models import Conversation
from embeddings.embedding_manager import EmbeddingManager
from retrieval.chroma_vector_store import ChromaVectorStore
from services.conversation_summary_service import ConversationSummaryService


class ConversationMemory:
    """
    Retrieves semantically relevant conversations for a user
    while filtering duplicate conversation memories.
    """

    DUPLICATE_SIMILARITY_THRESHOLD = 0.92

    def __init__(self):
        self.embedding_manager = EmbeddingManager()
        self.vector_store = ChromaVectorStore()
        self.summary_service = ConversationSummaryService()

    # =====================================================
    # DUPLICATE DETECTION
    # =====================================================

    @staticmethod
    def _normalize_text(text: str) -> str:
        """
        Normalize text before duplicate comparison.
        """

        return " ".join(
            (text or "").strip().lower().split()
        )

    def _is_duplicate(
        self,
        candidate: dict,
        existing: dict,
    ) -> bool:
        """
        Determine whether two conversations represent
        the same or nearly the same memory.
        """

        candidate_title = self._normalize_text(
            candidate.get("title", "")
        )

        existing_title = self._normalize_text(
            existing.get("title", "")
        )

        candidate_summary = self._normalize_text(
            candidate.get("summary", "")
        )

        existing_summary = self._normalize_text(
            existing.get("summary", "")
        )

        # -------------------------------------------------
        # 1. Exact title + summary duplicate
        # -------------------------------------------------

        if (
            candidate_title == existing_title
            and candidate_summary == existing_summary
        ):
            return True

        # -------------------------------------------------
        # 2. Same exact title
        #
        # Repeated conversations created from the same
        # prompt should not occupy multiple memory slots.
        # -------------------------------------------------

        if (
            candidate_title
            and candidate_title == existing_title
        ):
            return True

        # -------------------------------------------------
        # 3. Semantic duplicate detection
        # -------------------------------------------------

        candidate_text = (
            f"{candidate_title} {candidate_summary}"
        ).strip()

        existing_text = (
            f"{existing_title} {existing_summary}"
        ).strip()

        if not candidate_text or not existing_text:
            return False

        candidate_embedding = (
            self.embedding_manager.embed_text(
                candidate_text
            )
        )

        existing_embedding = (
            self.embedding_manager.embed_text(
                existing_text
            )
        )

        similarity = (
            self.embedding_manager.cosine_similarity(
                candidate_embedding,
                existing_embedding,
            )
        )

        return (
            similarity
            >= self.DUPLICATE_SIMILARITY_THRESHOLD
        )

    def _remove_duplicate_conversations(
        self,
        conversations: list,
    ) -> list:
        """
        Remove exact and semantic duplicate conversations.

        The first retrieved conversation is retained as
        the representative memory.
        """

        unique_conversations = []

        for candidate in conversations:

            duplicate_found = False

            for existing in unique_conversations:

                if self._is_duplicate(
                    candidate=candidate,
                    existing=existing,
                ):
                    duplicate_found = True
                    break

            if not duplicate_found:
                unique_conversations.append(
                    candidate
                )

        return unique_conversations

    # =====================================================
    # SEMANTIC CONVERSATION RETRIEVAL
    # =====================================================

    def get_recent_conversations(
        self,
        db: Session,
        user_id: int,
        prompt: str,
        limit: int = 5,
    ):
        """
        Retrieve conversations using semantic similarity
        and filter duplicate conversation memories.
        """

        query_embedding = (
            self.embedding_manager.embed_text(
                prompt
            )
        )

        results = (
            self.vector_store.search_conversations(
                query_embedding=query_embedding,
                top_k=limit,
                where={
                    "user_id": user_id
                },
            )
        )

        conversations = []

        if (
            results["ids"]
            and len(results["ids"][0]) > 0
        ):
            metadata_list = (
                results["metadatas"][0]
            )

            for metadata in metadata_list:

                conversation = (
                    db.query(Conversation)
                    .filter(
                        Conversation.id
                        == metadata["conversation_id"],
                        Conversation.user_id
                        == user_id,
                    )
                    .first()
                )

                if conversation:

                    summary = (
                        self.summary_service
                        .get_or_refresh_summary(
                            db=db,
                            conversation_id=(
                                conversation.id
                            ),
                        )
                    )

                    conversations.append(
                        {
                            "id": conversation.id,
                            "title": (
                                conversation.title
                            ),
                            "summary": summary,
                            "created_at": (
                                conversation
                                .created_at
                                .isoformat()
                            ),
                        }
                    )

        return self._remove_duplicate_conversations(
            conversations
        )

    # =====================================================
    # LATEST CONVERSATION RETRIEVAL
    # =====================================================

    def get_latest_conversations(
        self,
        db: Session,
        user_id: int,
        limit: int = 3,
    ):
        """
        Retrieve the latest conversations and filter
        duplicate conversation memories.
        """

        conversations = (
            db.query(Conversation)
            .filter(
                Conversation.user_id == user_id
            )
            .order_by(
                Conversation.created_at.desc()
            )
            .limit(limit)
            .all()
        )

        conversation_data = []

        for conversation in conversations:

            conversation_data.append(
                {
                    "id": conversation.id,
                    "title": conversation.title,
                    "summary": (
                        conversation.summary or ""
                    ),
                    "created_at": (
                        conversation
                        .created_at
                        .isoformat()
                    ),
                }
            )

        return self._remove_duplicate_conversations(
            conversation_data
        )