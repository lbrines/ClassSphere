"""
Redis cache configuration for ClassSphere

CRITICAL OBJECTIVES:
- Configure Redis connection with proper error handling
- Implement cache operations with async support
- Provide fallback when Redis is unavailable

DEPENDENCIES:
- redis[hiredis]
- asyncio
"""

import json
import asyncio
import logging
from typing import Optional, Any, Dict, Union
from redis import Redis
from redis.exceptions import ConnectionError, TimeoutError
import os

logger = logging.getLogger(__name__)

class CacheError(Exception):
    """Custom exception for cache operations"""
    pass

class RedisCache:
    """Redis cache client with error handling and fallback"""
    
    def __init__(self, redis_url: str = None):
        self.redis_url = redis_url or os.getenv("REDIS_URL", "redis://localhost:6379/1")
        self._client: Optional[Redis] = None
        self._is_connected = False
    
    async def connect(self) -> bool:
        """Connect to Redis with error handling"""
        try:
            self._client = Redis.from_url(self.redis_url, decode_responses=True)
            # Test connection
            self._client.ping()
            self._is_connected = True
            logger.info("✅ Redis connected successfully")
            return True
        except (ConnectionError, TimeoutError) as e:
            logger.warning(f"⚠️ Redis connection failed: {e}")
            self._is_connected = False
            return False
        except Exception as e:
            logger.error(f"❌ Redis connection error: {e}")
            self._is_connected = False
            return False
    
    async def disconnect(self):
        """Disconnect from Redis"""
        if self._client:
            try:
                self._client.close()
                self._is_connected = False
                logger.info("🔌 Redis disconnected")
            except Exception as e:
                logger.error(f"❌ Redis disconnect error: {e}")
    
    def is_connected(self) -> bool:
        """Check if Redis is connected"""
        return self._is_connected
    
    async def get(self, key: str) -> Optional[Any]:
        """Get value from cache"""
        if not self._is_connected or not self._client:
            return None
        
        try:
            value = self._client.get(key)
            if value:
                return json.loads(value)
            return None
        except (ConnectionError, TimeoutError) as e:
            logger.warning(f"⚠️ Redis get error: {e}")
            return None
        except Exception as e:
            logger.error(f"❌ Redis get error: {e}")
            return None
    
    async def set(self, key: str, value: Any, expire: int = 3600) -> bool:
        """Set value in cache with expiration"""
        if not self._is_connected or not self._client:
            return False
        
        try:
            serialized_value = json.dumps(value)
            result = self._client.set(key, serialized_value, ex=expire)
            return bool(result)
        except (ConnectionError, TimeoutError) as e:
            logger.warning(f"⚠️ Redis set error: {e}")
            return False
        except Exception as e:
            logger.error(f"❌ Redis set error: {e}")
            return False
    
    async def delete(self, key: str) -> bool:
        """Delete key from cache"""
        if not self._is_connected or not self._client:
            return False
        
        try:
            result = self._client.delete(key)
            return bool(result)
        except (ConnectionError, TimeoutError) as e:
            logger.warning(f"⚠️ Redis delete error: {e}")
            return False
        except Exception as e:
            logger.error(f"❌ Redis delete error: {e}")
            return False
    
    async def exists(self, key: str) -> bool:
        """Check if key exists in cache"""
        if not self._is_connected or not self._client:
            return False
        
        try:
            result = self._client.exists(key)
            return bool(result)
        except (ConnectionError, TimeoutError) as e:
            logger.warning(f"⚠️ Redis exists error: {e}")
            return False
        except Exception as e:
            logger.error(f"❌ Redis exists error: {e}")
            return False

# Global cache instance
_cache_instance: Optional[RedisCache] = None

async def get_cache() -> RedisCache:
    """Get or create cache instance"""
    global _cache_instance
    if _cache_instance is None:
        _cache_instance = RedisCache()
        await _cache_instance.connect()
    return _cache_instance

async def close_cache():
    """Close cache connection"""
    global _cache_instance
    if _cache_instance:
        await _cache_instance.disconnect()
        _cache_instance = None