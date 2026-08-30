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
from app.adapters.orm import UserModelRecord


def user_object_to_user_model_record(user: User) -> UserModelRecord:
    """Convert a domain User into a SQLAlchemy UserModelRecord."""

    return UserModelRecord(
        id=user.id,
        email=user.email,
        username=user.username,
        password_hash=user.password_hash
    )

def user_model_record_to_user_object(user_model_record: UserModelRecord) -> User:
    """Convert a SQLAlchemy UserModelRecord into a domain User."""

    return User(
        id=user_model_record.id,
        email=user_model_record.email,
        username=user_model_record.username,
        password_hash=user_model_record.password_hash
    )