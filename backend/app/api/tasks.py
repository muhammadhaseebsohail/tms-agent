Here's a basic implementation of your requirements using FastAPI, Pydantic, SQLAlchemy (for database models), and a hypothetical authentication system. Note that for a complete application, you'd need additional setup for the database connection, middleware, and more.

Database Models (using SQLAlchemy):

```python
from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, DateTime
from sqlalchemy.orm import relationship

from database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    hashed_password = Column(String)

class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(String, index=True)
    due_date = Column(DateTime, index=True)
    priority = Column(Integer, index=True)
    status = Column(Boolean, default=False)
    owner_id = Column(Integer, ForeignKey("users.id"))

    owner = relationship("User", back_populates="tasks")


User.tasks = relationship("Task", back_populates="owner", cascade="all, delete-orphan")
```

Pydantic Models:

```python
from pydantic import BaseModel
from datetime import datetime

class TaskBase(BaseModel):
    title: str
    description: str
    due_date: datetime
    priority: int
    status: bool

class TaskCreate(TaskBase):
    pass

class Task(TaskBase):
    id: int
    owner_id: int

    class Config:
        orm_mode = True
```

Service Layer Code:

```python
from sqlalchemy.orm import Session
from . import models, schemas

def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()

def create_user_task(db: Session, task: schemas.TaskCreate, user_id: int):
    db_task = models.Task(**task.dict(), owner_id=user_id)
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task

def get_tasks(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Task).offset(skip).limit(limit).all()

def get_task(db: Session, id: int):
    return db.query(models.Task).filter(models.Task.id == id).first()

def update_task(db: Session, task: schemas.Task):
    db_task = get_task(db, task.id)
    if db_task is None:
        return None
    for var, value in vars(task).items():
        setattr(db_task, var, value) if value else None
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task

def delete_task(db: Session, id: int):
    db_task = get_task(db, id)
    db.delete(db_task)
    db.commit()
    return db_task
```

FastAPI Endpoints:

```python
from typing import List
from fastapi import Depends, FastAPI, HTTPException, status
from sqlalchemy.orm import Session
from . import models, schemas, services
from .database import SessionLocal

app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/tasks/", response_model=schemas.Task)
def create_task(
    task: schemas.TaskCreate,
    db: Session = Depends(get_db),
    current_user: schemas.User = Depends(get_current_active_user),
):
    """
    Create new tasks with title, description, due date, priority, and status
    """
    return services.create_user_task(db=db, task=task, user_id=current_user.id)

@app.get("/tasks/", response_model=List[schemas.Task])
def read_tasks(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """
    Retrieve tasks
    """
    tasks = services.get_tasks(db, skip=skip, limit=limit)
    return tasks

@app.get("/tasks/{task_id}", response_model=schemas.Task)
def read_task(task_id: int, db: Session = Depends(get_db)):
    """
    Retrieve a task by its ID
    """
    task = services.get_task(db, task_id)
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return task

@app.patch("/tasks/{task_id}", response_model=schemas.Task)
def update_task(
    task_id: int, task: schemas.TaskCreate, db: Session = Depends(get_db)
):
    """
    Update a task by its ID
    """
    updated_task = services.update_task(db, task)
    if updated_task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return updated_task

@app.delete("/tasks/{task_id}", response_model=schemas.Task)
def delete_task(task_id: int, db: Session = Depends(get_db)):
    """
    Delete a task by its ID
    """
    deleted_task = services.delete_task(db, task_id)
    if deleted_task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return deleted_task
```

For unit tests, you would use a test database and the FastAPI TestClient. Here's an example for the create task endpoint:

```python
from fastapi.testclient import TestClient
from main import app
from datetime import datetime

client = TestClient(app)

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
```

Please note that the above code assumes there is a `get_current_active_user` function which authenticates a user and returns a User object. This function should be implemented according to the authentication method used (OAuth, JWT, etc.).