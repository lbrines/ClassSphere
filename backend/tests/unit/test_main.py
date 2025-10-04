import pytest
from fastapi.testclient import TestClient
from src.app.main import app

class TestMainApp:
    def test_root_endpoint(self):
        """Test root endpoint returns correct response."""
        client = TestClient(app)
        response = client.get("/")
        
        assert response.status_code == 200
        data = response.json()
        assert data["message"] == "ClassSphere API"
        assert data["version"] == "1.0.0"
        assert data["status"] == "running"
        assert data["port"] == 8000
    
    def test_docs_endpoint(self):
        """Test that docs endpoint is accessible."""
        client = TestClient(app)
        response = client.get("/docs")
        assert response.status_code == 200
    
    def test_redoc_endpoint(self):
        """Test that redoc endpoint is accessible."""
        client = TestClient(app)
        response = client.get("/redoc")
        assert response.status_code == 200
    
    def test_openapi_endpoint(self):
        """Test that OpenAPI schema endpoint is accessible."""
        client = TestClient(app)
        response = client.get("/openapi.json")
        assert response.status_code == 200
        
        data = response.json()
        assert data["info"]["title"] == "ClassSphere API"
        assert data["info"]["version"] == "1.0.0"
        assert data["info"]["description"] == "Dashboard Educativo Full-Stack"
    
    def test_app_title_and_version(self):
        """Test that app has correct title and version."""
        assert app.title == "ClassSphere API"
        assert app.version == "1.0.0"
        assert app.description == "Dashboard Educativo Full-Stack"
