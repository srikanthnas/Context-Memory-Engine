from sqlalchemy.orm import Session

from database.models import Message


class MessageMemory:
    """
    Retrieves recent messages from a conversation.
    """

    @staticmethod
    def get_recent_messages(
        db: Session,
        conversation_id: int,
        limit: int = 10,
    ):
        messages = (
            db.query(Message)
            .filter(Message.conversation_id == conversation_id)
            .order_by(Message.timestamp.desc())
            .limit(limit)
            .all()
        )

        return [
            {
                "id": message.id,
                "role": message.role,
                "content": message.content,
                "timestamp": message.timestamp.isoformat(),
            }
            for message in reversed(messages)
        ]