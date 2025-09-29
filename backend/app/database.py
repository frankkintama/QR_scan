import os
from motor.motor_asyncio import AsyncIOMotorClient
from beanie import init_beanie
from dotenv import load_dotenv

from app.models import User

load_dotenv()  # load .env file

MONGO_URI = os.getenv("MONGO_URI", "mongodb://root:password@mongo:27017?authSource=admin")
MONGO_DB = os.getenv("MONGO_DB", "mydatabase")


async def init_db():
    client = AsyncIOMotorClient(MONGO_URI)
    db = client[MONGO_DB]
    await init_beanie(database=db, document_models=[User])
    print(f"Connected to MongoDB at {MONGO_URI}, using database {MONGO_DB}")
