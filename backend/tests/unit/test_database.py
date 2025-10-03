"""
Tests for database module
"""
import pytest
from unittest.mock import Mock, patch, AsyncMock
from src.app.core.database import Database, database


class TestDatabase:
    """Test Database class"""
    
    def test_database_initialization(self):
        """Test database initialization"""
        db = Database()
        assert db.mongodb_client is None
        assert db.redis_client is None
    
    @patch('src.app.core.database.AsyncIOMotorClient')
    async def test_connect_to_mongodb_success(self, mock_client):
        """Test successful MongoDB connection"""
        mock_instance = AsyncMock()
        mock_instance.admin.command.return_value = {"ok": 1}
        mock_client.return_value = mock_instance
        
        db = Database()
        await db.connect_to_mongodb()
        
        assert db.mongodb_client is not None
        mock_client.assert_called_once()
        mock_instance.admin.command.assert_called_once_with('ping')
    
    @patch('src.app.core.database.Redis')
    def test_connect_to_redis_success(self, mock_redis):
        """Test successful Redis connection"""
        mock_instance = Mock()
        mock_instance.ping.return_value = True
        mock_redis.from_url.return_value = mock_instance
        
        db = Database()
        db.connect_to_redis()
        
        assert db.redis_client is not None
        mock_redis.from_url.assert_called_once()
        mock_instance.ping.assert_called_once()
    
    async def test_close_mongodb_connection(self):
        """Test MongoDB connection closure"""
        db = Database()
        mock_client = Mock()
        db.mongodb_client = mock_client
        
        await db.close_mongodb_connection()
        
        mock_client.close.assert_called_once()
    
    def test_close_redis_connection(self):
        """Test Redis connection closure"""
        db = Database()
        mock_client = Mock()
        db.redis_client = mock_client
        
        db.close_redis_connection()
        
        mock_client.close.assert_called_once()
    
    def test_get_mongodb_database_success(self):
        """Test getting MongoDB database instance"""
        db = Database()
        mock_client = Mock()
        mock_db = Mock()
        mock_client.dashboard_educativo = mock_db
        db.mongodb_client = mock_client
        
        result = db.get_mongodb_database()
        
        assert result == mock_db
    
    def test_get_mongodb_database_no_connection(self):
        """Test getting MongoDB database without connection"""
        db = Database()
        
        with pytest.raises(Exception, match="MongoDB not connected"):
            db.get_mongodb_database()
    
    def test_get_redis_client_success(self):
        """Test getting Redis client instance"""
        db = Database()
        mock_client = Mock()
        db.redis_client = mock_client
        
        result = db.get_redis_client()
        
        assert result == mock_client
    
    def test_get_redis_client_no_connection(self):
        """Test getting Redis client without connection"""
        db = Database()
        
        with pytest.raises(Exception, match="Redis not connected"):
            db.get_redis_client()


class TestGlobalDatabase:
    """Test global database instance"""
    
    def test_global_database_instance(self):
        """Test that global database instance exists"""
        assert database is not None
        assert isinstance(database, Database)
