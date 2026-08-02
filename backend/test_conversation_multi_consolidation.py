from database.connection import SessionLocal
from database.models import Conversation
from schemas.conversation import ConversationCreate
from services.conversation_service import ConversationService


def main():
    db = SessionLocal()

    try:
        service = ConversationService()

        user_id = 2

        prompts = [
            "Explain my programming skills from my resume.",
            "What coding skills do I have according to my resume?",
            "Tell me about my programming abilities from my resume.",
        ]

        print("\n" + "=" * 60)
        print("PHASE 26 - MULTI CONSOLIDATION TEST")
        print("=" * 60)

        before_count = (
            db.query(Conversation)
            .filter(Conversation.user_id == user_id)
            .count()
        )

        print("\nConversations before:", before_count)

        returned_ids = []

        for prompt in prompts:

            conversation = service.create_conversation(
                db=db,
                conversation=ConversationCreate(
                    user_id=user_id,
                    title=prompt,
                ),
            )

            returned_ids.append(
                conversation.id
            )

            print("\nPrompt:")
            print(prompt)

            print(
                "Returned conversation ID:",
                conversation.id,
            )

        after_count = (
            db.query(Conversation)
            .filter(Conversation.user_id == user_id)
            .count()
        )

        print("\n" + "=" * 60)
        print("VALIDATION")
        print("=" * 60)

        print("\nReturned IDs:", returned_ids)

        print(
            "Conversations after:",
            after_count,
        )

        unique_ids = set(returned_ids)

        assert len(unique_ids) == 1, (
            "Equivalent prompts were mapped to "
            "different conversations."
        )

        assert before_count == after_count, (
            "New duplicate conversations were created."
        )

        print(
            "\nAll equivalent prompts reused "
            "the same conversation."
        )

        print(
            "No duplicate conversations were created."
        )

        print(
            "\nMULTI CONSOLIDATION TEST PASSED"
        )

    finally:
        db.close()


if __name__ == "__main__":
    main()