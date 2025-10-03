"""
Database module for Dashboard Educativo Backend
Handles MongoDB and Redis connections with error prevention and cleanup
"""
import asyncio
import logging
from contextlib import asynccontextmanager
from typing import Optional
from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase
from redis import Redis
from redis.asyncio import Redis as AsyncRedis

from .config import settings

logger = logging.getLogger(__name__)

# Global database clients
_mongodb_client: Optional[AsyncIOMotorClient] = None
_redis_client: Optional[AsyncRedis] = None


async def get_database() -> AsyncIOMotorDatabase:
    """
    Get MongoDB database connection.
    Implements connection pooling and error handling.
    """
    global _mongodb_client
    
    try:
        if _mongodb_client is None:
            _mongodb_client = AsyncIOMotorClient(
                settings.MONGODB_URL,
                maxPoolSize=settings.MAX_CONNECTIONS,
                serverSelectionTimeoutMS=settings.CONNECTION_TIMEOUT * 1000,
                connectTimeoutMS=settings.CONNECTION_TIMEOUT * 1000,
                socketTimeoutMS=settings.REQUEST_TIMEOUT * 1000
            )
            
            # Test connection
            await _mongodb_client.admin.command('ping')
            logger.info("MongoDB connection established successfully")
        
        return _mongodb_client[settings.MONGODB_DATABASE]
        
    except Exception as e:
        logger.error(f"Failed to connect to MongoDB: {e}")
        raise Exception(f"Database connection failed: {e}")


async def get_redis_client() -> AsyncRedis:
    """
    Get Redis client connection.
    Implements connection pooling and error handling.
    """
    global _redis_client
    
    try:
        if _redis_client is None:
            _redis_client = AsyncRedis.from_url(
                settings.REDIS_URL,
                db=settings.REDIS_DB,
                password=settings.REDIS_PASSWORD,
                max_connections=settings.MAX_CONNECTIONS,
                socket_connect_timeout=settings.CONNECTION_TIMEOUT,
                socket_timeout=settings.REQUEST_TIMEOUT,
                retry_on_timeout=True
            )
            
            # Test connection
            await _redis_client.ping()
            logger.info("Redis connection established successfully")
        
        return _redis_client
        
    except Exception as e:
        logger.error(f"Failed to connect to Redis: {e}")
        raise Exception(f"Redis connection failed: {e}")


async def check_database_health() -> bool:
    """
    Check MongoDB database health.
    Returns True if healthy, False otherwise.
    """
    try:
        db = await get_database()
        await db.client.admin.command('ping')
        return True
    except Exception as e:
        logger.error(f"Database health check failed: {e}")
        return False


async def check_redis_health() -> bool:
    """
    Check Redis health.
    Returns True if healthy, False otherwise.
    """
    try:
        redis_client = await get_redis_client()
        await redis_client.ping()
        return True
    except Exception as e:
        logger.error(f"Redis health check failed: {e}")
        return False


async def cleanup_database() -> None:
    """
    Cleanup MongoDB connection.
    Implements graceful shutdown with error handling.
    """
    global _mongodb_client
    
    try:
        if _mongodb_client is not None:
            _mongodb_client.close()
            _mongodb_client = None
            logger.info("MongoDB connection closed successfully")
    except Exception as e:
        logger.error(f"Error closing MongoDB connection: {e}")


async def cleanup_redis() -> None:
    """
    Cleanup Redis connection.
    Implements graceful shutdown with error handling.
    """
    global _redis_client
    
    try:
        if _redis_client is not None:
            await _redis_client.close()
            _redis_client = None
            logger.info("Redis connection closed successfully")
    except Exception as e:
        logger.error(f"Error closing Redis connection: {e}")


@asynccontextmanager
async def DatabaseContextManager():
    """
    Context manager for database operations.
    Ensures proper cleanup and error handling.
    """
    db = None
    redis = None
    
    try:
        # Initialize connections
        db = await get_database()
        redis = await get_redis_client()
        
        yield db, redis
        
    except Exception as e:
        logger.error(f"Database context manager error: {e}")
        raise
    finally:
        # Cleanup connections
        try:
            if redis is not None:
                await cleanup_redis()
            if db is not None:
                await cleanup_database()
        except Exception as e:
            logger.error(f"Error during database cleanup: {e}")


class DatabaseManager:
    """
    Database manager class for handling connections and operations.
    Implements singleton pattern with proper cleanup.
    """
    
    _instance: Optional['DatabaseManager'] = None
    _mongodb_client: Optional[AsyncIOMotorClient] = None
    _redis_client: Optional[AsyncRedis] = None
    
    def __new__(cls) -> 'DatabaseManager':
        """Singleton pattern implementation."""
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    async def get_database(self) -> AsyncIOMotorDatabase:
        """Get database instance."""
        return await get_database()
    
    async def get_redis(self) -> AsyncRedis:
        """Get Redis instance."""
        return await get_redis_client()
    
    async def health_check(self) -> dict:
        """
        Perform comprehensive health check.
        Returns health status for all services.
        """
        try:
            # Check MongoDB
            mongodb_healthy = await check_database_health()
            
            # Check Redis
            redis_healthy = await check_redis_health()
            
            return {
                "mongodb": {
                    "status": "healthy" if mongodb_healthy else "unhealthy",
                    "url": settings.MONGODB_URL,
                    "database": settings.MONGODB_DATABASE
                },
                "redis": {
                    "status": "healthy" if redis_healthy else "unhealthy",
                    "url": settings.REDIS_URL,
                    "db": settings.REDIS_DB
                },
                "overall": "healthy" if (mongodb_healthy and redis_healthy) else "unhealthy"
            }
            
        except Exception as e:
            logger.error(f"Health check failed: {e}")
            return {
                "mongodb": {"status": "error", "error": str(e)},
                "redis": {"status": "error", "error": str(e)},
                "overall": "error"
            }
    
    async def cleanup(self) -> None:
        """Cleanup all connections."""
        try:
            await cleanup_database()
            await cleanup_redis()
            logger.info("All database connections cleaned up successfully")
        except Exception as e:
            logger.error(f"Error during cleanup: {e}")


# Global database manager instance
db_manager = DatabaseManager()