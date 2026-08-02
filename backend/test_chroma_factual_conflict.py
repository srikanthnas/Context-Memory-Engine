from database.connection import SessionLocal
from database.models import Conversation, Message
from schemas.message import MessageCreate

from services.message_service import MessageService
from memory.message_memory import MessageMemory
from memory.memory_engine import MemoryEngine
from retrieval.chroma_vector_store import ChromaVectorStore


def main():

    db = SessionLocal()

    message_service = MessageService()
    message_memory = MessageMemory()
    memory_engine = MemoryEngine()
    vector_store = ChromaVectorStore()

    created_ids = []

    try:

        print("\n" + "=" * 60)
        print("PHASE 27 - CHROMA FACTUAL CONFLICT TEST")
        print("=" * 60)

        # =================================================
        # FIND A REAL CONVERSATION
        # =================================================

        conversation = (
            db.query(Conversation)
            .order_by(Conversation.id.asc())
            .first()
        )

        assert conversation is not None, (
            "No conversation exists for testing."
        )

        user_id = conversation.user_id

        print("\nConversation:")
        print("ID:", conversation.id)
        print("User ID:", user_id)
        print("Title:", conversation.title)

        # =================================================
        # CREATE REAL MESSAGES THROUGH MESSAGE SERVICE
        # =================================================

        test_contents = [
            "My project backend uses Flask.",
            "My project backend now uses FastAPI.",
            "My project backend handles API requests.",
        ]

        print("\nCREATING TEST MESSAGES")
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

        # =================================================
        # SEMANTIC RETRIEVAL FROM CHROMADB
        # =================================================

        query = (
            "What backend technology "
            "does my project use?"
        )

        print("\nSEMANTIC QUERY")
        print("-" * 60)
        print(query)

        retrieved = (
            message_memory.search_relevant_messages(
                query=query,
                user_id=user_id,
                top_k=20,
            )
        )

        # Keep only temporary test messages.
        # Existing project memories must not interfere
        # with this test.

        test_retrieved = [
            message
            for message in retrieved
            if message.get("id") in created_ids
        ]

        print("\nRETRIEVED TEST MEMORIES")
        print("-" * 60)

        for message in test_retrieved:

            print(
                f"ID={message.get('id')} | "
                f"{message.get('content')} | "
                f"Score={message.get('score')}"
            )

        retrieved_ids = {
            message.get("id")
            for message in test_retrieved
        }

        # =================================================
        # VERIFY CHROMA RETRIEVAL
        # =================================================

        old_id = created_ids[0]
        new_id = created_ids[1]
        related_id = created_ids[2]

        assert old_id in retrieved_ids, (
            "Flask message was not retrieved "
            "from ChromaDB."
        )

        assert new_id in retrieved_ids, (
            "FastAPI message was not retrieved "
            "from ChromaDB."
        )

        print(
            "\nConflicting messages successfully "
            "retrieved from ChromaDB."
        )

        # =================================================
        # BUILD MEMORY
        # =================================================

        memory = {
            "conversations": [],
            "documents": [],
            "preferences": [],
            "messages": test_retrieved,
        }

        # =================================================
        # RUN REAL MEMORY ENGINE CONFLICT PIPELINE
        # =================================================

        resolved = (
            memory_engine._resolve_memory_conflicts(
                memory=memory,
            )
        )

        print("\nACTIVE MEMORY AFTER RESOLUTION")
        print("-" * 60)

        for message in resolved["messages"]:

            print(
                f"ID={message.get('id')} | "
                f"{message.get('content')}"
            )

        remaining_ids = {
            message.get("id")
            for message in resolved["messages"]
        }

        # =================================================
        # VALIDATE CONFLICT RESOLUTION
        # =================================================

        assert old_id not in remaining_ids, (
            "Older Flask fact survived "
            "active conflict resolution."
        )

        assert new_id in remaining_ids, (
            "Newer FastAPI fact was removed."
        )

        # Related message may or may not appear in the
        # semantic top-k results.
        #
        # If Chroma retrieved it, the conflict resolver
        # must preserve it.

        if related_id in retrieved_ids:

            assert related_id in remaining_ids, (
                "Related non-conflicting memory "
                "was incorrectly removed."
            )

        # =================================================
        # VERIFY SQLITE HISTORY
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
            "historical SQLite messages."
        )

        # =================================================
        # SUCCESS
        # =================================================

        print("\n" + "=" * 60)
        print("VALIDATION")
        print("=" * 60)

        print(
            "\nSQLite messages created successfully."
        )

        print(
            "Message embeddings stored in ChromaDB."
        )

        print(
            "Semantic retrieval returned "
            "the conflicting memories."
        )

        print(
            "Older Flask fact removed "
            "from active context."
        )

        print(
            "Newer FastAPI fact preserved."
        )

        if related_id in retrieved_ids:
            print(
                "Related non-conflicting "
                "memory preserved."
            )

        print(
            "Historical SQLite messages "
            "remained unchanged."
        )

        print(
            "\nCHROMA FACTUAL CONFLICT TEST PASSED"
        )

    finally:

        # =================================================
        # CLEAN UP CHROMADB
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

            # =============================================
            # CLEAN UP SQLITE
            # =============================================

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