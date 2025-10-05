"""
Modelo de usuario
"""
from enum import Enum
from pydantic import BaseModel, EmailStr


class UserRole(str, Enum):
    """Roles de usuario"""
    ADMIN = "admin"
    COORDINATOR = "coordinator"
    TEACHER = "teacher"
    STUDENT = "student"


class User(BaseModel):
    """Usuario del sistema"""
    id: str
    email: EmailStr
    name: str
    role: UserRole
    is_active: bool = True
    
    model_config = {"use_enum_values": True}


class UserInDB(User):
    """Usuario en base de datos"""
    hashed_password: str
