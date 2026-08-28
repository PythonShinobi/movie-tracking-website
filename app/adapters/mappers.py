"""Map between domain objects and persistence models."""

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