"""Database connections and management (Redis only)."""

import asyncio
import logging
from typing import Optional
import redis.asyncio as redis
from redis.asyncio import Redis

from .config import settings

logger = logging.getLogger(__name__)

# Global Redis client
_redis_client: Optional[Redis] = None


async def get_redis_client() -> Redis:
    """Get Redis client instance."""
    global _redis_client

    if _redis_client is None:
        try:
            _redis_client = redis.from_url(
                settings.redis_url,
                password=settings.redis_password,
                db=settings.redis_db,
                decode_responses=True,
                retry_on_timeout=True
            )
            # Test connection
            await _redis_client.ping()
            logger.info("Redis connection established successfully")
        except Exception as e:
            logger.error(f"Failed to connect to Redis: {e}")
            # Create a mock client for testing
            _redis_client = None
            raise

    return _redis_client


async def get_database():
    """Get database client (Redis only - no MongoDB)."""
    try:
        redis_client = await get_redis_client()
        return {"redis": redis_client}
    except Exception as e:
        logger.warning(f"Database connection warning: {e}")
        return {"redis": None}


async def check_database_health() -> dict:
    """Check database health status."""
    health = {"redis": False}

    try:
        redis_client = await get_redis_client()
        if redis_client:
            await redis_client.ping()
            health["redis"] = True
    except Exception as e:
        logger.warning(f"Redis health check failed: {e}")

    return health


async def cleanup_database():
    """Clean up database connections."""
    global _redis_client

    if _redis_client:
        try:
            await _redis_client.aclose()
            logger.info("Redis connection closed")
        except Exception as e:
            logger.error(f"Error closing Redis connection: {e}")
        finally:
            _redis_client = None


async def cleanup_redis():
    """Clean up Redis connection specifically."""
    await cleanup_database()