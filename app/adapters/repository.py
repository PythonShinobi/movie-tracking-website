"""Repository implementations for persistent domain objects.

Repositories provide an abstraction over data persistence, allowing the
application and domain layers to work with domain objects without depending
directly on database-specific details.

Examples:
    - UserRepository: Stores and retrieves User objects from the database.
    - get_by_email(): Retrieves a user using their email address.
    - add(): Persists a new User object and assigns its database-generated ID.
"""

from app.extensions import db
from app.domain.user import User
from app.adapters.orm import UserModelRecord
from app.adapters.mappers import (
    user_object_to_user_model_record,
    user_model_record_to_user_object
)


class UserRepository:
    """Provide persistence operations for User domain objects.

    The repository hides database-specific operations from the application
    and domain layers, allowing them to work with User objects without
    depending directly on the ORM.

    Examples:
        - add(): Persists a new User domain object.
        - get_by_email(): Retrieves a User by their email address.
    """

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

    def save_password_change(self, user: User) -> None:
        """Persist a password change for a user."""
    
        user_model_record = UserModelRecord.query.get(user.id)
    
        if user_model_record is None:
            raise ValueError("User does not exist.")
    
        user_model_record.password_hash = user.password_hash