"""
Database connection and management module.
"""
import asyncio
from contextlib import asynccontextmanager
from typing import Optional, Tuple
from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase
import redis.asyncio as redis
from loguru import logger

from .config import settings

# Global clients
_mongodb_client: Optional[AsyncIOMotorClient] = None
_redis_client: Optional[redis.Redis] = None


async def get_database() -> AsyncIOMotorDatabase:
    """Get MongoDB database connection."""
    global _mongodb_client
    
    if _mongodb_client is None:
        try:
            _mongodb_client = AsyncIOMotorClient(
                settings.MONGODB_URL,
                maxPoolSize=settings.MONGODB_MAX_CONNECTIONS,
                minPoolSize=settings.MONGODB_MIN_CONNECTIONS,
                serverSelectionTimeoutMS=5000,
                connectTimeoutMS=5000,
                socketTimeoutMS=5000
            )
            # Test connection
            await _mongodb_client.admin.command('ping')
            logger.info("MongoDB connection established")
        except Exception as e:
            logger.error(f"MongoDB connection failed: {e}")
            raise Exception("Database connection failed")
    
    return _mongodb_client[settings.MONGODB_DATABASE]


async def get_redis_client() -> redis.Redis:
    """Get Redis client connection."""
    global _redis_client
    
    if _redis_client is None:
        try:
            _redis_client = redis.from_url(
                settings.REDIS_URL,
                db=settings.REDIS_DB,
                password=settings.REDIS_PASSWORD,
                max_connections=settings.REDIS_MAX_CONNECTIONS,
                socket_connect_timeout=5,
                socket_timeout=5,
                retry_on_timeout=True
            )
            # Test connection
            await _redis_client.ping()
            logger.info("Redis connection established")
        except Exception as e:
            logger.error(f"Redis connection failed: {e}")
            raise Exception("Redis connection failed")
    
    return _redis_client


async def check_database_health() -> bool:
    """Check database health."""
    try:
        db = await get_database()
        await db.client.admin.command('ping')
        return True
    except Exception as e:
        logger.error(f"Database health check failed: {e}")
        return False


async def check_redis_health() -> bool:
    """Check Redis health."""
    try:
        redis_client = await get_redis_client()
        await redis_client.ping()
        return True
    except Exception as e:
        logger.error(f"Redis health check failed: {e}")
        return False


async def cleanup_database():
    """Cleanup database connections."""
    global _mongodb_client
    
    if _mongodb_client is not None:
        try:
            _mongodb_client.close()
            logger.info("MongoDB connection closed")
        except Exception as e:
            logger.error(f"Error closing MongoDB connection: {e}")
        finally:
            _mongodb_client = None


async def cleanup_redis():
    """Cleanup Redis connections."""
    global _redis_client
    
    if _redis_client is not None:
        try:
            await _redis_client.aclose()
            logger.info("Redis connection closed")
        except Exception as e:
            logger.error(f"Error closing Redis connection: {e}")
        finally:
            _redis_client = None


@asynccontextmanager
async def DatabaseContextManager():
    """Context manager for database operations."""
    db = None
    redis = None
    
    try:
        db = await get_database()
        redis = await get_redis_client()
        yield db, redis
    finally:
        if redis is not None:
            await cleanup_redis()
        if db is not None:
            await cleanup_database()


class DatabaseManager:
    """Singleton database manager."""
    _instance = None
    _initialized = False
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    async def initialize(self):
        """Initialize database connections."""
        if not self._initialized:
            try:
                await get_database()
                await get_redis_client()
                self._initialized = True
                logger.info("Database manager initialized")
            except Exception as e:
                logger.error(f"Database manager initialization failed: {e}")
                raise
    
    async def health_check(self) -> dict:
        """Perform comprehensive health check."""
        db_health = await check_database_health()
        redis_health = await check_redis_health()
        
        return {
            "database": "healthy" if db_health else "unhealthy",
            "redis": "healthy" if redis_health else "unhealthy",
            "overall": "healthy" if db_health and redis_health else "unhealthy"
        }
    
    async def cleanup(self):
        """Cleanup all connections."""
        await cleanup_database()
        await cleanup_redis()
        self._initialized = False
        logger.info("Database manager cleaned up")


# Global database manager instance
db_manager = DatabaseManager()