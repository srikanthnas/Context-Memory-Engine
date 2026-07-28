from typing import Optional

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
    def get_conversation(
        db: Session,
        conversation_id: int,
    ) -> Optional[Conversation]:

        return (
            db.query(Conversation)
            .filter(Conversation.id == conversation_id)
            .first()
        )

    @staticmethod
    def get_user_conversations(
        db: Session,
        user_id: int,
    ):

        return (
            db.query(Conversation)
            .filter(Conversation.user_id == user_id)
            .order_by(Conversation.created_at.desc())
            .all()
        )

    @staticmethod
    def get_latest_conversation(
        db: Session,
        user_id: int,
    ) -> Optional[Conversation]:

        return (
            db.query(Conversation)
            .filter(Conversation.user_id == user_id)
            .order_by(Conversation.created_at.desc())
            .first()
        )

    @staticmethod
    def get_all_conversations(
        db: Session,
    ):

        return (
            db.query(Conversation)
            .order_by(Conversation.created_at.desc())
            .all()
        )