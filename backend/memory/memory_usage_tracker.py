"""
Memory Usage Tracker

Tracks memories that are actually selected and used
in the final LLM context.
"""

from datetime import datetime

from sqlalchemy.orm import Session

from database.models import (
    Conversation,
    Document,
    Message,
    Preference,
)


class MemoryUsageTracker:
    """
    Updates adaptive-memory metadata for memories
    selected for the final LLM context.
    """

    IMPORTANCE_INCREMENT = 0.05
    MAX_IMPORTANCE = 5.0

    @classmethod
    def track(
        cls,
        db: Session,
        selected_memory: list,
    ):
        """
        Record usage of selected memories.

        Each unique database memory is updated only once
        during a single prompt.
        """

        touched = set()

        for memory in selected_memory:

            memory_type = memory.get("memory_type")

            model = None
            memory_id = None

            if memory_type == "document":
                model = Document
                memory_id = memory.get("document_id")

            elif memory_type == "conversation":
                model = Conversation
                memory_id = memory.get("id")

            elif memory_type == "message":
                model = Message
                memory_id = memory.get("id")

            elif memory_type == "preference":
                model = Preference
                memory_id = memory.get("id")

            if model is None or memory_id is None:
                continue

            # Prevent the same memory from being counted
            # multiple times during one prompt.
            key = (
                memory_type,
                memory_id,
            )

            if key in touched:
                continue

            database_memory = (
                db.query(model)
                .filter(model.id == memory_id)
                .first()
            )

            if database_memory is None:
                continue

            database_memory.last_accessed = datetime.utcnow()

            database_memory.access_count += 1

            database_memory.importance = min(
                database_memory.importance
                + cls.IMPORTANCE_INCREMENT,
                cls.MAX_IMPORTANCE,
            )

            touched.add(key)

        db.commit()