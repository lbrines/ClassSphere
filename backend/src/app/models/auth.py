"""
Modelos de autenticación con Pydantic v2
"""
from datetime import datetime
from enum import Enum
from typing import Optional
from pydantic import BaseModel, EmailStr, Field


class UserRole(str, Enum):
    """Roles de usuario con jerarquía"""
    ADMIN = "admin"
    COORDINATOR = "coordinator"
    TEACHER = "teacher"
    STUDENT = "student"


class User(BaseModel):
    """Modelo de usuario"""
    id: int
    email: EmailStr
    first_name: str
    last_name: str
    role: UserRole
    is_active: bool = True
    google_id: Optional[str] = None
    avatar_url: Optional[str] = None
    created_at: datetime
    last_login: Optional[datetime] = None

    class Config:
        from_attributes = True


class UserCreate(BaseModel):
    """Modelo para crear usuario"""
    email: EmailStr
    password: str = Field(..., min_length=8)
    first_name: str = Field(..., min_length=1, max_length=50)
    last_name: str = Field(..., min_length=1, max_length=50)
    role: UserRole = UserRole.STUDENT


class UserLogin(BaseModel):
    """Modelo para login"""
    email: EmailStr
    password: str


class UserUpdate(BaseModel):
    """Modelo para actualizar usuario"""
    first_name: Optional[str] = Field(None, min_length=1, max_length=50)
    last_name: Optional[str] = Field(None, min_length=1, max_length=50)
    role: Optional[UserRole] = None
    is_active: Optional[bool] = None


class Token(BaseModel):
    """Modelo de token JWT"""
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    expires_in: int


class TokenData(BaseModel):
    """Datos del token"""
    user_id: Optional[int] = None
    email: Optional[str] = None
    role: Optional[UserRole] = None


class GoogleOAuthRequest(BaseModel):
    """Request para OAuth de Google"""
    authorization_code: str
    code_verifier: str


class GoogleUserInfo(BaseModel):
    """Información de usuario de Google"""
    google_id: str
    email: EmailStr
    first_name: str
    last_name: str
    avatar_url: Optional[str] = None


class AuthResponse(BaseModel):
    """Respuesta de autenticación"""
    user: User
    token: Token