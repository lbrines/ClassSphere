"""
User model definitions for ClassSphere.
"""
from datetime import datetime
from typing import Optional
from enum import Enum
from pydantic import BaseModel, EmailStr, Field, ConfigDict


class UserRole(str, Enum):
    """User roles in hierarchical order."""
    ADMIN = "admin"
    COORDINATOR = "coordinator"
    TEACHER = "teacher"
    STUDENT = "student"


class UserBase(BaseModel):
    """Base user model."""
    email: EmailStr
    name: str = Field(..., min_length=1, max_length=255)
    role: UserRole = UserRole.STUDENT
    is_active: bool = True


class UserCreate(UserBase):
    """User creation model."""
    password: str = Field(..., min_length=8, max_length=255)


class UserUpdate(BaseModel):
    """User update model."""
    name: Optional[str] = Field(None, min_length=1, max_length=255)
    role: Optional[UserRole] = None
    is_active: Optional[bool] = None


class User(UserBase):
    """User model with ID and timestamps."""
    id: str = Field(..., description="User unique identifier")
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class UserInDB(User):
    """User model with hashed password (for internal use)."""
    hashed_password: str


class UserResponse(BaseModel):
    """User response model (without sensitive data)."""
    id: str
    email: EmailStr
    name: str
    role: UserRole
    is_active: bool
    created_at: datetime
    updated_at: datetime