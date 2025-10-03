import pytest
from fastapi.testclient import TestClient
from src.app.main import app, create_app

class TestMainApp:
    def test_app_creation(self):
        test_app = create_app()
        assert test_app is not None
        assert test_app.title == "Dashboard Educativo"
    
    def test_health_endpoint(self):
        client = TestClient(app)
        response = client.get("/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"
        assert data["app_name"] == "Dashboard Educativo"
        assert data["version"] == "0.1.0"
        assert data["environment"] == "development"
    
    def test_cors_middleware(self):
        client = TestClient(app)
        response = client.get("/health", headers={"Origin": "http://localhost:3000"})
        assert response.status_code == 200
        assert "access-control-allow-origin" in response.headers
        assert "access-control-allow-credentials" in response.headers
    
    def test_app_info(self):
        client = TestClient(app)
        response = client.get("/health")
        assert response.status_code == 200
        data = response.json()
        assert "status" in data
        assert "app_name" in data
        assert "version" in data
        assert "environment" in data