Here are comprehensive unit tests for the FastAPI endpoints:

```python
from fastapi.testclient import TestClient
import pytest

client = TestClient(app)

def test_register_new_user():
    user_data = {"username": "testuser", "email": "testuser@example.com", "password": "testpassword"}
    response = client.post("/register", json=user_data)
    assert response.status_code == 200
    assert response.json()["username"] == "testuser"
    assert "email" in response.json()

def test_register_existing_user():
    user_data = {"username": "testuser", "email": "testuser@example.com", "password": "testpassword"}
    response = client.post("/register", json=user_data)
    assert response.status_code == 400
    assert response.json() == {"detail": "Username already registered"}

def test_register_with_invalid_email():
    user_data = {"username": "testuser", "email": "invalid", "password": "testpassword"}
    response = client.post("/register", json=user_data)
    assert response.status_code == 422
    assert "value is not a valid email address" in str(response.json())

def test_register_with_short_password():
    user_data = {"username": "testuser", "email": "testuser@example.com", "password": "short"}
    response = client.post("/register", json=user_data)
    assert response.status_code == 422
    assert "ensure this value has at least 8 characters" in str(response.json())

def test_login_valid_user():
    login_data = {"username": "testuser", "password": "testpassword"}
    response = client.post("/login", data=login_data)
    assert response.status_code == 200
    assert "access_token" in response.json()

def test_login_invalid_user():
    login_data = {"username": "invaliduser", "password": "testpassword"}
    response = client.post("/login", data=login_data)
    assert response.status_code == 400
    assert response.json() == {"detail": "Invalid username or password"}

def test_login_wrong_password():
    login_data = {"username": "testuser", "password": "wrongpassword"}
    response = client.post("/login", data=login_data)
    assert response.status_code == 400
    assert response.json() == {"detail": "Invalid username or password"}

def test_login_no_password():
    login_data = {"username": "testuser"}
    response = client.post("/login", data=login_data)
    assert response.status_code == 422
    assert "field required" in str(response.json())
```

These tests cover the following scenarios:

1. Register a new user successfully
2. Attempt to register an existing user (error case)
3. Attempt to register with an invalid email (data validation)
4. Attempt to register with a password shorter than 8 characters (data validation)
5. Login with valid credentials successfully
6. Attempt to login with a non-existing username (error case)
7. Attempt to login with a wrong password (error case)
8. Attempt to login without providing a password (edge case)