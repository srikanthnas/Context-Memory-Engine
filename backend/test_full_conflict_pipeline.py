from database.connection import SessionLocal
from database.models import Conversation, Message
from schemas.message import MessageCreate

from services.message_service import MessageService
from memory.memory_engine import MemoryEngine
from retrieval.chroma_vector_store import ChromaVectorStore


def main():

    db = SessionLocal()

    message_service = MessageService()
    memory_engine = MemoryEngine()
    vector_store = ChromaVectorStore()

    created_ids = []

    try:

        print("\n" + "=" * 60)
        print("PHASE 27 - FULL MEMORY ENGINE CONFLICT TEST")
        print("=" * 60)

        # =================================================
        # FIND TEST CONVERSATION
        # =================================================

        conversation = (
            db.query(Conversation)
            .filter(
                Conversation.user_id == 2
            )
            .order_by(
                Conversation.id.asc()
            )
            .first()
        )

        assert conversation is not None, (
            "No conversation found for user 2."
        )

        user_id = conversation.user_id

        print("\nConversation:")
        print("ID:", conversation.id)
        print("Title:", conversation.title)

        # =================================================
        # CREATE CONFLICTING MEMORIES
        # =================================================

        test_contents = [
            "My project backend uses Flask.",
            "My project backend now uses FastAPI.",
            "My project backend handles API requests.",
        ]

        print("\nCREATING TEST MEMORIES")
        print("-" * 60)

        for content in test_contents:

            message = message_service.create_message(
                db=db,
                message=MessageCreate(
                    conversation_id=conversation.id,
                    role="user",
                    content=content,
                ),
            )

            created_ids.append(message.id)

            print(
                f"ID={message.id} | "
                f"{message.content}"
            )

        old_id = created_ids[0]
        new_id = created_ids[1]
        related_id = created_ids[2]

        # =================================================
        # RUN COMPLETE MEMORY ENGINE
        # =================================================

        query = (
            "What backend technology "
            "does my project use?"
        )

        print("\nQUERY")
        print("-" * 60)
        print(query)

        result = memory_engine.process_prompt(
            db=db,
            user_id=user_id,
            prompt=query,
        )

        # =================================================
        # RAW RETRIEVED MEMORY
        # =================================================

        retrieved_messages = result[
            "message_memory"
        ]

        retrieved_test_messages = [
            message
            for message in retrieved_messages
            if message.get("id") in created_ids
        ]

        print("\nRAW RETRIEVED TEST MEMORY")
        print("-" * 60)

        for message in retrieved_test_messages:

            print(
                f"ID={message.get('id')} | "
                f"{message.get('content')}"
            )

        retrieved_ids = {
            message.get("id")
            for message in retrieved_test_messages
        }

        assert old_id in retrieved_ids, (
            "Older Flask fact was not retrieved."
        )

        assert new_id in retrieved_ids, (
            "Newer FastAPI fact was not retrieved."
        )

        # =================================================
        # RESOLVED MEMORY
        # =================================================

        resolved_messages = result[
            "resolved_memory"
        ][
            "messages"
        ]

        resolved_test_messages = [
            message
            for message in resolved_messages
            if message.get("id") in created_ids
        ]

        print("\nRESOLVED TEST MEMORY")
        print("-" * 60)

        for message in resolved_test_messages:

            print(
                f"ID={message.get('id')} | "
                f"{message.get('content')}"
            )

        resolved_ids = {
            message.get("id")
            for message in resolved_test_messages
        }

        assert old_id not in resolved_ids, (
            "Older Flask fact survived "
            "conflict resolution."
        )

        assert new_id in resolved_ids, (
            "Newer FastAPI fact was removed."
        )

        if related_id in retrieved_ids:

            assert related_id in resolved_ids, (
                "Related API memory was "
                "incorrectly removed."
            )

        # =================================================
        # OPTIMIZED MEMORY
        # =================================================

        optimized_messages = result[
            "optimized_memory"
        ][
            "messages"
        ]

        optimized_test_messages = [
            message
            for message in optimized_messages
            if message.get("id") in created_ids
        ]

        print("\nOPTIMIZED TEST MEMORY")
        print("-" * 60)

        for message in optimized_test_messages:

            print(
                f"ID={message.get('id')} | "
                f"{message.get('content')}"
            )

        optimized_ids = {
            message.get("id")
            for message in optimized_test_messages
        }

        assert old_id not in optimized_ids, (
            "Old Flask fact reappeared "
            "during optimization."
        )

        # =================================================
        # FINAL CONTEXT
        # =================================================

        context = result["context"]

        print("\nFINAL CONTEXT")
        print("-" * 60)
        print(context)

        assert (
            "My project backend uses Flask."
            not in context
        ), (
            "Outdated Flask fact leaked "
            "into final LLM context."
        )

        assert (
            "My project backend now uses FastAPI."
            in context
        ), (
            "Current FastAPI fact is missing "
            "from final LLM context."
        )

        # =================================================
        # VERIFY DATABASE HISTORY
        # =================================================

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
            "SQLite history."
        )

        # =================================================
        # GEMINI CHECK
        # =================================================

        assert result["ai_response"] == (
            "[GEMINI CALL SKIPPED]"
        )

        # =================================================
        # SUCCESS
        # =================================================

        print("\n" + "=" * 60)
        print("VALIDATION")
        print("=" * 60)

        print(
            "\nConflicting facts retrieved successfully."
        )

        print(
            "Older Flask fact removed before optimization."
        )

        print(
            "Newer FastAPI fact survived optimization."
        )

        print(
            "Outdated fact did not reach final context."
        )

        print(
            "Current fact reached final context."
        )

        print(
            "SQLite history remained unchanged."
        )

        print(
            "Gemini was not called."
        )

        print(
            "\nFULL MEMORY ENGINE CONFLICT TEST PASSED"
        )

    finally:

        # =================================================
        # CLEAN CHROMADB
        # =================================================

        if created_ids:

            try:

                vector_store.delete_messages_by_message_ids(
                    created_ids
                )

                print(
                    "\nTemporary Chroma embeddings removed."
                )

            except Exception as error:

                print(
                    "\nChroma cleanup warning:",
                    error,
                )

            # =================================================
            # CLEAN SQLITE
            # =================================================

            try:

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
                    "Temporary SQLite messages removed."
                )

            except Exception as error:

                db.rollback()

                print(
                    "SQLite cleanup warning:",
                    error,
                )

        db.close()


if __name__ == "__main__":
    main()
    