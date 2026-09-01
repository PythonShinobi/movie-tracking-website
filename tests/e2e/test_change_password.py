def test_authenticated_user_can_change_password(client):
    """An authenticated user can change their password."""

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
        "/auth/change-password",
        data={
            "old_password": "password123",
            "new_password": "newpassword123",
            "new_password2": "newpassword123",
            "submit": "Update Password",
        },
    )

    assert response.status_code == 302