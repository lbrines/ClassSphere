"""Tests for database module."""

import pytest
from unittest.mock import AsyncMock, patch
from src.app.core.database import (
    get_redis_client,
    get_database,
    check_database_health,
    cleanup_database,
    cleanup_redis
)


class TestDatabase:
    """Test database functionality."""

    @pytest.mark.asyncio
    @patch('src.app.core.database.redis.from_url')
    async def test_get_redis_client_success(self, mock_redis_from_url):
        """Test successful Redis client creation."""
        mock_client = AsyncMock()
        mock_client.ping = AsyncMock(return_value=True)
        mock_redis_from_url.return_value = mock_client

        # Clear global client
        import src.app.core.database as db_module
        db_module._redis_client = None

        client = await get_redis_client()

        assert client == mock_client
        mock_client.ping.assert_called_once()

    @pytest.mark.asyncio
    @patch('src.app.core.database.redis.from_url')
    async def test_get_redis_client_connection_error(self, mock_redis_from_url):
        """Test Redis client connection error."""
        mock_client = AsyncMock()
        mock_client.ping = AsyncMock(side_effect=Exception("Connection failed"))
        mock_redis_from_url.return_value = mock_client

        # Clear global client
        import src.app.core.database as db_module
        db_module._redis_client = None

        with pytest.raises(Exception, match="Connection failed"):
            await get_redis_client()

    @pytest.mark.asyncio
    @patch('src.app.core.database.get_redis_client')
    async def test_get_database_success(self, mock_get_redis):
        """Test successful database retrieval."""
        mock_redis_client = AsyncMock()
        mock_get_redis.return_value = mock_redis_client

        db = await get_database()

        assert db["redis"] == mock_redis_client
        mock_get_redis.assert_called_once()

    @pytest.mark.asyncio
    @patch('src.app.core.database.get_redis_client')
    async def test_get_database_error(self, mock_get_redis):
        """Test database retrieval with error."""
        mock_get_redis.side_effect = Exception("Database error")

        db = await get_database()

        assert db["redis"] is None

    @pytest.mark.asyncio
    @patch('src.app.core.database.get_redis_client')
    async def test_check_database_health_success(self, mock_get_redis):
        """Test database health check success."""
        mock_redis_client = AsyncMock()
        mock_redis_client.ping = AsyncMock(return_value=True)
        mock_get_redis.return_value = mock_redis_client

        health = await check_database_health()

        assert health["redis"] is True
        mock_redis_client.ping.assert_called_once()

    @pytest.mark.asyncio
    @patch('src.app.core.database.get_redis_client')
    async def test_check_database_health_failure(self, mock_get_redis):
        """Test database health check failure."""
        mock_get_redis.side_effect = Exception("Health check failed")

        health = await check_database_health()

        assert health["redis"] is False

    @pytest.mark.asyncio
    async def test_cleanup_database_success(self):
        """Test successful database cleanup."""
        # Set up mock client
        import src.app.core.database as db_module
        mock_client = AsyncMock()
        mock_client.aclose = AsyncMock()
        db_module._redis_client = mock_client

        await cleanup_database()

        mock_client.aclose.assert_called_once()
        assert db_module._redis_client is None

    @pytest.mark.asyncio
    async def test_cleanup_database_error(self):
        """Test database cleanup with error."""
        # Set up mock client that fails
        import src.app.core.database as db_module
        mock_client = AsyncMock()
        mock_client.aclose = AsyncMock(side_effect=Exception("Cleanup failed"))
        db_module._redis_client = mock_client

        await cleanup_database()

        mock_client.aclose.assert_called_once()
        assert db_module._redis_client is None

    @pytest.mark.asyncio
    async def test_cleanup_database_no_client(self):
        """Test database cleanup with no client."""
        # Clear global client
        import src.app.core.database as db_module
        db_module._redis_client = None

        # Should not raise exception
        await cleanup_database()

    @pytest.mark.asyncio
    @patch('src.app.core.database.cleanup_database')
    async def test_cleanup_redis(self, mock_cleanup_database):
        """Test Redis cleanup."""
        await cleanup_redis()

        mock_cleanup_database.assert_called_once()