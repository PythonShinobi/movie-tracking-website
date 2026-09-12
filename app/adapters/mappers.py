"""Map between domain objects and persistence models.

Mappers translate objects between the domain layer and the persistence
layer, keeping domain models independent of database-specific models.

Examples:
    - user_object_to_user_model_record(): Converts a User domain object
      into a UserModelRecord for database persistence.
    - user_model_record_to_user_object(): Converts a UserModelRecord from
      the database into a User domain object.
"""

from app.domain.user import User
from app.domain.email_verification_token import EmailVerificationToken
from app.adapters.orm import (
    UserModelRecord,
    EmailVerificationTokenModelRecord
)


def user_object_to_user_model_record(user: User) -> UserModelRecord:
    """Convert a domain User into a SQLAlchemy UserModelRecord."""

    return UserModelRecord(
        id=user.id,
        email=user.email,
        username=user.username,
        password_hash=user.password_hash,
        email_verified=user.email_verified
    )

def user_model_record_to_user_object(user_model_record: UserModelRecord) -> User:
    """Convert a SQLAlchemy UserModelRecord into a domain User."""

    return User(
        id=user_model_record.id,
        email=user_model_record.email,
        username=user_model_record.username,
        password_hash=user_model_record.password_hash,
        email_verified=user_model_record.email_verified
    )

def email_verification_token_object_to_model_record(
    token: EmailVerificationToken
) -> EmailVerificationTokenModelRecord:
    """Convert a domain email verification token into an ORM record."""

    return EmailVerificationTokenModelRecord(
        id=token.id,
        user_id=token.user_id,
        random_token_hash=token.random_token_hash,
        expires_at=token.expires_at,
        used_at=token.used_at
    )

def email_verification_token_model_record_to_object(
    token_model_record: EmailVerificationTokenModelRecord
) -> EmailVerificationToken:
    """Convert an ORM email verification token into a domain object."""

    return EmailVerificationToken(
        id=token_model_record.id,
        user_id=token_model_record.user_id,
        random_token_hash=token_model_record.random_token_hash,
        expires_at=token_model_record.expires_at,
        used_at=token_model_record.used_at
    )