"""
Conversation Memory

Responsible for retrieving conversation history
from the database.
"""

from sqlalchemy.orm import Session

from database.models import Conversation


class ConversationMemory:
    """Conversation retrieval service."""

    def get_recent_conversations(
        self,
        db: Session,
        user_id: int,
        limit: int = 5,
    ):
        """
        Return the most recent conversations
        for the given user.
        """

        conversations = (
            db.query(Conversation)
            .filter(Conversation.user_id == user_id)
            .order_by(Conversation.created_at.desc())
            .limit(limit)
            .all()
        )

        return [
            {
                "conversation_id": conversation.id,
                "title": conversation.title,
                "created_at": conversation.created_at.isoformat(),
            }
            for conversation in conversations
        ]