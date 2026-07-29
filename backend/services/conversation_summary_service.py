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
    """

    def __init__(self):
        self.summarizer = ConversationSummarizer()
        self.embedding_manager = EmbeddingManager()
        self.vector_store = ChromaVectorStore()

    def generate_summary(
        self,
        db: Session,
        conversation_id: int,
    ) -> str:

        conversation = (
            db.query(Conversation)
            .filter(Conversation.id == conversation_id)
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

        summary = self.summarizer.summarize(
            title=conversation.title,
            messages=message_data,
        )

        conversation.summary = summary
        conversation.summary_updated = datetime.utcnow()

        db.commit()
        db.refresh(conversation)

        embedded = self.embedding_manager.embed_conversation(
            title=conversation.title,
            summary=summary,
            conversation_id=conversation.id,
            user_id=conversation.user_id,
        )

        self.vector_store.update_conversation(embedded)

        return summary