"""
Unit tests for main application module
"""
import pytest
from unittest.mock import AsyncMock, patch
from fastapi.testclient import TestClient

from src.app.main import app, lifespan


class TestMainApp:
    """Test cases for main FastAPI application."""
    
    def test_app_creation(self):
        """Test that FastAPI app is created correctly."""
        assert app is not None
        assert app.title == "Dashboard Educativo API"
        assert app.version == "1.0.0"
    
    def test_app_cors_configuration(self):
        """Test CORS configuration."""
        # Check that CORS middleware is added
        middleware_types = [middleware.cls.__name__ for middleware in app.user_middleware]
        assert "CORSMiddleware" in middleware_types
    
    def test_health_endpoint(self, test_client, mock_mongodb, mock_redis):
        """Test health check endpoint."""
        with patch('src.app.core.database.get_database') as mock_get_db, \
             patch('src.app.core.database.get_redis_client') as mock_get_redis:
            
            mock_get_db.return_value = mock_mongodb
            mock_get_redis.return_value = mock_redis
            
            response = test_client.get("/health")
            
            assert response.status_code == 200
            data = response.json()
            assert data["status"] == "healthy"
            assert "timestamp" in data
            assert "version" in data
    
    def test_root_endpoint(self, test_client):
        """Test root endpoint."""
        response = test_client.get("/")
        
        assert response.status_code == 200
        data = response.json()
        assert "message" in data
        assert "Dashboard Educativo" in data["message"]
    
    def test_docs_endpoint(self, test_client):
        """Test that API documentation is available."""
        response = test_client.get("/docs")
        
        assert response.status_code == 200
        assert "text/html" in response.headers["content-type"]
    
    def test_openapi_endpoint(self, test_client):
        """Test OpenAPI schema endpoint."""
        response = test_client.get("/openapi.json")
        
        assert response.status_code == 200
        data = response.json()
        assert data["info"]["title"] == "Dashboard Educativo API"
        assert data["info"]["version"] == "1.0.0"
    
    @pytest.mark.asyncio
    async def test_lifespan_startup_success(self, mock_mongodb, mock_redis):
        """Test lifespan startup success."""
        with patch('src.app.core.database.get_database') as mock_get_db, \
             patch('src.app.core.database.get_redis_client') as mock_get_redis:
            
            mock_get_db.return_value = mock_mongodb
            mock_get_redis.return_value = mock_redis
            
            # Test lifespan startup
            async with lifespan(app):
                pass
            
            mock_get_db.assert_called_once()
            mock_get_redis.assert_called_once()
    
    @pytest.mark.asyncio
    async def test_lifespan_startup_database_error(self):
        """Test lifespan startup with database error."""
        with patch('src.app.core.database.get_database') as mock_get_db:
            mock_get_db.side_effect = Exception("Database connection failed")
            
            # Should handle startup errors gracefully
            async with lifespan(app):
                pass
            
            mock_get_db.assert_called_once()
    
    @pytest.mark.asyncio
    async def test_lifespan_startup_redis_error(self, mock_mongodb):
        """Test lifespan startup with Redis error."""
        with patch('src.app.core.database.get_database') as mock_get_db, \
             patch('src.app.core.database.get_redis_client') as mock_get_redis:
            
            mock_get_db.return_value = mock_mongodb
            mock_get_redis.side_effect = Exception("Redis connection failed")
            
            # Should handle startup errors gracefully
            async with lifespan(app):
                pass
            
            mock_get_db.assert_called_once()
            mock_get_redis.assert_called_once()
    
    @pytest.mark.asyncio
    async def test_lifespan_shutdown_success(self, mock_mongodb, mock_redis):
        """Test lifespan shutdown success."""
        with patch('src.app.core.database.get_database') as mock_get_db, \
             patch('src.app.core.database.get_redis_client') as mock_get_redis, \
             patch('src.app.core.database.cleanup_database') as mock_cleanup_db, \
             patch('src.app.core.database.cleanup_redis') as mock_cleanup_redis:
            
            mock_get_db.return_value = mock_mongodb
            mock_get_redis.return_value = mock_redis
            
            # Test lifespan shutdown
            async with lifespan(app):
                pass
            
            mock_cleanup_db.assert_called_once()
            mock_cleanup_redis.assert_called_once()
    
    @pytest.mark.asyncio
    async def test_lifespan_shutdown_database_error(self, mock_mongodb, mock_redis):
        """Test lifespan shutdown with database cleanup error."""
        with patch('src.app.core.database.get_database') as mock_get_db, \
             patch('src.app.core.database.get_redis_client') as mock_get_redis, \
             patch('src.app.core.database.cleanup_database') as mock_cleanup_db, \
             patch('src.app.core.database.cleanup_redis') as mock_cleanup_redis:
            
            mock_get_db.return_value = mock_mongodb
            mock_get_redis.return_value = mock_redis
            mock_cleanup_db.side_effect = Exception("Database cleanup failed")
            
            # Should handle shutdown errors gracefully
            async with lifespan(app):
                pass
            
            mock_cleanup_db.assert_called_once()
            mock_cleanup_redis.assert_called_once()
    
    @pytest.mark.asyncio
    async def test_lifespan_shutdown_redis_error(self, mock_mongodb, mock_redis):
        """Test lifespan shutdown with Redis cleanup error."""
        with patch('src.app.core.database.get_database') as mock_get_db, \
             patch('src.app.core.database.get_redis_client') as mock_get_redis, \
             patch('src.app.core.database.cleanup_database') as mock_cleanup_db, \
             patch('src.app.core.database.cleanup_redis') as mock_cleanup_redis:
            
            mock_get_db.return_value = mock_mongodb
            mock_get_redis.return_value = mock_redis
            mock_cleanup_redis.side_effect = Exception("Redis cleanup failed")
            
            # Should handle shutdown errors gracefully
            async with lifespan(app):
                pass
            
            mock_cleanup_db.assert_called_once()
            mock_cleanup_redis.assert_called_once()
    
    def test_cors_headers(self, test_client):
        """Test CORS headers are present."""
        response = test_client.options("/health")
        
        assert response.status_code == 200
        # Check for CORS headers (they might be lowercase)
        headers_lower = {k.lower(): v for k, v in response.headers.items()}
        assert "access-control-allow-origin" in headers_lower
        assert "access-control-allow-credentials" in headers_lower
    
    def test_error_handling(self, test_client):
        """Test error handling for non-existent endpoints."""
        response = test_client.get("/non-existent-endpoint")
        
        assert response.status_code == 404
        data = response.json()
        assert "detail" in data
    
    def test_app_middleware_order(self):
        """Test that middleware is added in correct order."""
        middleware_types = [middleware.cls.__name__ for middleware in app.user_middleware]
        
        # CORS should be first
        assert middleware_types[0] == "CORSMiddleware"
    
    def test_app_routes_registration(self):
        """Test that routes are properly registered."""
        route_paths = [route.path for route in app.routes]
        
        assert "/" in route_paths
        assert "/health" in route_paths
        assert "/docs" in route_paths
        assert "/openapi.json" in route_paths
    
    def test_app_configuration(self):
        """Test app configuration."""
        assert app.debug is False
        assert app.docs_url == "/docs"
        assert app.redoc_url == "/redoc"
        assert app.openapi_url == "/openapi.json"
    
    @pytest.mark.asyncio
    async def test_lifespan_context_manager_timeout(self):
        """Test lifespan context manager timeout handling."""
        with patch('src.app.core.database.get_database') as mock_get_db, \
             patch('src.app.core.database.get_redis_client') as mock_get_redis:
            
            # Simulate slow startup
            async def slow_startup():
                import asyncio
                await asyncio.sleep(0.1)  # Simulate delay
                return AsyncMock()
            
            mock_get_db.side_effect = slow_startup
            mock_get_redis.side_effect = slow_startup
            
            # Should handle timeout gracefully
            async with lifespan(app):
                pass
            
            mock_get_db.assert_called_once()
            mock_get_redis.assert_called_once()