"""Application services for authentication."""

from app.domain.user import User
from app.adapters.repository import UserRepository
from app.adapters.password_hasher import PasswordHasher

class AuthenticationService:
    """Provide authentication-related application services."""

    def __init__(
            self, 
            repository: UserRepository,
            password_hasher: PasswordHasher
    ) -> None:
        self.user_repository = repository
        self.password_hasher = password_hasher

    def register(
            self,
            email: str,
            username: str,
            password: str,
    ) -> User:
        """Register a new user."""

        existing_user = self.user_repository.get_by_email(email)

        if existing_user is not None:
            raise ValueError("Email already exists.")

        password_hash = self.password_hasher.hash(password)

        user = User(
            id=None,
            email=email,
            username=username,
            password_hash=password_hash
        )

        self.user_repository.add(user)

        return user