from fastapi_users import FastAPIUsers
from fastapi_users.authentication import CookieTransport, AuthenticationBackend, JWTStrategy
from beanie import PydanticObjectId

from app.models import User
from app.manager import get_user_manager
from app.core.settings import settings


# Cấu hình cookie để lưu JWT token
cookie_transport = CookieTransport(
    cookie_name="fastapiuserauth",  # Tên cookie
    cookie_max_age=3600,             # Expire sau 1 giờ (3600 giây)
    cookie_secure=False,             # True = chỉ gửi qua HTTPS (set False cho development)
    cookie_httponly=True,            # JavaScript không thể đọc cookie (bảo mật XSS)
    cookie_samesite="lax",           # Cookie chỉ gửi trong same-site requests
    cookie_path="/",                 # Cookie có hiệu lực trên toàn bộ domain
    cookie_domain=None       # Domain của cookie
)


# Strategy tạo và verify JWT token
def get_jwt_strategy() -> JWTStrategy:
    return JWTStrategy(secret=settings.SECRET_KEY, lifetime_seconds=settings.JWT_LIFETIME_SECONDS)

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
