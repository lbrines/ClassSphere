import pytest
from unittest.mock import patch, AsyncMock, Mock
from contextlib import asynccontextmanager
from src.app.main import lifespan, app

class TestLifespan:
    @pytest.mark.asyncio
    async def test_lifespan_startup_success(self):
        """Test lifespan startup success"""
        with patch('src.app.main.database') as mock_db:
            mock_db.connect_to_mongodb = AsyncMock()
            mock_db.connect_to_redis = Mock()
            
            async with lifespan(app):
                mock_db.connect_to_mongodb.assert_called_once()
                mock_db.connect_to_redis.assert_called_once()
    
    @pytest.mark.asyncio
    async def test_lifespan_startup_mongodb_error(self):
        """Test lifespan startup with MongoDB error"""
        with patch('src.app.main.database') as mock_db:
            mock_db.connect_to_mongodb = AsyncMock(side_effect=Exception("MongoDB connection failed"))
            mock_db.connect_to_redis = Mock()
            
            async with lifespan(app):
                mock_db.connect_to_mongodb.assert_called_once()
                mock_db.connect_to_redis.assert_not_called()
    
    @pytest.mark.asyncio
    async def test_lifespan_startup_redis_error(self):
        """Test lifespan startup with Redis error"""
        with patch('src.app.main.database') as mock_db:
            mock_db.connect_to_mongodb = AsyncMock()
            mock_db.connect_to_redis = Mock(side_effect=Exception("Redis connection failed"))
            
            async with lifespan(app):
                mock_db.connect_to_mongodb.assert_called_once()
                mock_db.connect_to_redis.assert_called_once()
    
    @pytest.mark.asyncio
    async def test_lifespan_shutdown_success(self):
        """Test lifespan shutdown success"""
        with patch('src.app.main.database') as mock_db:
            mock_db.connect_to_mongodb = AsyncMock()
            mock_db.connect_to_redis = Mock()
            mock_db.close_mongodb_connection = AsyncMock()
            mock_db.close_redis_connection = Mock()
            
            async with lifespan(app):
                pass
            
            mock_db.close_mongodb_connection.assert_called_once()
            mock_db.close_redis_connection.assert_called_once()
    
    @pytest.mark.asyncio
    async def test_lifespan_shutdown_mongodb_error(self):
        """Test lifespan shutdown with MongoDB error"""
        with patch('src.app.main.database') as mock_db:
            mock_db.connect_to_mongodb = AsyncMock()
            mock_db.connect_to_redis = Mock()
            mock_db.close_mongodb_connection = AsyncMock(side_effect=Exception("MongoDB shutdown failed"))
            mock_db.close_redis_connection = Mock()
            
            async with lifespan(app):
                pass
            
            mock_db.close_mongodb_connection.assert_called_once()
            mock_db.close_redis_connection.assert_not_called()
    
    @pytest.mark.asyncio
    async def test_lifespan_shutdown_redis_error(self):
        """Test lifespan shutdown with Redis error"""
        with patch('src.app.main.database') as mock_db:
            mock_db.connect_to_mongodb = AsyncMock()
            mock_db.connect_to_redis = Mock()
            mock_db.close_mongodb_connection = AsyncMock()
            mock_db.close_redis_connection = Mock(side_effect=Exception("Redis shutdown failed"))
            
            async with lifespan(app):
                pass
            
            mock_db.close_mongodb_connection.assert_called_once()
            mock_db.close_redis_connection.assert_called_once()
    
    @pytest.mark.asyncio
    async def test_lifespan_full_cycle(self):
        """Test complete lifespan cycle"""
        with patch('src.app.main.database') as mock_db:
            mock_db.connect_to_mongodb = AsyncMock()
            mock_db.connect_to_redis = Mock()
            mock_db.close_mongodb_connection = AsyncMock()
            mock_db.close_redis_connection = Mock()
            
            async with lifespan(app):
                mock_db.connect_to_mongodb.assert_called_once()
                mock_db.connect_to_redis.assert_called_once()
            
            mock_db.close_mongodb_connection.assert_called_once()
            mock_db.close_redis_connection.assert_called_once()