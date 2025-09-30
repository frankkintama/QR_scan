from beanie import Document, PydanticObjectId
from fastapi_users_db_beanie import BeanieBaseUser
from fastapi_users import schemas

class User(BeanieBaseUser, Document):
    class Settings:
        name = "User"
        email_collation = None

# Pydantic models
# BaseUser[uuid.UUID]:
# id(UUID), email(str)
# is_active(bool), is_superuser(bool), is_verified(bool)
class UserRead(schemas.BaseUser[PydanticObjectId]):
    pass

# BaseUserCreate:
# email(str), password(str)
class UserCreate(schemas.BaseUserCreate):
    pass

# BaseUserUpdate
# email: Optional(str), password: Optional(str)
class UserUpdate(schemas.BaseUserUpdate):
    pass