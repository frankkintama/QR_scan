import uuid
from fastapi import FastAPI
from fastapi_users import FastAPIUsers
from fastapi_users.authentication import CookieTransport, AuthenticationBackend, JWTStrategy
from fastapi_users.db import BeanieUserDatabase

from app.models import User, UserCreate, UserRead, UserUpdate
from app.database import init_db


SECRET = "SUPERSECRETKEY"  # load from .env in production


async def get_user_db():
    yield BeanieUserDatabase(User)


# Transport: how users authenticate (cookie, bearer token, etc.)
cookie_transport = CookieTransport(cookie_max_age=3600)


def get_jwt_strategy() -> JWTStrategy:
    return JWTStrategy(secret=SECRET, lifetime_seconds=3600)


auth_backend = AuthenticationBackend(
    name="jwt",
    transport=cookie_transport,
    get_strategy=get_jwt_strategy,
)


fastapi_users = FastAPIUsers[User, uuid.UUID](
    get_user_db,
    [auth_backend],
)


app = FastAPI()


@app.on_event("startup")
async def on_startup():
    await init_db()


# Register authentication routes
app.include_router(
    fastapi_users.get_auth_router(auth_backend), 
    prefix="/auth", 
    tags=["auth"]
)

# Register user management routes
app.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate), 
    prefix="/auth", 
    tags=["auth"]
)

app.include_router(
    fastapi_users.get_users_router(UserRead, UserUpdate), 
    prefix="/users", 
    tags=["users"]
)
