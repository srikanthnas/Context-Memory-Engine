from sqlalchemy.orm import Session

from database.models import User
from schemas.user import UserCreate


class UserService:
    """Handles user-related business logic."""

    @staticmethod
    def create_user(db: Session, user: UserCreate) -> User:
        new_user = User(
            username=user.username,
            email=user.email,
        )

        db.add(new_user)
        db.commit()
        db.refresh(new_user)

        return new_user

    @staticmethod
    def get_all_users(db: Session):
        return (
            db.query(User)
            .order_by(User.created_at.desc())
            .all()
        )

    @staticmethod
    def get_user_by_id(db: Session, user_id: int):
        return (
            db.query(User)
            .filter(User.id == user_id)
            .first()
        )