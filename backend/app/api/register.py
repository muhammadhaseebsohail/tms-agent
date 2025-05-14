The task requires several components, let's start by defining the Pydantic models:

```python
from pydantic import BaseModel, EmailStr, Field

class UserBase(BaseModel):
    email: EmailStr
    username: str = Field(..., min_length=3, max_length=50)

class UserRegister(UserBase):
    password: str = Field(..., min_length=8, max_length=50)

class UserLogin(BaseModel):
    username: str = Field(..., min_length=3, max_length=50)
    password: str = Field(..., min_length=8, max_length=50)
```

Next, we'll create the User database model:

```python
from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class UserDB(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    username = Column(String, unique=True, index=True)
    hashed_password = Column(String)
```

Now, let's create the services for user registration and login:

```python
from passlib.context import CryptContext
from sqlalchemy.orm import Session

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_user(db: Session, username: str):
    return db.query(UserDB).filter(UserDB.username == username).first()

def create_user(db: Session, user: UserRegister):
    hashed_password = pwd_context.hash(user.password)
    db_user = UserDB(email=user.email, username=user.username, hashed_password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def authenticate_user(db: Session, username: str, password: str):
    user = get_user(db, username)
    if not user:
        return False
    if not pwd_context.verify(password, user.hashed_password):
        return False
    return user
```

Now, let's define the FastAPI endpoints:

```python
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.security.oauth2 import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from typing import Optional

app = FastAPI()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/register", response_model=UserBase)
def register(user: UserRegister, db: Session = Depends(get_db)):
    """
    Register a new user
    """
    db_user = get_user(db, username=user.username)
    if db_user:
        raise HTTPException(status_code=400, detail="Username already registered")
    user_in_db = create_user(db, user)
    return user_in_db

@app.post("/login", response_model=str)
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    """
    Login an existing user
    """
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=400, detail="Invalid username or password")
    return {"access_token": user.id, "token_type": "bearer"}
```

Finally, let's add some tests:

```python
from fastapi.testclient import TestClient

client = TestClient(app)

def test_create_user():
    response = client.post("/register", data={"username": "testuser", "email": "testuser@example.com", "password": "testpassword"})
    assert response.status_code == 200
    assert response.json()["username"] == "testuser"

def test_create_existing_user():
    response = client.post("/register", data={"username": "testuser", "email": "testuser@example.com", "password": "testpassword"})
    assert response.status_code == 400

def test_login():
    response = client.post("/login", data={"username": "testuser", "password": "testpassword"})
    assert response.status_code == 200
    assert "access_token" in response.json()

def test_login_wrong_password():
    response = client.post("/login", data={"username": "testuser", "password": "wrongpassword"})
    assert response.status_code == 400
```
This code covers the basic user registration and login functionality. It uses best practices such as dependency injection and Pydantic models for data validation. It also uses Passlib for password hashing.