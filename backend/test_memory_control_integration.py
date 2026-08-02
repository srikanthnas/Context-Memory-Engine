from database.connection import SessionLocal
from database.models import Preference, User
from memory.memory_engine import MemoryEngine


TEST_KEY = "preferred_ide"


def main():

    print("\n" + "=" * 60)
    print("PHASE 33.3 - MEMORY CONTROL INTEGRATION TEST")
    print("=" * 60)

    db = SessionLocal()

    try:

        user = (
            db.query(User)
            .order_by(User.id.asc())
            .first()
        )

        assert user is not None

        # ==================================================
        # BACKUP EXISTING VALUE
        # ==================================================

        existing_rows = (
            db.query(Preference)
            .filter(
                Preference.user_id == user.id,
                Preference.key == TEST_KEY,
            )
            .all()
        )

        backup_values = [
            row.value
            for row in existing_rows
        ]

        for row in existing_rows:
            db.delete(row)

        db.commit()

        # ==================================================
        # ENGINE
        # ==================================================

        engine = MemoryEngine()

        # Skip Gemini.
        engine._generate_response = (
            lambda context:
            "[TEST MEMORY CONTROL RESPONSE]"
        )

        # ==================================================
        # TEST 1 — REMEMBER
        # ==================================================

        result = engine.process_prompt(
            db=db,
            user_id=user.id,
            prompt=(
                "Remember that my preferred IDE "
                "is VS Code."
            ),
        )

        print("\nREMEMBER")
        print("-" * 60)
        print(result["memory_command"])

        assert result["memory_command"] == {
            "action": "remember",
            "key": "preferred_ide",
            "value": "VS Code",
            "success": True,
        }

        # Explicit command must not also trigger
        # automatic Phase 32 extraction.

        assert result["profile_updates"] == []

        rows = (
            db.query(Preference)
            .filter(
                Preference.user_id == user.id,
                Preference.key == TEST_KEY,
            )
            .all()
        )

        assert len(rows) == 1
        assert rows[0].value == "VS Code"

        # Because command handling occurs before retrieval,
        # the remembered value should be available during
        # the same request.

        assert any(
            item["key"] == TEST_KEY
            and item["value"] == "VS Code"
            for item in result["preference_memory"]
        )

        # ==================================================
        # TEST 2 — UPDATE THROUGH REMEMBER
        # ==================================================

        result = engine.process_prompt(
            db=db,
            user_id=user.id,
            prompt=(
                "Remember that my preferred IDE "
                "is PyCharm."
            ),
        )

        rows = (
            db.query(Preference)
            .filter(
                Preference.user_id == user.id,
                Preference.key == TEST_KEY,
            )
            .all()
        )

        assert len(rows) == 1
        assert rows[0].value == "PyCharm"

        print("\nUPDATE")
        print("-" * 60)
        print("preferred_ide = PyCharm")

        # ==================================================
        # TEST 3 — FORGET
        # ==================================================

        result = engine.process_prompt(
            db=db,
            user_id=user.id,
            prompt="Forget my preferred IDE.",
        )

        print("\nFORGET")
        print("-" * 60)
        print(result["memory_command"])

        assert result["memory_command"] == {
            "action": "forget",
            "key": "preferred_ide",
            "success": True,
        }

        rows = (
            db.query(Preference)
            .filter(
                Preference.user_id == user.id,
                Preference.key == TEST_KEY,
            )
            .all()
        )

        assert rows == []

        # Forgotten memory must also be absent from
        # retrieval after deletion.

        assert not any(
            item["key"] == TEST_KEY
            for item in result["preference_memory"]
        )

        # ==================================================
        # TEST 4 — NORMAL PROMPT
        # ==================================================

        result = engine.process_prompt(
            db=db,
            user_id=user.id,
            prompt="Explain polymorphism in Java.",
        )

        assert result["memory_command"] is None

        print("\nNORMAL PROMPT")
        print("-" * 60)
        print("No explicit memory command detected.")

        # ==================================================
        # VALIDATION
        # ==================================================

        print("\n" + "=" * 60)
        print("VALIDATION")
        print("=" * 60)

        print("\nRemember command persisted memory.")
        print("Remember command updated existing memory.")
        print("Duplicate memory avoided.")
        print("Explicit command bypassed automatic extraction.")
        print("Remembered memory reached retrieval.")
        print("Forget command removed persistent memory.")
        print("Forgotten memory disappeared from retrieval.")
        print("Normal prompts remained unaffected.")
        print("LLM boundary reached without Gemini.")

        print(
            "\nMEMORY CONTROL INTEGRATION TEST PASSED"
        )

    finally:

        if 'user' in locals():

            # Remove Phase 33 test data.

            (
                db.query(Preference)
                .filter(
                    Preference.user_id == user.id,
                    Preference.key == TEST_KEY,
                )
                .delete(
                    synchronize_session=False
                )
            )

            db.commit()

            # Restore previous values if any existed.

            for value in backup_values:

                restored = Preference(
                    user_id=user.id,
                    key=TEST_KEY,
                    value=value,
                )

                db.add(restored)

            db.commit()

        db.close()


if __name__ == "__main__":
    main()