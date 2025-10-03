"""
Unit tests for database module
"""
import pytest
from unittest.mock import AsyncMock, patch
from motor.motor_asyncio import AsyncIOMotorClient

from src.app.core.database import get_database, get_redis_client


class TestDatabase:
    """Test cases for database connections."""
    
    @pytest.mark.asyncio
    async def test_get_database_success(self, mock_mongodb):
        """Test successful database connection."""
        with patch('src.app.core.database.AsyncIOMotorClient') as mock_client_class:
            mock_client_class.return_value = mock_mongodb
            
            db = await get_database()
            
            assert db is not None
            mock_client_class.assert_called_once()
            mock_mongodb.admin.command.assert_called_once()
    
    @pytest.mark.asyncio
    async def test_get_database_connection_error(self):
        """Test database connection error handling."""
        with patch('src.app.core.database.AsyncIOMotorClient') as mock_client_class:
            mock_client_class.side_effect = Exception("Connection failed")
            
            with pytest.raises(Exception, match="Connection failed"):
                await get_database()
    
    @pytest.mark.asyncio
    async def test_get_redis_client_success(self, mock_redis):
        """Test successful Redis connection."""
        with patch('src.app.core.database.AsyncRedis') as mock_redis_class:
            mock_redis_class.from_url.return_value = mock_redis
            
            redis_client = await get_redis_client()
            
            assert redis_client is not None
            mock_redis_class.from_url.assert_called_once()
            mock_redis.ping.assert_called_once()
    
    @pytest.mark.asyncio
    async def test_get_redis_client_connection_error(self):
        """Test Redis connection error handling."""
        with patch('src.app.core.database.AsyncRedis') as mock_redis_class:
            mock_redis_class.from_url.side_effect = Exception("Redis connection failed")
            
            with pytest.raises(Exception, match="Redis connection failed"):
                await get_redis_client()
    
    @pytest.mark.asyncio
    async def test_database_health_check_success(self, mock_mongodb):
        """Test database health check success."""
        with patch('src.app.core.database.get_database') as mock_get_db:
            mock_get_db.return_value = mock_mongodb
            
            from src.app.core.database import check_database_health
            
            result = await check_database_health()
            
            assert result is True
            mock_mongodb.client.admin.command.assert_called_once()
    
    @pytest.mark.asyncio
    async def test_database_health_check_failure(self):
        """Test database health check failure."""
        with patch('src.app.core.database.get_database') as mock_get_db:
            mock_db = AsyncMock()
            mock_db.admin.command.side_effect = Exception("Health check failed")
            mock_get_db.return_value = mock_db
            
            from src.app.core.database import check_database_health
            
            result = await check_database_health()
            
            assert result is False
    
    @pytest.mark.asyncio
    async def test_redis_health_check_success(self, mock_redis):
        """Test Redis health check success."""
        with patch('src.app.core.database.get_redis_client') as mock_get_redis:
            mock_get_redis.return_value = mock_redis
            
            from src.app.core.database import check_redis_health
            
            result = await check_redis_health()
            
            assert result is True
            mock_redis.ping.assert_called_once()
    
    @pytest.mark.asyncio
    async def test_redis_health_check_failure(self):
        """Test Redis health check failure."""
        with patch('src.app.core.database.get_redis_client') as mock_get_redis:
            mock_redis = AsyncMock()
            mock_redis.ping.side_effect = Exception("Redis ping failed")
            mock_get_redis.return_value = mock_redis
            
            from src.app.core.database import check_redis_health
            
            result = await check_redis_health()
            
            assert result is False
    
    @pytest.mark.asyncio
    async def test_database_cleanup_success(self, mock_mongodb):
        """Test database cleanup success."""
        with patch('src.app.core.database._mongodb_client', mock_mongodb):
            from src.app.core.database import cleanup_database
            
            await cleanup_database()
            
            mock_mongodb.close.assert_called_once()
    
    @pytest.mark.asyncio
    async def test_database_cleanup_error(self):
        """Test database cleanup error handling."""
        with patch('src.app.core.database.get_database') as mock_get_db:
            mock_db = AsyncMock()
            mock_db.close.side_effect = Exception("Cleanup failed")
            mock_get_db.return_value = mock_db
            
            from src.app.core.database import cleanup_database
            
            # Should not raise exception, just log error
            await cleanup_database()
            
            mock_db.close.assert_called_once()
    
    @pytest.mark.asyncio
    async def test_redis_cleanup_success(self, mock_redis):
        """Test Redis cleanup success."""
        with patch('src.app.core.database._redis_client', mock_redis):
            from src.app.core.database import cleanup_redis
            
            await cleanup_redis()
            
            mock_redis.close.assert_called_once()
    
    @pytest.mark.asyncio
    async def test_redis_cleanup_error(self):
        """Test Redis cleanup error handling."""
        with patch('src.app.core.database.get_redis_client') as mock_get_redis:
            mock_redis = AsyncMock()
            mock_redis.close.side_effect = Exception("Redis cleanup failed")
            mock_get_redis.return_value = mock_redis
            
            from src.app.core.database import cleanup_redis
            
            # Should not raise exception, just log error
            await cleanup_redis()
            
            mock_redis.close.assert_called_once()
    
    @pytest.mark.asyncio
    async def test_database_context_manager_success(self, mock_mongodb):
        """Test database context manager success."""
        with patch('src.app.core.database.get_database') as mock_get_db:
            mock_get_db.return_value = mock_mongodb
            
            from src.app.core.database import DatabaseContextManager
            
            async with DatabaseContextManager() as db:
                assert db is not None
            
            mock_mongodb.close.assert_called_once()
    
    @pytest.mark.asyncio
    async def test_database_context_manager_error(self):
        """Test database context manager error handling."""
        with patch('src.app.core.database.get_database') as mock_get_db:
            mock_db = AsyncMock()
            mock_db.close.side_effect = Exception("Context manager cleanup failed")
            mock_get_db.return_value = mock_db
            
            from src.app.core.database import DatabaseContextManager
            
            # Should handle cleanup errors gracefully
            async with DatabaseContextManager() as db:
                assert db is not None
            
            mock_db.close.assert_called_once()