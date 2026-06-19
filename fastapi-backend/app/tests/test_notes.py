def get_token(client):
    """
    Create a test user and return JWT token.
    """

    client.post(
        "/api/v1/auth/register",
        json={
            "email": "note@example.com",
            "password": "password123"
        }
    )

    response = client.post(
        "/api/v1/auth/login",
        json={
            "email": "note@example.com",
            "password": "password123"
        }
    )

    assert response.status_code == 200

    payload = response.json()

    assert payload["success"] is True

    data = payload["data"]

    assert "access_token" in data

    return data["access_token"]


def test_create_note(test_client):
    token = get_token(test_client)

    response = test_client.post(
        "/api/v1/notes",
        json={
            "title": "Test Note",
            "content": "Hello"
        },
        headers={
            "Authorization": f"Bearer {token}"
        }
    )

    assert response.status_code == 201

    data = response.json()

    assert data["title"] == "Test Note"
    assert data["content"] == "Hello"
    assert "id" in data
    assert "owner_id" in data


def test_get_notes(test_client):
    token = get_token(test_client)

    create_response = test_client.post(
        "/api/v1/notes",
        json={
            "title": "My Note",
            "content": "Content"
        },
        headers={
            "Authorization": f"Bearer {token}"
        }
    )

    assert create_response.status_code == 201

    response = test_client.get(
        "/api/v1/notes",
        headers={
            "Authorization": f"Bearer {token}"
        }
    )

    assert response.status_code == 200

    data = response.json()

    assert isinstance(data, list)
    assert len(data) >= 1

    first_note = data[0]

    assert "id" in first_note
    assert "title" in first_note
    assert "content" in first_note 

    assert first_note["title"] == "My Note"