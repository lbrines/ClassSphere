"""
Rate Limiter Middleware

CRITICAL OBJECTIVES:
- Implement rate limiting with Redis backend
- Support multiple time windows (minute, hour, day)
- Graceful degradation when Redis is unavailable
- Configurable limits per endpoint

DEPENDENCIES:
- redis
- asyncio
- logging
"""

import asyncio
import logging
from typing import Dict, Any, Optional
from datetime import datetime, timedelta, timezone
import json

from src.app.core.cache import get_cache
from src.app.core.config import get_settings

logger = logging.getLogger(__name__)

class RateLimiter:
    """
    Rate limiter implementation with Redis backend
    Supports multiple time windows and graceful degradation
    """
    
    def __init__(
        self,
        requests_per_minute: int = 60,
        requests_per_hour: int = 1000,
        requests_per_day: int = 10000,
        redis_url: str = None
    ):
        """
        Initialize rate limiter with configurable limits
        
        Args:
            requests_per_minute: Maximum requests per minute
            requests_per_hour: Maximum requests per hour
            requests_per_day: Maximum requests per day
            redis_url: Redis connection URL
        """
        self.requests_per_minute = requests_per_minute
        self.requests_per_hour = requests_per_hour
        self.requests_per_day = requests_per_day
        
        # Get Redis client
        self.redis_client = get_cache()
        
        logger.info(f"Rate limiter initialized: {requests_per_minute}/min, {requests_per_hour}/hour, {requests_per_day}/day")
    
    async def check_rate_limit(self, identifier: str, endpoint: str = "default") -> Dict[str, Any]:
        """
        Check if request is within rate limits
        
        Args:
            identifier: Client identifier (IP, user ID, etc.)
            endpoint: Endpoint being accessed
            
        Returns:
            Dict with allowed status, remaining requests, and reset time
        """
        try:
            # Create unique key for this identifier and endpoint
            key_prefix = f"rate_limit:{endpoint}:{identifier}"
            
            # Check all time windows
            minute_result = await self._check_window(key_prefix, "minute", self.requests_per_minute, 60)
            hour_result = await self._check_window(key_prefix, "hour", self.requests_per_hour, 3600)
            day_result = await self._check_window(key_prefix, "day", self.requests_per_day, 86400)
            
            # Request is allowed only if all windows allow it
            allowed = minute_result["allowed"] and hour_result["allowed"] and day_result["allowed"]
            
            # Get the most restrictive remaining count
            remaining = min(
                minute_result["remaining"],
                hour_result["remaining"],
                day_result["remaining"]
            )
            
            # Get the earliest reset time
            reset_times = [r["reset_time"] for r in [minute_result, hour_result, day_result] if r["reset_time"]]
            reset_time = min(reset_times) if reset_times else None
            
            return {
                "allowed": allowed,
                "remaining": remaining,
                "reset_time": reset_time,
                "limits": {
                    "minute": self.requests_per_minute,
                    "hour": self.requests_per_hour,
                    "day": self.requests_per_day
                }
            }
            
        except Exception as e:
            logger.error(f"Rate limiter error for {identifier}: {e}")
            # Graceful degradation: allow request when Redis is unavailable
            return {
                "allowed": True,
                "remaining": None,
                "reset_time": None,
                "limits": {
                    "minute": self.requests_per_minute,
                    "hour": self.requests_per_hour,
                    "day": self.requests_per_day
                },
                "error": "Rate limiter unavailable, allowing request"
            }
    
    async def _check_window(self, key_prefix: str, window: str, limit: int, ttl: int) -> Dict[str, Any]:
        """
        Check rate limit for a specific time window
        
        Args:
            key_prefix: Redis key prefix
            window: Window name (minute, hour, day)
            limit: Maximum requests for this window
            ttl: Time to live in seconds
            
        Returns:
            Dict with allowed status and remaining requests
        """
        try:
            key = f"{key_prefix}:{window}"
            
            # Get current count
            current_count = await self.redis_client.get(key)
            current_count = int(current_count) if current_count else 0
            
            # Check if limit would be exceeded
            if current_count >= limit:
                return {
                    "allowed": False,
                    "remaining": 0,
                    "reset_time": datetime.now(timezone.utc) + timedelta(seconds=ttl)
                }
            
            # Increment counter
            new_count = await self.redis_client.incr(key)
            
            # Set expiration if this is the first request
            if new_count == 1:
                await self.redis_client.expire(key, ttl)
            
            return {
                "allowed": True,
                "remaining": max(0, limit - new_count),
                "reset_time": datetime.now(timezone.utc) + timedelta(seconds=ttl)
            }
            
        except Exception as e:
            logger.error(f"Rate limiter window check error for {window}: {e}")
            # Graceful degradation: allow request
            return {
                "allowed": True,
                "remaining": None,
                "reset_time": None
            }
    
    async def reset_rate_limit(self, identifier: str, endpoint: str = "default") -> bool:
        """
        Reset rate limit for a specific identifier and endpoint
        
        Args:
            identifier: Client identifier
            endpoint: Endpoint being accessed
            
        Returns:
            True if reset was successful
        """
        try:
            key_prefix = f"rate_limit:{endpoint}:{identifier}"
            
            # Delete all time window keys
            keys_to_delete = [
                f"{key_prefix}:minute",
                f"{key_prefix}:hour",
                f"{key_prefix}:day"
            ]
            
            for key in keys_to_delete:
                await self.redis_client.delete(key)
            
            logger.info(f"Rate limit reset for {identifier} on {endpoint}")
            return True
            
        except Exception as e:
            logger.error(f"Rate limit reset error for {identifier}: {e}")
            return False
    
    async def get_rate_limit_status(self, identifier: str, endpoint: str = "default") -> Dict[str, Any]:
        """
        Get current rate limit status without incrementing counters
        
        Args:
            identifier: Client identifier
            endpoint: Endpoint being accessed
            
        Returns:
            Dict with current status
        """
        try:
            key_prefix = f"rate_limit:{endpoint}:{identifier}"
            
            # Get current counts for all windows
            minute_count = await self.redis_client.get(f"{key_prefix}:minute") or 0
            hour_count = await self.redis_client.get(f"{key_prefix}:hour") or 0
            day_count = await self.redis_client.get(f"{key_prefix}:day") or 0
            
            return {
                "current_usage": {
                    "minute": int(minute_count),
                    "hour": int(hour_count),
                    "day": int(day_count)
                },
                "limits": {
                    "minute": self.requests_per_minute,
                    "hour": self.requests_per_hour,
                    "day": self.requests_per_day
                },
                "remaining": {
                    "minute": max(0, self.requests_per_minute - int(minute_count)),
                    "hour": max(0, self.requests_per_hour - int(hour_count)),
                    "day": max(0, self.requests_per_day - int(day_count))
                }
            }
            
        except Exception as e:
            logger.error(f"Rate limit status error for {identifier}: {e}")
            return {
                "current_usage": {"minute": 0, "hour": 0, "day": 0},
                "limits": {
                    "minute": self.requests_per_minute,
                    "hour": self.requests_per_hour,
                    "day": self.requests_per_day
                },
                "remaining": {"minute": 0, "hour": 0, "day": 0},
                "error": "Rate limiter unavailable"
            }

# Global rate limiter instance
rate_limiter = RateLimiter()

async def check_rate_limit(identifier: str, endpoint: str = "default") -> Dict[str, Any]:
    """
    Check rate limit for a request
    
    Args:
        identifier: Client identifier
        endpoint: Endpoint being accessed
        
    Returns:
        Rate limit check result
    """
    return await rate_limiter.check_rate_limit(identifier, endpoint)

async def reset_rate_limit(identifier: str, endpoint: str = "default") -> bool:
    """
    Reset rate limit for a client
    
    Args:
        identifier: Client identifier
        endpoint: Endpoint being accessed
        
    Returns:
        True if reset was successful
    """
    return await rate_limiter.reset_rate_limit(identifier, endpoint)

async def get_rate_limit_status(identifier: str, endpoint: str = "default") -> Dict[str, Any]:
    """
    Get rate limit status for a client
    
    Args:
        identifier: Client identifier
        endpoint: Endpoint being accessed
        
    Returns:
        Rate limit status
    """
    return await rate_limiter.get_rate_limit_status(identifier, endpoint)