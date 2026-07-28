from database.connection import SessionLocal
from memory.memory_engine import MemoryEngine


def main():
    db = SessionLocal()

    try:
        engine = MemoryEngine()

        result = engine.process_prompt(
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

    finally:
        db.close()


if __name__ == "__main__":
    main()