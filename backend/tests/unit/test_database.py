import pytest
from unittest.mock import Mock, patch, AsyncMock
from src.app.core.database import Database, database

class TestDatabase:
    @pytest.mark.asyncio
    @patch('src.app.core.database.AsyncIOMotorClient')
    async def test_connect_to_mongodb_success(self, mock_client):
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
        mock_instance = Mock()
        mock_redis.from_url.return_value = mock_instance
        
        db = Database()
        db.connect_to_redis()
        
        assert db.redis_client is not None
        mock_redis.from_url.assert_called_once()
    
    @pytest.mark.asyncio
    async def test_close_mongodb_connection(self):
        db = Database()
        db.mongodb_client = AsyncMock()
        
        await db.close_mongodb_connection()
        
        assert db.mongodb_client is None
    
    def test_close_redis_connection(self):
        db = Database()
        db.redis_client = Mock()
        
        db.close_redis_connection()
        
        assert db.redis_client is None
    
    def test_get_mongodb_client(self):
        db = Database()
        db.mongodb_client = Mock()
        
        client = db.get_mongodb_client()
        assert client is not None
    
    def test_get_redis_client(self):
        db = Database()
        db.redis_client = Mock()
        
        client = db.get_redis_client()
        assert client is not None
    
    def test_database_singleton(self):
        assert database is not None
        assert isinstance(database, Database)