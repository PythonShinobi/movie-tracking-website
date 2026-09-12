"""End-to-end tests for login routes."""
"""End-to-end tests verify complete user workflows through the application.

These tests exercise the application from the external interface, such as
HTTP requests, through the relevant application layers and into the database.
They verify that the different components work together correctly to produce
the expected behavior from a user's perspective.
"""

from app.extensions import db
from app.adapters.orm import UserModelRecord
from app.adapters.password_hasher import PasswordHasher

def test_login_with_valid_credentials(client, app):
    with app.app_context():
        user = UserModelRecord(
            email="john@example.com",
            username="john",
            password_hash=PasswordHasher().hash("password123"),
            email_verified=True,
        )

        db.session.add(user)
        db.session.commit()

    response = client.post(
        "/auth/login",
        data={
            "email": "john@example.com",
            "password": "password123",
            "submit": "Login",
        },
    )

    assert response.status_code == 302


def test_login_with_unknown_email(client):
    response = client.post(
        "/auth/login",
        data={
            "email": "unknown@example.com",
            "password": "password123",
            "submit": "Login",
        },
    )

    assert response.status_code == 200


def test_login_with_incorrect_password(client, app):
    with app.app_context():
        user = UserModelRecord(
            email="john@example.com",
            username="john",
            password_hash=PasswordHasher().hash("password123"),
            email_verified=True,
        )

        db.session.add(user)
        db.session.commit()

    response = client.post(
        "/auth/login",
        data={
            "email": "john@example.com",
            "password": "wrongpassword",
            "submit": "Login",
        },
    )

    assert response.status_code == 200


def test_authenticated_user_can_access_protected_route(client, app):
    with app.app_context():
        user = UserModelRecord(
            email="john@example.com",
            username="john",
            password_hash=PasswordHasher().hash("password123"),
            email_verified=True,
        )

        db.session.add(user)
        db.session.commit()

    client.post(
        "/auth/login",
        data={
            "email": "john@example.com",
            "password": "password123",
            "submit": "Login",
        },
    )

    response = client.get("/profile")

    assert response.status_code == 200


def test_unauthenticated_user_cannot_access_protected_route(client):
    response = client.get("/profile")

    assert response.status_code == 302