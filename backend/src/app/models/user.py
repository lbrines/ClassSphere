from sqlalchemy import Column, String, Boolean, DateTime, Enum
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func
from pydantic import BaseModel, EmailStr
from enum import Enum as PyEnum
from typing import Optional
from datetime import datetime
import uuid

Base = declarative_base()

class UserRole(PyEnum):
    ADMIN = "admin"
    COORDINATOR = "coordinador"
    TEACHER = "teacher"
    STUDENT = "estudiante"

class User(Base):
    __tablename__ = "users"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email = Column(String, unique=True, index=True, nullable=False)
    name = Column(String, nullable=False)
    role = Column(Enum(UserRole), nullable=False, default=UserRole.STUDENT)
    google_id = Column(String, unique=True, nullable=True)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    last_login = Column(DateTime(timezone=True), nullable=True)

# Pydantic models
class UserBase(BaseModel):
    email: EmailStr
    name: str
    role: UserRole = UserRole.STUDENT

class UserCreate(UserBase):
    password: str

class UserUpdate(BaseModel):
    name: Optional[str] = None
    role: Optional[UserRole] = None
    is_active: Optional[bool] = None

class UserInDB(UserBase):
    id: uuid.UUID
    google_id: Optional[str] = None
    is_active: bool
    created_at: datetime
    updated_at: Optional[datetime] = None
    last_login: Optional[datetime] = None
    
    class Config:
        from_attributes = True

class User(UserInDB):
    pass
