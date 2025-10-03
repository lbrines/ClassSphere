"""
User models using Pydantic v2 with ConfigDict.
"""
from datetime import datetime
from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field, field_validator, ConfigDict
from enum import Enum


class UserRole(str, Enum):
    """User roles enum."""
    ADMIN = "admin"
    TEACHER = "teacher"
    STUDENT = "student"
    COORDINATOR = "coordinator"


class UserStatus(str, Enum):
    """User status enum."""
    ACTIVE = "active"
    INACTIVE = "inactive"
    PENDING = "pending"
    SUSPENDED = "suspended"


class UserBase(BaseModel):
    """Base user model."""
    email: str = Field(..., description="User email address")
    name: str = Field(..., min_length=2, max_length=100, description="User full name")
    role: UserRole = Field(default=UserRole.STUDENT, description="User role")
    status: UserStatus = Field(default=UserStatus.ACTIVE, description="User status")
    
    # Optional fields for compatibility with MockService and Google API
    google_id: Optional[str] = Field(default=None, description="Google user ID")
    avatar_url: Optional[str] = Field(default=None, description="User avatar URL")
    phone: Optional[str] = Field(default=None, description="User phone number")
    department: Optional[str] = Field(default=None, description="User department")
    grade_level: Optional[str] = Field(default=None, description="User grade level")
    
    # Metadata fields
    created_at: Optional[datetime] = Field(default_factory=datetime.utcnow, description="Creation timestamp")
    updated_at: Optional[datetime] = Field(default_factory=datetime.utcnow, description="Last update timestamp")
    last_login: Optional[datetime] = Field(default=None, description="Last login timestamp")
    
    # Pydantic v2 Configuration
    model_config = ConfigDict(
        from_attributes=True,
        validate_assignment=True,
        use_enum_values=True,
        json_encoders={
            datetime: lambda v: v.isoformat()
        }
    )
    
    @field_validator('email')
    @classmethod
    def validate_email(cls, v: str) -> str:
        """Validate email format."""
        import re
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not re.match(pattern, v):
            raise ValueError('Invalid email format')
        return v.lower()
    
    @field_validator('name')
    @classmethod
    def validate_name(cls, v: str) -> str:
        """Validate name format."""
        if not v.strip():
            raise ValueError('Name cannot be empty')
        return v.strip().title()


class UserCreate(UserBase):
    """User creation model."""
    password: str = Field(..., min_length=8, description="User password")
    confirm_password: str = Field(..., description="Password confirmation")
    
    @field_validator('password')
    @classmethod
    def validate_password(cls, v: str) -> str:
        """Validate password strength."""
        if len(v) < 8:
            raise ValueError('Password must be at least 8 characters long')
        
        has_upper = any(c.isupper() for c in v)
        has_lower = any(c.islower() for c in v)
        has_digit = any(c.isdigit() for c in v)
        has_special = any(c in "!@#$%^&*()_+-=[]{}|;:,.<>?" for c in v)
        
        if not (has_upper and has_lower and has_digit and has_special):
            raise ValueError('Password must contain uppercase, lowercase, digit and special character')
        
        return v
    
    @field_validator('confirm_password')
    @classmethod
    def validate_confirm_password(cls, v: str, info) -> str:
        """Validate password confirmation."""
        if 'password' in info.data and v != info.data['password']:
            raise ValueError('Passwords do not match')
        return v


class UserUpdate(BaseModel):
    """User update model."""
    name: Optional[str] = Field(None, min_length=2, max_length=100, description="User full name")
    role: Optional[UserRole] = Field(None, description="User role")
    status: Optional[UserStatus] = Field(None, description="User status")
    phone: Optional[str] = Field(None, description="User phone number")
    department: Optional[str] = Field(None, description="User department")
    grade_level: Optional[str] = Field(None, description="User grade level")
    avatar_url: Optional[str] = Field(None, description="User avatar URL")
    
    # Pydantic v2 Configuration
    model_config = ConfigDict(
        from_attributes=True,
        validate_assignment=True,
        use_enum_values=True,
        json_encoders={
            datetime: lambda v: v.isoformat()
        }
    )
    
    @field_validator('name')
    @classmethod
    def validate_name(cls, v: Optional[str]) -> Optional[str]:
        """Validate name format."""
        if v is not None and not v.strip():
            raise ValueError('Name cannot be empty')
        return v.strip().title() if v else None


class UserResponse(UserBase):
    """User response model."""
    user_id: str = Field(..., description="User unique identifier")
    permissions: List[str] = Field(default_factory=list, description="User permissions")
    is_verified: bool = Field(default=False, description="Email verification status")
    
    # Exclude sensitive fields from response
    model_config = ConfigDict(
        from_attributes=True,
        validate_assignment=True,
        use_enum_values=True,
        json_encoders={
            datetime: lambda v: v.isoformat()
        }
    )


class UserLogin(BaseModel):
    """User login model."""
    email: str = Field(..., description="User email address")
    password: str = Field(..., description="User password")
    remember_me: bool = Field(default=False, description="Remember user session")
    
    # Pydantic v2 Configuration
    model_config = ConfigDict(
        validate_assignment=True,
        json_encoders={
            datetime: lambda v: v.isoformat()
        }
    )
    
    @field_validator('email')
    @classmethod
    def validate_email(cls, v: str) -> str:
        """Validate email format."""
        import re
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not re.match(pattern, v):
            raise ValueError('Invalid email format')
        return v.lower()


class UserProfile(BaseModel):
    """User profile model for public display."""
    user_id: str = Field(..., description="User unique identifier")
    name: str = Field(..., description="User full name")
    role: UserRole = Field(..., description="User role")
    avatar_url: Optional[str] = Field(None, description="User avatar URL")
    department: Optional[str] = Field(None, description="User department")
    grade_level: Optional[str] = Field(None, description="User grade level")
    
    # Pydantic v2 Configuration
    model_config = ConfigDict(
        from_attributes=True,
        validate_assignment=True,
        use_enum_values=True,
        json_encoders={
            datetime: lambda v: v.isoformat()
        }
    )


class UserStats(BaseModel):
    """User statistics model."""
    user_id: str = Field(..., description="User unique identifier")
    total_logins: int = Field(default=0, description="Total login count")
    last_login: Optional[datetime] = Field(None, description="Last login timestamp")
    courses_enrolled: int = Field(default=0, description="Number of enrolled courses")
    assignments_completed: int = Field(default=0, description="Number of completed assignments")
    average_grade: Optional[float] = Field(None, description="Average grade")
    
    # Pydantic v2 Configuration
    model_config = ConfigDict(
        from_attributes=True,
        validate_assignment=True,
        use_enum_values=True,
        json_encoders={
            datetime: lambda v: v.isoformat()
        }
    )


class UserSearch(BaseModel):
    """User search model."""
    query: str = Field(..., min_length=1, description="Search query")
    role: Optional[UserRole] = Field(None, description="Filter by role")
    status: Optional[UserStatus] = Field(None, description="Filter by status")
    department: Optional[str] = Field(None, description="Filter by department")
    limit: int = Field(default=20, ge=1, le=100, description="Results limit")
    offset: int = Field(default=0, ge=0, description="Results offset")
    
    # Pydantic v2 Configuration
    model_config = ConfigDict(
        validate_assignment=True,
        use_enum_values=True
    )
    
    @field_validator('query')
    @classmethod
    def validate_query(cls, v: str) -> str:
        """Validate search query."""
        if not v.strip():
            raise ValueError('Search query cannot be empty')
        return v.strip()