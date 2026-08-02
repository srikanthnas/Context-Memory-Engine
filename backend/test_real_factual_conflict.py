from datetime import datetime, timedelta

from database.connection import SessionLocal
from database.models import Conversation, Message
from memory.memory_engine import MemoryEngine


def main():

    db = SessionLocal()
    engine = MemoryEngine()

    created_ids = []

    try:

        print("\n" + "=" * 60)
        print("PHASE 27 - REAL FACTUAL CONFLICT TEST")
        print("=" * 60)

        # -------------------------------------------------
        # Find a real conversation
        # -------------------------------------------------

        conversation = (
            db.query(Conversation)
            .order_by(Conversation.id.asc())
            .first()
        )

        assert conversation is not None, (
            "No conversation exists for testing."
        )

        print("\nUsing conversation:")
        print("ID:", conversation.id)
        print("Title:", conversation.title)

        base_time = datetime.utcnow()

        # -------------------------------------------------
        # Create temporary historical facts
        # -------------------------------------------------

        old_message = Message(
            conversation_id=conversation.id,
            role="user",
            content="My project backend uses Flask.",
            timestamp=base_time - timedelta(minutes=3),
        )

        new_message = Message(
            conversation_id=conversation.id,
            role="user",
            content=(
                "My project backend now uses FastAPI."
            ),
            timestamp=base_time - timedelta(minutes=2),
        )

        related_message = Message(
            conversation_id=conversation.id,
            role="user",
            content=(
                "My project backend handles API requests."
            ),
            timestamp=base_time - timedelta(minutes=1),
        )

        db.add_all(
            [
                old_message,
                new_message,
                related_message,
            ]
        )

        db.commit()

        db.refresh(old_message)
        db.refresh(new_message)
        db.refresh(related_message)

        created_ids = [
            old_message.id,
            new_message.id,
            related_message.id,
        ]

        print("\nTemporary SQLite messages:")
        print("-" * 60)

        for message in [
            old_message,
            new_message,
            related_message,
        ]:
            print(
                f"ID={message.id} | "
                f"{message.content}"
            )

        # -------------------------------------------------
        # Retrieve REAL SQLite messages
        # -------------------------------------------------

        database_messages = (
            db.query(Message)
            .filter(
                Message.id.in_(created_ids)
            )
            .order_by(
                Message.timestamp.asc()
            )
            .all()
        )

        message_memory = [
            {
                "id": message.id,
                "role": message.role,
                "content": message.content,
                "timestamp":
                    message.timestamp.isoformat(),
            }
            for message in database_messages
        ]

        memory = {
            "conversations": [],
            "documents": [],
            "preferences": [],
            "messages": message_memory,
        }

        print("\nACTIVE MEMORY BEFORE RESOLUTION")
        print("-" * 60)

        for message in memory["messages"]:
            print(
                f"ID={message['id']} | "
                f"{message['content']}"
            )

        # -------------------------------------------------
        # Run actual MemoryEngine conflict pipeline
        # -------------------------------------------------

        resolved = (
            engine._resolve_memory_conflicts(
                memory=memory,
            )
        )

        print("\nACTIVE MEMORY AFTER RESOLUTION")
        print("-" * 60)

        for message in resolved["messages"]:
            print(
                f"ID={message['id']} | "
                f"{message['content']}"
            )

        remaining_ids = {
            message["id"]
            for message in resolved["messages"]
        }

        # -------------------------------------------------
        # Validate active context
        # -------------------------------------------------

        assert old_message.id not in remaining_ids, (
            "Older Flask fact survived."
        )

        assert new_message.id in remaining_ids, (
            "Newer FastAPI fact was removed."
        )

        assert related_message.id in remaining_ids, (
            "Related non-conflicting message was removed."
        )

        # -------------------------------------------------
        # Validate SQLite history
        # -------------------------------------------------

        stored_messages = (
            db.query(Message)
            .filter(
                Message.id.in_(created_ids)
            )
            .all()
        )

        stored_ids = {
            message.id
            for message in stored_messages
        }

        assert stored_ids == set(created_ids), (
            "Conflict resolution modified "
            "historical SQLite data."
        )

        print("\n" + "=" * 60)
        print("VALIDATION")
        print("=" * 60)

        print(
            "\nOlder Flask fact removed "
            "from active context."
        )

        print(
            "Newer FastAPI fact preserved."
        )

        print(
            "Related message preserved."
        )

        print(
            "All historical messages still "
            "exist in SQLite."
        )

        print(
            "\nREAL FACTUAL CONFLICT TEST PASSED"
        )

    finally:

        # -------------------------------------------------
        # Clean up temporary test records
        # -------------------------------------------------

        if created_ids:

            (
                db.query(Message)
                .filter(
                    Message.id.in_(created_ids)
                )
                .delete(
                    synchronize_session=False
                )
            )

            db.commit()

            print(
                "\nTemporary SQLite test "
                "messages cleaned up."
            )

        db.close()


if __name__ == "__main__":
    main()