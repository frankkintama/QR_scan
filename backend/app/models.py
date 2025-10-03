from beanie import Document, PydanticObjectId
from fastapi_users_db_beanie import BeanieBaseUser
from fastapi_users import schemas
from pydantic import BaseModel, EmailStr, Field, model_validator
from typing import Optional

# Model chính - đại diện cho document trong MongoDB
class User(BeanieBaseUser, Document):
    username: str  # Thêm field username vì Beanie mặc định chỉ cung cấp: 
                   # id, email, hashed_password, 
                   # is_active, is_superuser, is_verified

    class Settings:
        name = "User"  # Tên collection trong MongoDB sẽ là "User"
        email_collation = None  # Tắt collation - MongoDB sẽ phân biệt chữ hoa/thường
                               
# Schema cho response - khi trả data về cho client
# dùng cho GET /users/me, /users/{id}, /users/
class UserRead(schemas.BaseUser[PydanticObjectId]):
    email: EmailStr  # Khai báo lại để đảm bảo thứ tự field
    username: str    # Thêm username 

# Schema cho registration - validate data khi tạo user mới
# dùng cho POST /auth/register
class UserCreate(schemas.BaseUserCreate):
    email: EmailStr   
    username: str  = Field(..., min_length=5, max_length=20)  
    password: str     
    confirmPassword: str

    @model_validator(mode="after")
    def passwords_match(self) -> "UserCreate":
        if self.password != self.confirmPassword:
            raise ValueError("Mật khẩu không trùng")
        return self


    class Config:
        schema_extra = {  # Ví dụ hiển thị trong Swagger 
            "example": {
                "email": "user@example.com",
                "username": "myuser",
                "password": "password123",
            }
        }

# Schema cho update - cho phép cập nhật thông tin user
# dùng cho PATCH /users/{id}
class UserUpdate(schemas.BaseUserUpdate):
    username: Optional[str] = None  # Username không bắt buộc khi update
    # BaseUserUpdate đã có: email (Optional), password (Optional)
