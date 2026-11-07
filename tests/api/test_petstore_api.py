import pytest
import uuid

@pytest.fixture
def user_payload():
    """Generates a unique user payload dictionary for a test."""
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

@pytest.fixture
def existing_user(api_context, user_payload):
    # Setup: Create the user
    create_response = api_context.post("user", data=user_payload)
    assert create_response.status == 200, "Fixture Setup Failed: Could not create user"

    yield user_payload

    # Teardown: Clean up the user to prevent database bloat
    # We ignore 404s here in case the test itself already deleted the user (like TC6)
    api_context.delete(f"user/{user_payload['username']}")


# ==========================================
# TC 1: Create User
# ==========================================
def test_create_user(api_context, user_payload):
    """Uses user_payload directly since we are testing the creation endpoint."""
    response = api_context.post("user", data=user_payload)
    assert response.status == 200
    data = response.json()
    assert data["message"] == str(user_payload["id"])

    # Clean up so we don't leave junk data after the test
    api_context.delete(f"user/{user_payload['username']}")


# ==========================================
# TC 2: Get User by Username
# ==========================================
def test_get_user(api_context, existing_user):
    """Uses existing_user fixture, ensuring the user is already in the database."""
    response = api_context.get(f"user/{existing_user['username']}")
    assert response.status == 200
    data = response.json()
    assert data["username"] == existing_user["username"]


# ==========================================
# TC 3: Update User
# ==========================================
def test_update_user(api_context, existing_user):
    updated_user = existing_user.copy()
    updated_user["firstName"] = "Senior QA"

    put_response = api_context.put(f"user/{existing_user['username']}", data=updated_user)
    assert put_response.status == 200

    get_response = api_context.get(f"user/{existing_user['username']}")
    assert get_response.status == 200
    assert get_response.json()["firstName"] == "Senior QA"


# ==========================================
# TC 4: User Login
# ==========================================
def test_user_login(api_context, existing_user):
    response = api_context.get("user/login", params={
        "username": existing_user["username"],
        "password": existing_user["password"]
    })
    assert response.status == 200
    assert "logged in user session" in response.text()


# ==========================================
# TC 5: User Logout
# ==========================================
def test_user_logout(api_context):
    """Stateless call, no user required."""
    response = api_context.get("user/logout")
    assert response.status == 200


# ==========================================
# TC 6: Delete User
# ==========================================
def test_delete_user(api_context, existing_user):
    response = api_context.delete(f"user/{existing_user['username']}")
    assert response.status == 200

    # Verify the user is actually gone
    verify_response = api_context.get(f"user/{existing_user['username']}")
    assert verify_response.status == 404


# ==========================================
# TC 7: Get Non-Existent User (Negative Test)
# ==========================================
def test_get_nonexistent_user(api_context):
    response = api_context.get("user/nonexistent_fake_user_99999")
    assert response.status == 404