To implement the comments feature, we will need the following:

1. An endpoint to post a comment
2. An endpoint to get all comments on a task
3. A Pydantic model for the comments
4. A service layer to handle the business logic
5. Database models for comments and tasks
6. Unit tests

Here is the code:

```python
from typing import List
from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
from pydantic import BaseModel
from . import models, schemas, crud
from .database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

class CommentBase(BaseModel):
    text: str

class CommentCreate(CommentBase):
    pass

class Comment(CommentBase):
    id: int
    task_id: int
    class Config:
        orm_mode = True

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/tasks/{task_id}/comments/", response_model=Comment)
def create_comment(task_id: int, comment: CommentCreate, db: Session = Depends(get_db)):
    """
    Create a new comment on a task.
    """
    return crud.create_comment(db=db, comment=comment, task_id=task_id)

@app.get("/tasks/{task_id}/comments/", response_model=List[Comment])
def read_comments(task_id: int, db: Session = Depends(get_db)):
    """
    Get all comments on a task.
    """
    comments = crud.get_comments(db, task_id=task_id)
    if comments is None:
        raise HTTPException(status_code=404, detail="Comments not found")
    return comments
```

In the `crud.py` file:

```python
from sqlalchemy.orm import Session
from . import models, schemas

def get_comments(db: Session, task_id: int):
    return db.query(models.Comment).filter(models.Comment.task_id == task_id).all()

def create_comment(db: Session, comment: schemas.CommentCreate, task_id: int):
    db_comment = models.Comment(text=comment.text, task_id=task_id)
    db.add(db_comment)
    db.commit()
    db.refresh(db_comment)
    return db_comment
```

In the `models.py` file:

```python
from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from .database import Base

class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)

class Comment(Base):
    __tablename__ = "comments"

    id = Column(Integer, primary_key=True, index=True)
    text = Column(String, index=True)
    task_id = Column(Integer, ForeignKey("tasks.id"))

    task = relationship("Task", back_populates="comments")
```

For the unit test, you can use the `TestClient` from `fastapi.testclient` to simulate HTTP requests and check the responses.

```python
from fastapi.testclient import TestClient
from .main import app

client = TestClient(app)

def test_create_comment():
    response = client.post("/tasks/1/comments/", json={"text": "Great work!"})
    assert response.status_code == 200
    assert response.json()["text"] == "Great work!"

def test_read_comments():
    response = client.get("/tasks/1/comments/")
    assert response.status_code == 200
    assert "comments" in response.json()
```