from database.connection import SessionLocal
from database.models import Conversation
from retrieval.chroma_vector_store import ChromaVectorStore


def main():

    conversation_id = 15

    db = SessionLocal()
    vector_store = ChromaVectorStore()

    try:
        print("\n" + "=" * 60)
        print("CLEANUP TEST CONVERSATION")
        print("=" * 60)

        # =====================================================
        # DELETE FROM CHROMA
        # =====================================================

        vector_id = f"conversation_{conversation_id}"

        vector_store.conversation_collection.delete(
            ids=[vector_id]
        )

        print(
            f"\nDeleted {vector_id} from ChromaDB."
        )

        # =====================================================
        # DELETE FROM SQLITE
        # =====================================================

        conversation = (
            db.query(Conversation)
            .filter(
                Conversation.id == conversation_id
            )
            .first()
        )

        if conversation:

            print("\nDeleting SQLite conversation:")
            print("ID:", conversation.id)
            print("Title:", conversation.title)

            db.delete(conversation)
            db.commit()

            print("\nDeleted from SQLite.")

        else:

            print(
                "\nConversation ID 15 "
                "not found in SQLite."
            )

        # =====================================================
        # VERIFY CHROMA
        # =====================================================

        remaining = (
            vector_store.conversation_collection.get(
                ids=[vector_id]
            )
        )

        assert not remaining["ids"], (
            "Conversation still exists in ChromaDB."
        )

        # =====================================================
        # VERIFY SQLITE
        # =====================================================

        remaining_db = (
            db.query(Conversation)
            .filter(
                Conversation.id == conversation_id
            )
            .first()
        )

        assert remaining_db is None, (
            "Conversation still exists in SQLite."
        )

        print("\n" + "=" * 60)
        print("CLEANUP COMPLETE")
        print("=" * 60)

        print("\nSQLite: removed")
        print("ChromaDB: removed")

    finally:
        db.close()


if __name__ == "__main__":
    main()