from app.adapters.orm import UserModelRecord


def test_authenticated_user_can_delete_account(client, app):
    client.post(
        "/auth/register",
        data={
            "email": "john@example.com",
            "username": "john",
            "password": "password123",
            "password_confirmation": "password123",
            "submit": "Register",
        }
    )

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
        user = UserModelRecord.query.filter_by(email="john@example.com").first()
        
        assert user is None


def test_delete_account_rejects_incorrect_password(client, app):
    """An incorrect password does not delete the account."""

    client.post(
        "/auth/register",
        data={
            "email": "john@example.com",
            "username": "john",
            "password": "password123",
            "password_confirmation": "password123",
            "submit": "Register",
        },
    )

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