"""
Tests for lifespan context manager
"""
import pytest
from unittest.mock import patch, AsyncMock, Mock
from contextlib import asynccontextmanager
from src.app.main import lifespan, app


class TestLifespan:
    """Test lifespan context manager"""
    
    @pytest.mark.asyncio
    async def test_lifespan_startup_success(self):
        """Test successful startup"""
        with patch('src.app.main.database') as mock_db:
            mock_db.connect_to_mongodb = AsyncMock()
            mock_db.connect_to_redis = Mock()
            
            # Test the lifespan context manager
            async with lifespan(app):
                # Verify startup was called
                mock_db.connect_to_mongodb.assert_called_once()
                mock_db.connect_to_redis.assert_called_once()
    
    @pytest.mark.asyncio
    async def test_lifespan_startup_mongodb_error(self):
        """Test startup with MongoDB connection error"""
        with patch('src.app.main.database') as mock_db:
            mock_db.connect_to_mongodb = AsyncMock(side_effect=Exception("MongoDB connection failed"))
            mock_db.connect_to_redis = Mock()
            
            # Test the lifespan context manager with MongoDB error
            async with lifespan(app):
                # MongoDB should fail, Redis should not be called
                mock_db.connect_to_mongodb.assert_called_once()
                mock_db.connect_to_redis.assert_not_called()
    
    @pytest.mark.asyncio
    async def test_lifespan_startup_redis_error(self):
        """Test startup with Redis connection error"""
        with patch('src.app.main.database') as mock_db:
            mock_db.connect_to_mongodb = AsyncMock()
            mock_db.connect_to_redis = Mock(side_effect=Exception("Redis connection failed"))
            
            # Test the lifespan context manager with Redis error
            async with lifespan(app):
                # MongoDB should succeed, Redis should fail
                mock_db.connect_to_mongodb.assert_called_once()
                mock_db.connect_to_redis.assert_called_once()
    
    @pytest.mark.asyncio
    async def test_lifespan_shutdown_success(self):
        """Test successful shutdown"""
        with patch('src.app.main.database') as mock_db:
            mock_db.connect_to_mongodb = AsyncMock()
            mock_db.connect_to_redis = Mock()
            mock_db.close_mongodb_connection = AsyncMock()
            mock_db.close_redis_connection = Mock()
            
            # Test the lifespan context manager
            async with lifespan(app):
                pass  # This will trigger shutdown
            
            # Verify shutdown was called
            mock_db.close_mongodb_connection.assert_called_once()
            mock_db.close_redis_connection.assert_called_once()
    
    @pytest.mark.asyncio
    async def test_lifespan_shutdown_mongodb_error(self):
        """Test shutdown with MongoDB error"""
        with patch('src.app.main.database') as mock_db:
            mock_db.connect_to_mongodb = AsyncMock()
            mock_db.connect_to_redis = Mock()
            mock_db.close_mongodb_connection = AsyncMock(side_effect=Exception("MongoDB shutdown failed"))
            mock_db.close_redis_connection = Mock()
            
            # Test the lifespan context manager with MongoDB shutdown error
            async with lifespan(app):
                pass  # This will trigger shutdown
            
            # MongoDB shutdown should fail, Redis should not be called (sequential execution)
            mock_db.close_mongodb_connection.assert_called_once()
            mock_db.close_redis_connection.assert_not_called()
    
    @pytest.mark.asyncio
    async def test_lifespan_shutdown_redis_error(self):
        """Test shutdown with Redis error"""
        with patch('src.app.main.database') as mock_db:
            mock_db.connect_to_mongodb = AsyncMock()
            mock_db.connect_to_redis = Mock()
            mock_db.close_mongodb_connection = AsyncMock()
            mock_db.close_redis_connection = Mock(side_effect=Exception("Redis shutdown failed"))
            
            # Test the lifespan context manager with Redis shutdown error
            async with lifespan(app):
                pass  # This will trigger shutdown
            
            # MongoDB shutdown should succeed, Redis should fail
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
            
            # Test the complete lifespan
            async with lifespan(app):
                # Verify startup
                mock_db.connect_to_mongodb.assert_called_once()
                mock_db.connect_to_redis.assert_called_once()
            
            # Verify shutdown
            mock_db.close_mongodb_connection.assert_called_once()
            mock_db.close_redis_connection.assert_called_once()
