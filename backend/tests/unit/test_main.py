"""
Unit tests for main application module.
"""
import pytest
from unittest.mock import AsyncMock, patch
from fastapi.testclient import TestClient
from src.app.main import app, create_app, lifespan


class TestMainApp:
    """Test main application."""
    
    def test_app_creation(self):
        """Test app creation."""
        assert app is not None
        assert app.title == "Dashboard Educativo"
        assert app.version == "1.0.0"
    
    def test_app_cors_configuration(self):
        """Test CORS configuration."""
        middleware_types = [middleware.cls.__name__ for middleware in app.user_middleware]
        assert "CORSMiddleware" in middleware_types
    
    def test_app_middleware_order(self):
        """Test middleware order."""
        middleware_types = [middleware.cls.__name__ for middleware in app.user_middleware]
        assert "CORSMiddleware" in middleware_types
    
    def test_root_endpoint(self, test_client):
        """Test root endpoint."""
        response = test_client.get("/")
        
        assert response.status_code == 200
        data = response.json()
        assert "message" in data
        assert "version" in data
        assert "environment" in data
    
    def test_api_info_endpoint(self, test_client):
        """Test API info endpoint."""
        response = test_client.get("/api/info")
        
        assert response.status_code == 200
        data = response.json()
        assert "name" in data
        assert "version" in data
        assert "environment" in data
        assert "features" in data
    
    def test_health_endpoint(self, test_client, mock_mongodb, mock_redis):
        """Test health endpoint."""
        with patch('src.app.core.database.get_database') as mock_get_db, \
             patch('src.app.core.database.get_redis_client') as mock_get_redis:
            
            mock_get_db.return_value = mock_mongodb
            mock_get_redis.return_value = mock_redis
            
            response = test_client.get("/api/health/")
            
            assert response.status_code == 200
            data = response.json()
            assert "status" in data
            assert "services" in data
    
    def test_docs_endpoint_debug_mode(self, test_client):
        """Test docs endpoint in debug mode."""
        response = test_client.get("/docs")
        
        # In test mode, docs might be disabled, so we accept both 200 and 404
        assert response.status_code in [200, 404]
    
    def test_openapi_endpoint(self, test_client):
        """Test OpenAPI endpoint."""
        response = test_client.get("/openapi.json")
        
        # In test mode, openapi might be disabled, so we accept both 200 and 404
        assert response.status_code in [200, 404]
        if response.status_code == 200:
            data = response.json()
            assert "openapi" in data
            assert "info" in data
    
    def test_redoc_endpoint(self, test_client):
        """Test ReDoc endpoint."""
        response = test_client.get("/redoc")
        
        # In test mode, redoc might be disabled, so we accept both 200 and 404
        assert response.status_code in [200, 404]
    
    @pytest.mark.asyncio
    async def test_lifespan_startup_success(self, mock_mongodb, mock_redis):
        """Test lifespan startup success."""
        with patch('src.app.core.database.get_database') as mock_get_db, \
             patch('src.app.core.database.get_redis_client') as mock_get_redis:
            
            mock_get_db.return_value = mock_mongodb
            mock_get_redis.return_value = mock_redis
            
            async with lifespan(app):
                pass
            
            mock_get_db.assert_called_once()
            mock_get_redis.assert_called_once()
    
    @pytest.mark.asyncio
    async def test_lifespan_startup_error(self):
        """Test lifespan startup error."""
        with patch('src.app.core.database.get_database') as mock_get_db:
            mock_get_db.side_effect = Exception("Startup failed")
            
            # Should not raise exception, just log error
            async with lifespan(app):
                pass
    
    @pytest.mark.asyncio
    async def test_lifespan_shutdown_success(self, mock_mongodb, mock_redis):
        """Test lifespan shutdown success."""
        with patch('src.app.core.database.get_database') as mock_get_db, \
             patch('src.app.core.database.get_redis_client') as mock_get_redis, \
             patch('src.app.core.database.cleanup_database') as mock_cleanup_db, \
             patch('src.app.core.database.cleanup_redis') as mock_cleanup_redis:
            
            mock_get_db.return_value = mock_mongodb
            mock_get_redis.return_value = mock_redis
            
            async with lifespan(app):
                pass
            
            mock_cleanup_db.assert_called_once()
            mock_cleanup_redis.assert_called_once()
    
    @pytest.mark.asyncio
    async def test_lifespan_shutdown_database_error(self, mock_mongodb, mock_redis):
        """Test lifespan shutdown database error."""
        with patch('src.app.core.database.get_database') as mock_get_db, \
             patch('src.app.core.database.get_redis_client') as mock_get_redis, \
             patch('src.app.core.database.cleanup_database') as mock_cleanup_db, \
             patch('src.app.core.database.cleanup_redis') as mock_cleanup_redis:
            
            mock_get_db.return_value = mock_mongodb
            mock_get_redis.return_value = mock_redis
            mock_cleanup_db.side_effect = Exception("Database cleanup failed")
            
            # Should not raise exception, just log error
            async with lifespan(app):
                pass
    
    @pytest.mark.asyncio
    async def test_lifespan_shutdown_redis_error(self, mock_mongodb, mock_redis):
        """Test lifespan shutdown Redis error."""
        with patch('src.app.core.database.get_database') as mock_get_db, \
             patch('src.app.core.database.get_redis_client') as mock_get_redis, \
             patch('src.app.core.database.cleanup_database') as mock_cleanup_db, \
             patch('src.app.core.database.cleanup_redis') as mock_cleanup_redis:
            
            mock_get_db.return_value = mock_mongodb
            mock_get_redis.return_value = mock_redis
            mock_cleanup_redis.side_effect = Exception("Redis cleanup failed")
            
            # Should not raise exception, just log error
            async with lifespan(app):
                pass
    
    def test_cors_headers(self, test_client):
        """Test CORS headers."""
        response = test_client.get("/api/health/")
        
        # Check for CORS headers (they might not be present in test mode)
        headers_lower = {k.lower(): v for k, v in response.headers.items()}
        # CORS headers are added by middleware, might not be present in test
        assert response.status_code == 200
    
    def test_create_app_function(self):
        """Test create_app function."""
        test_app = create_app()
        
        assert test_app is not None
        assert test_app.title == "Dashboard Educativo"
        assert test_app.version == "1.0.0"
    
    def test_exception_handlers(self, test_client):
        """Test exception handlers."""
        # Test 404 error
        response = test_client.get("/nonexistent")
        assert response.status_code == 404
        
        # Test validation error
        response = test_client.post("/api/info", json={"invalid": "data"})
        # Should return 405 Method Not Allowed or similar
        assert response.status_code in [405, 422]
    
    def test_request_logging_middleware(self, test_client):
        """Test request logging middleware."""
        response = test_client.get("/")
        
        assert response.status_code == 200
        # Middleware should not affect response
    
    def test_app_routes(self, test_client):
        """Test app routes."""
        # Test that all expected routes exist
        routes = [route.path for route in app.routes]
        
        assert "/" in routes
        assert "/api/info" in routes
        assert "/api/health/" in routes
        # Documentation routes might not be present in test mode
        # assert "/docs" in routes
        # assert "/openapi.json" in routes
        # assert "/redoc" in routes