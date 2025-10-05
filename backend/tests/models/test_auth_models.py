"""
Tests for authentication models
"""
import pytest
from datetime import datetime
from pydantic import ValidationError
from app.models.auth import (
    User, UserCreate, UserLogin, Token, TokenData,
    AuthResponse, GoogleUserInfo, GoogleOAuthRequest,
    UserRole
)


class TestUserRole:
    """Test UserRole enum"""

    def test_user_role_values(self):
        """Test that all user roles have correct values"""
        assert UserRole.ADMIN == "admin"
        assert UserRole.COORDINATOR == "coordinator"
        assert UserRole.TEACHER == "teacher"
        assert UserRole.STUDENT == "student"

    def test_user_role_hierarchy(self):
        """Test user role hierarchy logic"""
        roles = [UserRole.ADMIN, UserRole.COORDINATOR, UserRole.TEACHER, UserRole.STUDENT]
        assert len(roles) == 4
        assert all(isinstance(role, UserRole) for role in roles)


class TestUser:
    """Test User model"""

    def test_user_creation_success(self):
        """Test successful user creation"""
        user = User(
            id=1,
            email="test@example.com",
            first_name="Test",
            last_name="User",
            role=UserRole.STUDENT,
            is_active=True,
            google_id=None,
            avatar_url=None,
            created_at=datetime.now(),
            last_login=None
        )

        assert user.id == 1
        assert user.email == "test@example.com"
        assert user.role == UserRole.STUDENT
        assert user.is_active is True

    def test_user_with_google_id(self):
        """Test user with Google ID"""
        user = User(
            id=1,
            email="test@example.com",
            first_name="Test",
            last_name="User",
            role=UserRole.STUDENT,
            is_active=True,
            google_id="123456789",
            avatar_url="https://example.com/avatar.jpg",
            created_at=datetime.now(),
            last_login=datetime.now()
        )

        assert user.google_id == "123456789"
        assert user.avatar_url == "https://example.com/avatar.jpg"

    def test_user_invalid_email(self):
        """Test user creation with invalid email"""
        with pytest.raises(ValidationError):
            User(
                id=1,
                email="invalid-email",
                first_name="Test",
                last_name="User",
                role=UserRole.STUDENT,
                is_active=True,
                created_at=datetime.now()
            )


class TestUserCreate:
    """Test UserCreate model"""

    def test_user_create_success(self):
        """Test successful UserCreate validation"""
        user_create = UserCreate(
            email="test@example.com",
            password="password123",
            first_name="Test",
            last_name="User",
            role=UserRole.STUDENT
        )

        assert user_create.email == "test@example.com"
        assert user_create.password == "password123"
        assert user_create.role == UserRole.STUDENT

    def test_user_create_invalid_email(self):
        """Test UserCreate with invalid email"""
        with pytest.raises(ValidationError):
            UserCreate(
                email="invalid-email",
                password="password123",
                first_name="Test",
                last_name="User",
                role=UserRole.STUDENT
            )

    def test_user_create_missing_fields(self):
        """Test UserCreate with missing required fields"""
        with pytest.raises(ValidationError):
            UserCreate(
                email="test@example.com",
                # Missing password
                first_name="Test",
                last_name="User",
                role=UserRole.STUDENT
            )


class TestUserLogin:
    """Test UserLogin model"""

    def test_user_login_success(self):
        """Test successful UserLogin validation"""
        login = UserLogin(
            email="test@example.com",
            password="password123"
        )

        assert login.email == "test@example.com"
        assert login.password == "password123"

    def test_user_login_invalid_email(self):
        """Test UserLogin with invalid email"""
        with pytest.raises(ValidationError):
            UserLogin(
                email="invalid-email",
                password="password123"
            )

    def test_user_login_missing_password(self):
        """Test UserLogin with missing password"""
        with pytest.raises(ValidationError):
            UserLogin(
                email="test@example.com"
                # Missing password
            )


class TestToken:
    """Test Token model"""

    def test_token_creation(self):
        """Test Token model creation"""
        token = Token(
            access_token="access_token_here",
            refresh_token="refresh_token_here",
            token_type="bearer",
            expires_in=3600
        )

        assert token.access_token == "access_token_here"
        assert token.refresh_token == "refresh_token_here"
        assert token.token_type == "bearer"
        assert token.expires_in == 3600

    def test_token_missing_fields(self):
        """Test Token with missing required fields"""
        with pytest.raises(ValidationError):
            Token(
                access_token="access_token_here",
                # Missing refresh_token
                token_type="bearer",
                expires_in=3600
            )


class TestTokenData:
    """Test TokenData model"""

    def test_token_data_creation(self):
        """Test TokenData creation"""
        token_data = TokenData(
            user_id=1,
            email="test@example.com",
            role=UserRole.ADMIN
        )

        assert token_data.user_id == 1
        assert token_data.email == "test@example.com"
        assert token_data.role == UserRole.ADMIN

    def test_token_data_optional_role(self):
        """Test TokenData with optional role"""
        token_data = TokenData(
            user_id=1,
            email="test@example.com",
            role=None
        )

        assert token_data.role is None


class TestAuthResponse:
    """Test AuthResponse model"""

    def test_auth_response_creation(self):
        """Test AuthResponse creation"""
        user = User(
            id=1,
            email="test@example.com",
            first_name="Test",
            last_name="User",
            role=UserRole.STUDENT,
            is_active=True,
            created_at=datetime.now()
        )

        token = Token(
            access_token="access_token",
            refresh_token="refresh_token",
            token_type="bearer",
            expires_in=3600
        )

        auth_response = AuthResponse(user=user, token=token)

        assert auth_response.user == user
        assert auth_response.token == token


class TestGoogleUserInfo:
    """Test GoogleUserInfo model"""

    def test_google_user_info_creation(self):
        """Test GoogleUserInfo creation"""
        google_user = GoogleUserInfo(
            sub="123456789",
            email="test@gmail.com",
            given_name="Test",
            family_name="User",
            picture="https://example.com/avatar.jpg"
        )

        assert google_user.sub == "123456789"
        assert google_user.email == "test@gmail.com"
        assert google_user.given_name == "Test"
        assert google_user.family_name == "User"
        assert google_user.picture == "https://example.com/avatar.jpg"

    def test_google_user_info_optional_fields(self):
        """Test GoogleUserInfo with optional fields"""
        google_user = GoogleUserInfo(
            sub="123456789",
            email="test@gmail.com",
            given_name="Test",
            family_name="User"
            # picture is optional
        )

        assert google_user.picture is None


class TestGoogleOAuthRequest:
    """Test GoogleOAuthRequest model"""

    def test_google_oauth_request_creation(self):
        """Test GoogleOAuthRequest creation"""
        request = GoogleOAuthRequest(
            code="auth_code_here",
            code_verifier="code_verifier_here"
        )

        assert request.code == "auth_code_here"
        assert request.code_verifier == "code_verifier_here"

    def test_google_oauth_request_missing_fields(self):
        """Test GoogleOAuthRequest with missing fields"""
        with pytest.raises(ValidationError):
            GoogleOAuthRequest(
                code="auth_code_here"
                # Missing code_verifier
            )