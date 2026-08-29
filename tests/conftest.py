"""Shared pytest fixtures for the test suite."""

import pytest

from app import create_app


@pytest.fixture
def app():
    """Create a Flask application for testing."""

    app = create_app("testing")

    return app


@pytest.fixture
def client(app):
    """Create a test client for the Flask application."""

    return app.test_client()