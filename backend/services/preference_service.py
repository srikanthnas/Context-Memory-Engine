from sqlalchemy.orm import Session

from database.models import Preference
from schemas.preference import PreferenceCreate


class PreferenceService:
    """Handles preference-related business logic."""

    @staticmethod
    def create_preference(
        db: Session,
        preference: PreferenceCreate,
    ) -> Preference:

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
        return (
            db.query(Preference)
            .filter(Preference.user_id == user_id)
            .all()
        )