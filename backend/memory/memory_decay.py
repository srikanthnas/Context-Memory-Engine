"""
Memory Decay

Gradually reduces the importance of memories
that have not been accessed for a long time.

Memories are never deleted by this component.
"""

from datetime import datetime, timedelta

from sqlalchemy.orm import Session

from database.models import (
    Conversation,
    Document,
    Message,
    Preference,
)


class MemoryDecay:
    """
    Applies controlled importance decay to inactive memories.
    """

    MIN_IMPORTANCE = 1.0

    DECAY_AMOUNT = 0.05

    DECAY_AFTER_DAYS = 7

    @classmethod
    def apply_decay(
        cls,
        db: Session,
    ):
        """
        Apply decay to memories that have not been
        accessed within the configured time period.
        """

        cutoff = datetime.utcnow() - timedelta(
            days=cls.DECAY_AFTER_DAYS
        )

        models = [
            Document,
            Conversation,
            Message,
            Preference,
        ]

        total_decayed = 0

        for model in models:

            memories = (
                db.query(model)
                .filter(
                    model.last_accessed < cutoff,
                    model.importance > cls.MIN_IMPORTANCE,
                )
                .all()
            )

            for memory in memories:

                memory.importance = max(
                    cls.MIN_IMPORTANCE,
                    memory.importance - cls.DECAY_AMOUNT,
                )

                total_decayed += 1

        db.commit()

        return total_decayed