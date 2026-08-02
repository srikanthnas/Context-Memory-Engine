from database.connection import SessionLocal
from database.models import Preference, User
from services.preference_service import PreferenceService


TEST_KEY = "phase32_test_location"


def main():

    print("\n" + "=" * 60)
    print("PHASE 32.2 - USER PROFILE UPSERT TEST")
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

        # ----------------------------------------------
        # Remove previous test data
        # ----------------------------------------------

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
        # CREATE
        # ==============================================

        first = (
            PreferenceService.upsert_profile_fact(
                db=db,
                user_id=user.id,
                key=TEST_KEY,
                value="Bengaluru",
            )
        )

        first_id = first.id

        print("\nINITIAL PROFILE FACT")
        print("-" * 60)

        print(
            f"ID={first.id} | "
            f"{first.key} = {first.value}"
        )

        assert first.value == "Bengaluru"

        # ==============================================
        # UPDATE
        # ==============================================

        second = (
            PreferenceService.upsert_profile_fact(
                db=db,
                user_id=user.id,
                key=TEST_KEY,
                value="Mysuru",
            )
        )

        print("\nUPDATED PROFILE FACT")
        print("-" * 60)

        print(
            f"ID={second.id} | "
            f"{second.key} = {second.value}"
        )

        # Same row should have been updated.

        assert second.id == first_id

        assert second.value == "Mysuru"

        # ==============================================
        # VERIFY DATABASE
        # ==============================================

        rows = (
            db.query(Preference)
            .filter(
                Preference.user_id == user.id,
                Preference.key == TEST_KEY,
            )
            .all()
        )

        assert len(rows) == 1, (
            "Duplicate profile rows were created."
        )

        assert rows[0].value == "Mysuru"

        # ==============================================
        # VALIDATION
        # ==============================================

        print("\n" + "=" * 60)
        print("VALIDATION")
        print("=" * 60)

        print("\nProfile fact created successfully.")
        print("Existing profile fact updated successfully.")
        print("No duplicate profile row created.")
        print("Latest profile value preserved.")

        print(
            "\nUSER PROFILE UPSERT TEST PASSED"
        )

    finally:

        # ----------------------------------------------
        # Clean test data
        # ----------------------------------------------

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