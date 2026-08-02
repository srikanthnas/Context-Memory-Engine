from typing import Optional

from sqlalchemy.orm import Session

from database.models import Conversation
from schemas.conversation import ConversationCreate

from embeddings.embedding_manager import EmbeddingManager
from retrieval.chroma_vector_store import ChromaVectorStore


class ConversationService:
    """
    Handles conversation-related business logic.

    Also prevents unnecessary duplicate conversations
    from being created for highly similar prompts.
    """

    DUPLICATE_THRESHOLD = 0.72

    def __init__(self):
        self.embedding_manager = EmbeddingManager()
        self.vector_store = ChromaVectorStore()

    # =====================================================
    # FIND DUPLICATE CONVERSATION
    # =====================================================

    def find_duplicate_conversation(
        self,
        db: Session,
        user_id: int,
        title: str,
        threshold: float = None,
    ) -> Optional[Conversation]:
        """
        Search existing conversation memory for a conversation
        that is semantically very similar to the new title.

        Returns the matching Conversation if similarity is above
        the threshold. Otherwise returns None.
        """

        if threshold is None:
            threshold = self.DUPLICATE_THRESHOLD

        query_embedding = self.embedding_manager.embed_text(title)

        results = self.vector_store.search_conversations(
            query_embedding=query_embedding,
            top_k=5,
            where={
                "user_id": user_id,
            },
        )

        if not results:
            return None

        ids = results.get("ids", [])
        metadatas = results.get("metadatas", [])
        distances = results.get("distances", [])

        if not ids or not ids[0]:
            return None

        metadata_list = (
            metadatas[0]
            if metadatas
            else []
        )

        distance_list = (
            distances[0]
            if distances
            else []
        )

        for metadata, distance in zip(
            metadata_list,
            distance_list,
        ):

            # Chroma collection uses squared L2 distance.
            # SentenceTransformer embeddings are normalized/behave such that:
            #
            # squared_l2 = 2 * (1 - cosine_similarity)
            #
            # Therefore:
            # cosine_similarity = 1 - (distance / 2)

            similarity = 1 - (distance / 2)

            if similarity < threshold:
                continue

            conversation_id = metadata.get(
                "conversation_id"
            )

            if conversation_id is None:
                continue

            conversation = (
                db.query(Conversation)
                .filter(
                    Conversation.id == conversation_id,
                    Conversation.user_id == user_id,
                )
                .first()
            )

            if conversation:
                return conversation

        return None

    # =====================================================
    # CREATE CONVERSATION
    # =====================================================

    def create_conversation(
        self,
        db: Session,
        conversation: ConversationCreate,
    ) -> Conversation:
        """
        Create a conversation.

        Before creating a new conversation, check whether
        a highly similar conversation already exists.
        """

        duplicate = self.find_duplicate_conversation(
            db=db,
            user_id=conversation.user_id,
            title=conversation.title,
        )

        if duplicate:
            return duplicate

        new_conversation = Conversation(
            user_id=conversation.user_id,
            title=conversation.title,
        )

        db.add(new_conversation)
        db.commit()
        db.refresh(new_conversation)

        # ==========================================
        # Store Conversation Embedding
        # ==========================================

        embedded_conversation = (
            self.embedding_manager.embed_conversation(
                title=new_conversation.title,
                summary="",
                conversation_id=new_conversation.id,
                user_id=new_conversation.user_id,
            )
        )

        self.vector_store.add_conversations(
            [embedded_conversation]
        )

        return new_conversation

    # =====================================================
    # GET CONVERSATION
    # =====================================================

    @staticmethod
    def get_conversation(
        db: Session,
        conversation_id: int,
    ) -> Optional[Conversation]:

        return (
            db.query(Conversation)
            .filter(
                Conversation.id == conversation_id
            )
            .first()
        )

    # =====================================================
    # GET USER CONVERSATIONS
    # =====================================================

    @staticmethod
    def get_user_conversations(
        db: Session,
        user_id: int,
    ):

        return (
            db.query(Conversation)
            .filter(
                Conversation.user_id == user_id
            )
            .order_by(
                Conversation.created_at.desc()
            )
            .all()
        )

    # =====================================================
    # GET LATEST CONVERSATION
    # =====================================================

    @staticmethod
    def get_latest_conversation(
        db: Session,
        user_id: int,
    ) -> Optional[Conversation]:

        return (
            db.query(Conversation)
            .filter(
                Conversation.user_id == user_id
            )
            .order_by(
                Conversation.created_at.desc()
            )
            .first()
        )

    # =====================================================
    # GET ALL CONVERSATIONS
    # =====================================================

    @staticmethod
    def get_all_conversations(
        db: Session,
    ):

        return (
            db.query(Conversation)
            .order_by(
                Conversation.created_at.desc()
            )
            .all()
        )