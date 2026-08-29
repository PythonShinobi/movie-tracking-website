"""Shared pytest fixtures for the test suite."""

import pytest

from app import create_app
from app.extensions import db


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