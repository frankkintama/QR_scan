from typing import Optional
from bson import ObjectId #ID mặc định của MongoDB (dạng hex 24 ký tự)
from fastapi import Request, Depends
from fastapi.security import OAuth2PasswordRequestForm # Form chuẩn OAuth2 (username + password)
from fastapi_users import BaseUserManager
from beanie import PydanticObjectId
from fastapi_users_db_beanie import BeanieUserDatabase

from app.models import User
from app.core.settings import settings


class UserManager(BaseUserManager[User, PydanticObjectId]):
    reset_password_token_secret = settings.SECRET_KEY
    verification_token_secret = settings.SECRET_KEY

    def parse_id(self, user_id: str) -> PydanticObjectId:
        """Convert string ID to MongoDB ObjectId"""
        return PydanticObjectId(ObjectId(user_id))

    async def authenticate(
        self, credentials: OAuth2PasswordRequestForm
    ) -> Optional[User]:
        
        # Try finding user by email first
        user = await self.user_db.get_by_email(credentials.username)
        
        # If not found, try finding by username
        if user is None:
            user = await User.find_one(User.username == credentials.username)
        
        # User not found
        if user is None:
            # Hash password to prevent timing attacks
            self.password_helper.hash(credentials.password)
            return None

        # Verify password
        verified, updated_password_hash = self.password_helper.verify_and_update(
            credentials.password, user.hashed_password
        )
        
        if not verified:
            return None
        
        # Update hash if algorithm was updated
        if updated_password_hash is not None:
            await self.user_db.update(user, {"hashed_password": updated_password_hash})
        
        return user

    async def on_after_register(self, user: User, request: Optional[Request] = None):
        """Callback after user registration"""
        print(f"User {user.id} has registered.")

    async def on_after_forgot_password(
        self, user: User, token: str, request: Optional[Request] = None
    ):
        """Callback after forgot password request"""
        print(f"User {user.id} has forgot their password. Reset token: {token}")

    async def on_after_request_verify(
        self, user: User, token: str, request: Optional[Request] = None
    ):
        """Callback after verification request"""
        print(f"Verification requested for user {user.id}. Verification token: {token}")


async def get_user_db():
    """Dependency to provide user database"""
    yield BeanieUserDatabase(User)


async def get_user_manager(user_db: BeanieUserDatabase = Depends(get_user_db)):
    """Dependency to provide user manager"""
    yield UserManager(user_db)

