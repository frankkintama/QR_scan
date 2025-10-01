import os
from bson import ObjectId  # ID mặc định của MongoDB (dạng hex 24 ký tự)
from typing import Optional
from fastapi import FastAPI, Request, Depends
from fastapi_users import FastAPIUsers, BaseUserManager
from fastapi_users.authentication import CookieTransport, AuthenticationBackend, JWTStrategy
from fastapi_users_db_beanie import BeanieUserDatabase
from fastapi.security import OAuth2PasswordRequestForm  # Form chuẩn OAuth2 (username + password)
from fastapi.middleware.cors import CORSMiddleware

from beanie import init_beanie, PydanticObjectId
from contextlib import asynccontextmanager
from app.models import User, UserCreate, UserRead, UserUpdate
from app.database import init_db
from dotenv import load_dotenv

load_dotenv()
SECRET = os.getenv("SECRET")  # Key để mã hóa JWT token

# Dependency injection - cung cấp database connection cho FastAPI Users
async def get_user_db():
    yield BeanieUserDatabase(User)

# UserManager quản lý logic liên quan đến user
class UserManager(BaseUserManager[User, PydanticObjectId]):
    reset_password_token_secret = SECRET  # Secret cho reset password token
    verification_token_secret = SECRET    # Secret cho email verification token

    # Chuyển đổi string ID thành MongoDB ObjectId
    def parse_id(self, user_id: str) -> PydanticObjectId:
        return PydanticObjectId(ObjectId(user_id))

    # Override method authenticate để hỗ trợ login bằng username
    async def authenticate(
        self, credentials: OAuth2PasswordRequestForm
    ) -> Optional[User]:
        # Thử tìm user theo email trước
        user = await self.user_db.get_by_email(credentials.username)
        
        # Nếu không tìm thấy, thử tìm theo username
        if user is None:
            user = await User.find_one(User.username == credentials.username)
        
        # Không tìm thấy user
        if user is None:
            # Hash password để tránh timing attack (bảo mật)
            self.password_helper.hash(credentials.password)
            return None

        # Verify password với hashed_password trong database
        verified, updated_password_hash = self.password_helper.verify_and_update(
            credentials.password, user.hashed_password
        )
        
        # Sai password
        if not verified:
            return None
        
        # Nếu hash algorithm được update, lưu hash mới
        if updated_password_hash is not None:
            await self.user_db.update(user, {"hashed_password": updated_password_hash})

        return user  # Login thành công

    # Callback sau khi user đăng ký
    async def on_after_register(self, user: User, request: Optional[Request] = None):
        print(f"User {user.id} has registered.")

    # Callback khi user yêu cầu reset password
    async def on_after_forgot_password(
        self, user: User, token: str, request: Optional[Request] = None
    ):
        print(f"User {user.id} has forgot their password. Reset token: {token}")

    # Callback khi user yêu cầu verify email
    async def on_after_request_verify(
        self, user: User, token: str, request: Optional[Request] = None
    ):
        print(f"Verification requested for user {user.id}. Verification token: {token}")

# Dependency injection cho UserManager
async def get_user_manager(user_db: BeanieUserDatabase = Depends(get_user_db)):
    yield UserManager(user_db)

# Cấu hình cookie để lưu JWT token
cookie_transport = CookieTransport(
    cookie_name="fastapiuserauth",  # Tên cookie
    cookie_max_age=3600,             # Expire sau 1 giờ (3600 giây)
    cookie_secure=False,             # True = chỉ gửi qua HTTPS (set False cho development)
    cookie_httponly=True,            # JavaScript không thể đọc cookie (bảo mật XSS)
    cookie_samesite="lax",           # Cookie chỉ gửi trong same-site requests
    cookie_path="/",                 # Cookie có hiệu lực trên toàn bộ domain
    cookie_domain="localhost"        # Domain của cookie
)

# Strategy tạo và verify JWT token
def get_jwt_strategy() -> JWTStrategy:
    return JWTStrategy(secret=SECRET, lifetime_seconds=3600)

# Authentication backend kết hợp cookie transport và JWT strategy
auth_backend = AuthenticationBackend(
    name="jwt",
    transport=cookie_transport,      # Dùng cookie để transport token
    get_strategy=get_jwt_strategy,   # Dùng JWT để mã hóa
)

# Khởi tạo FastAPIUsers - tạo tất cả routes authentication
fastapi_users = FastAPIUsers[User, PydanticObjectId](
    get_user_manager,   # UserManager để quản lý logic
    [auth_backend],     # List các backend authentication 
)

# Lifespan context manager - chạy code khi app start/stop
@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()  # Kết nối MongoDB khi server khởi động
    yield            # Server đang chạy
    pass            # Cleanup khi server tắt 

# Khởi tạo FastAPI app
app = FastAPI(lifespan=lifespan)

# Cấu hình CORS - cho phép frontend gọi API từ origin khác
origins = [
    "http://localhost:3000",      
    "http://127.0.0.1:3000",      
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,        
    allow_credentials=True,       # Cho phép gửi cookie
    allow_methods=["*"],          # Cho phép tất cả HTTP methods (GET, POST, etc.)
    allow_headers=["*"],          # Cho phép tất cả headers
)



# Auth routes: /auth/login, /auth/logout
app.include_router(
    fastapi_users.get_auth_router(auth_backend), 
    prefix="/auth", 
    tags=["auth"]
)

# Register route: /auth/register
app.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate), 
    prefix="/auth", 
    tags=["auth"]
)

# User management routes: GET/PATCH/DELETE /users/{id}
app.include_router(
    fastapi_users.get_users_router(UserRead, UserUpdate), 
    prefix="/users", 
    tags=["users"]
)

# Tạo dependency để lấy current authenticated user
current_user = fastapi_users.current_user()

# Custom endpoint - lấy thông tin user hiện tại
@app.get("/users/me", response_model=UserRead, tags=["users"])
async def get_me(user: User = Depends(current_user)):
    """Get current authenticated user"""
    return user

# Debug endpoint - kiểm tra cookies
@app.get("/debug/request")
async def debug_request(request: Request):
    return {
        "cookies": dict(request.cookies),
        "cookie_header": request.headers.get("cookie")
    }
