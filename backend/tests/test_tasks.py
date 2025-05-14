Here are the comprehensive unit tests for the FastAPI endpoints:

```python
from fastapi.testclient import TestClient
from main import app
from datetime import datetime

client = TestClient(app)

# Test Creating Task
def test_create_task():
    response = client.post(
        "/tasks/",
        json={
            "title": "test task",
            "description": "test description",
            "due_date": datetime.now().isoformat(),
            "priority": 1,
            "status": False,
            "owner_id": 1,
        },
    )
    assert response.status_code == 200
    assert response.json()["title"] == "test task"

# Test Creating Task with Invalid Data
def test_create_task_invalid_data():
    response = client.post(
        "/tasks/",
        json={
            "title": "",
            "description": "test description",
            "due_date": datetime.now().isoformat(),
            "priority": 1,
            "status": False,
            "owner_id": 1,
        },
    )
    assert response.status_code == 422

# Test Reading Tasks
def test_read_tasks():
    response = client.get("/tasks/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

# Test Reading Task
def test_read_task():
    response = client.get("/tasks/1")
    assert response.status_code == 200
    assert "title" in response.json()

# Test Reading Non-Existent Task
def test_read_non_existent_task():
    response = client.get("/tasks/1000000")
    assert response.status_code == 404

# Test Updating Task
def test_update_task():
    response = client.patch(
        "/tasks/1",
        json={
            "title": "updated test task",
            "description": "updated test description",
            "due_date": datetime.now().isoformat(),
            "priority": 1,
            "status": True,
        },
    )
    assert response.status_code == 200
    assert response.json()["title"] == "updated test task"

# Test Updating Non-Existent Task
def test_update_non_existent_task():
    response = client.patch(
        "/tasks/1000000",
        json={
            "title": "updated test task",
            "description": "updated test description",
            "due_date": datetime.now().isoformat(),
            "priority": 1,
            "status": True,
        },
    )
    assert response.status_code == 404

# Test Deleting Task
def test_delete_task():
    response = client.delete("/tasks/1")
    assert response.status_code == 200
    assert "id" in response.json()

# Test Deleting Non-Existent Task
def test_delete_non_existent_task():
    response = client.delete("/tasks/1000000")
    assert response.status_code == 404
```

These tests cover the following scenarios:

- Success cases: The tests `test_create_task`, `test_read_tasks`, `test_read_task`, `test_update_task`, and `test_delete_task` ensure that the endpoints work as expected when provided with valid data.
- Error cases: The tests `test_create_task_invalid_data`, `test_read_non_existent_task`, `test_update_non_existent_task`, and `test_delete_non_existent_task` check how the endpoints handle errors such as invalid data or requests for non-existent resources.
- Data validation: The test `test_create_task_invalid_data` checks that the endpoint validates the provided data and rejects invalid inputs.
- Edge cases: Reading, updating, and deleting a non-existent task are edge cases that test how the API handles uncommon but possible situations.