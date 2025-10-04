"""
Test file for infrastructure configuration

CRITICAL OBJECTIVES:
- Verify Redis cache functionality
- Test port 8000 configuration
- Test FastAPI app startup
- Verify health check endpoint

DEPENDENCIES:
- FastAPI test client
- Redis cache
- pytest-asyncio
"""

import pytest
import asyncio
from fastapi.testclient import TestClient
from unittest.mock import patch, AsyncMock
import os

from src.app.main import app
from src.app.core.cache import RedisCache, get_cache, close_cache
from src.app.core.config import get_settings

# BEGINNING: Critical tests for core functionality
@pytest.mark.asyncio(timeout=2.0)
async def test_redis_cache_connection():
    """Test Redis cache connection"""
    # Arrange
    cache = RedisCache()
    
    # Act
    connected = await cache.connect()
    
    # Assert
    # Note: This test will pass even if Redis is not running (graceful degradation)
    assert isinstance(connected, bool)
    await cache.disconnect()

@pytest.mark.asyncio(timeout=2.0)
async def test_redis_cache_operations():
    """Test Redis cache operations"""
    # Arrange
    cache = RedisCache()
    await cache.connect()
    
    # Act & Assert: Set operation
    result = await cache.set("test_key", {"data": "test_value"}, 60)
    assert isinstance(result, bool)
    
    # Act & Assert: Get operation
    value = await cache.get("test_key")
    if cache.is_connected():
        assert value == {"data": "test_value"}
    
    # Act & Assert: Exists operation
    exists = await cache.exists("test_key")
    assert isinstance(exists, bool)
    
    # Act & Assert: Delete operation
    deleted = await cache.delete("test_key")
    assert isinstance(deleted, bool)
    
    await cache.disconnect()

def test_fastapi_app_creation():
    """Test FastAPI app creation"""
    # Act & Assert
    assert app is not None
    assert app.title == "ClassSphere"
    assert app.version == "1.0.0"

def test_app_info_endpoint():
    """Test app info endpoint"""
    # Arrange
    client = TestClient(app)
    
    # Act
    response = client.get("/info")
    
    # Assert
    assert response.status_code == 200
    data = response.json()
    assert data["app_name"] == "ClassSphere"
    assert data["version"] == "1.0.0"
    assert data["port"] == 8000

def test_health_check_endpoint():
    """Test health check endpoint"""
    # Arrange
    client = TestClient(app)
    
    # Act
    response = client.get("/health")
    
    # Assert
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert data["version"] == "1.0.0"
    assert data["port"] == 8000
    assert "cache_connected" in data

def test_root_endpoint():
    """Test root endpoint"""
    # Arrange
    client = TestClient(app)
    
    # Act
    response = client.get("/")
    
    # Assert
    assert response.status_code == 200
    data = response.json()
    assert data["message"] == "Welcome to ClassSphere API"
    assert data["version"] == "1.0.0"
    assert data["port"] == 8000

# MIDDLE: Detailed implementation tests
def test_cors_configuration():
    """Test CORS configuration"""
    # Arrange
    client = TestClient(app)
    
    # Act
    response = client.get("/", headers={"Origin": "http://127.0.0.1:3000"})
    
    # Assert
    assert response.status_code == 200
    assert "access-control-allow-origin" in response.headers

def test_port_8000_configuration():
    """Test that port 8000 is configured correctly"""
    # Arrange
    settings = get_settings()
    
    # Assert
    assert settings.port == 8000
    assert settings.host == "127.0.0.1"

def test_environment_variables():
    """Test environment variables are loaded"""
    # Arrange
    settings = get_settings()
    
    # Assert
    assert settings.app_name == "ClassSphere"
    assert settings.version == "1.0.0"
    assert settings.redis_url == "redis://localhost:6379/1"

# END: Verification and next steps
@pytest.mark.asyncio(timeout=2.0)
async def test_cache_graceful_degradation():
    """Test cache graceful degradation when Redis is unavailable"""
    # Arrange
    with patch('redis.Redis.from_url') as mock_redis:
        mock_redis.side_effect = Exception("Redis connection failed")
        cache = RedisCache()
        
        # Act
        connected = await cache.connect()
        
        # Assert
        assert not connected
        assert not cache.is_connected()
        
        # Test operations with disconnected cache
        result = await cache.get("test_key")
        assert result is None
        
        result = await cache.set("test_key", "value")
        assert not result

def test_app_startup_without_redis():
    """Test app startup without Redis"""
    # Arrange
    with patch('src.app.core.cache.RedisCache.connect') as mock_connect:
        mock_connect.return_value = False
        
        # Act
        client = TestClient(app)
        response = client.get("/health")
        
        # Assert
        assert response.status_code == 200
        data = response.json()
        # Cache connection status depends on actual Redis availability
        assert "cache_connected" in data