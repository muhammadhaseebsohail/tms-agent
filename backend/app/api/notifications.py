To implement the notifications feature, we'll create an endpoint to create a notification, one to retrieve all notifications for a user, and another to mark a notification as read.

Here's the complete code:

```python
from typing import List
from fastapi import FastAPI, HTTPException, Depends, status
from sqlalchemy.orm import Session
from pydantic import BaseModel
from sqlalchemy import Boolean, Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime
import uvicorn

Base = declarative_base()

class NotificationDB(Base):
    __tablename__ = "notifications"
    
    id = Column(Integer, primary_key=True, index=True)
    task_id = Column(Integer, index=True)
    user_id = Column(Integer, index=True)
    message = Column(String)
    read = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)

class NotificationBase(BaseModel):
    task_id: int
    user_id: int
    message: str

class NotificationCreate(NotificationBase):
    pass

class Notification(NotificationBase):
    id: int
    read: bool
    created_at: datetime

    class Config:
        orm_mode = True

app = FastAPI()

@app.post("/notifications/", response_model=Notification)
async def create_notification(notification: NotificationCreate):
    """
    Create a new notification.
    """
    db_notification = NotificationDB(**notification.dict())
    session.add(db_notification)
    session.commit()
    session.refresh(db_notification)
    return db_notification

@app.get("/notifications/{user_id}", response_model=List[Notification])
async def read_notifications(user_id: int):
    """
    Get all notifications for a specific user.
    """
    notifications = session.query(NotificationDB).filter(NotificationDB.user_id == user_id).all()
    if notifications is None:
        raise HTTPException(status_code=404, detail="Notifications not found")
    return notifications

@app.put("/notifications/{notification_id}", response_model=Notification)
async def mark_notification_as_read(notification_id: int):
    """
    Mark a specific notification as read.
    """
    notification = session.query(NotificationDB).get(notification_id)
    if notification is None:
        raise HTTPException(status_code=404, detail="Notification not found")
    notification.read = True
    session.commit()
    return notification
```

For testing, you can use Pytest:

```python
def test_create_notification():
    response = client.post("/notifications/", json={"task_id": 1, "user_id": 1, "message": "Test"})
    assert response.status_code == 200
    data = response.json()
    assert data["task_id"] == 1
    assert data["user_id"] == 1
    assert data["message"] == "Test"
    assert "id" in data
    assert "read" in data
    assert "created_at" in data

def test_read_notifications():
    response = client.get("/notifications/1")
    assert response.status_code == 200

def test_mark_notification_as_read():
    response = client.put("/notifications/1")
    assert response.status_code == 200
    data = response.json()
    assert data["read"] is True
```

This is a basic implementation and may require additional enhancements like adding authentication and implementing a database connection.