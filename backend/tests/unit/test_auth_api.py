"""
Test file for auth API endpoints

CRITICAL OBJECTIVES:
- Verify authentication API endpoints
- Test OAuth integration
- Test JWT token handling
- Test user management

DEPENDENCIES:
- FastAPI TestClient
- pytest-asyncio
- unittest.mock
"""

import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, AsyncMock
import json

from src.app.main import app
from src.app.services.auth_service import AuthService

# BEGINNING: Critical tests for core functionality
def test_login_success():
    """Test successful login"""
    # Arrange
    client = TestClient(app)
    login_data = {
        "email": "test@classsphere.com",
        "password": "test123"
    }
    
    # Act
    response = client.post("/auth/login", json=login_data)
    
    # Assert
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert "refresh_token" in data
    assert "token_type" in data
    assert "expires_in" in data
    assert "user" in data
    assert data["token_type"] == "bearer"
    assert data["user"]["email"] == "test@classsphere.com"

def test_login_invalid_credentials():
    """Test login with invalid credentials"""
    # Arrange
    client = TestClient(app)
    login_data = {
        "email": "invalid@example.com",
        "password": "wrongpassword"
    }
    
    # Act
    response = client.post("/auth/login", json=login_data)
    
    # Assert
    assert response.status_code == 401
    assert "Invalid credentials" in response.json()["detail"]

def test_google_oauth_initiation():
    """Test Google OAuth initiation"""
    # Arrange
    client = TestClient(app)
    
    # Act
    response = client.get("/auth/google")
    
    # Assert
    assert response.status_code == 200
    data = response.json()
    assert "authorization_url" in data
    assert "state" in data
    assert "https://accounts.google.com/o/oauth2/v2/auth" in data["authorization_url"]

def test_google_oauth_callback_success():
    """Test successful Google OAuth callback"""
    # Arrange
    client = TestClient(app)
    code = "test_authorization_code"
    state = "test_state"
    
    with patch('src.app.services.oauth_service.OAuthService.handle_oauth_callback') as mock_callback:
        mock_callback.return_value = {
            "user": {
                "sub": "google_test_user",
                "email": "test@example.com",
                "name": "Test User",
                "role": "student"
            },
            "tokens": {
                "access_token": "mock_access_token",
                "refresh_token": "mock_refresh_token",
                "token_type": "bearer",
                "expires_in": 1800
            }
        }
        
        # Act
        response = client.get(f"/auth/google/callback?code={code}&state={state}")
        
        # Assert
        assert response.status_code == 200
        data = response.json()
        assert "message" in data
        assert "user" in data
        assert "tokens" in data
        assert data["user"]["email"] == "test@example.com"

def test_google_oauth_callback_failure():
    """Test Google OAuth callback failure"""
    # Arrange
    client = TestClient(app)
    code = "invalid_code"
    state = "invalid_state"
    
    with patch('src.app.services.oauth_service.OAuthService.handle_oauth_callback') as mock_callback:
        mock_callback.return_value = None
        
        # Act
        response = client.get(f"/auth/google/callback?code={code}&state={state}")
        
        # Assert
        assert response.status_code == 400
        assert "OAuth callback failed" in response.json()["detail"]

# MIDDLE: Detailed implementation tests
def test_get_current_user_info():
    """Test get current user info with valid token"""
    # Arrange
    client = TestClient(app)
    auth_service = AuthService()
    
    # Create test token
    user_data = {
        "sub": "test_user_123",
        "email": "test@classsphere.com",
        "name": "Test User",
        "role": "teacher"
    }
    token = auth_service.create_access_token(user_data)
    
    # Act
    response = client.get(
        "/auth/me",
        headers={"Authorization": f"Bearer {token}"}
    )
    
    # Assert
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == "test_user_123"
    assert data["email"] == "test@classsphere.com"
    assert data["name"] is None  # Name is not included in token by default
    assert data["role"] == "teacher"

def test_get_current_user_info_no_token():
    """Test get current user info without token"""
    # Arrange
    client = TestClient(app)
    
    # Act
    response = client.get("/auth/me")
    
    # Assert
    assert response.status_code == 401

def test_token_refresh_success():
    """Test successful token refresh"""
    # Arrange
    client = TestClient(app)
    auth_service = AuthService()
    
    # Create test refresh token
    user_data = {
        "sub": "test_user_123",
        "email": "test@classsphere.com",
        "name": "Test User",
        "role": "teacher"
    }
    refresh_token = auth_service.create_refresh_token(user_data)
    
    refresh_data = {"refresh_token": refresh_token}
    
    # Act
    response = client.post("/auth/refresh", json=refresh_data)
    
    # Assert
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert "refresh_token" in data
    assert "token_type" in data
    assert "expires_in" in data
    assert "user" in data

def test_token_refresh_invalid_token():
    """Test token refresh with invalid refresh token"""
    # Arrange
    client = TestClient(app)
    refresh_data = {"refresh_token": "invalid_refresh_token"}
    
    # Act
    response = client.post("/auth/refresh", json=refresh_data)
    
    # Assert
    assert response.status_code == 401
    assert "Invalid refresh token" in response.json()["detail"]

def test_logout_success():
    """Test successful logout"""
    # Arrange
    client = TestClient(app)
    auth_service = AuthService()
    
    # Create test token
    user_data = {
        "sub": "test_user_123",
        "email": "test@classsphere.com",
        "name": "Test User",
        "role": "teacher"
    }
    token = auth_service.create_access_token(user_data)
    
    # Act
    response = client.post(
        "/auth/logout",
        headers={"Authorization": f"Bearer {token}"}
    )
    
    # Assert
    assert response.status_code == 200
    assert "Logged out successfully" in response.json()["message"]

def test_verify_token_valid():
    """Test token verification with valid token"""
    # Arrange
    client = TestClient(app)
    auth_service = AuthService()
    
    # Create test token
    user_data = {
        "sub": "test_user_123",
        "email": "test@classsphere.com",
        "name": "Test User",
        "role": "teacher"
    }
    token = auth_service.create_access_token(user_data)
    
    # Act
    response = client.get(
        "/auth/verify",
        headers={"Authorization": f"Bearer {token}"}
    )
    
    # Assert
    assert response.status_code == 200
    data = response.json()
    assert data["valid"] is True
    assert data["user"]["id"] == "test_user_123"

def test_verify_token_invalid():
    """Test token verification with invalid token"""
    # Arrange
    client = TestClient(app)
    
    # Act
    response = client.get(
        "/auth/verify",
        headers={"Authorization": "Bearer invalid_token"}
    )
    
    # Assert
    assert response.status_code == 200
    data = response.json()
    assert data["valid"] is False
    assert data["user"] is None

def test_verify_token_no_token():
    """Test token verification without token"""
    # Arrange
    client = TestClient(app)
    
    # Act
    response = client.get("/auth/verify")
    
    # Assert
    assert response.status_code == 200
    data = response.json()
    assert data["valid"] is False
    assert data["user"] is None

# END: Verification and next steps
def test_login_missing_fields():
    """Test login with missing required fields"""
    # Arrange
    client = TestClient(app)
    login_data = {"email": "test@classsphere.com"}  # Missing password
    
    # Act
    response = client.post("/auth/login", json=login_data)
    
    # Assert
    assert response.status_code == 422  # Validation error

def test_refresh_missing_token():
    """Test refresh with missing refresh token"""
    # Arrange
    client = TestClient(app)
    refresh_data = {}  # Missing refresh_token
    
    # Act
    response = client.post("/auth/refresh", json=refresh_data)
    
    # Assert
    assert response.status_code == 422  # Validation error