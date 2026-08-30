"""Application services for authentication."""

from app.domain.user import User
from app.adapters.repository import UserRepository
from app.adapters.password_hasher import PasswordHasher


class AuthenticationService:
    """Provide authentication-related application services.

    This service coordinates authentication use cases by combining domain
    objects with the required application dependencies. It keeps
    authentication workflows independent of HTTP routes and infrastructure
    details.

    Examples:
        - register(): Creates and persists a new user after validating that
          the email is not already registered.
        - login(): Authenticates a user by verifying their email and password.
    """

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

    def login(self, email: str, password: str) -> User:
        """Authenticate a user using their email and password."""

        user = self.user_repository.get_by_email(email)

        if user is None:
            raise ValueError("Invalid email or password")

        if not self.password_hasher.verify(password, user.password_hash):
            raise ValueError("Invalid email or password")

        return user