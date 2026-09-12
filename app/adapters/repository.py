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
        - get_by_id(): Retrieves a User by their database ID.
        - get_by_email(): Retrieves a User by their email address.
        - save_password_change(): Persists a user's new password hash.
        - save(): Persists changes made to an existing User.
        - delete(): Removes a User from persistent storage.
    """

    def add(self, user_domain_object: User) -> None:
        """Persist a new user.

        The User domain object is converted into a database record and
        added to the current database session. The session is flushed
        so that the database-generated ID can be copied back to the
        domain object.

        Args:
            user: The User domain object to persist.
        """

        user_model_record = user_object_to_user_model_record(user_domain_object)

        db.session.add(user_model_record)  # Pending database operation.
        db.session.flush()  # Make the generated ID available.

        user_domain_object.id = user_model_record.id  # Copy the ID back to the domain user.

    def get_by_id(self, user_id: int) -> User | None:
        """Retrieve a user by database ID.

        Args:
            user_id: The database ID of the user to retrieve.

        Returns:
            The matching User domain object, or None if the user does not exist.
        """

        user_model_record = db.session.get(UserModelRecord, user_id)

        if user_model_record is None:
            return None

        return user_model_record_to_user_object(user_model_record)

    def get_by_email(self, email: str) -> User | None:
        """Retrieve a user by email address.

        Args:
            email: The email address associated with the user.

        Returns:
            The matching User domain object, or None if no user
            has the supplied email address.
        """

        user_model_record = (
            UserModelRecord
            .query
            .filter_by(email=email)
            .first()
        )

        if user_model_record is None:
            return None

        return user_model_record_to_user_object(user_model_record)

    def save_password_change(self, user_domain_object: User) -> None:
        """Persist a password change for an existing user.

        The existing database record is located using the user's ID,
        and its password hash is replaced with the value from the
        domain object.

        Args:
            user: The User domain object containing the updated password hash.

        Raises:
            ValueError: If the user does not exist in persistent storage.
        """

        user_model_record = db.session.get(UserModelRecord, user_domain_object.id)

        if user_model_record is None:
            raise ValueError("User does not exist.")

        user_model_record.password_hash = user_domain_object.password_hash

    def save(self, user_domain_object: User) -> None:
        """Persist changes made to an existing user.

        The existing database record is located using the user's ID,
        and its fields are updated to match the current state of the
        domain object.

        Args:
            user: The User domain object containing the updated state.

        Raises:
            ValueError: If the user does not exist in persistent storage.
        """

        user_model_record = db.session.get(UserModelRecord, user_domain_object.id)

        if user_model_record is None:
            raise ValueError("User does not exist.")

        user_model_record.email = user_domain_object.email
        user_model_record.username = user_domain_object.username
        user_model_record.password_hash = user_domain_object.password_hash
        user_model_record.email_verified = user_domain_object.email_verified

    def delete(self, user_domain_object: User) -> None:
        """Delete a user from persistent storage.

        The corresponding database record is located using the user's ID
        and marked for deletion in the current database session.

        Args:
            user: The User domain object to delete.

        Raises:
            ValueError: If the user does not exist in persistent storage.
        """

        user_model_record = db.session.get(UserModelRecord, user_domain_object.id)

        if user_model_record is None:
            raise ValueError("User does not exist.")

        db.session.delete(user_model_record)


class EmailVerificationTokenRepository:
    """Persist and retrieve email verification tokens.

    This repository provides the persistence operations required by the
    application service without exposing database details to the domain
    model. It converts between EmailVerificationToken domain objects and
    their SQLAlchemy database records.

    The repository supports adding new tokens, finding tokens by their
    hashed value, and saving changes when a token is marked as used.
    """

    def add(self, token_domain_object: EmailVerificationToken) -> None:
        """Add a new verification token to the database.

        The domain token is converted into a database record and added
        to the current SQLAlchemy session. The session is flushed so
        that the database-generated ID can be copied back to the domain
        object.

        Args:
            token: The email verification token to persist.
        """

        token_model_record = email_verification_token_object_to_model_record(token_domain_object)

        db.session.add(token_model_record)  # Pending database operation.
        db.session.flush()  # Make the generated ID available.

        token_domain_object.id = token_model_record.id  # Copy the ID back to the domain object.

    def get_by_token_hash(
        self,
        random_token_hash: str
    ) -> EmailVerificationToken | None:
        """Retrieve a verification token using its hashed token value.

        The random verification token is never stored in the database.
        Instead, the hash supplied by the authentication service is used
        to locate the corresponding database record.

        Args:
            random_token_hash: SHA-256 hash of the raw verification token.

        Returns:
            The matching EmailVerificationToken domain object, or None
            if no token with the supplied hash exists.
        """

        token_model_record = (
            EmailVerificationTokenModelRecord
            .query
            .filter_by(random_token_hash=random_token_hash)
            .first()
        )

        if token_model_record is None:
            return None

        return email_verification_token_model_record_to_object(
            token_model_record
        )

    def save(self, token_domain_object: EmailVerificationToken) -> None:
        """Persist changes made to an existing verification token.

        This method retrieves the existing database record using the
        domain object's ID and updates its used_at value. This is used
        when a verification token is marked as used after successful
        email verification.

        Args:
            token: The verification token containing the updated state.

        Raises:
            ValueError: If no database record exists for the token ID.
        """

        token_model_record = db.session.get(
            EmailVerificationTokenModelRecord,
            token_domain_object.id
        )

        if token_model_record is None:
            raise ValueError("Verification token does not exist.")

        token_model_record.used_at = token_domain_object.used_at