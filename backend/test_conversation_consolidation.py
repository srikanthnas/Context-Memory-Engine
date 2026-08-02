from database.connection import SessionLocal
from services.conversation_service import ConversationService


def main():
    db = SessionLocal()

    try:
        service = ConversationService()

        print("\n" + "=" * 60)
        print("PHASE 26 - CONVERSATION CONSOLIDATION TEST")
        print("=" * 60)

        title = (
            "Explain my programming skills "
            "from my resume."
        )

        print("\nSearching for duplicate of:")
        print(title)

        duplicate = service.find_duplicate_conversation(
            db=db,
            user_id=2,
            title=title,
        )

        print("\n" + "=" * 60)
        print("RESULT")
        print("=" * 60)

        if duplicate is None:
            print("No duplicate found.")

        else:
            print(
                f"Duplicate conversation ID: "
                f"{duplicate.id}"
            )
            print(
                f"Title: {duplicate.title}"
            )

        assert duplicate is not None, (
            "Expected duplicate conversation "
            "was not detected."
        )

        print(
            "\nCONVERSATION CONSOLIDATION "
            "TEST PASSED"
        )

    finally:
        db.close()


if __name__ == "__main__":
    main()