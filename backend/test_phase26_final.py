from database.connection import SessionLocal
from database.models import Conversation
from schemas.conversation import ConversationCreate
from services.conversation_service import ConversationService


def main():
    db = SessionLocal()

    try:
        service = ConversationService()
        user_id = 2

        print("\n" + "=" * 60)
        print("PHASE 26 - FINAL INTEGRATION TEST")
        print("=" * 60)

        # ---------------------------------------------
        # Similar topic
        # ---------------------------------------------

        first = service.create_conversation(
            db=db,
            conversation=ConversationCreate(
                user_id=user_id,
                title=(
                    "Explain my programming skills "
                    "from my resume."
                ),
            ),
        )

        second = service.create_conversation(
            db=db,
            conversation=ConversationCreate(
                user_id=user_id,
                title=(
                    "Tell me about my coding abilities "
                    "according to my resume."
                ),
            ),
        )

        print("\nSIMILAR TOPIC")
        print("-" * 60)

        print("First ID:", first.id)
        print("Second ID:", second.id)

        assert first.id == second.id, (
            "Similar topics were not consolidated."
        )

        # ---------------------------------------------
        # Different topic
        # ---------------------------------------------

        third = service.create_conversation(
            db=db,
            conversation=ConversationCreate(
                user_id=user_id,
                title=(
                    "Explain the architecture of my "
                    "Context Memory Engine project."
                ),
            ),
        )

        print("\nDIFFERENT TOPIC")
        print("-" * 60)

        print("Programming conversation ID:", first.id)
        print("Project conversation ID:", third.id)

        assert third.id != first.id, (
            "Unrelated topics were incorrectly consolidated."
        )

        print("\n" + "=" * 60)
        print("VALIDATION")
        print("=" * 60)

        print("Similar prompts consolidated correctly.")
        print("Different topics remained separate.")

        print(
            "\nPHASE 26 FINAL INTEGRATION TEST PASSED"
        )

    finally:
        db.close()


if __name__ == "__main__":
    main()