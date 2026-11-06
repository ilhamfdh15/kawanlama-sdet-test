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

# ==========================================
# TC 1: Create User
# Objective: Verify that a new user can be successfully created via the API.
# Steps: Send POST request to /user with dynamic user payload.
# Expected Result: Status code 200, and the response message matches the user ID.
# ==========================================
def test_create_user(api_context, dynamic_user):
    response = api_context.post("user", data=dynamic_user)
    assert response.status == 200
    data = response.json()
    assert data["message"] == str(dynamic_user["id"])


# ==========================================
# TC 2: Get User by Username
# Objective: Verify that an existing user's details can be retrieved.
# Steps: Send GET request to /user/{username} using the previously created username.
# Expected Result: Status code 200, and the returned username matches the requested username.
# ==========================================
def test_get_user(api_context, dynamic_user):
    response = api_context.get(f"user/{dynamic_user['username']}")
    assert response.status == 200
    data = response.json()
    assert data["username"] == dynamic_user["username"]


# ==========================================
# TC 3: Update User
# Objective: Verify that an existing user's information can be updated.
# Steps:
#   1. Modify the user's firstName in the payload.
#   2. Send PUT request to /user/{username} with the updated payload.
#   3. Send GET request to verify the change was saved.
# Expected Result: Both requests return status 200, and the GET request reflects the new firstName.
# ==========================================
def test_update_user(api_context, dynamic_user):
    updated_user = dynamic_user.copy()
    updated_user["firstName"] = "Senior QA"

    put_response = api_context.put(f"user/{dynamic_user['username']}", data=updated_user)
    assert put_response.status == 200

    get_response = api_context.get(f"user/{dynamic_user['username']}")
    assert get_response.status == 200
    assert get_response.json()["firstName"] == "Senior QA"


# ==========================================
# TC 4: User Login
# Objective: Verify that a user can successfully log into the system.
# Steps: Send GET request to /user/login with the username and password as query parameters.
# Expected Result: Status code 200, and the response text contains a login session confirmation.
# ==========================================
def test_user_login(api_context, dynamic_user):
    response = api_context.get(f"user/login", params={
        "username": dynamic_user["username"],
        "password": dynamic_user["password"]
    })
    assert response.status == 200
    assert "logged in user session" in response.text()


# ==========================================
# TC 5: User Logout
# Objective: Verify that a user can successfully log out of the current session.
# Steps: Send GET request to /user/logout.
# Expected Result: Status code 200.
# ==========================================
def test_user_logout(api_context):
    response = api_context.get("user/logout")
    assert response.status == 200


# ==========================================
# TC 6: Delete User
# Objective: Verify that an existing user can be deleted from the system.
# Steps: Send DELETE request to /user/{username}.
# Expected Result: Status code 200.
# ==========================================
def test_delete_user(api_context, dynamic_user):
    response = api_context.delete(f"user/{dynamic_user['username']}")
    assert response.status == 200


# ==========================================
# TC 7: Get Non-Existent User (Negative Test)
# Objective: Verify that the API handles requests for non-existent or deleted users properly.
# Steps: Send GET request to /user/{username} using a fake or deleted username.
# Expected Result: Status code 404 (Not Found).
# ==========================================
def test_get_nonexistent_user(api_context):
    response = api_context.get("user/nonexistent_fake_user_99999")
    assert response.status == 404