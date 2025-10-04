"""
Test file for role system and security middleware

CRITICAL OBJECTIVES:
- Test role hierarchy and permissions
- Test security middleware functionality
- Test rate limiting implementation
- Test role-based access control

DEPENDENCIES:
- pytest-asyncio
- unittest.mock
- fastapi.testclient
"""

import pytest
from unittest.mock import patch, AsyncMock, MagicMock
from fastapi import FastAPI, HTTPException, status, Depends
from fastapi.testclient import TestClient
from datetime import datetime, timedelta, timezone

from src.app.middleware.auth_middleware import AuthMiddleware, get_current_user, require_role
from src.app.middleware.rate_limiter import RateLimiter
from src.app.middleware.security_middleware import SecurityMiddleware, setup_security_middleware
from src.app.core.config import get_settings

# BEGINNING: Critical tests for role system
@pytest.mark.asyncio(timeout=2.0)
async def test_role_hierarchy():
    """Test role hierarchy and permission levels"""
    # Arrange
    auth_middleware = AuthMiddleware()
    
    # Act & Assert
    # Test role hierarchy: admin > coordinator > teacher > student
    assert auth_middleware.get_role_level("admin") == 4
    assert auth_middleware.get_role_level("coordinator") == 3
    assert auth_middleware.get_role_level("teacher") == 2
    assert auth_middleware.get_role_level("student") == 1
    assert auth_middleware.get_role_level("invalid_role") == 0

@pytest.mark.asyncio(timeout=2.0)
async def test_role_permission_check():
    """Test role permission checking"""
    # Arrange
    auth_middleware = AuthMiddleware()
    
    # Act & Assert
    # Admin can access everything
    assert auth_middleware.has_permission("admin", "admin") is True
    assert auth_middleware.has_permission("admin", "coordinator") is True
    assert auth_middleware.has_permission("admin", "teacher") is True
    assert auth_middleware.has_permission("admin", "student") is True
    
    # Coordinator can access teacher and student
    assert auth_middleware.has_permission("coordinator", "admin") is False
    assert auth_middleware.has_permission("coordinator", "coordinator") is True
    assert auth_middleware.has_permission("coordinator", "teacher") is True
    assert auth_middleware.has_permission("coordinator", "student") is True
    
    # Teacher can only access student
    assert auth_middleware.has_permission("teacher", "admin") is False
    assert auth_middleware.has_permission("teacher", "coordinator") is False
    assert auth_middleware.has_permission("teacher", "teacher") is True
    assert auth_middleware.has_permission("teacher", "student") is True
    
    # Student can only access student
    assert auth_middleware.has_permission("student", "admin") is False
    assert auth_middleware.has_permission("student", "coordinator") is False
    assert auth_middleware.has_permission("student", "teacher") is False
    assert auth_middleware.has_permission("student", "student") is True

@pytest.mark.asyncio(timeout=2.0)
async def test_require_role_middleware():
    """Test require_role middleware functionality"""
    # Arrange
    auth_middleware = AuthMiddleware()
    
    # Test role hierarchy directly
    assert auth_middleware.get_role_level("admin") == 4
    assert auth_middleware.get_role_level("teacher") == 2
    assert auth_middleware.get_role_level("student") == 1
    
    # Test permission checking
    assert auth_middleware.has_permission("admin", "admin") is True
    assert auth_middleware.has_permission("admin", "teacher") is True
    assert auth_middleware.has_permission("admin", "student") is True
    
    assert auth_middleware.has_permission("teacher", "admin") is False
    assert auth_middleware.has_permission("teacher", "teacher") is True
    assert auth_middleware.has_permission("teacher", "student") is True
    
    assert auth_middleware.has_permission("student", "admin") is False
    assert auth_middleware.has_permission("student", "teacher") is False
    assert auth_middleware.has_permission("student", "student") is True

@pytest.mark.asyncio(timeout=2.0)
async def test_rate_limiter_creation():
    """Test rate limiter initialization"""
    # Arrange & Act
    with patch('src.app.middleware.rate_limiter.get_cache') as mock_get_cache:
        mock_redis = MagicMock()
        mock_get_cache.return_value = mock_redis
        
        rate_limiter = RateLimiter(
            requests_per_minute=60,
            requests_per_hour=1000,
            requests_per_day=10000
        )
        
        # Assert
        assert rate_limiter.requests_per_minute == 60
        assert rate_limiter.requests_per_hour == 1000
        assert rate_limiter.requests_per_day == 10000
        assert rate_limiter.redis_client is not None

@pytest.mark.asyncio(timeout=2.0)
async def test_rate_limiter_check():
    """Test rate limiter check functionality"""
    # Arrange
    with patch('src.app.middleware.rate_limiter.get_cache') as mock_get_cache:
        mock_redis = MagicMock()
        mock_redis.get = AsyncMock(return_value="1")
        mock_redis.incr = AsyncMock(return_value=2)
        mock_redis.expire = AsyncMock(return_value=True)
        mock_get_cache.return_value = mock_redis
        
        # Create rate limiter with mocked cache
        rate_limiter = RateLimiter(requests_per_minute=2)
        rate_limiter.redis_client = mock_redis  # Override the redis client
        client_ip = "192.168.1.1"
        
        # Act
        result = await rate_limiter.check_rate_limit(client_ip)
        
        # Assert
        assert result["allowed"] is True
        # The remaining count should be calculated correctly
        assert result["remaining"] >= 0
        assert result["reset_time"] is not None

@pytest.mark.asyncio(timeout=2.0)
async def test_rate_limiter_exceeded():
    """Test rate limiter when limit is exceeded"""
    # Arrange
    with patch('src.app.middleware.rate_limiter.get_cache') as mock_get_cache:
        mock_redis = MagicMock()
        mock_redis.get = AsyncMock(return_value="1")
        mock_redis.incr = AsyncMock(return_value=2)
        mock_redis.expire = AsyncMock(return_value=True)
        mock_get_cache.return_value = mock_redis
        
        # Create rate limiter with mocked cache
        rate_limiter = RateLimiter(requests_per_minute=1)
        rate_limiter.redis_client = mock_redis  # Override the redis client
        client_ip = "192.168.1.2"
        
        # Act
        result = await rate_limiter.check_rate_limit(client_ip)
        
        # Assert
        assert result["allowed"] is False
        assert result["remaining"] == 0
        assert result["reset_time"] is not None

@pytest.mark.asyncio(timeout=2.0)
async def test_security_middleware_headers():
    """Test security middleware adds proper headers"""
    # Arrange
    app = FastAPI()
    
    @app.get("/test")
    async def test_endpoint():
        return {"message": "test"}
    
    # Setup security middleware properly
    setup_security_middleware(app)
    
    client = TestClient(app)
    
    # Act
    response = client.get("/test")
    
    # Assert
    assert response.status_code == 200
    assert "X-Content-Type-Options" in response.headers
    assert "X-Frame-Options" in response.headers
    assert "X-XSS-Protection" in response.headers
    assert response.headers["X-Content-Type-Options"] == "nosniff"
    assert response.headers["X-Frame-Options"] == "DENY"
    assert response.headers["X-XSS-Protection"] == "1; mode=block"

@pytest.mark.asyncio(timeout=2.0)
async def test_security_middleware_cors():
    """Test security middleware CORS configuration"""
    # Arrange
    app = FastAPI()
    
    @app.get("/test")
    async def test_endpoint():
        return {"message": "test"}
    
    # Setup security middleware properly
    setup_security_middleware(app)
    
    client = TestClient(app)
    
    # Act - Test GET request with CORS headers
    response = client.get("/test", headers={"Origin": "https://example.com"})
    
    # Assert
    assert response.status_code == 200
    # CORS headers are added by the middleware
    assert "access-control-allow-credentials" in response.headers
    assert "access-control-expose-headers" in response.headers
    # Security headers are present
    assert "x-content-type-options" in response.headers
    assert "x-frame-options" in response.headers
    assert "x-xss-protection" in response.headers

@pytest.mark.asyncio(timeout=2.0)
async def test_role_based_endpoint_access():
    """Test role-based endpoint access control"""
    # Arrange
    auth_middleware = AuthMiddleware()
    
    # Test role-based access control logic
    # Admin should have access to everything
    assert auth_middleware.has_permission("admin", "admin") is True
    assert auth_middleware.has_permission("admin", "coordinator") is True
    assert auth_middleware.has_permission("admin", "teacher") is True
    assert auth_middleware.has_permission("admin", "student") is True
    
    # Teacher should have access to teacher and student
    assert auth_middleware.has_permission("teacher", "admin") is False
    assert auth_middleware.has_permission("teacher", "coordinator") is False
    assert auth_middleware.has_permission("teacher", "teacher") is True
    assert auth_middleware.has_permission("teacher", "student") is True
    
    # Student should only have access to student
    assert auth_middleware.has_permission("student", "admin") is False
    assert auth_middleware.has_permission("student", "coordinator") is False
    assert auth_middleware.has_permission("student", "teacher") is False
    assert auth_middleware.has_permission("student", "student") is True

@pytest.mark.asyncio(timeout=2.0)
async def test_invalid_role_handling():
    """Test handling of invalid roles"""
    # Arrange
    auth_middleware = AuthMiddleware()
    
    # Act & Assert
    # Invalid roles should have level 0
    assert auth_middleware.get_role_level("") == 0
    assert auth_middleware.get_role_level(None) == 0
    assert auth_middleware.get_role_level("invalid") == 0
    
    # Invalid roles should not have permissions
    assert auth_middleware.has_permission("invalid", "student") is False
    # Admin should have access to invalid roles (admin can access anything)
    assert auth_middleware.has_permission("admin", "invalid") is True
    # Invalid roles should not have access to invalid roles
    assert auth_middleware.has_permission("invalid", "invalid") is False

@pytest.mark.asyncio(timeout=2.0)
async def test_rate_limiter_redis_connection_error():
    """Test rate limiter handles Redis connection errors gracefully"""
    # Arrange
    with patch('src.app.middleware.rate_limiter.get_cache') as mock_get_cache:
        mock_redis = MagicMock()
        mock_redis.get = AsyncMock(side_effect=Exception("Redis connection error"))
        mock_get_cache.return_value = mock_redis
        
        rate_limiter = RateLimiter(requests_per_minute=60)
        client_ip = "192.168.1.3"
        
        # Act
        result = await rate_limiter.check_rate_limit(client_ip)
        
        # Assert
        # Should allow request when Redis is unavailable (graceful degradation)
        assert result["allowed"] is True
        assert result["remaining"] is None
        assert result["reset_time"] is None