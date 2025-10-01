import os
from motor.motor_asyncio import AsyncIOMotorClient
from beanie import init_beanie
from dotenv import load_dotenv

from app.models import User

load_dotenv()  # load .env file

MONGO_URI = os.getenv("MONGO_URI")
MONGO_DB = os.getenv("MONGO_DB")


async def init_db():
    #Tạo client kết nối đến MongoDB, motor cho phép làm việc với MongoDB
    client = AsyncIOMotorClient(MONGO_URI)
    #chọn database để dùng
    db = client[MONGO_DB]
    await init_beanie(database=db, document_models=[User])
    print(f"Connected to MongoDB at {MONGO_URI}, using database {MONGO_DB}")
