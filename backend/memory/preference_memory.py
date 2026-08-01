from sqlalchemy.orm import Session

from database.models import Preference


class PreferenceMemory:
    """
    Retrieves stored user preferences together with
    adaptive-memory metadata.
    """

    @staticmethod
    def get_preferences(
        db: Session,
        user_id: int,
    ):
        """
        Retrieve all preferences belonging to a user.
        """

        preferences = (
            db.query(Preference)
            .filter(
                Preference.user_id == user_id
            )
            .all()
        )

        return [
            {
                "id": preference.id,
                "user_id": preference.user_id,
                "key": preference.key,
                "value": preference.value,
                "importance": preference.importance,
                "access_count": preference.access_count,
                "last_accessed": (
                    preference.last_accessed.isoformat()
                    if preference.last_accessed
                    else None
                ),
            }
            for preference in preferences
        ]