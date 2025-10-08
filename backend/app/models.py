from beanie import Document, PydanticObjectId, before_event, Replace, Update
from fastapi_users_db_beanie import BeanieBaseUser
from fastapi_users import schemas
from pydantic import EmailStr, Field, model_validator
from typing import Optional, Dict
from datetime import datetime, timezone, timedelta

VIETNAM_TZ = timezone(timedelta(hours=7))
def get_vietnam_time():
        return datetime.now(VIETNAM_TZ)

# Model chính - đại diện cho document trong MongoDB
class User(BeanieBaseUser, Document):
    username: str                      # Thêm field username vì Beanie mặc định chỉ cung cấp: 
    full_name: Optional[str] = None    # id, email, hashed_password, 
    role: str = Field(default="user", description="user | staff | admin")                                  # is_active, is_superuser, is_verified
    
    #profile_picture
    #bio
    #phone
    
    created_at: datetime = Field(default_factory=get_vietnam_time)
    updated_at: datetime = Field(default_factory=get_vietnam_time)
    
    @before_event([Replace, Update])
    def update_timestamp(self):
        self.updated_at = get_vietnam_time()


    is_deleted: bool = False
    settings: Dict = Field(default_factory=dict)

    class Settings:
        name = "User"  # Tên collection trong MongoDB sẽ là "User"
        email_collation = None  # Tắt collation - MongoDB sẽ phân biệt chữ hoa/thường

#                              
# Schema cho response - khi trả data về cho client
# dùng cho GET /users/me, /users/{id}, /users/
class UserRead(schemas.BaseUser[PydanticObjectId]):
    email: EmailStr  # Khai báo lại để đảm bảo thứ tự field
    username: str    # Thêm username 

#
# Schema cho registration - validate data khi tạo user mới
# dùng cho POST /auth/register
class UserCreate(schemas.BaseUserCreate):
    email: EmailStr   
    username: str  = Field(..., min_length=5, max_length=20)  
    password: str     
    confirmPassword: str
    role: str = "user"

    @model_validator(mode="after")
    def passwords_match(self) -> "UserCreate":
        if self.password != self.confirmPassword:
            raise ValueError("Mật khẩu không trùng")
        return self

#
# Schema cho update - cho phép cập nhật thông tin user
# dùng cho PATCH /users/{id}
class UserUpdate(schemas.BaseUserUpdate):
    username: Optional[str] = None  # Username không bắt buộc khi update
    # BaseUserUpdate đã có: email (Optional), password (Optional)
