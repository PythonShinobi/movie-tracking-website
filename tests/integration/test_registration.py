"""Integration tests for user registration."""

from app.adapters.orm import UserModelRecord


def test_register_creates_user(client, app):
    response = client.post(
        "/auth/register",
        data={
            "email": "john@example.com",
            "username": "john",
            "password": "password123",
            "password_confirmation": "password123",
            "submit": "Register",
        },
    )

    assert response.status_code == 302

    with app.app_context():
        user = UserModelRecord.query.filter_by(
            email="john@example.com"
        ).first()

        assert user is not None
        assert user.username == "john"
        assert user.password_hash != "password123"