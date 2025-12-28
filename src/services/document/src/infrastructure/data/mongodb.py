from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase
from typing import Optional

from src.infrastructure.config.settings import settings


class MongoDBClient:
    """MongoDB client singleton."""

    _client: Optional[AsyncIOMotorClient] = None
    _database: Optional[AsyncIOMotorDatabase] = None

    @classmethod
    async def connect(cls):
        """Connect to MongoDB."""
        if cls._client is None:
            cls._client = AsyncIOMotorClient(settings.MONGODB_URL)
            cls._database = cls._client[settings.MONGODB_DATABASE]

    @classmethod
    async def disconnect(cls):
        """Disconnect from MongoDB."""
        if cls._client:
            cls._client.close()
            cls._client = None
            cls._database = None

    @classmethod
    def get_database(cls) -> AsyncIOMotorDatabase:
        """Get database instance."""
        if cls._database is None:
            raise RuntimeError("Database not connected. Call connect() first.")
        return cls._database

    @classmethod
    def get_collection(cls, name: str):
        """Get collection by name."""
        return cls.get_database()[name]


# Global instance
mongodb_client = MongoDBClient()
