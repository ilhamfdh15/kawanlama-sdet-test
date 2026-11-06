import pytest
import uuid

@pytest.fixture(scope="session")
def dynamic_user():
    """Generates a completely unique user payload for the test session using UUID."""
    unique_suffix = uuid.uuid4().hex[:6]
    return {
        "id": int(str(uuid.uuid4().int)[:8]),
        "username": f"qa_user_{unique_suffix}",
        "firstName": "QA",
        "lastName": "Engineer",
        "email": f"qa_{unique_suffix}@example.com",
        "password": "password123",
        "phone": "1234567890",
        "userStatus": 1
    }

def test_create_user(api_context, dynamic_user):
    response = api_context.post("user", data=dynamic_user)
    assert response.status == 200
    data = response.json()
    assert data["message"] == str(dynamic_user["id"])

def test_get_user(api_context, dynamic_user):
    response = api_context.get(f"user/{dynamic_user['username']}")
    assert response.status == 200
    data = response.json()
    assert data["username"] == dynamic_user["username"]

def test_update_user(api_context, dynamic_user):
    updated_user = dynamic_user.copy()
    updated_user["firstName"] = "Senior QA"

    put_response = api_context.put(f"user/{dynamic_user['username']}", data=updated_user)
    assert put_response.status == 200

    get_response = api_context.get(f"user/{dynamic_user['username']}")
    assert get_response.status == 200
    assert get_response.json()["firstName"] == "Senior QA"

def test_user_login(api_context, dynamic_user):
    response = api_context.get(f"user/login", params={
        "username": dynamic_user["username"],
        "password": dynamic_user["password"]
    })
    assert response.status == 200
    assert "logged in user session" in response.text()

def test_user_logout(api_context):
    response = api_context.get("user/logout")
    assert response.status == 200

def test_delete_user(api_context, dynamic_user):
    response = api_context.delete(f"user/{dynamic_user['username']}")
    assert response.status == 200

def test_get_nonexistent_user(api_context):
    response = api_context.get("user/nonexistent_fake_user_99999")
    assert response.status == 404