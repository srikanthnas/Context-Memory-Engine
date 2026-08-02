from database.connection import SessionLocal
from memory.conversation_memory import ConversationMemory


def main():
    db = SessionLocal()

    try:
        conversation_memory = ConversationMemory()

        print("\n" + "=" * 60)
        print("PHASE 26 - DUPLICATE CONVERSATION TEST")
        print("=" * 60)

        prompt = "Explain my programming skills from my resume."

        print("\nQuery:")
        print(prompt)

        conversations = (
            conversation_memory.get_recent_conversations(
                db=db,
                user_id=2,
                prompt=prompt,
                limit=10,
            )
        )

        print("\n" + "=" * 60)
        print("CONVERSATIONS AFTER DUPLICATE FILTERING")
        print("=" * 60)

        for conversation in conversations:
            print(f"\nID: {conversation['id']}")
            print(f"Title: {conversation['title']}")
            print(
                f"Summary: "
                f"{conversation.get('summary', '')}"
            )
            print("-" * 60)

        print("\nTotal unique conversations:")
        print(len(conversations))

        # Check for exact duplicate title + summary pairs.
        seen = set()

        for conversation in conversations:

            key = (
                conversation.get("title", "")
                .strip()
                .lower(),

                conversation.get("summary", "")
                .strip()
                .lower(),
            )

            assert key not in seen, (
                "Duplicate conversation survived filtering."
            )

            seen.add(key)

        print("\nDUPLICATE CONVERSATION TEST PASSED")

    finally:
        db.close()


if __name__ == "__main__":
    main()