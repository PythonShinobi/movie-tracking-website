"""End-to-end tests for authentication routes."""

def test_register_endpoint(client):
    response = client.post(
        "/auth/register",
        json={
            "email": "john@example.com",
            "username": "john",
            "password": "password123",
        },
    )

    assert response.status_code == 201