To implement task status tracking, we will need two endpoints: one for updating the status of a task and another for retrieving the current status of a task. 

Let's start by creating the Task model, Pydantic models, and service layer. The Pydantic models will be used to validate data, while the service layer will handle interactions with the database. 

```python
from typing import Optional
from pydantic import BaseModel
from sqlalchemy import Boolean, Column, Integer, String
from fastapi import FastAPI
from sqlalchemy.orm import Session
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class TaskModel(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    status = Column(Boolean, default=False)

class Task(BaseModel):
    id: int
    title: str
    status: bool

class TaskUpdate(BaseModel):
    status: bool

app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.on_event("startup")
async def startup_event():
    Base.metadata.create_all(bind=engine)

def get_task(db: Session, task_id: int):
    return db.query(TaskModel).filter(TaskModel.id == task_id).first()

def update_task(db: Session, task: TaskModel, task_update: TaskUpdate):
    task.status = task_update.status
    db.commit()
    return task
```

Next, let's implement the endpoints.

```python
from fastapi import Depends, HTTPException, status

@app.get("/tasks/{task_id}", response_model=Task)
async def track_task_status(task_id: int, db: Session = Depends(get_db)):
    """
    Track a task's status.

    Args:
    task_id (int): Unique identifier of the task.
    """
    task = get_task(db, task_id)
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return task

@app.patch("/tasks/{task_id}", response_model=Task)
async def update_task_status(task_id: int, task_update: TaskUpdate, db: Session = Depends(get_db)):
    """
    Update a task's status.

    Args:
    task_id (int): Unique identifier of the task.
    task_update (TaskUpdate): New status for the task.
    """
    task = get_task(db, task_id)
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return update_task(db, task, task_update)
```

Finally, let's write some tests for these endpoints.

```python
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@app.on_event("startup")
async def startup_event():
    Base.metadata.create_all(bind=engine)

client = TestClient(app)

def test_track_task_status():
    response = client.get("/tasks/1")
    assert response.status_code == 200
    assert response.json() == {"id": 1, "title": "Test task", "status": False}

def test_update_task_status():
    response = client.patch("/tasks/1", json={"status": True})
    assert response.status_code == 200
    assert response.json() == {"id": 1, "title": "Test task", "status": True}
```

Remember to replace "SessionLocal" and "engine" with your actual database session and engine.