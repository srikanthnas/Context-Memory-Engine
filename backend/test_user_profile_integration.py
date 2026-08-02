from database.connection import SessionLocal
from database.models import Preference, User
from memory.memory_engine import MemoryEngine


TEST_KEY = "location"


def main():

    print("\n" + "=" * 60)
    print("PHASE 32.3 - USER PROFILE INTEGRATION TEST")
    print("=" * 60)

    db = SessionLocal()

    try:

        user = (
            db.query(User)
            .order_by(User.id.asc())
            .first()
        )

        assert user is not None, (
            "No user available for test."
        )

        # ==================================================
        # BACK UP EXISTING LOCATION
        # ==================================================

        existing = (
            db.query(Preference)
            .filter(
                Preference.user_id == user.id,
                Preference.key == TEST_KEY,
            )
            .first()
        )

        original_value = (
            existing.value
            if existing
            else None
        )

        original_id = (
            existing.id
            if existing
            else None
        )

        # ==================================================
        # MEMORY ENGINE
        # ==================================================

        engine = MemoryEngine()

        # Skip Gemini during pipeline testing.
        engine._generate_response = (
            lambda context:
            "[TEST PROFILE RESPONSE]"
        )

        # ==================================================
        # FIRST PROFILE STATEMENT
        # ==================================================

        result = engine.process_prompt(
            db=db,
            user_id=user.id,
            prompt="I live in Bengaluru.",
        )

        print("\nPROFILE UPDATES")
        print("-" * 60)

        print(
            result["profile_updates"]
        )

        assert any(
            item["key"] == "location"
            and item["value"] == "Bengaluru"
            for item in result["profile_updates"]
        )

        # ==================================================
        # VERIFY SAME-REQUEST RETRIEVAL
        # ==================================================

        retrieved_preferences = (
            result["preference_memory"]
        )

        assert any(
            item["key"] == "location"
            and item["value"] == "Bengaluru"
            for item in retrieved_preferences
        ), (
            "New profile fact was not available "
            "during same-request retrieval."
        )

        # ==================================================
        # UPDATE PROFILE
        # ==================================================

        result = engine.process_prompt(
            db=db,
            user_id=user.id,
            prompt="I live in Mysuru.",
        )

        assert any(
            item["key"] == "location"
            and item["value"] == "Mysuru"
            for item in result["profile_updates"]
        )

        # ==================================================
        # VERIFY DATABASE
        # ==================================================

        rows = (
            db.query(Preference)
            .filter(
                Preference.user_id == user.id,
                Preference.key == TEST_KEY,
            )
            .all()
        )

        assert len(rows) == 1, (
            "Duplicate location profile facts created."
        )

        assert rows[0].value == "Mysuru"

        # ==================================================
        # VERIFY MEMORY RETRIEVAL
        # ==================================================

        assert any(
            item["key"] == "location"
            and item["value"] == "Mysuru"
            for item in result["preference_memory"]
        )

        # ==================================================
        # VERIFY FINAL CONTEXT
        # ==================================================

        assert (
            "location = Mysuru"
            in result["context"]
        ), (
            "Updated profile fact did not reach "
            "final context."
        )

        # ==================================================
        # VERIFY LLM BOUNDARY
        # ==================================================

        assert (
            result["ai_response"]
            == "[TEST PROFILE RESPONSE]"
        )

        print("\nFINAL PROFILE")
        print("-" * 60)

        print(
            "location = Mysuru"
        )

        print("\n" + "=" * 60)
        print("VALIDATION")
        print("=" * 60)

        print("\nProfile fact automatically extracted.")
        print("Profile fact persisted to SQLite.")
        print("Profile update replaced old value.")
        print("Duplicate profile rows avoided.")
        print("Updated profile retrieved from memory.")
        print("Updated profile reached final context.")
        print("LLM boundary reached without Gemini.")

        print(
            "\nUSER PROFILE INTEGRATION TEST PASSED"
        )

    finally:

        # ==================================================
        # RESTORE ORIGINAL USER DATA
        # ==================================================

        current_rows = (
            db.query(Preference)
            .filter(
                Preference.user_id == user.id,
                Preference.key == TEST_KEY,
            )
            .all()
        )

        for row in current_rows:

            if (
                original_id is None
                or row.id != original_id
            ):
                db.delete(row)

        if original_id is not None:

            original = (
                db.query(Preference)
                .filter(
                    Preference.id == original_id
                )
                .first()
            )

            if original:
                original.value = original_value

        db.commit()
        db.close()


if __name__ == "__main__":
    main()