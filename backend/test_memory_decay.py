"""
Controlled test for adaptive memory decay.
"""

from datetime import datetime, timedelta

from database.connection import SessionLocal
from database.models import Preference
from memory.memory_decay import MemoryDecay


def main():
    db = SessionLocal()

    test_preference = None

    try:
        # ---------------------------------------
        # Create temporary old memory
        # ---------------------------------------

        test_preference = Preference(
            user_id=2,
            key="__decay_test__",
            value="temporary",
            importance=2.0,
            access_count=5,
            last_accessed=(
                datetime.utcnow()
                - timedelta(days=10)
            ),
        )

        db.add(test_preference)
        db.commit()
        db.refresh(test_preference)

        print("\n" + "=" * 60)
        print("BEFORE DECAY")
        print("=" * 60)

        print("ID:", test_preference.id)
        print("Importance:", test_preference.importance)
        print("Access Count:", test_preference.access_count)
        print("Last Accessed:", test_preference.last_accessed)

        # ---------------------------------------
        # Apply decay
        # ---------------------------------------

        total_decayed = MemoryDecay.apply_decay(
            db=db,
        )

        db.refresh(test_preference)

        print("\n" + "=" * 60)
        print("AFTER DECAY")
        print("=" * 60)

        print("Importance:", test_preference.importance)
        print("Access Count:", test_preference.access_count)
        print("Last Accessed:", test_preference.last_accessed)

        print("\nTotal memories decayed:", total_decayed)

        # ---------------------------------------
        # Verification
        # ---------------------------------------

        expected_importance = 1.95

        assert abs(
            test_preference.importance
            - expected_importance
        ) < 0.0001, (
            "Decay test failed: incorrect importance."
        )

        assert test_preference.access_count == 5, (
            "Decay test failed: access_count changed."
        )

        print("\nDECAY TEST PASSED")

    finally:

        # Remove temporary test preference
        if test_preference is not None:

            test_preference = db.merge(
                test_preference
            )

            db.delete(test_preference)
            db.commit()

        db.close()


if __name__ == "__main__":
    main()
    