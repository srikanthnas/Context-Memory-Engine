from sqlalchemy.orm import Session

from database.models import Message
from schemas.message import MessageCreate


class MessageService:
    """Handles message-related business logic."""

    @staticmethod
    def create_message(
        db: Session,
        message: MessageCreate,
    ) -> Message:

        new_message = Message(
            conversation_id=message.conversation_id,
            role=message.role,
            content=message.content,
        )

        db.add(new_message)
        db.commit()
        db.refresh(new_message)

        return new_message

    @staticmethod
    def get_messages(
        db: Session,
        conversation_id: int,
    ):
        return (
            db.query(Message)
            .filter(Message.conversation_id == conversation_id)
            .order_by(Message.timestamp.asc())
            .all()
        )