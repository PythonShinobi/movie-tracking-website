"""Application services for authentication."""

from hashlib import sha256
from datetime import datetime, UTC

from app.domain.user import User
from app.adapters.password_hasher import PasswordHasher
from app.services.token import EmailVerificationTokenService
from app.adapters.repository import (
    UserRepository,
    EmailVerificationTokenRepository
)


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
        password_hasher: PasswordHasher,
        token_service: EmailVerificationTokenService | None = None,
        token_repository: EmailVerificationTokenRepository | None = None,
        email_sender=None
    ) -> None:
        self.user_repository = repository
        self.password_hasher = password_hasher
        self.token_service = token_service
        self.token_repository = token_repository
        self.email_sender = email_sender


    def register(
        self,
        email: str,
        username: str,
        password: str,
    ) -> User:
        """Register a new user and create an email verification token."""

        if self.token_service is None:
            # A runtime error occurs when a software program crashes 
            # or stops working while it is running.
            raise RuntimeError(
                "Token service is required for registration."
            )

        if self.token_repository is None:
            raise RuntimeError(
                "Token repository is required for registration."
            )

        if self.email_sender is None:
            raise RuntimeError(
                "Email sender is required for registration."
            )

        # Find a user associated with the supplied email address.
        existing_user = self.user_repository.get_by_email(email)

        # Check if the supplied email is already registered.
        if existing_user is not None:
            # Raise an error if an identical email is in the database.
            raise ValueError("Email already exists.")

        # Hash the user supplied password if the email is new.
        password_hash = self.password_hasher.hash(password)

        # Create the user object.
        user = User(
            id=None,
            email=email,
            username=username,
            password_hash=password_hash
        )

        # Add the current pending user object to the database.
        self.user_repository.add(user)

        # Create a verification token object for the unverified user object.
        token_domain_object, random_token = (
            self.token_service.create_verification_token(user.id)
        )

        # Add the current pending token object to the database.
        self.token_repository.add(token_domain_object)

        # Send an email to the current registered unverified user which 
        # contains the random token.
        self.email_sender(
            to=user.email,
            subject="Verify your email",
            template="auth/email/verify_email",
            username=user.username,
            random_token=random_token
        )

        return user


    def verify_email(self, random_token: str) -> None:
        """Verify a user's email using a verification token."""

        # Encode random token value to bytes.
        random_token_bytes = random_token.encode("utf-8")

        # Hash the random token bytes using sha256.
        random_token_hash = (
            sha256(random_token_bytes)
            .hexdigest()
        )

        # Fetch EmailVerificationToken object from the database
        # that is associated with this random token hash.
        token_domain_object = (
            self
            .token_repository
            .get_by_token_hash(random_token_hash)
        )

        # Executes if the requested token is not returned.
        if token_domain_object is None:
            raise ValueError("Invalid verification token.")

        # Get the current time.
        now = datetime.now(UTC)

        # Check if the token has already been used.
        if token_domain_object.is_used():
            raise ValueError("Verification token has already been used.")

        # Check if the token has already expired.
        if token_domain_object.is_expired(now):
            raise ValueError("Verification token has expired.")

        # Retrieve a user object associated with this token object.
        user = (
            self
            .user_repository
            .get_by_id(token_domain_object.user_id)
        )

        # Executes if the requested user object is not returned.
        if user is None:
            raise ValueError("User does not exist.")

        user.verify_email()  # Call 'verify_email' for the retrieved user object.
        self.user_repository.save(user)

        token_domain_object.mark_used(now)  # Mark the users' token as used after email verification.
        self.token_repository.save(token_domain_object)


    def login(self, email: str, password: str) -> User:
        """Authenticate a user using their email and password."""

        user = self.user_repository.get_by_email(email)

        if user is None:
            raise ValueError("Invalid email or password")

        if not self.password_hasher.verify(password, user.password_hash):
            raise ValueError("Invalid email or password")

        if not user.email_verified:
            raise ValueError("Please verify your email before logging in.")

        return user


    def change_password(
        self,
        user: User,
        old_password: str,
        new_password: str
    ) -> None:
        """Change a user's password after verifying the current password."""

        if not self.password_hasher.verify(old_password, user.password_hash):
            raise ValueError("Invalid current password.")

        new_password_hash = self.password_hasher.hash(new_password)

        user.change_password(new_password_hash)

        self.user_repository.save_password_change(user)


    def delete_account(
        self,
        user_model_object: User,
        password: str
    ) -> None:
        """Delete a user's account after verifying their password."""

        if not self.password_hasher.verify(
            password, user_model_object.password_hash
        ):
            raise ValueError("Invalid password.")

        self.user_repository.delete(user_model_object)


    