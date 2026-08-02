from sqlalchemy.orm import Session

from database.models import Preference
from schemas.preference import PreferenceCreate


class PreferenceService:
    """
    Handles preference and persistent user-profile
    storage.
    """

    @staticmethod
    def create_preference(
        db: Session,
        preference: PreferenceCreate,
    ) -> Preference:
        """
        Create a preference using the existing API flow.
        """

        new_preference = Preference(
            user_id=preference.user_id,
            key=preference.key,
            value=preference.value,
        )

        db.add(new_preference)
        db.commit()
        db.refresh(new_preference)

        return new_preference

    @staticmethod
    def get_preferences(
        db: Session,
        user_id: int,
    ):
        """
        Retrieve all preferences for a user.
        """

        return (
            db.query(Preference)
            .filter(
                Preference.user_id == user_id
            )
            .all()
        )

    @staticmethod
    def upsert_profile_fact(
        db: Session,
        user_id: int,
        key: str,
        value: str,
    ) -> Preference:
        """
        Create or update a persistent user-profile fact.

        A user should have only one active value for
        each profile key.

        Example:

        location = Bengaluru

        Later:

        location = Mysuru

        The existing row is updated instead of creating
        another location row.
        """

        existing = (
            db.query(Preference)
            .filter(
                Preference.user_id == user_id,
                Preference.key == key,
            )
            .order_by(
                Preference.id.desc()
            )
            .first()
        )

        if existing:

            existing.value = value

            db.commit()
            db.refresh(existing)

            return existing

        new_fact = Preference(
            user_id=user_id,
            key=key,
            value=value,
        )

        db.add(new_fact)
        db.commit()
        db.refresh(new_fact)

        return new_fact

    @classmethod
    def save_profile_facts(
        cls,
        db: Session,
        user_id: int,
        facts: list,
    ):
        """
        Save multiple extracted profile facts.

        Each fact must contain:

        {
            "key": "...",
            "value": "..."
        }
        """

        saved = []

        for fact in facts:

            key = fact.get("key")
            value = fact.get("value")

            if not key or not value:
                continue

            preference = cls.upsert_profile_fact(
                db=db,
                user_id=user_id,
                key=key,
                value=value,
            )

            saved.append(
                preference
            )

        return saved