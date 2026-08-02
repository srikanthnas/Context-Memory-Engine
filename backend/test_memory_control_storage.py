from database.connection import SessionLocal
from database.models import Preference, User
from services.preference_service import PreferenceService


TEST_KEY = "phase33_preferred_ide"


def main():

    print("\n" + "=" * 60)
    print("PHASE 33.2 - MEMORY CONTROL STORAGE TEST")
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

        # ==============================================
        # CLEAN PREVIOUS TEST DATA
        # ==============================================

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

        # ==============================================
        # TEST 1 — REMEMBER
        # ==============================================

        remembered = (
            PreferenceService.upsert_profile_fact(
                db=db,
                user_id=user.id,
                key=TEST_KEY,
                value="VS Code",
            )
        )

        print("\nREMEMBER")
        print("-" * 60)

        print(
            f"ID={remembered.id} | "
            f"{remembered.key} = {remembered.value}"
        )

        assert remembered.value == "VS Code"

        # ==============================================
        # TEST 2 — UPDATE REMEMBERED VALUE
        # ==============================================

        updated = (
            PreferenceService.upsert_profile_fact(
                db=db,
                user_id=user.id,
                key=TEST_KEY,
                value="Eclipse",
            )
        )

        print("\nUPDATE")
        print("-" * 60)

        print(
            f"ID={updated.id} | "
            f"{updated.key} = {updated.value}"
        )

        assert updated.id == remembered.id
        assert updated.value == "Eclipse"

        rows = (
            db.query(Preference)
            .filter(
                Preference.user_id == user.id,
                Preference.key == TEST_KEY,
            )
            .all()
        )

        assert len(rows) == 1, (
            "Remember created duplicate rows."
        )

        # ==============================================
        # TEST 3 — FORGET
        # ==============================================

        removed = (
            PreferenceService.forget_profile_fact(
                db=db,
                user_id=user.id,
                key=TEST_KEY,
            )
        )

        print("\nFORGET")
        print("-" * 60)

        print(
            "Removed:",
            removed,
        )

        assert removed is True

        rows = (
            db.query(Preference)
            .filter(
                Preference.user_id == user.id,
                Preference.key == TEST_KEY,
            )
            .all()
        )

        assert rows == [], (
            "Forgotten memory still exists."
        )

        # ==============================================
        # TEST 4 — FORGET NON-EXISTING MEMORY
        # ==============================================

        removed_again = (
            PreferenceService.forget_profile_fact(
                db=db,
                user_id=user.id,
                key=TEST_KEY,
            )
        )

        assert removed_again is False

        # ==============================================
        # VALIDATION
        # ==============================================

        print("\n" + "=" * 60)
        print("VALIDATION")
        print("=" * 60)

        print("\nExplicit memory stored.")
        print("Existing memory updated.")
        print("Duplicate memory avoided.")
        print("Explicit memory forgotten.")
        print("Missing memory handled safely.")

        print(
            "\nMEMORY CONTROL STORAGE TEST PASSED"
        )

    finally:

        (
            db.query(Preference)
            .filter(
                Preference.key == TEST_KEY
            )
            .delete(
                synchronize_session=False
            )
        )

        db.commit()
        db.close()


if __name__ == "__main__":
    main()