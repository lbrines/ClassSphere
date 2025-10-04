"""
Dashboard Educativo - Simple Integration Tests
Context-Aware Implementation - Day 9 Medium Priority
"""

import pytest
from fastapi.testclient import TestClient
from src.app.main import app


class TestSimpleIntegration:
    """Simple API Integration Tests"""
    
    @pytest.fixture
    def client(self):
        """Test client fixture"""
        return TestClient(app)
    
    def test_health_endpoint(self, client):
        """Test health endpoint"""
        response = client.get("/api/v1/health")
        
        assert response.status_code == 200
        data = response.json()
        
        # Verify response structure
        assert "status" in data
        assert "timestamp" in data
        assert "app_name" in data
        assert "context_management" in data
        
        # Verify context management data
        context_data = data["context_management"]
        assert "context_log_path" in context_data
        assert "context_health" in context_data
    
    def test_auth_login(self, client):
        """Test authentication login"""
        login_data = {
            "username": "test_user",
            "password": "test_password"
        }
        
        response = client.post("/api/v1/auth/login", json=login_data)
        
        assert response.status_code == 200
        data = response.json()
        
        # Verify response structure
        assert "access_token" in data
        assert "refresh_token" in data
        assert "token_type" in data
        assert "expires_in" in data
        assert "user" in data
        
        # Verify token structure
        assert data["token_type"] == "bearer"
        assert data["expires_in"] == 1800
        
        # Verify user data
        user_data = data["user"]
        assert "user_id" in user_data
        assert "username" in user_data
        assert "email" in user_data
        assert "role" in user_data
    
    def test_auth_me(self, client):
        """Test auth/me endpoint"""
        # First login to get token
        login_data = {
            "username": "test_user",
            "password": "test_password"
        }
        
        login_response = client.post("/api/v1/auth/login", json=login_data)
        assert login_response.status_code == 200
        
        token_data = login_response.json()
        access_token = token_data["access_token"]
        
        # Test /auth/me endpoint
        headers = {"Authorization": f"Bearer {access_token}"}
        response = client.get("/api/v1/auth/me", headers=headers)
        
        assert response.status_code == 200
        data = response.json()
        
        # Verify response structure
        assert "user_id" in data
        assert "username" in data
        assert "email" in data
        assert "role" in data
    
    def test_google_oauth(self, client):
        """Test Google OAuth"""
        response = client.get("/api/v1/auth/google/authorize")
        
        assert response.status_code == 200
        data = response.json()
        
        # Verify response structure
        assert "authorization_url" in data
        assert "state" in data
        assert "scopes" in data
        
        # Verify authorization URL
        auth_url = data["authorization_url"]
        assert "https://accounts.google.com/o/oauth2/v2/auth" in auth_url
        assert "client_id" in auth_url
        assert "response_type=code" in auth_url
        
        # Verify scopes
        scopes = data["scopes"]
        assert len(scopes) > 0
        assert any("classroom" in scope for scope in scopes)
    
    def test_google_api(self, client):
        """Test Google API"""
        response = client.get("/api/v1/google/health")
        
        assert response.status_code == 200
        data = response.json()
        
        # Verify response structure
        assert "status" in data
        assert "service" in data
        assert "base_url" in data
        assert "scopes" in data
        assert "context_id" in data
        
        # Verify service data
        assert data["status"] == "healthy"
        assert data["service"] == "google_classroom"
        assert "classroom.googleapis.com" in data["base_url"]
    
    def test_error_handling(self, client):
        """Test error handling"""
        # Test invalid token
        headers = {"Authorization": "Bearer invalid_token"}
        response = client.get("/api/v1/auth/me", headers=headers)
        
        assert response.status_code == 401
        data = response.json()
        
        # Verify error response structure
        assert "detail" in data
        assert "Token expired" in data["detail"]
    
    def test_performance(self, client):
        """Test performance"""
        import time
        
        # Test response time
        start_time = time.time()
        response = client.get("/api/v1/health")
        end_time = time.time()
        
        response_time = end_time - start_time
        
        # Verify response time is under 2 seconds
        assert response_time < 2.0
        assert response.status_code == 200