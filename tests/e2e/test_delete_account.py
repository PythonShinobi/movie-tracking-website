from app.extensions import db
from app.adapters.orm import UserModelRecord
from app.adapters.password_hasher import PasswordHasher


def test_authenticated_user_can_delete_account(client, app):
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
            "submit": "Login"
        }
    )

    response = client.post(
        "/auth/delete-account",
        data={
            "password": "password123",
            "confirm": "y",
            "submit": "Delete Account"
        }
    )

    assert response.status_code == 302

    with app.app_context():
        user = UserModelRecord.query.filter_by(
            email="john@example.com"
        ).first()

        assert user is None


def test_delete_account_rejects_incorrect_password(client, app):
    """An incorrect password does not delete the account."""

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

    response = client.post(
        "/auth/delete-account",
        data={
            "password": "wrongpassword",
            "confirm": "y",
            "submit": "Delete Account",
        },
    )

    assert response.status_code == 200

    with app.app_context():
        user = UserModelRecord.query.filter_by(
            email="john@example.com"
        ).first()

        assert user is not None