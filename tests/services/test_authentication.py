"""Tests for the authentication application service."""

import pytest

from app.extensions import db
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

    def verify(self, password: str, password_hash: str) -> bool:
        """Verify a password against the predictable fake hash."""
        return self.hash(password) == password_hash


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


def test_login_returns_user_with_valid_credentials() -> None:
    repository = FakeRepository()
    password_hasher = FakePasswordHasher()

    user = User(
        id=1,
        email="john@example.com",
        username="john",
        password_hash="hashed-password123"
    )

    repository.add(user)

    service = AuthenticationService(
        repository=repository,
        password_hasher=password_hasher
    )

    result = service.login(
        email="john@example.com",
        password="password123"
    )

    assert result == user


def test_login_rejects_unknown_email() -> None:
    repository = FakeRepository()
    password_hasher = FakePasswordHasher()

    service = AuthenticationService(
        repository=repository,
        password_hasher=password_hasher
    )

    with pytest.raises(ValueError, match="Invalid email or password"):
        service.login(
            email="uknown@example.com",
            password="password123"
        )


def test_login_rejects_incorrect_password() -> None:
    repository = FakeRepository()
    password_hasher = FakePasswordHasher()

    user = User(
        id=1,
        email="john@example.com",
        username="john",
        password_hash="hashed_password"
    )

    repository.add(user)

    service = AuthenticationService(
        repository=repository,
        password_hasher=password_hasher
    )

    password_hasher.should_verify = False

    with pytest.raises(ValueError, match="Invalid email or password"):
        service.login(
            email="john@example.com",
            password="wrong_password"
        )


def test_change_password_updates_password(app, repository, password_hasher):
    """Changing a password replaces the user's existing password hash."""

    with app.app_context():
        service = AuthenticationService(repository, password_hasher)

        user = User(
            id=None,
            email="john@example.com",
            username="john",
            password_hash=password_hasher.hash("oldpassword")
        )

        repository.add(user)
        db.session.commit()

        old_hash = user.password_hash

        service.change_password(
            user=user,
            old_password="oldpassword",
            new_password="newpassword"
        )

        assert user.password_hash != old_hash
        assert password_hasher.verify(
            "newpassword",
            user.password_hash
        )


def test_change_password_rejects_incorrect_current_password(
    app,
    repository,
    password_hasher
):
    """Changing a password fails when the current password is incorrect."""

    with app.app_context():
        service = AuthenticationService(repository, password_hasher)

        user = User(
            id=None,
            email="john@example.com",
            username="john",
            password_hash=password_hasher.hash("oldpassword")
        )

        repository.add(user)
        db.session.commit()

        with pytest.raises(ValueError, match="Invalid current password."):
            service.change_password(
                user=user,
                old_password="wrongpassword",
                new_password="newpassword"
            )


def test_change_password_saves_user(
    app,
    repository,
    password_hasher
):
    """Changing a password persists the updated user through the repository."""

    with app.app_context():
        service = AuthenticationService(repository, password_hasher)

        user = User(
            id=None,
            email="john@example.com",
            username="john",
            password_hash=password_hasher.hash("oldpassword")
        )

        repository.add(user)
        db.session.commit()

        service.change_password(
            user=user,
            old_password="oldpassword",
            new_password="newpassword"
        )

        db.session.commit()

        saved_user = repository.get_by_email("john@example.com")

        assert saved_user is not None
        assert password_hasher.verify(
            "newpassword",
            saved_user.password_hash
        )