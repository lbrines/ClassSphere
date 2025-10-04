"""Tests for user models with Pydantic v2."""

import pytest
from datetime import datetime
from pydantic import ValidationError
from pydantic.types import SecretStr

from src.app.models.user import (
    UserRole,
    UserStatus,
    UserBase,
    UserCreate,
    UserUpdate,
    UserResponse,
    UserInDB,
    UserPermissions,
    PasswordReset
)


class TestUserRole:
    """Test UserRole enumeration."""

    def test_user_roles(self):
        """Test all user roles."""
        assert UserRole.ADMIN == "admin"
        assert UserRole.COORDINATOR == "coordinator"
        assert UserRole.TEACHER == "teacher"
        assert UserRole.STUDENT == "student"


class TestUserStatus:
    """Test UserStatus enumeration."""

    def test_user_statuses(self):
        """Test all user statuses."""
        assert UserStatus.ACTIVE == "active"
        assert UserStatus.INACTIVE == "inactive"
        assert UserStatus.SUSPENDED == "suspended"
        assert UserStatus.PENDING == "pending"


class TestUserBase:
    """Test UserBase model."""

    def test_valid_user_base(self):
        """Test valid user base model."""
        user = UserBase(
            email="test@example.com",
            full_name="Test User",
            role=UserRole.STUDENT,
            status=UserStatus.ACTIVE
        )

        assert user.email == "test@example.com"
        assert user.full_name == "Test User"
        assert user.role == UserRole.STUDENT
        assert user.status == UserStatus.ACTIVE
        assert user.is_active is True

    def test_email_normalization(self):
        """Test email normalization."""
        user = UserBase(
            email="  TEST@EXAMPLE.COM  ",
            full_name="Test User"
        )
        assert user.email == "test@example.com"

    def test_full_name_validation(self):
        """Test full name validation."""
        # Valid name
        user = UserBase(
            email="test@example.com",
            full_name="  Test User  "
        )
        assert user.full_name == "Test User"

        # Too short
        with pytest.raises(ValidationError, match="Full name must be at least 2 characters"):
            UserBase(
                email="test@example.com",
                full_name="A"
            )

        # Too long
        with pytest.raises(ValidationError, match="Full name must be less than 100 characters"):
            UserBase(
                email="test@example.com",
                full_name="A" * 101
            )

    def test_invalid_email(self):
        """Test invalid email validation."""
        with pytest.raises(ValidationError):
            UserBase(
                email="invalid-email",
                full_name="Test User"
            )

    def test_defaults(self):
        """Test default values."""
        user = UserBase(
            email="test@example.com",
            full_name="Test User"
        )

        assert user.role == UserRole.STUDENT
        assert user.status == UserStatus.ACTIVE
        assert user.is_active is True

    def test_config_dict(self):
        """Test ConfigDict configuration."""
        user = UserBase(
            email="test@example.com",
            full_name="Test User"
        )

        # Test from_attributes
        assert hasattr(user.model_config, '__getitem__')
        assert user.model_config['from_attributes'] is True
        assert user.model_config['str_strip_whitespace'] is True
        assert user.model_config['validate_assignment'] is True
        assert user.model_config['extra'] == "forbid"


class TestUserCreate:
    """Test UserCreate model."""

    def test_valid_user_create(self):
        """Test valid user creation."""
        user = UserCreate(
            email="test@example.com",
            full_name="Test User",
            password=SecretStr("TestPass123!"),
            confirm_password=SecretStr("TestPass123!")
        )

        assert user.email == "test@example.com"
        assert user.full_name == "Test User"
        assert user.password.get_secret_value() == "TestPass123!"

    def test_password_validation_length(self):
        """Test password length validation."""
        # Too short
        with pytest.raises(ValidationError, match="Password must be at least 8 characters"):
            UserCreate(
                email="test@example.com",
                full_name="Test User",
                password=SecretStr("Short1!"),
                confirm_password=SecretStr("Short1!")
            )

        # Too long
        with pytest.raises(ValidationError, match="Password must be less than 128 characters"):
            UserCreate(
                email="test@example.com",
                full_name="Test User",
                password=SecretStr("A" * 129),
                confirm_password=SecretStr("A" * 129)
            )

    def test_password_complexity_validation(self):
        """Test password complexity validation."""
        # Missing uppercase
        with pytest.raises(ValidationError, match="Password must contain"):
            UserCreate(
                email="test@example.com",
                full_name="Test User",
                password=SecretStr("testpass123!"),
                confirm_password=SecretStr("testpass123!")
            )

        # Missing lowercase
        with pytest.raises(ValidationError, match="Password must contain"):
            UserCreate(
                email="test@example.com",
                full_name="Test User",
                password=SecretStr("TESTPASS123!"),
                confirm_password=SecretStr("TESTPASS123!")
            )

        # Missing digit
        with pytest.raises(ValidationError, match="Password must contain"):
            UserCreate(
                email="test@example.com",
                full_name="Test User",
                password=SecretStr("TestPass!"),
                confirm_password=SecretStr("TestPass!")
            )

        # Missing special character
        with pytest.raises(ValidationError, match="Password must contain"):
            UserCreate(
                email="test@example.com",
                full_name="Test User",
                password=SecretStr("TestPass123"),
                confirm_password=SecretStr("TestPass123")
            )

    def test_password_confirmation(self):
        """Test password confirmation validation."""
        with pytest.raises(ValidationError, match="Passwords do not match"):
            UserCreate(
                email="test@example.com",
                full_name="Test User",
                password=SecretStr("TestPass123!"),
                confirm_password=SecretStr("DifferentPass123!")
            )


class TestUserUpdate:
    """Test UserUpdate model."""

    def test_valid_user_update(self):
        """Test valid user update."""
        user_update = UserUpdate(
            full_name="Updated Name",
            role=UserRole.TEACHER,
            status=UserStatus.INACTIVE,
            is_active=False
        )

        assert user_update.full_name == "Updated Name"
        assert user_update.role == UserRole.TEACHER
        assert user_update.status == UserStatus.INACTIVE
        assert user_update.is_active is False

    def test_partial_update(self):
        """Test partial user update."""
        user_update = UserUpdate(full_name="Only Name")

        assert user_update.full_name == "Only Name"
        assert user_update.role is None
        assert user_update.status is None
        assert user_update.is_active is None

    def test_empty_update(self):
        """Test empty user update."""
        user_update = UserUpdate()

        assert user_update.full_name is None
        assert user_update.role is None
        assert user_update.status is None
        assert user_update.is_active is None

    def test_full_name_validation(self):
        """Test full name validation in update."""
        # Valid update
        user_update = UserUpdate(full_name="  Valid Name  ")
        assert user_update.full_name == "Valid Name"

        # Invalid update - too short
        with pytest.raises(ValidationError, match="Full name must be at least 2 characters"):
            UserUpdate(full_name="A")


class TestUserResponse:
    """Test UserResponse model."""

    def test_valid_user_response(self):
        """Test valid user response."""
        now = datetime.now()
        user = UserResponse(
            id="user123",
            email="test@example.com",
            full_name="Test User",
            role=UserRole.STUDENT,
            status=UserStatus.ACTIVE,
            is_active=True,
            created_at=now,
            updated_at=now,
            last_login=now,
            google_id="google123"
        )

        assert user.id == "user123"
        assert user.email == "test@example.com"
        assert user.created_at == now
        assert user.google_id == "google123"

    def test_optional_fields(self):
        """Test optional fields in user response."""
        user = UserResponse(
            id="user123",
            email="test@example.com",
            full_name="Test User",
            created_at=datetime.now()
        )

        assert user.updated_at is None
        assert user.last_login is None
        assert user.google_id is None

    def test_datetime_serialization(self):
        """Test datetime serialization."""
        now = datetime.now()
        user = UserResponse(
            id="user123",
            email="test@example.com",
            full_name="Test User",
            created_at=now
        )

        # Test that datetime serialization method exists
        assert hasattr(user, 'serialize_datetime')

        # Test datetime serialization
        result = user.serialize_datetime(now)
        assert result == now.isoformat()

        # Test None serialization
        result = user.serialize_datetime(None)
        assert result is None


class TestUserInDB:
    """Test UserInDB model."""

    def test_valid_user_in_db(self):
        """Test valid user in database."""
        now = datetime.now()
        user = UserInDB(
            id="user123",
            email="test@example.com",
            full_name="Test User",
            created_at=now,
            hashed_password="hashed_password_here",
            google_sub="google_sub_123"
        )

        assert user.id == "user123"
        assert user.hashed_password == "hashed_password_here"
        assert user.google_sub == "google_sub_123"

    def test_oauth_tokens(self):
        """Test OAuth token fields."""
        user = UserInDB(
            id="user123",
            email="test@example.com",
            full_name="Test User",
            created_at=datetime.now(),
            hashed_password="hashed_password_here",
            google_access_token="access_token",
            google_refresh_token="refresh_token"
        )

        assert user.google_access_token == "access_token"
        assert user.google_refresh_token == "refresh_token"


class TestUserPermissions:
    """Test UserPermissions model."""

    def test_valid_user_permissions(self):
        """Test valid user permissions."""
        permissions = UserPermissions(
            user_id="user123",
            role=UserRole.TEACHER,
            permissions=["read:courses", "write:courses"],
            scopes=["classroom.courses.readonly"]
        )

        assert permissions.user_id == "user123"
        assert permissions.role == UserRole.TEACHER
        assert "read:courses" in permissions.permissions
        assert "classroom.courses.readonly" in permissions.scopes

    def test_role_permissions_admin(self):
        """Test admin role permissions."""
        permissions = UserPermissions.get_role_permissions(UserRole.ADMIN)

        assert "read:all" in permissions
        assert "write:all" in permissions
        assert "delete:all" in permissions
        assert "manage:users" in permissions
        assert "manage:system" in permissions

    def test_role_permissions_coordinator(self):
        """Test coordinator role permissions."""
        permissions = UserPermissions.get_role_permissions(UserRole.COORDINATOR)

        assert "read:courses" in permissions
        assert "write:courses" in permissions
        assert "read:users" in permissions
        assert "write:students" in permissions
        assert "manage:courses" in permissions

    def test_role_permissions_teacher(self):
        """Test teacher role permissions."""
        permissions = UserPermissions.get_role_permissions(UserRole.TEACHER)

        assert "read:own_courses" in permissions
        assert "write:own_courses" in permissions
        assert "read:students" in permissions
        assert "write:grades" in permissions

    def test_role_permissions_student(self):
        """Test student role permissions."""
        permissions = UserPermissions.get_role_permissions(UserRole.STUDENT)

        assert "read:own_data" in permissions
        assert "read:own_courses" in permissions
        assert "read:own_grades" in permissions

    def test_unknown_role_permissions(self):
        """Test unknown role permissions."""
        # This should return empty list for unknown roles
        permissions = UserPermissions.get_role_permissions("unknown_role")
        assert permissions == []


class TestPasswordReset:
    """Test PasswordReset model."""

    def test_valid_password_reset(self):
        """Test valid password reset."""
        reset = PasswordReset(
            token="reset_token_123",
            new_password=SecretStr("NewPass123!"),
            confirm_password=SecretStr("NewPass123!")
        )

        assert reset.token == "reset_token_123"
        assert reset.new_password.get_secret_value() == "NewPass123!"

    def test_password_validation(self):
        """Test password validation in reset."""
        # Same validation as UserCreate
        with pytest.raises(ValidationError, match="Password must be at least 8 characters"):
            PasswordReset(
                token="token",
                new_password=SecretStr("Short1!"),
                confirm_password=SecretStr("Short1!")
            )

    def test_password_confirmation_mismatch(self):
        """Test password confirmation mismatch in reset."""
        with pytest.raises(ValidationError, match="Passwords do not match"):
            PasswordReset(
                token="token",
                new_password=SecretStr("NewPass123!"),
                confirm_password=SecretStr("DifferentPass123!")
            )

    def test_model_serialization(self):
        """Test model serialization and validation."""
        reset = PasswordReset(
            token="reset_token_123",
            new_password=SecretStr("NewPass123!"),
            confirm_password=SecretStr("NewPass123!")
        )

        # Test model dump
        data = reset.model_dump()
        assert "token" in data
        assert "new_password" in data
        assert "confirm_password" in data

        # Test model validation
        validated = PasswordReset.model_validate(data)
        assert validated.token == reset.token