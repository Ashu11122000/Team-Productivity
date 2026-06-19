def test_register(test_client):
    response = test_client.post(
        "/api/v1/auth/register",
        json={
            "email": "test@example.com",
            "password": "password123"
        }
    )

    # Assert means check that the response status code is either 200 (OK) or 201 (Created)
    assert response.status_code in (200, 201)

    # payload = response.json() means convert the response body to a Python dictionary
    payload = response.json()

    assert payload["success"] is True
    assert payload["message"] == "User registered successfully"

    assert "data" in payload

    data = payload["data"]

    assert "user_id" in data
    assert data["email"] == "test@example.com"
    assert data["role"] == "MEMBER"


def test_login(test_client):
    test_client.post(
        "/api/v1/auth/register",
        json={
            "email": "login@example.com",
            "password": "password123"
        }
    )

    response = test_client.post(
        "/api/v1/auth/login",
        json={
            "email": "login@example.com",
            "password": "password123"
        }
    )

    assert response.status_code == 200

    payload = response.json()

    assert payload["success"] is True
    assert payload["message"] == "Login successful"

    data = payload["data"]

    assert "access_token" in data
    assert data["token_type"] == "bearer"

    assert "user" in data
    assert data["user"]["email"] == "login@example.com"