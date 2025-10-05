"""
Tests for AuthService
"""
import pytest
from fastapi import HTTPException
from app.services.auth_service import AuthService
from app.models.auth import UserCreate, UserRole


class TestAuthService:
    """Test AuthService functionality"""

    def setup_method(self):
        """Setup test method"""
        self.auth_service = AuthService()

    def test_get_user_by_email_success(self):
        """Test getting user by email"""
        user = self.auth_service.get_user_by_email("admin@classsphere.com")
        assert user is not None
        assert user.email == "admin@classsphere.com"
        assert user.role == UserRole.ADMIN

    def test_get_user_by_email_not_found(self):
        """Test getting non-existent user by email"""
        user = self.auth_service.get_user_by_email("nonexistent@example.com")
        assert user is None

    def test_get_user_by_id_success(self):
        """Test getting user by ID"""
        user = self.auth_service.get_user_by_id(1)
        assert user is not None
        assert user.id == 1
        assert user.email == "admin@classsphere.com"

    def test_get_user_by_id_not_found(self):
        """Test getting non-existent user by ID"""
        user = self.auth_service.get_user_by_id(999)
        assert user is None

    def test_authenticate_user_success(self):
        """Test successful user authentication"""
        user = self.auth_service.authenticate_user("admin@classsphere.com", "admin123")
        assert user is not None
        assert user.email == "admin@classsphere.com"

    def test_authenticate_user_wrong_password(self):
        """Test authentication with wrong password"""
        user = self.auth_service.authenticate_user("admin@classsphere.com", "wrongpassword")
        assert user is None

    def test_authenticate_user_nonexistent_email(self):
        """Test authentication with non-existent email"""
        user = self.auth_service.authenticate_user("nonexistent@example.com", "password")
        assert user is None

    def test_login_success(self):
        """Test successful login"""
        auth_response = self.auth_service.login("admin@classsphere.com", "admin123")

        assert auth_response.user.email == "admin@classsphere.com"
        assert auth_response.token.access_token is not None
        assert auth_response.token.refresh_token is not None
        assert auth_response.token.token_type == "bearer"

    def test_login_invalid_credentials(self):
        """Test login with invalid credentials"""
        with pytest.raises(HTTPException) as exc_info:
            self.auth_service.login("admin@classsphere.com", "wrongpassword")

        assert exc_info.value.status_code == 401
        assert "Invalid credentials" in str(exc_info.value.detail)

    def test_create_user_success(self):
        """Test successful user creation"""
        user_create = UserCreate(
            email="newuser@example.com",
            password="password123",
            first_name="New",
            last_name="User",
            role=UserRole.STUDENT
        )

        user = self.auth_service.create_user(user_create)
        assert user.email == "newuser@example.com"
        assert user.first_name == "New"
        assert user.role == UserRole.STUDENT
        assert user.is_active is True

        # Verify user was added to the database
        retrieved_user = self.auth_service.get_user_by_email("newuser@example.com")
        assert retrieved_user is not None

    def test_create_user_duplicate_email(self):
        """Test creating user with existing email"""
        user_create = UserCreate(
            email="admin@classsphere.com",  # Already exists
            password="password123",
            first_name="Duplicate",
            last_name="User",
            role=UserRole.STUDENT
        )

        with pytest.raises(HTTPException) as exc_info:
            self.auth_service.create_user(user_create)

        assert exc_info.value.status_code == 400
        assert "already registered" in str(exc_info.value.detail)

    def test_create_tokens(self):
        """Test token creation"""
        user = self.auth_service.get_user_by_email("admin@classsphere.com")
        token = self.auth_service.create_tokens(user)

        assert token.access_token is not None
        assert token.refresh_token is not None
        assert token.token_type == "bearer"
        assert token.expires_in == 1800

    def test_all_demo_users_exist(self):
        """Test that all demo users are properly initialized"""
        demo_emails = [
            "admin@classsphere.com",
            "coordinator@classsphere.com",
            "teacher@classsphere.com",
            "student@classsphere.com"
        ]

        for email in demo_emails:
            user = self.auth_service.get_user_by_email(email)
            assert user is not None, f"Demo user {email} not found"
            assert user.is_active is True

    def test_demo_users_roles(self):
        """Test that demo users have correct roles"""
        role_mapping = {
            "admin@classsphere.com": UserRole.ADMIN,
            "coordinator@classsphere.com": UserRole.COORDINATOR,
            "teacher@classsphere.com": UserRole.TEACHER,
            "student@classsphere.com": UserRole.STUDENT,
        }

        for email, expected_role in role_mapping.items():
            user = self.auth_service.get_user_by_email(email)
            assert user.role == expected_role, f"User {email} has wrong role"