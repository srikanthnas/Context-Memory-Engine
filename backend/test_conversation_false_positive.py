from database.connection import SessionLocal
from database.models import Conversation
from schemas.conversation import ConversationCreate
from services.conversation_service import ConversationService


def main():
    db = SessionLocal()

    try:
        service = ConversationService()

        user_id = 2

        # Intentionally different topic
        title = "What education qualifications are listed in my resume?"

        print("\n" + "=" * 60)
        print("PHASE 26 - FALSE POSITIVE CONSOLIDATION TEST")
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

        assert after_count == before_count + 1, (
            "False positive detected: "
            "different conversation was incorrectly consolidated."
        )

        assert result.title == title, (
            "Existing unrelated conversation was reused."
        )

        print("\nNew conversation created successfully.")
        print("No false-positive consolidation occurred.")

        print(
            "\nFALSE POSITIVE CONSOLIDATION TEST PASSED"
        )

    finally:
        db.close()


if __name__ == "__main__":
    main()