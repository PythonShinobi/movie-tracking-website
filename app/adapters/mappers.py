"""Map between domain objects and persistence models."""

from app.domain.user import User
from app.adapters.orm import UserModel

def user_to_model(user: User) -> UserModel:
    """Convert a domain User into a SQLAlchemy UserModel."""

    return UserModel(
        id=user.id,
        email=user.email,
        username=user.username,
        password_hash=user.password_hash
    )

def model_to_user(user_model: UserModel) -> User:
    """Convert a SQLAlchemy UserModel into a domain User."""

    return User(
        id=user_model.id,
        email=user_model.email,
        username=user_model.username,
        password_hash=user_model.password_hash
    )