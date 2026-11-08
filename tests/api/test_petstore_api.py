import pytest

@pytest.fixture
def user_payload():
    return {
        "id": 998877,
        "username": "sdet_tester_99",
        "firstName": "SDET",
        "lastName": "Tester",
        "email": "sdet@example.com",
        "password": "Password123",
        "phone": "08996001601",
        "userStatus": 1
    }

@pytest.fixture
def create_user_cleanup(api_context):
    users_to_delete = []

    yield users_to_delete

    for username in users_to_delete:
        api_context.delete(f"user/{username}")

def test_create_user(api_context, user_payload, create_user_cleanup):
    response = api_context.post("user", data=user_payload)
    create_user_cleanup.append(user_payload["username"])

    assert response.status == 200
    assert response.json()["message"] == str(user_payload["id"])

def test_get_user(api_context, user_payload, create_user_cleanup):
    api_context.post("user", data=user_payload)
    create_user_cleanup.append(user_payload["username"])

    response = api_context.get(f"user/{user_payload['username']}")
    assert response.status == 200
    assert response.json()["username"] == user_payload["username"]

def test_user_login(api_context, user_payload, create_user_cleanup):
    api_context.post("user", data=user_payload)
    create_user_cleanup.append(user_payload["username"])

    response = api_context.get("user/login", params={
        "username": user_payload["username"],
        "password": user_payload["password"]
    })

    assert response.status == 200
    assert "logged in user session" in response.json()["message"]

def test_user_logout(api_context):
    response = api_context.get("user/logout")
    assert response.status == 200

def test_delete_user(api_context, user_payload):
    api_context.post("user", data=user_payload)

    response = api_context.delete(f"user/{user_payload['username']}")
    assert response.status == 200

    check_response = api_context.get(f"user/{user_payload['username']}")
    assert check_response.status == 404

def test_get_nonexistent_user(api_context):
    response = api_context.get("user/invalid_random_user_name_999")
    assert response.status == 404