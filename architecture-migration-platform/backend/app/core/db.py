from motor.motor_asyncio import AsyncIOMotorClient
import os
from dotenv import load_dotenv

load_dotenv()

class Database:
    """Manages dynamic state and AIR graph storage for the platform."""
    client: AsyncIOMotorClient = None
    db = None

    @classmethod
    def connect(cls):
        # Defaults to local MongoDB if no env var is set
        uri = os.getenv("MONGO_URI", "mongodb://localhost:27017")
        cls.client = AsyncIOMotorClient(uri)
        cls.db = cls.client.migration_platform
        print("Successfully connected to MongoDB.")

    @classmethod
    def disconnect(cls):
        if cls.client:
            cls.client.close()

def get_db():
    return Database.db