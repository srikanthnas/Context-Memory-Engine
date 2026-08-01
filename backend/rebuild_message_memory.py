from database.connection import SessionLocal
from database.models import Conversation, Message
from embeddings.embedding_manager import EmbeddingManager
from retrieval.chroma_vector_store import ChromaVectorStore


def main():

    db = SessionLocal()

    embedding_manager = EmbeddingManager()
    vector_store = ChromaVectorStore()

    try:

        print("\nRebuilding message memory...")

        # Remove ONLY old message vectors.
        vector_store.reset_message_collection()

        messages = (
            db.query(Message)
            .order_by(Message.id.asc())
            .all()
        )

        rebuilt = 0
        skipped = 0

        for message in messages:

            conversation = (
                db.query(Conversation)
                .filter(
                    Conversation.id
                    == message.conversation_id
                )
                .first()
            )

            if conversation is None:
                skipped += 1
                continue

            embedded_message = (
                embedding_manager.embed_message(
                    message=message.content,
                    message_id=message.id,
                    conversation_id=message.conversation_id,
                    user_id=conversation.user_id,
                    role=message.role,
                )
            )

            vector_store.add_messages(
                [embedded_message]
            )

            rebuilt += 1

        print("\n" + "=" * 50)
        print("MESSAGE MEMORY REBUILD COMPLETE")
        print("=" * 50)

        print(f"Rebuilt messages: {rebuilt}")
        print(f"Skipped messages: {skipped}")
        print(
            "Chroma message count:",
            vector_store.message_collection.count(),
        )

    finally:
        db.close()


if __name__ == "__main__":
    main()