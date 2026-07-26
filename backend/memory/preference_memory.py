from sqlalchemy.orm import Session

from database.models import Preference


class PreferenceMemory:

    @staticmethod
    def get_preferences(db: Session, user_id: int):

        preferences = (
            db.query(Preference)
            .filter(Preference.user_id == user_id)
            .all()
        )

        return [
            {
                "key": preference.key,
                "value": preference.value,
            }
            for preference in preferences
        ]