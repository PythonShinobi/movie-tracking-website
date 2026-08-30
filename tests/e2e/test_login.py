"""End-to-end tests for login routes."""

def test_login_with_valid_credentials(client):
    # First create a user through registration.
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


def test_login_with_incorrect_password(client):
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

    response = client.post(
        "/auth/login",
        data={
            "email": "john@example.com",
            "password": "wrongpassword",
            "submit": "Login",
        },
    )

    assert response.status_code == 200