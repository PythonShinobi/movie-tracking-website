"""End-to-end tests for authentication routes."""

def test_register_endpoint(client):
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
    assert response.headers["Location"] == "/auth/register"