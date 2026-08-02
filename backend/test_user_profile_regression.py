from database.connection import SessionLocal
from database.models import Preference, User
from memory.memory_engine import MemoryEngine


TEST_KEYS = {
    "name",
    "location",
}


def main():

    print("\n" + "=" * 60)
    print("PHASE 32 - USER PROFILE REGRESSION TEST")
    print("=" * 60)

    db = SessionLocal()

    backups = {}

    try:

        user = (
            db.query(User)
            .order_by(User.id.asc())
            .first()
        )

        assert user is not None

        # ==================================================
        # BACKUP EXISTING DATA
        # ==================================================

        for key in TEST_KEYS:

            rows = (
                db.query(Preference)
                .filter(
                    Preference.user_id == user.id,
                    Preference.key == key,
                )
                .all()
            )

            backups[key] = [
                {
                    "id": row.id,
                    "value": row.value,
                }
                for row in rows
            ]

            for row in rows:
                db.delete(row)

        db.commit()

        # ==================================================
        # MEMORY ENGINE
        # ==================================================

        engine = MemoryEngine()

        engine._generate_response = (
            lambda context:
            "[TEST PROFILE RESPONSE]"
        )

        # ==================================================
        # TEST 1 — NORMAL PROMPT
        # ==================================================

        result = engine.process_prompt(
            db=db,
            user_id=user.id,
            prompt="Explain binary search.",
        )

        assert result["profile_updates"] == [], (
            "Normal prompt incorrectly created "
            "profile memory."
        )

        print(
            "\nNormal prompt correctly ignored."
        )

        # ==================================================
        # TEST 2 — MULTIPLE PROFILE FACTS
        # ==================================================

        result = engine.process_prompt(
            db=db,
            user_id=user.id,
            prompt=(
                "My name is Alex. "
                "I live in Bengaluru."
            ),
        )

        updates = {
            item["key"]: item["value"]
            for item in result[
                "profile_updates"
            ]
        }

        assert updates.get(
            "name"
        ) == "Alex"

        assert updates.get(
            "location"
        ) == "Bengaluru"

        print(
            "Multiple profile facts extracted."
        )

        # ==================================================
        # TEST 3 — UPDATE ONLY LOCATION
        # ==================================================

        result = engine.process_prompt(
            db=db,
            user_id=user.id,
            prompt="I live in Mysuru.",
        )

        rows = (
            db.query(Preference)
            .filter(
                Preference.user_id == user.id,
                Preference.key.in_(
                    TEST_KEYS
                ),
            )
            .all()
        )

        profile = {
            row.key: row.value
            for row in rows
        }

        assert profile.get(
            "name"
        ) == "Alex"

        assert profile.get(
            "location"
        ) == "Mysuru"

        assert len(rows) == 2, (
            "Unexpected duplicate profile rows."
        )

        print(
            "Independent profile update passed."
        )

        # ==================================================
        # TEST 4 — PROFILE REACHES CONTEXT
        # ==================================================

        assert (
            "name = Alex"
            in result["context"]
        )

        assert (
            "location = Mysuru"
            in result["context"]
        )

        print(
            "Persistent profile reached context."
        )

        # ==================================================
        # VALIDATION
        # ==================================================

        print("\n" + "=" * 60)
        print("VALIDATION")
        print("=" * 60)

        print(
            "\nNon-profile prompts ignored."
        )

        print(
            "Multiple profile facts supported."
        )

        print(
            "Individual facts update independently."
        )

        print(
            "Duplicate profile rows avoided."
        )

        print(
            "Persistent profile survives across prompts."
        )

        print(
            "Profile memory reaches final context."
        )

        print(
            "\nUSER PROFILE REGRESSION TEST PASSED"
        )

    finally:

        # ==================================================
        # REMOVE TEST DATA
        # ==================================================

        if 'user' in locals():

            (
                db.query(Preference)
                .filter(
                    Preference.user_id
                    == user.id,
                    Preference.key.in_(
                        TEST_KEYS
                    ),
                )
                .delete(
                    synchronize_session=False
                )
            )

            db.commit()

            # ==============================================
            # RESTORE ORIGINAL DATA
            # ==============================================

            for key, rows in backups.items():

                for row in rows:

                    restored = Preference(
                        user_id=user.id,
                        key=key,
                        value=row["value"],
                    )

                    db.add(restored)

            db.commit()

        db.close()


if __name__ == "__main__":
    main()