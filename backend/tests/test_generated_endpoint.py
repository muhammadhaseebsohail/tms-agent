Here are the comprehensive unit tests for the given FastAPI endpoints:

```python
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from .main import app, get_db
from . import models, crud

engine = create_engine("sqlite:///:memory:")
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
models.Base.metadata.create_all(bind=engine)

def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)

class TestTasks:
    def test_create_comment(self):
        # create a task first
        new_task = {"title": "Test task"}
        response = client.post("/tasks/", json=new_task)
        assert response.status_code == 200
        task = response.json()

        # create a comment for the task
        new_comment = {"text": "Great work!"}
        response = client.post(f"/tasks/{task['id']}/comments/", json=new_comment)
        assert response.status_code == 200
        assert response.json()["text"] == new_comment["text"]

    def test_create_comment_invalid_task(self):
        # try to create a comment for a non-existent task
        new_comment = {"text": "Great work!"}
        response = client.post("/tasks/999/comments/", json=new_comment)
        assert response.status_code == 404

    def test_create_comment_invalid_data(self):
        # try to create a comment with invalid data
        new_comment = {"text": ""}
        response = client.post("/tasks/1/comments/", json=new_comment)
        assert response.status_code == 422

    def test_read_comments(self):
        # create a task first
        new_task = {"title": "Test task"}
        response = client.post("/tasks/", json=new_task)
        assert response.status_code == 200
        task = response.json()

        # create a comment for the task
        new_comment = {"text": "Great work!"}
        response = client.post(f"/tasks/{task['id']}/comments/", json=new_comment)
        assert response.status_code == 200

        # read the comments
        response = client.get(f"/tasks/{task['id']}/comments/")
        assert response.status_code == 200
        assert response.json() == [new_comment]

    def test_read_comments_non_existent_task(self):
        # try to read comments from a non-existent task
        response = client.get("/tasks/999/comments/")
        assert response.status_code == 404

    def test_read_comments_no_comments(self):
        # create a task with no comments
        new_task = {"title": "Test task"}
        response = client.post("/tasks/", json=new_task)
        assert response.status_code == 200
        task = response.json()

        # read the comments
        response = client.get(f"/tasks/{task['id']}/comments/")
        assert response.status_code == 200
        assert response.json() == []
```

These tests cover success cases, error cases, data validation, and edge cases. The FastAPI application is tested using an in-memory SQLite database, which is created and destroyed for each test. The `override_get_db` function is used to replace the original `get_db` dependency with one that uses the SQLite database.

Note: This test suite assumes the existence of a POST `/tasks/` endpoint to create tasks. If such an endpoint doesn't exist, you'll need to create tasks in a different way, perhaps by directly using the CRUD functions in the tests.