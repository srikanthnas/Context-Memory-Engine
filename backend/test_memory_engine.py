from database.connection import SessionLocal
from services.chat_service import ChatService


def main():
    db = SessionLocal()

    try:
        chat = ChatService()

        result = chat.chat(
            db=db,
            user_id=1,
            prompt="What programming languages are mentioned in my resume?",
        )

        print("\n" + "=" * 60)
        print("AI RESPONSE")
        print("=" * 60)
        print(result["ai_response"])

        print("\n" + "=" * 60)
        print("CONTEXT")
        print("=" * 60)
        print(result["context"])

        print("\n" + "=" * 60)
        print("UNIFIED MEMORY")
        print("=" * 60)

        for item in result["unified_memory"]:
            print(item["memory_type"], "->", item["score"])

        print("\n" + "=" * 60)
        print("SELECTED MEMORY")
        print("=" * 60)

        for item in result["selected_memory"]:
            print(
                item["memory_type"],
                "->",
                item["score"],
            )

    finally:
        db.close()


if __name__ == "__main__":
    main()