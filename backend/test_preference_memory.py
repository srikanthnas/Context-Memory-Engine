from database.connection import SessionLocal
from database.models import Preference
from memory.preference_memory import PreferenceMemory


def main():
    db = SessionLocal()

    try:
        user_id = 2

        print("\n" + "=" * 60)
        print("CREATING TEST PREFERENCE")
        print("=" * 60)

        preference = (
            db.query(Preference)
            .filter(
                Preference.user_id == user_id,
                Preference.key == "response_style",
            )
            .first()
        )

        if not preference:
            preference = Preference(
                user_id=user_id,
                key="response_style",
                value="concise",
            )

            db.add(preference)
            db.commit()
            db.refresh(preference)

            print("Created new preference.")
        else:
            print("Preference already exists.")

        print("\nDatabase preference:")
        print("ID:", preference.id)
        print("Key:", preference.key)
        print("Value:", preference.value)
        print("Access Count:", preference.access_count)
        print("Importance:", preference.importance)
        print("Last Accessed:", preference.last_accessed)

        print("\n" + "=" * 60)
        print("PREFERENCE MEMORY RETRIEVAL")
        print("=" * 60)

        memories = PreferenceMemory.get_preferences(
            db=db,
            user_id=user_id,
        )

        for memory in memories:
            print(memory)

    finally:
        db.close()


if __name__ == "__main__":
    main()