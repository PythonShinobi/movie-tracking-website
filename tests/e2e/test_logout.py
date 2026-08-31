def test_authenticated_user_can_logout(client):
    """An authenticated user can log out."""

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

    response = client.get("/auth/logout")

    assert response.status_code == 302


def test_logged_out_user_cannot_access_protected_route(client):
    """A logged-out user cannot access a protected route."""

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

    client.get("/auth/logout")

    response = client.get("/profile")

    assert response.status_code == 302


def test_logout_removes_authenticated_session(client):
    """Logging out removes the user's authenticated session."""

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

    client.get("/auth/logout")

    response = client.get("/profile")

    assert response.status_code == 302