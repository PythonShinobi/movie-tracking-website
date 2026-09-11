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
from app.domain.email_verification_token import EmailVerificationToken
from app.adapters.orm import UserModelRecord, EmailVerificationTokenModelRecord
from app.adapters.mappers import (
    user_object_to_user_model_record,
    user_model_record_to_user_object,
    email_verification_token_model_record_to_object,
    email_verification_token_object_to_model_record
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


    def get_by_id(self, user_id: int) -> User | None:
        """Retrieve a user by database ID."""

        user_model_record = db.session.get(UserModelRecord, user_id)

        if user_model_record is None:
            return None

        return user_model_record_to_user_object(user_model_record)
    

    def get_by_email(self, email: str) -> User | None:
        """Retrieve a user by email address."""

        user_model_record = (
            UserModelRecord
            .query
            .filter_by(email=email)
            .first()
        )

        if user_model_record is None:
            return None

        return user_model_record_to_user_object(user_model_record)
    

    def save_password_change(self, user: User) -> None:
        """Persist a password change for an existing user."""
    
        user_model_record = db.session.get(UserModelRecord, user.id)
    
        if user_model_record is None:
            raise ValueError("User does not exist.")
    
        user_model_record.password_hash = user.password_hash


    def save(self, user: User) -> None:
        """Persist changes made to an existing user."""
    
        user_model_record = db.session.get(UserModelRecord, user.id)
    
        if user_model_record is None:
            raise ValueError("User does not exist.")
    
        user_model_record.email = user.email
        user_model_record.username = user.username
        user_model_record.password_hash = user.password_hash
        user_model_record.email_verified = user.email_verified


    def delete(self, user: User) -> None:
        """Delete a user from persistent storage."""

        user_model_record = db.session.get(UserModelRecord, user.id)

        if user_model_record is None:
            raise ValueError("User does not exist.")

        db.session.delete(user_model_record)


class EmailVerificationTokenRepository:
    def add(self, token: EmailVerificationToken) -> None:
        token_record = email_verification_token_object_to_model_record(token)

        db.session.add(token_record)  # Pending database operation.
        db.session.flush()  # Send pending changes to database so that the generated ID is available.

        token.id = token_record.id  # Copy the database generated ID back the the token domain object.


    def get_by_token_hash(self, token_hash: str) -> EmailVerificationToken | None:
        token_record = (
            EmailVerificationTokenModelRecord
            .query
            .filter_by(token_hash=token_hash)
            .first()
        )

        if token_record is None:
            return None

        return email_verification_token_model_record_to_object(token_record)


    def save(self, token: EmailVerificationToken) -> None:
        token_record = db.session.get(EmailVerificationTokenModelRecord, token.id)

        if token_record is None:
            raise ValueError("Verification token does not exist.")

        token_record.used_at = token.used_at