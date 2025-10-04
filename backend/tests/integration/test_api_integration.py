import pytest
from fastapi.testclient import TestClient
from src.app.main import app

class TestAPIIntegration:
    def test_health_endpoint_integration(self):
        """Test health endpoint integration with real database and Redis."""
        client = TestClient(app)
        response = client.get("/api/v1/health")
        
        assert response.status_code == 200
        data = response.json()
        
        # Should have all required fields
        assert "status" in data
        assert "timestamp" in data
        assert "services" in data
        assert "version" in data
        assert "environment" in data
        
        # Services should have database and redis
        assert "database" in data["services"]
        assert "redis" in data["services"]
        
        # Version should be correct
        assert data["version"] == "1.0.0"
        assert data["environment"] == "development"
    
    def test_root_endpoint_integration(self):
        """Test root endpoint integration."""
        client = TestClient(app)
        response = client.get("/")
        
        assert response.status_code == 200
        data = response.json()
        
        assert data["message"] == "ClassSphere API"
        assert data["version"] == "1.0.0"
        assert data["status"] == "running"
        assert data["port"] == 8000
    
    def test_api_structure(self):
        """Test that API has correct structure."""
        client = TestClient(app)
        response = client.get("/openapi.json")
        assert response.status_code == 200
        
        openapi_data = response.json()
        
        # Check API info
        assert openapi_data["info"]["title"] == "ClassSphere API"
        assert openapi_data["info"]["version"] == "1.0.0"
        
        # Check paths
        assert "/" in openapi_data["paths"]
        assert "/api/v1/health" in openapi_data["paths"]
        # Note: /docs, /redoc, /openapi.json are not included in OpenAPI paths by default
