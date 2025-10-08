import os
from dotenv import load_dotenv

from motor.motor_asyncio import AsyncIOMotorClient
from beanie import init_beanie
from app.models import User

load_dotenv()


class Settings:
    # Security
    SECRET_KEY: str = os.getenv("SECRET")
    
    # JWT
    JWT_LIFETIME_SECONDS: int = 3600
    
    # Database
    MONGO_URI: str = os.getenv("MONGO_URI")
    MONGO_DB: str = os.getenv("MONGO_DB")


settings = Settings()

async def init_db():
    #Tạo client kết nối đến MongoDB, motor cho phép làm việc với MongoDB
    client = AsyncIOMotorClient(settings.MONGO_URI)
    #chọn database để dùng
    db = client[settings.MONGO_DB]
    await init_beanie(database=db, document_models=[User])
    print(f"Connected to MongoDB at {settings.MONGO_URI}, using database {settings.MONGO_DB}")
