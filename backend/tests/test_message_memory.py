from database.connection import SessionLocal
from memory.message_memory import MessageMemory


def main():
    db = SessionLocal()

    try:
        result = MessageMemory.get_recent_messages(
            db=db,
            conversation_id=1,
        )

        print("\n===== MESSAGE MEMORY OUTPUT =====")
        print(result)

    finally:
        db.close()


if __name__ == "__main__":
    main()