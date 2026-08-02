from database.connection import SessionLocal
from database.models import Preference
from memory.memory_engine import MemoryEngine


def main():
    db = SessionLocal()

    temporary = None

    try:
        user_id = 2

        engine = MemoryEngine()

        print("\n" + "=" * 60)
        print("PHASE 27 - CONFLICT PIPELINE TEST")
        print("=" * 60)

        # -------------------------------------------------
        # Create a newer conflicting preference
        # -------------------------------------------------

        temporary = Preference(
            user_id=user_id,
            key="response_style",
            value="detailed",
        )

        db.add(temporary)
        db.commit()
        db.refresh(temporary)

        print("\nTemporary preference:")
        print(
            f"ID={temporary.id} | "
            f"{temporary.key}={temporary.value}"
        )

        # -------------------------------------------------
        # Retrieve memory using the real MemoryEngine
        # -------------------------------------------------

        prepared_prompt = engine._prepare_prompt(
            user_id=user_id,
            prompt="Explain my programming skills.",
        )

        memory = engine._retrieve_memories(
            db=db,
            user_id=user_id,
            prepared_prompt=prepared_prompt,
        )

        print("\nBEFORE CONFLICT RESOLUTION")
        print("-" * 60)

        for preference in memory["preferences"]:
            print(
                preference["key"],
                "=",
                preference["value"],
                "| ID:",
                preference.get("id"),
            )

        # -------------------------------------------------
        # Resolve conflicts
        # -------------------------------------------------

        resolved_memory = (
            engine._resolve_memory_conflicts(
                memory=memory,
            )
        )

        print("\nAFTER CONFLICT RESOLUTION")
        print("-" * 60)

        for preference in resolved_memory["preferences"]:
            print(
                preference["key"],
                "=",
                preference["value"],
                "| ID:",
                preference.get("id"),
            )

        # -------------------------------------------------
        # Validate
        # -------------------------------------------------

        response_styles = [
            preference
            for preference
            in resolved_memory["preferences"]
            if preference["key"] == "response_style"
        ]

        assert len(response_styles) == 1, (
            "Conflict resolver allowed multiple "
            "response_style preferences through."
        )

        assert (
            response_styles[0]["id"]
            == temporary.id
        ), (
            "Newest preference was not selected."
        )

        assert (
            response_styles[0]["value"]
            == "detailed"
        )

        print("\n" + "=" * 60)
        print("VALIDATION")
        print("=" * 60)

        print(
            "\nConflict resolution executed "
            "inside the MemoryEngine pipeline."
        )

        print(
            "Newest preference survived."
        )

        print(
            "Older conflicting preference was removed."
        )

        print(
            "\nCONFLICT PIPELINE TEST PASSED"
        )

    finally:

        # -------------------------------------------------
        # Always clean up test preference
        # -------------------------------------------------

        if temporary is not None:

            temporary_db = (
                db.query(Preference)
                .filter(
                    Preference.id == temporary.id
                )
                .first()
            )

            if temporary_db is not None:
                db.delete(temporary_db)
                db.commit()

        db.close()


if __name__ == "__main__":
    main()