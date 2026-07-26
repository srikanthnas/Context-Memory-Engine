from sqlalchemy.orm import Session

from database.models import Conversation


class ConversationMemory:
    """
    Retrieves previous conversations for a user.
    """

    @staticmethod
    def get_recent_conversations(
        db: Session,
        user_id: int,
        limit: int = 5,
    ):
        conversations = (
            db.query(Conversation)
            .filter(Conversation.user_id == user_id)
            .order_by(Conversation.created_at.desc())
            .limit(limit)
            .all()
        )

        return [
            {
                "id": conversation.id,
                "title": conversation.title,
                "created_at": conversation.created_at.isoformat(),
            }
            for conversation in conversations
        ]