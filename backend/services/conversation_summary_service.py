from datetime import datetime

from sqlalchemy.orm import Session

from database.models import Conversation
from embeddings.embedding_manager import EmbeddingManager
from memory.conversation_summarizer import ConversationSummarizer
from retrieval.chroma_vector_store import ChromaVectorStore
from services.message_service import MessageService


class ConversationSummaryService:
    """
    Generates, stores and updates conversation summaries.

    If LLM-based summary generation is unavailable,
    a deterministic fallback summary is generated so
    the memory pipeline can continue operating.
    """

    def __init__(self):
        self.summarizer = ConversationSummarizer()
        self.embedding_manager = EmbeddingManager()
        self.vector_store = ChromaVectorStore()

    def is_summary_stale(
        self,
        db: Session,
        conversation_id: int,
    ) -> bool:
        """
        Check whether the conversation summary needs
        to be generated or refreshed.

        A summary is stale when:
        1. No summary exists.
        2. No summary timestamp exists.
        3. A newer message exists after the summary.
        """

        conversation = (
            db.query(Conversation)
            .filter(
                Conversation.id == conversation_id
            )
            .first()
        )

        if conversation is None:
            raise ValueError("Conversation not found.")

        if not conversation.summary:
            return True

        if conversation.summary_updated is None:
            return True

        messages = MessageService.get_messages(
            db=db,
            conversation_id=conversation_id,
        )

        if not messages:
            return False

        latest_message = messages[-1]

        return (
            latest_message.timestamp
            > conversation.summary_updated
        )

    def get_or_refresh_summary(
        self,
        db: Session,
        conversation_id: int,
    ) -> str:
        """
        Return the existing summary when it is fresh.

        If the summary is missing or stale,
        regenerate and persist it.
        """

        conversation = (
            db.query(Conversation)
            .filter(
                Conversation.id == conversation_id
            )
            .first()
        )

        if conversation is None:
            raise ValueError("Conversation not found.")

        if self.is_summary_stale(
            db=db,
            conversation_id=conversation_id,
        ):
            return self.generate_summary(
                db=db,
                conversation_id=conversation_id,
            )

        return conversation.summary

    def _build_fallback_summary(
        self,
        conversation: Conversation,
        messages: list,
    ) -> str:
        """
        Generate a lightweight deterministic summary
        when the LLM summarizer is unavailable.

        This prevents Gemini quota/rate-limit failures
        from breaking the memory pipeline.
        """

        user_messages = [
            message.content.strip()
            for message in messages
            if (
                message.role == "user"
                and message.content
                and message.content.strip()
            )
        ]

        if user_messages:
            # Keep the fallback concise while still
            # representing the actual conversation.
            latest_user_messages = user_messages[-3:]

            combined = " ".join(
                latest_user_messages
            )

            # Prevent extremely large fallback summaries.
            max_length = 1000

            if len(combined) > max_length:
                combined = (
                    combined[:max_length].rstrip()
                    + "..."
                )

            return combined

        # Final fallback if no user message exists.
        return conversation.title

    def generate_summary(
        self,
        db: Session,
        conversation_id: int,
    ) -> str:
        """
        Generate and persist a conversation summary.

        Primary path:
            LLM-generated summary.

        Fallback path:
            Deterministic summary generated from
            conversation messages.

        Both paths persist the summary in SQLite and
        update the conversation embedding in ChromaDB.
        """

        conversation = (
            db.query(Conversation)
            .filter(
                Conversation.id == conversation_id
            )
            .first()
        )

        if conversation is None:
            raise ValueError("Conversation not found.")

        messages = MessageService.get_messages(
            db=db,
            conversation_id=conversation_id,
        )

        if not messages:
            return ""

        message_data = [
            {
                "role": message.role,
                "content": message.content,
            }
            for message in messages
        ]

        # ==================================================
        # Attempt normal LLM summarization
        # ==================================================

        try:

            summary = self.summarizer.summarize(
                title=conversation.title,
                messages=message_data,
            )

            if not summary or not summary.strip():
                raise ValueError(
                    "LLM returned an empty summary."
                )

            summary = summary.strip()

        except Exception as error:

            print(
                "\nWARNING: LLM summary generation failed."
            )

            print(
                "Using deterministic fallback summary."
            )

            print(
                f"Reason: {type(error).__name__}: {error}"
            )

            summary = self._build_fallback_summary(
                conversation=conversation,
                messages=messages,
            )

        # ==================================================
        # Persist summary in SQLite
        # ==================================================

        conversation.summary = summary

        conversation.summary_updated = (
            datetime.utcnow()
        )

        db.commit()
        db.refresh(conversation)

        # ==================================================
        # Update conversation embedding in ChromaDB
        # ==================================================

        embedded = (
            self.embedding_manager.embed_conversation(
                title=conversation.title,
                summary=summary,
                conversation_id=conversation.id,
                user_id=conversation.user_id,
            )
        )

        self.vector_store.update_conversation(
            embedded
        )

        return summary