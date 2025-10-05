"""
Tests for authentication API endpoints
"""
import pytest
from app.models.auth import UserRole


class TestAuthLogin:
    """Test login functionality"""

    def test_login_success_admin(self, client):
        """Test successful admin login"""
        response = client.post(
            "/api/v1/auth/login",
            json={"email": "admin@classsphere.com", "password": "admin123"}
        )
        assert response.status_code == 200

        data = response.json()
        assert "user" in data
        assert "token" in data

        # Verify user data
        user = data["user"]
        assert user["email"] == "admin@classsphere.com"
        assert user["role"] == "admin"
        assert user["is_active"] is True

        # Verify token data
        token = data["token"]
        assert "access_token" in token
        assert "refresh_token" in token
        assert token["token_type"] == "bearer"
        assert token["expires_in"] == 1800

    def test_login_success_all_roles(self, client):
        """Test successful login for all user roles"""
        test_cases = [
            ("admin@classsphere.com", "admin123", "admin"),
            ("coordinator@classsphere.com", "coord123", "coordinator"),
            ("teacher@classsphere.com", "teacher123", "teacher"),
            ("student@classsphere.com", "student123", "student"),
        ]

        for email, password, expected_role in test_cases:
            response = client.post(
                "/api/v1/auth/login",
                json={"email": email, "password": password}
            )
            assert response.status_code == 200

            data = response.json()
            assert data["user"]["email"] == email
            assert data["user"]["role"] == expected_role

    def test_login_invalid_email(self, client):
        """Test login with non-existent email"""
        response = client.post(
            "/api/v1/auth/login",
            json={"email": "nonexistent@example.com", "password": "password"}
        )
        assert response.status_code == 401
        assert "Incorrect email or password" in response.json()["detail"]

    def test_login_invalid_password(self, client):
        """Test login with wrong password"""
        response = client.post(
            "/api/v1/auth/login",
            json={"email": "admin@classsphere.com", "password": "wrongpassword"}
        )
        assert response.status_code == 401
        assert "Incorrect email or password" in response.json()["detail"]

    def test_login_missing_email(self, client):
        """Test login with missing email"""
        response = client.post(
            "/api/v1/auth/login",
            json={"password": "admin123"}
        )
        assert response.status_code == 422

    def test_login_missing_password(self, client):
        """Test login with missing password"""
        response = client.post(
            "/api/v1/auth/login",
            json={"email": "admin@classsphere.com"}
        )
        assert response.status_code == 422

    def test_login_invalid_json(self, client):
        """Test login with invalid JSON"""
        response = client.post(
            "/api/v1/auth/login",
            data="invalid json",
            headers={"Content-Type": "application/json"}
        )
        assert response.status_code == 422


class TestAuthMe:
    """Test current user endpoint"""

    def test_me_success(self, client, admin_token, auth_headers):
        """Test successful user info retrieval"""
        response = client.get(
            "/api/v1/auth/me",
            headers=auth_headers(admin_token)
        )
        assert response.status_code == 200

        data = response.json()
        assert data["email"] == "admin@classsphere.com"
        assert data["role"] == "admin"
        assert data["is_active"] is True

    def test_me_all_roles(self, client, admin_token, coordinator_token,
                         teacher_token, student_token, auth_headers):
        """Test user info for all roles"""
        test_cases = [
            (admin_token, "admin@classsphere.com", "admin"),
            (coordinator_token, "coordinator@classsphere.com", "coordinator"),
            (teacher_token, "teacher@classsphere.com", "teacher"),
            (student_token, "student@classsphere.com", "student"),
        ]

        for token, expected_email, expected_role in test_cases:
            response = client.get(
                "/api/v1/auth/me",
                headers=auth_headers(token)
            )
            assert response.status_code == 200

            data = response.json()
            assert data["email"] == expected_email
            assert data["role"] == expected_role

    def test_me_no_token(self, client):
        """Test user info without token"""
        response = client.get("/api/v1/auth/me")
        assert response.status_code == 403

    def test_me_invalid_token(self, client, auth_headers):
        """Test user info with invalid token"""
        response = client.get(
            "/api/v1/auth/me",
            headers=auth_headers("invalid-token")
        )
        assert response.status_code == 401
        assert "Could not validate credentials" in response.json()["detail"]

    def test_me_expired_token(self, client, auth_headers):
        """Test user info with expired token"""
        # Create a token with past expiration
        expired_token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxIiwiZXhwIjoxNjAwMDAwMDAwfQ.invalid"
        response = client.get(
            "/api/v1/auth/me",
            headers=auth_headers(expired_token)
        )
        assert response.status_code == 401


class TestAuthRefresh:
    """Test token refresh functionality"""

    def test_refresh_success(self, client):
        """Test successful token refresh"""
        # First login to get refresh token
        login_response = client.post(
            "/api/v1/auth/login",
            json={"email": "admin@classsphere.com", "password": "admin123"}
        )
        refresh_token = login_response.json()["token"]["refresh_token"]

        # Use refresh token
        response = client.post(
            "/api/v1/auth/refresh",
            json={"refresh_token": refresh_token}
        )
        assert response.status_code == 200

        data = response.json()
        assert "access_token" in data
        assert "refresh_token" in data
        assert data["token_type"] == "bearer"

    def test_refresh_invalid_token(self, client):
        """Test refresh with invalid token"""
        response = client.post(
            "/api/v1/auth/refresh",
            json={"refresh_token": "invalid-token"}
        )
        assert response.status_code == 401

    def test_refresh_missing_token(self, client):
        """Test refresh with missing token"""
        response = client.post("/api/v1/auth/refresh", json={})
        assert response.status_code == 422