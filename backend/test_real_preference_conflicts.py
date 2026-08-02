from database.connection import SessionLocal
from database.models import Preference
from memory.preference_memory import PreferenceMemory
from memory.memory_conflict_resolver import (
    MemoryConflictResolver,
)


def main():
    db = SessionLocal()

    try:
        user_id = 2

        preference_memory = PreferenceMemory()
        resolver = MemoryConflictResolver()

        print("\n" + "=" * 60)
        print("PHASE 27 - REAL PREFERENCE CONFLICT TEST")
        print("=" * 60)

        # ---------------------------------------------
        # Create temporary conflicting preference
        # ---------------------------------------------

        existing = (
            db.query(Preference)
            .filter(
                Preference.user_id == user_id,
                Preference.key == "response_style",
            )
            .all()
        )

        print("\nExisting response_style preferences:")

        for preference in existing:
            print(
                f"ID={preference.id} | "
                f"{preference.key}={preference.value}"
            )

        temporary = Preference(
            user_id=user_id,
            key="response_style",
            value="detailed",
        )

        db.add(temporary)
        db.commit()
        db.refresh(temporary)

        print("\nTemporary conflicting preference created:")
        print(
            f"ID={temporary.id} | "
            f"{temporary.key}={temporary.value}"
        )

        # ---------------------------------------------
        # Retrieve real preferences
        # ---------------------------------------------

        preferences = (
            preference_memory.get_preferences(
                db=db,
                user_id=user_id,
            )
        )

        print("\nRETRIEVED")
        print("-" * 60)

        for preference in preferences:
            print(
                preference["key"],
                "=",
                preference["value"],
                "|",
                preference.get("last_accessed"),
            )

        # ---------------------------------------------
        # Resolve
        # ---------------------------------------------

        memory = {
            "conversations": [],
            "messages": [],
            "documents": [],
            "preferences": preferences,
        }

        resolved = resolver.resolve(memory)

        print("\nRESOLVED")
        print("-" * 60)

        for preference in resolved["preferences"]:
            print(
                preference["key"],
                "=",
                preference["value"],
            )

        response_styles = [
            preference
            for preference
            in resolved["preferences"]
            if preference["key"] == "response_style"
        ]

        assert len(response_styles) == 1, (
            "Multiple response_style preferences "
            "survived conflict resolution."
        )

        print("\nConflict resolved successfully.")

        # ---------------------------------------------
        # Cleanup temporary test data
        # ---------------------------------------------

        db.delete(temporary)
        db.commit()

        print("Temporary preference removed.")

        print(
            "\nREAL PREFERENCE CONFLICT TEST PASSED"
        )

    finally:
        db.close()


if __name__ == "__main__":
    main()