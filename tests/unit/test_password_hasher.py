"""Tests for the bcrypt password hasher."""

from app.adapters.password_hasher import PasswordHasher

def test_hash_does_not_return_plaintext_password() -> None:
    hasher = PasswordHasher()

    password = "password123"

    password_hash = hasher.hash(password)

    assert password_hash != password

def test_hash_returns_different_hashes_for_same_password() -> None:
    hasher = PasswordHasher()

    password = "password123"

    first_hash = hasher.hash(password)
    second_hash = hasher.hash(password)

    assert first_hash != second_hash

def test_verify_returns_true_for_correct_password() -> None:
    hasher = PasswordHasher()

    password = "password123"

    password_hash = hasher.hash(password)

    assert hasher.verify(password, password_hash) is True

def test_verify_returns_false_for_incorrect_password() -> None:
    hasher = PasswordHasher()

    password_hash = hasher.hash("password123")

    assert hasher.verify("wrong-password", password_hash) is False