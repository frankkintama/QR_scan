from beanie import Document
from fastapi_users.db import BeanieBaseUser
from fastapi_users import schemas
import uuid

# Database model
class User(BeanieBaseUser, Document):
    id: uuid.UUID
    pass

# Pydantic models
class UserRead(schemas.BaseUser[uuid.UUID]):
    pass

class UserCreate(schemas.BaseUserCreate):
    pass

class UserUpdate(schemas.BaseUserUpdate):
    pass