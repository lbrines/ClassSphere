"""
Unit tests for authentication endpoints.
"""
import asyncio
import pytest
from unittest.mock import patch, AsyncMock
from fastapi.testclient import TestClient


def test_login_success(client):
    """Test successful login."""
    response = client.post(
        "/api/v1/auth/login",
        json={"email": "admin@classsphere.edu", "password": "secret"}
    )

    assert response.status_code == 200
    data = response.json()

    assert data["success"] is True
    assert "data" in data
    assert "token" in data["data"]
    assert "user" in data["data"]
    assert data["data"]["user"]["email"] == "admin@classsphere.edu"
    assert data["data"]["user"]["role"] == "admin"


def test_login_invalid_credentials(client):
    """Test login with invalid credentials."""
    response = client.post(
        "/api/v1/auth/login",
        json={"email": "admin@classsphere.edu", "password": "wrong"}
    )

    assert response.status_code == 401
    data = response.json()
    assert "Invalid" in data["detail"]


def test_login_nonexistent_user(client):
    """Test login with nonexistent user."""
    response = client.post(
        "/api/v1/auth/login",
        json={"email": "nonexistent@example.com", "password": "password"}
    )

    assert response.status_code == 401


def test_login_timeout():
    """Test login timeout handling."""
    from src.app.main import create_app

    app = create_app()

    with patch('src.app.services.auth_service.AuthService.authenticate_user') as mock_auth:
        # Mock timeout
        import asyncio

        async def timeout_auth(*args):
            await asyncio.sleep(6.0)  # Longer than timeout
            return None

        mock_auth.side_effect = timeout_auth

        client = TestClient(app)
        response = client.post(
            "/api/v1/auth/login",
            json={"email": "test@example.com", "password": "password"}
        )

        assert response.status_code == 408
        assert "timeout" in response.json()["detail"]


def test_get_current_user_info_success():
    """Test getting current user info with valid token."""
    from src.app.main import create_app

    app = create_app()

    # Mock valid token verification (must be async)
    with patch('src.app.api.endpoints.auth.verify_token', new_callable=AsyncMock) as mock_verify:
        with patch('src.app.services.auth_service.AuthService.get_user_by_id', new_callable=AsyncMock) as mock_get_user:
            # Set return values for async mocks
            mock_verify.return_value = {
                "sub": "admin-001",
                "email": "admin@classsphere.edu",
                "role": "admin"
            }

            from src.app.models.user import UserRole, UserInDB
            from datetime import datetime

            mock_user = UserInDB(
                id="admin-001",
                email="admin@classsphere.edu",
                name="System Administrator",
                role=UserRole.ADMIN,
                hashed_password="hash",
                is_active=True,
                created_at=datetime.utcnow(),
                updated_at=datetime.utcnow()
            )

            mock_get_user.return_value = mock_user

            client = TestClient(app)
            response = client.get(
                "/api/v1/auth/me",
                headers={"Authorization": "Bearer valid-token"}
            )

            assert response.status_code == 200
            data = response.json()

            assert data["success"] is True
            assert data["data"]["email"] == "admin@classsphere.edu"
            assert data["data"]["role"] == "admin"


def test_get_current_user_info_invalid_token():
    """Test getting current user info with invalid token."""
    from src.app.main import create_app

    app = create_app()

    with patch('src.app.core.security.verify_token') as mock_verify:
        from src.app.core.security import AuthenticationError
        mock_verify.side_effect = AuthenticationError("Invalid token")

        client = TestClient(app)
        response = client.get(
            "/api/v1/auth/me",
            headers={"Authorization": "Bearer invalid-token"}
        )

        assert response.status_code == 401


def test_get_current_user_info_no_token(client):
    """Test getting current user info without token."""
    response = client.get("/api/v1/auth/me")

    assert response.status_code == 403  # FastAPI returns 403 for missing auth


def test_verify_token_success():
    """Test token verification with valid token."""
    from src.app.main import create_app

    app = create_app()

    with patch('src.app.api.endpoints.auth.verify_token', new_callable=AsyncMock) as mock_verify:
        mock_verify.return_value = {
            "sub": "admin-001",
            "email": "admin@classsphere.edu",
            "role": "admin",
            "exp": 9999999999
        }

        client = TestClient(app)
        response = client.post(
            "/api/v1/auth/verify",
            headers={"Authorization": "Bearer valid-token"}
        )

        assert response.status_code == 200
        data = response.json()

        assert data["success"] is True
        assert data["data"]["valid"] is True
        assert data["data"]["user_id"] == "admin-001"
        assert data["data"]["email"] == "admin@classsphere.edu"


def test_verify_token_invalid():
    """Test token verification with invalid token."""
    from src.app.main import create_app

    app = create_app()

    with patch('src.app.core.security.verify_token') as mock_verify:
        from src.app.core.security import AuthenticationError
        mock_verify.side_effect = AuthenticationError("Invalid token")

        client = TestClient(app)
        response = client.post(
            "/api/v1/auth/verify",
            headers={"Authorization": "Bearer invalid-token"}
        )

        assert response.status_code == 401


def test_logout_success(client):
    """Test logout endpoint."""
    response = client.post("/api/v1/auth/logout")

    assert response.status_code == 200
    data = response.json()

    assert data["success"] is True
    assert data["data"]["logged_out"] is True