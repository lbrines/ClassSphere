"""User models with Pydantic v2."""

from datetime import datetime
from typing import Optional, List
from enum import Enum

from pydantic import BaseModel, ConfigDict, EmailStr, field_validator, field_serializer
from pydantic.types import SecretStr


class UserRole(str, Enum):
    """User roles enumeration."""
    ADMIN = "admin"
    COORDINATOR = "coordinator"
    TEACHER = "teacher"
    STUDENT = "student"


class UserStatus(str, Enum):
    """User status enumeration."""
    ACTIVE = "active"
    INACTIVE = "inactive"
    SUSPENDED = "suspended"
    PENDING = "pending"


class UserBase(BaseModel):
    """Base user model with common fields."""

    email: EmailStr
    full_name: str
    role: UserRole = UserRole.STUDENT
    status: UserStatus = UserStatus.ACTIVE
    is_active: bool = True

    model_config = ConfigDict(
        from_attributes=True,
        str_strip_whitespace=True,
        validate_assignment=True,
        extra="forbid"
    )

    @field_validator("full_name")
    @classmethod
    def validate_full_name(cls, v: str) -> str:
        """Validate full name."""
        if len(v.strip()) < 2:
            raise ValueError("Full name must be at least 2 characters")
        if len(v.strip()) > 100:
            raise ValueError("Full name must be less than 100 characters")
        return v.strip()

    @field_validator("email")
    @classmethod
    def validate_email(cls, v: str) -> str:
        """Validate email format."""
        return v.lower().strip()


class UserCreate(UserBase):
    """User creation model."""

    password: SecretStr
    confirm_password: SecretStr

    @field_validator("password")
    @classmethod
    def validate_password(cls, v: SecretStr) -> SecretStr:
        """Validate password strength."""
        password = v.get_secret_value()

        if len(password) < 8:
            raise ValueError("Password must be at least 8 characters")
        if len(password) > 128:
            raise ValueError("Password must be less than 128 characters")

        # Check for at least one uppercase, lowercase, digit, and special char
        has_upper = any(c.isupper() for c in password)
        has_lower = any(c.islower() for c in password)
        has_digit = any(c.isdigit() for c in password)
        has_special = any(c in "!@#$%^&*()_+-=[]{}|;:,.<>?" for c in password)

        if not all([has_upper, has_lower, has_digit, has_special]):
            raise ValueError(
                "Password must contain at least one uppercase letter, "
                "one lowercase letter, one digit, and one special character"
            )

        return v

    def model_post_init(self, __context) -> None:
        """Validate password confirmation."""
        if self.password.get_secret_value() != self.confirm_password.get_secret_value():
            raise ValueError("Passwords do not match")


class UserUpdate(BaseModel):
    """User update model."""

    full_name: Optional[str] = None
    role: Optional[UserRole] = None
    status: Optional[UserStatus] = None
    is_active: Optional[bool] = None

    model_config = ConfigDict(
        from_attributes=True,
        str_strip_whitespace=True,
        validate_assignment=True,
        extra="forbid"
    )

    @field_validator("full_name")
    @classmethod
    def validate_full_name(cls, v: Optional[str]) -> Optional[str]:
        """Validate full name if provided."""
        if v is None:
            return v
        if len(v.strip()) < 2:
            raise ValueError("Full name must be at least 2 characters")
        if len(v.strip()) > 100:
            raise ValueError("Full name must be less than 100 characters")
        return v.strip()


class UserResponse(UserBase):
    """User response model."""

    id: str
    created_at: datetime
    updated_at: Optional[datetime] = None
    last_login: Optional[datetime] = None
    google_id: Optional[str] = None

    model_config = ConfigDict(
        from_attributes=True
    )

    @field_serializer('created_at', 'updated_at', 'last_login', when_used='json')
    def serialize_datetime(self, value: Optional[datetime]) -> Optional[str]:
        """Serialize datetime to ISO format."""
        return value.isoformat() if value else None


class UserInDB(UserResponse):
    """User model as stored in database."""

    hashed_password: str
    google_sub: Optional[str] = None
    google_access_token: Optional[str] = None
    google_refresh_token: Optional[str] = None


class UserPermissions(BaseModel):
    """User permissions model."""

    user_id: str
    role: UserRole
    permissions: List[str]
    scopes: List[str] = []

    model_config = ConfigDict(
        from_attributes=True,
        extra="forbid"
    )

    @classmethod
    def get_role_permissions(cls, role: UserRole) -> List[str]:
        """Get default permissions for a role."""
        role_permissions = {
            UserRole.ADMIN: [
                "read:all", "write:all", "delete:all",
                "manage:users", "manage:system", "manage:courses"
            ],
            UserRole.COORDINATOR: [
                "read:courses", "write:courses", "read:users",
                "write:students", "read:metrics", "manage:courses"
            ],
            UserRole.TEACHER: [
                "read:own_courses", "write:own_courses", "read:students",
                "write:grades", "read:metrics"
            ],
            UserRole.STUDENT: [
                "read:own_data", "read:own_courses", "read:own_grades"
            ]
        }
        return role_permissions.get(role, [])


class PasswordReset(BaseModel):
    """Password reset model."""

    token: str
    new_password: SecretStr
    confirm_password: SecretStr

    model_config = ConfigDict(extra="forbid")

    @field_validator("new_password")
    @classmethod
    def validate_password(cls, v: SecretStr) -> SecretStr:
        """Validate password strength."""
        password = v.get_secret_value()

        if len(password) < 8:
            raise ValueError("Password must be at least 8 characters")
        if len(password) > 128:
            raise ValueError("Password must be less than 128 characters")

        has_upper = any(c.isupper() for c in password)
        has_lower = any(c.islower() for c in password)
        has_digit = any(c.isdigit() for c in password)
        has_special = any(c in "!@#$%^&*()_+-=[]{}|;:,.<>?" for c in password)

        if not all([has_upper, has_lower, has_digit, has_special]):
            raise ValueError(
                "Password must contain at least one uppercase letter, "
                "one lowercase letter, one digit, and one special character"
            )

        return v

    def model_post_init(self, __context) -> None:
        """Validate password confirmation."""
        if self.new_password.get_secret_value() != self.confirm_password.get_secret_value():
            raise ValueError("Passwords do not match")