from database.connection import SessionLocal
from memory.memory_engine import MemoryEngine


def main():
    db = SessionLocal()

    try:
        engine = MemoryEngine()

        result = engine.process_prompt(
            db=db,
            user_id=1,
            prompt="What did we talk about before?"
        )

        print("\n===== MEMORY ENGINE OUTPUT =====")
        print(result)

    finally:
        db.close()


if __name__ == "__main__":
    main()