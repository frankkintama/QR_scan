from fastapi import FastAPI

from fastapi.middleware.cors import CORSMiddleware

from contextlib import asynccontextmanager
from app.models import User, UserCreate, UserRead, UserUpdate
from app.core.auth import fastapi_users, auth_backend

from app.routers import users, admin
from app.core.settings import  init_db


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

#
#
#


app.include_router(admin.router)
app.include_router(users.router)
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

