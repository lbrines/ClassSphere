"""
Database configuration and connection management
"""
from motor.motor_asyncio import AsyncIOMotorClient
from redis import Redis
from src.app.core.config import settings
from typing import Optional


class Database:
    """Database connection manager"""
    
    def __init__(self):
        self.mongodb_client: Optional[AsyncIOMotorClient] = None
        self.redis_client: Optional[Redis] = None
    
    async def connect_to_mongodb(self):
        """Connect to MongoDB"""
        self.mongodb_client = AsyncIOMotorClient(settings.mongodb_url)
        # Test connection
        await self.mongodb_client.admin.command('ping')
        print("Connected to MongoDB")
    
    def connect_to_redis(self):
        """Connect to Redis"""
        self.redis_client = Redis.from_url(settings.redis_url)
        # Test connection
        self.redis_client.ping()
        print("Connected to Redis")
    
    async def close_mongodb_connection(self):
        """Close MongoDB connection"""
        if self.mongodb_client:
            self.mongodb_client.close()
            print("Disconnected from MongoDB")
    
    def close_redis_connection(self):
        """Close Redis connection"""
        if self.redis_client:
            self.redis_client.close()
            print("Disconnected from Redis")
    
    def get_mongodb_database(self):
        """Get MongoDB database instance"""
        if not self.mongodb_client:
            raise Exception("MongoDB not connected")
        return self.mongodb_client.dashboard_educativo
    
    def get_redis_client(self):
        """Get Redis client instance"""
        if not self.redis_client:
            raise Exception("Redis not connected")
        return self.redis_client


# Global database instance
database = Database()
