"""
Dashboard Educativo - API Integration Tests
Context-Aware Implementation - Day 9 Medium Priority
"""

import pytest
import httpx
from fastapi.testclient import TestClient
from unittest.mock import patch, AsyncMock
import json

from src.app.main import app
from src.core.context_logger import context_logger
import asyncio


class TestAPIIntegration:
    """API Integration Tests with Context Tracking"""
    
    @pytest.fixture
    def client(self):
        """Test client fixture"""
        return TestClient(app)
    
    @pytest.fixture
    def context_id(self):
        """Context ID for testing"""
        return "test-api-integration-001"
    
    def test_health_endpoint_integration(self, client, context_id):
        """Test health endpoint with context tracking"""
        
        # Log test start
        asyncio.run(context_logger.log_context_status(
            context_id=context_id,
            priority="MEDIUM",
            status="started",
            message="Health endpoint integration test started",
            phase="testing",
            task="health_integration_test"
        ))
        
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
        
        # Log test completion
        asyncio.run(context_logger.log_context_status(
            context_id=context_id,
            priority="MEDIUM",
            status="completed",
            message="Health endpoint integration test completed successfully",
            phase="testing",
            task="health_integration_test"
        ))
    
    def test_auth_login_integration(self, client, context_id):
        """Test authentication login integration"""
        
        # Log test start
        asyncio.run(context_logger.log_context_status(
            context_id=context_id,
            priority="MEDIUM",
            status="started",
            message="Auth login integration test started",
            phase="testing",
            task="auth_login_integration_test"
        ))
        
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
        
        # Log test completion
        asyncio.run(context_logger.log_context_status(
            context_id=context_id,
            priority="MEDIUM",
            status="completed",
            message="Auth login integration test completed successfully",
            phase="testing",
            task="auth_login_integration_test"
        ))
    
    def test_auth_me_integration(self, client, context_id):
        """Test auth/me endpoint integration"""
        
        # Log test start
        asyncio.run(context_logger.log_context_status(
            context_id=context_id,
            priority="MEDIUM",
            status="started",
            message="Auth me integration test started",
            phase="testing",
            task="auth_me_integration_test"
        ))
        
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
        
        # Log test completion
        asyncio.run(context_logger.log_context_status(
            context_id=context_id,
            priority="MEDIUM",
            status="completed",
            message="Auth me integration test completed successfully",
            phase="testing",
            task="auth_me_integration_test"
        ))
    
    def test_google_oauth_integration(self, client, context_id):
        """Test Google OAuth integration"""
        
        # Log test start
        asyncio.run(context_logger.log_context_status(
            context_id=context_id,
            priority="MEDIUM",
            status="started",
            message="Google OAuth integration test started",
            phase="testing",
            task="google_oauth_integration_test"
        ))
        
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
        
        # Log test completion
        asyncio.run(context_logger.log_context_status(
            context_id=context_id,
            priority="MEDIUM",
            status="completed",
            message="Google OAuth integration test completed successfully",
            phase="testing",
            task="google_oauth_integration_test"
        ))
    
    def test_google_api_integration(self, client, context_id):
        """Test Google API integration"""
        
        # Log test start
        asyncio.run(context_logger.log_context_status(
            context_id=context_id,
            priority="MEDIUM",
            status="started",
            message="Google API integration test started",
            phase="testing",
            task="google_api_integration_test"
        ))
        
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
        
        # Log test completion
        asyncio.run(context_logger.log_context_status(
            context_id=context_id,
            priority="MEDIUM",
            status="completed",
            message="Google API integration test completed successfully",
            phase="testing",
            task="google_api_integration_test"
        ))
    
    def test_context_logging_integration(self, context_id):
        """Test context logging integration"""
        
        # Log test start
        asyncio.run(context_logger.log_context_status(
            context_id=context_id,
            priority="MEDIUM",
            status="started",
            message="Context logging integration test started",
            phase="testing",
            task="context_logging_integration_test"
        ))
        
        # Get logs
        logs = context_logger.get_logs()
        
        # Verify logs exist
        assert len(logs) > 0
        
        # Find our test log
        test_logs = [log for log in logs if log["context_id"] == context_id]
        assert len(test_logs) > 0
        
        # Verify log structure
        test_log = test_logs[0]
        assert "timestamp" in test_log
        assert "context_id" in test_log
        assert "context_priority" in test_log
        assert "status" in test_log
        assert "memory_management" in test_log
        
        # Log test completion
        asyncio.run(context_logger.log_context_status(
            context_id=context_id,
            priority="MEDIUM",
            status="completed",
            message="Context logging integration test completed successfully",
            phase="testing",
            task="context_logging_integration_test"
        ))
    
    def test_error_handling_integration(self, client, context_id):
        """Test error handling integration"""
        
        # Log test start
        asyncio.run(context_logger.log_context_status(
            context_id=context_id,
            priority="MEDIUM",
            status="started",
            message="Error handling integration test started",
            phase="testing",
            task="error_handling_integration_test"
        ))
        
        # Test invalid token
        headers = {"Authorization": "Bearer invalid_token"}
        response = client.get("/api/v1/auth/me", headers=headers)
        
        assert response.status_code == 401
        data = response.json()
        
        # Verify error response structure
        assert "detail" in data
        assert "Token expired" in data["detail"]
        
        # Log test completion
        asyncio.run(context_logger.log_context_status(
            context_id=context_id,
            priority="MEDIUM",
            status="completed",
            message="Error handling integration test completed successfully",
            phase="testing",
            task="error_handling_integration_test"
        ))