from beanie import Document, PydanticObjectId
from fastapi_users_db_beanie import BeanieBaseUser
from fastapi_users import schemas
from pydantic import BaseModel, EmailStr, Field
from typing import Optional

class User(BeanieBaseUser, Document):
    username: str

    class Settings:
        name = "User"
        email_collation = None

# Pydantic models
# BaseUser[uuid.UUID]:
# id(UUID), email(str)
# is_active(bool), is_superuser(bool), is_verified(bool)
class UserRead(schemas.BaseUser[PydanticObjectId]):
    email: EmailStr
    username: str

# BaseUserCreate:
# email(str), password(str)
class UserCreate(schemas.BaseUserCreate):
    email: EmailStr
    username: str
    password: str

    class Config:
        schema_extra = {
            "example": {
                "email": "user@example.com",
                "username": "myuser",
                "password": "password123",
            }
        }

# BaseUserUpdate
# email: Optional(str), password: Optional(str)
class UserUpdate(schemas.BaseUserUpdate):
    username: Optional[str] = None