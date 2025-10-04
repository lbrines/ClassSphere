import pytest
from unittest.mock import Mock, patch
from fastapi.testclient import TestClient
from src.app.main import app

class TestHealthCheck:
    def test_health_check_success(self):
        """Test health check endpoint with successful database and Redis connections."""
        client = TestClient(app)
        
        with patch('src.app.api.health.get_db') as mock_get_db, \
             patch('redis.Redis.from_url') as mock_redis:
            
            # Mock database connection
            mock_db = Mock()
            mock_db.execute.return_value = None
            mock_get_db.return_value.__enter__.return_value = mock_db
            
            # Mock Redis connection
            mock_redis_instance = Mock()
            mock_redis_instance.ping.return_value = True
            mock_redis.return_value = mock_redis_instance
            
            response = client.get("/api/v1/health")
            
            assert response.status_code == 200
            data = response.json()
            assert data["status"] == "healthy"
            assert data["services"]["database"] == "healthy"
            assert data["services"]["redis"] == "healthy"
            assert data["version"] == "1.0.0"
            assert data["environment"] == "development"
    
    def test_health_check_database_error(self):
        """Test health check endpoint with database connection error."""
        client = TestClient(app)

        # Patch the database dependency at app level
        with patch('src.app.core.database.get_db') as mock_get_db, \
             patch('redis.Redis.from_url') as mock_redis:

            # Mock database error - patch the dependency function itself
            def db_error_generator():
                raise Exception("Database connection failed")

            mock_get_db.side_effect = db_error_generator

            # Mock Redis connection success
            mock_redis_instance = Mock()
            mock_redis_instance.ping.return_value = True
            mock_redis.return_value = mock_redis_instance

            response = client.get("/api/v1/health")

            assert response.status_code == 200
            data = response.json()
            assert data["status"] == "unhealthy"
            assert "unhealthy" in data["services"]["database"]
            assert data["services"]["redis"] == "healthy"
    
    def test_health_check_redis_error(self):
        """Test health check endpoint with Redis connection error."""
        client = TestClient(app)
        
        with patch('src.app.api.health.get_db') as mock_get_db, \
             patch('redis.Redis.from_url') as mock_redis:
            
            # Mock database connection success
            mock_db = Mock()
            mock_db.execute.return_value = None
            mock_get_db.return_value.__enter__.return_value = mock_db
            
            # Mock Redis error
            mock_redis.side_effect = Exception("Redis connection failed")
            
            response = client.get("/api/v1/health")
            
            assert response.status_code == 200
            data = response.json()
            assert data["status"] == "unhealthy"
            assert data["services"]["database"] == "healthy"
            assert "unhealthy" in data["services"]["redis"]
