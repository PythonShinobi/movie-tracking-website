"""Tests for the authentication application service."""

import pytest

from app.domain.user import User
from app.services.authentication import AuthenticationService


class FakeRepository:
    """In-memory repository used to test the authentication service."""

    def __init__(self) -> None:
        self.users = []

    def add(self, user: User) -> None:
        """Stores a user in memory."""

        self.users.append(user)

    def get_by_email(self, email: str) -> User | None:
        """Find a user by email."""

        return next(
            (user for user in self.users if user.email == email), 
            None
        )


class FakePasswordHasher:
    """Fake password hasher used to test the service."""

    def hash(self, password: str) -> str:
        """Return a predictable password hash."""

        return f"hashed-{password}"


def test_register_creates_user() -> None:
    repository = FakeRepository()
    password_hasher = FakePasswordHasher()

    service = AuthenticationService(
        repository=repository,
        password_hasher=password_hasher
    )

    user = service.register(
        email="john@example.com",
        username="john",
        password="password123"
    )

    assert user.email == "john@example.com"
    assert user.username == "john"
    assert user.password_hash == "hashed-password123"


def test_register_adds_user_to_repository() -> None:
    repository = FakeRepository()
    password_hasher = FakePasswordHasher()

    service = AuthenticationService(
        repository=repository,
        password_hasher=password_hasher
    )

    user = service.register(
        email="john@example.com",
        username="john",
        password="password123"
    )

    assert user in repository.users


def test_register_hashes_password() -> None:
    repository = FakeRepository()
    password_hasher = FakePasswordHasher()

    service = AuthenticationService(
        repository=repository,
        password_hasher=password_hasher
    )

    user = service.register(
        email="john@example.com",
        username="john",
        password="password123"
    )

    assert user.password_hash != "password123"
    assert user.password_hash == "hashed-password123"


def test_register_rejects_existing_email() -> None:
    repository = FakeRepository()
    password_hasher = FakePasswordHasher()

    existing_user = User(
        id=1,
        email="john@example.com",
        username="john",
        password_hash="existing-hash"
    )

    repository.add(existing_user)

    service = AuthenticationService(
        repository=repository,
        password_hasher=password_hasher
    )

    with pytest.raises(ValueError, match="Email already exists."):
        service.register(
            email="john@example.com",
            username="john",
            password="password123"
        )