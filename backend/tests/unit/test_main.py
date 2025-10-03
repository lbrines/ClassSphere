"""
Tests for main FastAPI application
"""
import pytest
from fastapi.testclient import TestClient
from src.app.main import app, create_app


class TestMainApp:
    """Test main FastAPI application"""
    
    def test_app_creation(self):
        """Test that app can be created"""
        assert app is not None
    
    def test_create_app_function(self):
        """Test create_app function"""
        test_app = create_app()
        assert test_app is not None
        assert test_app.title == "Dashboard Educativo"
        assert test_app.version == "0.1.0"
    
    def test_health_endpoint(self):
        """Test health check endpoint"""
        client = TestClient(app)
        response = client.get("/health")
        
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"
        assert data["app_name"] == "Dashboard Educativo"
        assert data["version"] == "0.1.0"
        assert data["environment"] == "development"
    
    def test_health_endpoint_response_format(self):
        """Test health endpoint response format"""
        client = TestClient(app)
        response = client.get("/health")
        
        assert response.status_code == 200
        data = response.json()
        
        # Check all required fields are present
        required_fields = ["status", "app_name", "version", "environment"]
        for field in required_fields:
            assert field in data
        
        # Check field types
        assert isinstance(data["status"], str)
        assert isinstance(data["app_name"], str)
        assert isinstance(data["version"], str)
        assert isinstance(data["environment"], str)
    
    def test_cors_middleware(self):
        """Test CORS middleware is configured"""
        client = TestClient(app)
        response = client.get("/health", headers={"Origin": "http://localhost:3000"})
        
        # CORS headers should be present
        assert "access-control-allow-origin" in response.headers
        assert "access-control-allow-credentials" in response.headers
