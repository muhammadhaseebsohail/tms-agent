Based on the provided code, you already have Pydantic models for request/response:

- `CommentBase`: Used as a base model for creating and reading comments.
- `CommentCreate`: Request model used to create a new comment.
- `Comment`: Response model used to represent a comment.

The complete set of models should look like this:

```python
from pydantic import BaseModel

class CommentBase(BaseModel):
    """
    Base model for comments.
    """
    text: str

class CommentCreate(CommentBase):
    """
    Request model for creating a comment.
    """
    pass

class Comment(CommentBase):
    """
    Response model for comments.
    """
    id: int
    task_id: int
    class Config:
        orm_mode = True
```

These models are used in the service layer (`crud.py`) to handle the business logic of creating and reading comments. 

In the case of the database models, you also have:

- `Task`: Represents a task in the database. Contains a foreign key relationship with comments.
- `Comment`: Represents a comment in the database. Contains a foreign key to the task it is associated with.

These models look like this:

```python
from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from .database import Base

class Task(Base):
    """
    Database model for tasks.
    """
    __tablename__ = "tasks"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)

class Comment(Base):
    """
    Database model for comments.
    """
    __tablename__ = "comments"
    id = Column(Integer, primary_key=True, index=True)
    text = Column(String, index=True)
    task_id = Column(Integer, ForeignKey("tasks.id"))
    task = relationship("Task", back_populates="comments")
```

In terms of unit tests, provided tests are checking the HTTP status code and the response content of the `create_comment` and `read_comments` endpoints. 

In order to increase the coverage, consider adding tests for error scenarios and edge cases (e.g., creating a comment on a non-existent task, trying to read comments from a non-existent task, etc).