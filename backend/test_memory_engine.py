from database.connection import SessionLocal
from services.chat_service import ChatService


def main():
    db = SessionLocal()

    try:
        chat = ChatService()

        result = chat.chat(
            db=db,
            user_id=2,
            prompt="Explain my programming skills from my resume.",
        )

        print("\n" + "=" * 60)
        print("SELECTED MEMORY")
        print("=" * 60)

        for item in result["selected_memory"]:
            print(
                item["memory_type"],
                "->",
                item["score"],
            )

            if item["memory_type"] == "preference":
                print(
                    "PREFERENCE:",
                    item.get("key"),
                    "=",
                    item.get("value"),
                )

            elif item["memory_type"] == "document":
                print(
                    "FILE:",
                    item.get("filename"),
                )
                print(
                    "CHUNK:\n",
                    item.get("chunk"),
                )

            print("-" * 60)

        print("\n" + "=" * 60)
        print("FINAL CONTEXT")
        print("=" * 60)
        print(result["context"])

        # Gemini intentionally skipped while testing memory pipeline
        print("\n" + "=" * 60)
        print("GEMINI CALL SKIPPED")
        print("=" * 60)

    finally:
        db.close()


if __name__ == "__main__":
    main()