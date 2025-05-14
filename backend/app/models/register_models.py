In the provided code, the request/response models have already been created using Pydantic, a Python library for data validation using Python type annotations.

Here are the Pydantic models used:

1. UserBase: This is the base model for a user and includes the fields `email` and `username`. The email is validated using `EmailStr` from Pydantic, which checks if the given string is a valid email. The username has a minimum and maximum length restriction.

```python
class UserBase(BaseModel):
    email: EmailStr
    username: str = Field(..., min_length=3, max_length=50)
```

2. UserRegister: This model inherits from UserBase and adds a `password` field. The password has minimum and maximum length restrictions.

```python
class UserRegister(UserBase):
    password: str = Field(..., min_length=8, max_length=50)
```

3. UserLogin: This model is used when a user attempts to login. It contains `username` and `password` fields with restrictions on length.

```python
class UserLogin(BaseModel):
    username: str = Field(..., min_length=3, max_length=50)
    password: str = Field(..., min_length=8, max_length=50)
```

These models are used to validate the data in the request when a user is registering or logging in. They are also used to generate the OpenAPI schema for the API.

The UserDB model is a database model used for SQLAlchemy, which represents a table in the database. It is not a Pydantic model, but it is used in the service layer to interact with the database:

```python
class UserDB(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    username = Column(String, unique=True, index=True)
    hashed_password = Column(String)
```

The API does not return any explicit response models, but FastAPI automatically generates them from the return values of the endpoint functions and the Pydantic models. The `/register` endpoint returns a UserBase model, and the `/login` endpoint returns a dictionary with an access token.