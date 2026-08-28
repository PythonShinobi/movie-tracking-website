"""Repository implementations for persistent domain objects."""

from app.extensions import db
from app.domain.user import User
from app.adapters.orm import UserModelRecord
from app.adapters.mappers import (
    user_object_to_user_model_record,
    user_model_record_to_user_object
)


class UserRepository:
    """Provide persistence operations for User domain objects."""

    def add(self, user: User) -> None:
        """Persist a new user."""

        user_model_record = user_object_to_user_model_record(user)

        db.session.add(user_model_record)  # Pending database operation.
        db.session.flush()  # Send pending changes to the database so the generated ID is available.

        user.id = user_model_record.id  # Copy the database-generated ID back to the domain user.

    def get_by_email(self, email: str) -> User | None:
        """Retrieve a user by email address."""

        user_model_record = UserModelRecord.query.filter_by(email=email).first()

        if user_model_record is None:
            return None

        return user_model_record_to_user_object(user_model_record)