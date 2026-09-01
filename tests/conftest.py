"""Shared pytest fixtures for the test suite."""

import pytest

from app import create_app
from app.extensions import db
from app.adapters.repository import UserRepository
from app.adapters.password_hasher import PasswordHasher


@pytest.fixture
def app():
    """Create a Flask application for testing."""
    app = create_app("testing")

    with app.app_context():
        db.create_all()

    yield app

    with app.app_context():
        db.drop_all()


@pytest.fixture
def client(app):
    """Create a test client for the Flask application."""
    return app.test_client()


@pytest.fixture
def repository():
    """Provide a user repository for service tests."""
    return UserRepository()


@pytest.fixture
def password_hasher():
    """Provide a password hasher for service tests."""
    return PasswordHasher()