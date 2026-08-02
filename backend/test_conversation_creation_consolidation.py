from database.connection import SessionLocal
from database.models import Conversation
from schemas.conversation import ConversationCreate
from services.conversation_service import ConversationService


def main():
    db = SessionLocal()

    try:
        service = ConversationService()

        user_id = 2
        title = "What coding skills do I have according to my resume?"

        print("\n" + "=" * 60)
        print("PHASE 26 - CREATION CONSOLIDATION TEST")
        print("=" * 60)

        before_count = (
            db.query(Conversation)
            .filter(Conversation.user_id == user_id)
            .count()
        )

        print("\nConversations before:", before_count)

        request = ConversationCreate(
            user_id=user_id,
            title=title,
        )

        result = service.create_conversation(
            db=db,
            conversation=request,
        )

        after_count = (
            db.query(Conversation)
            .filter(Conversation.user_id == user_id)
            .count()
        )

        print("\nReturned conversation:")
        print("ID:", result.id)
        print("Title:", result.title)

        print("\nConversations after:", after_count)

        print("\n" + "=" * 60)
        print("VALIDATION")
        print("=" * 60)

        assert before_count == after_count, (
            "Duplicate conversation was created."
        )

        print(
            "\nNo new conversation created."
        )

        print(
            "Existing conversation reused successfully."
        )

        print(
            "\nCREATION CONSOLIDATION TEST PASSED"
        )

    finally:
        db.close()


if __name__ == "__main__":
    main()