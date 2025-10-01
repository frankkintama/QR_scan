import os
from bson import ObjectId
from typing import Optional
from fastapi import FastAPI, Request, Depends
from fastapi_users import FastAPIUsers, BaseUserManager
from fastapi_users.authentication import CookieTransport, AuthenticationBackend, JWTStrategy
from fastapi_users_db_beanie import BeanieUserDatabase
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.middleware.cors import CORSMiddleware

from beanie import init_beanie, PydanticObjectId
from motor.motor_asyncio import AsyncIOMotorClient
from contextlib import asynccontextmanager
from app.models import User, UserCreate, UserRead, UserUpdate
from app.database import init_db
from dotenv import load_dotenv

load_dotenv()
SECRET = os.getenv("SECRET")  

#kết nối Beanie đến User, Beanie giúp tương tác với MongoDB
async def get_user_db():
    yield BeanieUserDatabase(User)

class UserManager(BaseUserManager[User, PydanticObjectId]):
    reset_password_token_secret = SECRET
    verification_token_secret = SECRET

    def parse_id(self, user_id: str) -> PydanticObjectId:
        return PydanticObjectId(ObjectId(user_id))

    async def authenticate(
        self, credentials: OAuth2PasswordRequestForm
    ) -> Optional[User]:
        user = await self.user_db.get_by_email(credentials.username)
        if user is None:
            # Try to find by username if email lookup fails
            user = await User.find_one(User.username == credentials.username)
        
        if user is None:
            self.password_helper.hash(credentials.password)
            return None

        verified, updated_password_hash = self.password_helper.verify_and_update(
            credentials.password, user.hashed_password
        )
        if not verified:
            return None
        
        if updated_password_hash is not None:
            await self.user_db.update(user, {"hashed_password": updated_password_hash})

        return user

    async def on_after_register(self, user: User, request: Optional[Request] = None):
        print(f"User {user.id} has registered.")

    async def on_after_forgot_password(
        self, user: User, token: str, request: Optional[Request] = None
    ):
        print(f"User {user.id} has forgot their password. Reset token: {token}")

    async def on_after_request_verify(
        self, user: User, token: str, request: Optional[Request] = None
    ):
        print(f"Verification requested for user {user.id}. Verification token: {token}")


async def get_user_manager(user_db: BeanieUserDatabase = Depends(get_user_db)):
    yield UserManager(user_db)

#định nghĩa cookie để lưu JWT
cookie_transport = CookieTransport(
    cookie_name="fastapiuserauth",
    cookie_max_age=3600,
    cookie_secure=False,
    cookie_httponly=True,
    cookie_samesite="lax",
    cookie_path="/",
    cookie_domain="localhost"
    )


def get_jwt_strategy() -> JWTStrategy:
    return JWTStrategy(secret=SECRET, lifetime_seconds=3600)


auth_backend = AuthenticationBackend(
    name="jwt",
    transport=cookie_transport,
    get_strategy=get_jwt_strategy,
)

#khởi tạo FastAPIUsers với model User, primary key UUID, DB connection, Authetication backend
fastapi_users = FastAPIUsers[User, PydanticObjectId](
    get_user_manager,
    [auth_backend],
)

#khi server start, kết nối Mongo và tạo Beanie
@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    yield
    pass

#cấu hình CORS(Cross-Origin Resource Sharing) để frontend gọi API
app = FastAPI(lifespan=lifespan)

origins = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True, #cho phép gửi cookie
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register authentication: tạo /auth/login, /auth/logout, /auth/refresh-token
app.include_router(
    fastapi_users.get_auth_router(auth_backend), 
    prefix="/auth", 
    tags=["auth"]
)

# Register user management
# User creation: tạo /auth/register
app.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate), 
    prefix="/auth", 
    tags=["auth"]
)

#User update: tạo list /users/
# get/update/delete người dùng với /users/{id}
app.include_router(
    fastapi_users.get_users_router(UserRead, UserUpdate), 
    prefix="/users", 
    tags=["users"]
)

#create /users/me
current_user = fastapi_users.current_user()

@app.get("/users/me", response_model=UserRead, tags=["users"])
async def get_me(user: User = Depends(current_user)):
    """Get current authenticated user"""
    return user

@app.get("/debug/request")
async def debug_request(request: Request):
    return {
        "cookies": dict(request.cookies),
        "cookie_header": request.headers.get("cookie")
    }