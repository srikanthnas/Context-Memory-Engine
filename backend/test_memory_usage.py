from database.connection import SessionLocal
from database.models import (
    Conversation,
    Document,
    Message,
    Preference,
)


def main():
    db = SessionLocal()

    try:
        print("\n" + "=" * 60)
        print("DOCUMENTS")
        print("=" * 60)

        documents = db.query(Document).all()

        for item in documents:
            print(
                f"ID={item.id} | "
                f"File={item.filename} | "
                f"Access Count={item.access_count} | "
                f"Importance={item.importance} | "
                f"Last Accessed={item.last_accessed}"
            )

        print("\n" + "=" * 60)
        print("CONVERSATIONS")
        print("=" * 60)

        conversations = db.query(Conversation).all()

        for item in conversations:
            print(
                f"ID={item.id} | "
                f"Title={item.title} | "
                f"Access Count={item.access_count} | "
                f"Importance={item.importance} | "
                f"Last Accessed={item.last_accessed}"
            )

        print("\n" + "=" * 60)
        print("MESSAGES")
        print("=" * 60)

        messages = db.query(Message).all()

        for item in messages:
            print(
                f"ID={item.id} | "
                f"Role={item.role} | "
                f"Access Count={item.access_count} | "
                f"Importance={item.importance} | "
                f"Last Accessed={item.last_accessed}"
            )

        print("\n" + "=" * 60)
        print("PREFERENCES")
        print("=" * 60)

        preferences = db.query(Preference).all()

        for item in preferences:
            print(
                f"ID={item.id} | "
                f"{item.key}={item.value} | "
                f"Access Count={item.access_count} | "
                f"Importance={item.importance} | "
                f"Last Accessed={item.last_accessed}"
            )

    finally:
        db.close()


if __name__ == "__main__":
    main()