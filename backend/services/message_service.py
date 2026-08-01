from sqlalchemy.orm import Session

from database.models import Conversation, Message
from schemas.message import MessageCreate

from embeddings.embedding_manager import EmbeddingManager
from retrieval.chroma_vector_store import ChromaVectorStore


class MessageService:
    """
    Handles message-related business logic.
    """

    embedding_manager = EmbeddingManager()
    vector_store = ChromaVectorStore()

    @staticmethod
    def create_message(
        db: Session,
        message: MessageCreate,
    ) -> Message:

        # ---------------------------------------
        # Save message in SQLite
        # ---------------------------------------

        new_message = Message(
            conversation_id=message.conversation_id,
            role=message.role,
            content=message.content,
        )

        db.add(new_message)
        db.commit()
        db.refresh(new_message)

        # ---------------------------------------
        # Find conversation owner
        # ---------------------------------------

        conversation = (
            db.query(Conversation)
            .filter(
                Conversation.id == message.conversation_id
            )
            .first()
        )

        if conversation:

            embedded_message = (
                MessageService.embedding_manager.embed_message(
                    message=message.content,
                    conversation_id=message.conversation_id,
                    user_id=conversation.user_id,
                    role=message.role,
                    message_id=new_message.id,
                )
            )

            MessageService.vector_store.add_messages(
                [embedded_message]
            )

        return new_message

    @staticmethod
    def get_messages(
        db: Session,
        conversation_id: int,
    ):
        return (
            db.query(Message)
            .filter(
                Message.conversation_id == conversation_id
            )
            .order_by(Message.timestamp.asc())
            .all()
        )