from sqlalchemy.orm import Session

from database.models import Conversation
from schemas.conversation import ConversationCreate


class ConversationService:
    """Handles conversation-related business logic."""

    @staticmethod
    def create_conversation(
        db: Session,
        conversation: ConversationCreate,
    ) -> Conversation:

        new_conversation = Conversation(
            user_id=conversation.user_id,
            title=conversation.title,
        )

        db.add(new_conversation)
        db.commit()
        db.refresh(new_conversation)

        return new_conversation

    @staticmethod
    def get_all_conversations(db: Session):
        return (
            db.query(Conversation)
            .order_by(Conversation.created_at.desc())
            .all()
        )