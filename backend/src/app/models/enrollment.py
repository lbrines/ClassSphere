"""
Enrollment models using Pydantic v2 with ConfigDict.
"""
from datetime import datetime
from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field, field_validator, ConfigDict
from enum import Enum


class EnrollmentStatus(str, Enum):
    """Enrollment status enum."""
    PENDING = "pending"
    ACTIVE = "active"
    COMPLETED = "completed"
    DROPPED = "dropped"
    SUSPENDED = "suspended"


class EnrollmentRole(str, Enum):
    """Enrollment role enum."""
    STUDENT = "student"
    TEACHER_ASSISTANT = "teacher_assistant"
    OBSERVER = "observer"


class EnrollmentBase(BaseModel):
    """Base enrollment model."""
    user_id: str = Field(..., description="User ID")
    course_id: str = Field(..., description="Course ID")
    role: EnrollmentRole = Field(default=EnrollmentRole.STUDENT, description="Enrollment role")
    status: EnrollmentStatus = Field(default=EnrollmentStatus.PENDING, description="Enrollment status")
    
    # Optional fields
    enrollment_date: Optional[datetime] = Field(default_factory=datetime.utcnow, description="Enrollment date")
    completion_date: Optional[datetime] = Field(default=None, description="Completion date")
    final_grade: Optional[float] = Field(default=None, ge=0, le=100, description="Final grade")
    credits_earned: Optional[int] = Field(default=None, ge=0, le=10, description="Credits earned")
    
    # Metadata
    created_at: Optional[datetime] = Field(default_factory=datetime.utcnow, description="Creation timestamp")
    updated_at: Optional[datetime] = Field(default_factory=datetime.utcnow, description="Last update timestamp")
    
    # Pydantic v2 Configuration
    model_config = ConfigDict(
        from_attributes=True,
        validate_assignment=True,
        use_enum_values=True,
        json_encoders={
            datetime: lambda v: v.isoformat()
        }
    )
    
    @field_validator('completion_date')
    @classmethod
    def validate_completion_date(cls, v: Optional[datetime], info) -> Optional[datetime]:
        """Validate completion date is after enrollment date."""
        if v is not None:
            enrollment_date = info.data.get('enrollment_date')
            if enrollment_date is not None and v < enrollment_date:
                raise ValueError('Completion date must be after enrollment date')
        return v


class EnrollmentCreate(EnrollmentBase):
    """Enrollment creation model."""
    pass


class EnrollmentUpdate(BaseModel):
    """Enrollment update model."""
    role: Optional[EnrollmentRole] = Field(None, description="Enrollment role")
    status: Optional[EnrollmentStatus] = Field(None, description="Enrollment status")
    completion_date: Optional[datetime] = Field(None, description="Completion date")
    final_grade: Optional[float] = Field(None, ge=0, le=100, description="Final grade")
    credits_earned: Optional[int] = Field(None, ge=0, le=10, description="Credits earned")
    
    # Pydantic v2 Configuration
    model_config = ConfigDict(
        from_attributes=True,
        validate_assignment=True,
        use_enum_values=True,
        json_encoders={
            datetime: lambda v: v.isoformat()
        }
    )


class EnrollmentResponse(EnrollmentBase):
    """Enrollment response model."""
    id: str = Field(..., description="Enrollment unique identifier")
    
    # User information
    user_name: Optional[str] = Field(None, description="User name")
    user_email: Optional[str] = Field(None, description="User email")
    
    # Course information
    course_title: Optional[str] = Field(None, description="Course title")
    course_code: Optional[str] = Field(None, description="Course code")
    
    # Statistics
    assignments_completed: int = Field(default=0, description="Number of completed assignments")
    assignments_total: int = Field(default=0, description="Total number of assignments")
    average_grade: Optional[float] = Field(None, ge=0, le=100, description="Average grade")
    
    # Pydantic v2 Configuration
    model_config = ConfigDict(
        from_attributes=True,
        validate_assignment=True,
        use_enum_values=True,
        json_encoders={
            datetime: lambda v: v.isoformat()
        }
    )


class EnrollmentList(BaseModel):
    """Enrollment list model."""
    enrollments: List[EnrollmentResponse] = Field(..., description="List of enrollments")
    total: int = Field(..., description="Total number of enrollments")
    page: int = Field(..., ge=1, description="Current page number")
    size: int = Field(..., ge=1, le=100, description="Page size")
    
    # Pydantic v2 Configuration
    model_config = ConfigDict(
        from_attributes=True,
        validate_assignment=True,
        json_encoders={
            datetime: lambda v: v.isoformat()
        }
    )


class EnrollmentSearch(BaseModel):
    """Enrollment search model."""
    user_id: Optional[str] = Field(None, description="User filter")
    course_id: Optional[str] = Field(None, description="Course filter")
    role: Optional[EnrollmentRole] = Field(None, description="Role filter")
    status: Optional[EnrollmentStatus] = Field(None, description="Status filter")
    enrolled_after: Optional[datetime] = Field(None, description="Enrollment date filter (after)")
    enrolled_before: Optional[datetime] = Field(None, description="Enrollment date filter (before)")
    page: int = Field(default=1, ge=1, description="Page number")
    size: int = Field(default=20, ge=1, le=100, description="Page size")
    
    # Pydantic v2 Configuration
    model_config = ConfigDict(
        from_attributes=True,
        validate_assignment=True,
        use_enum_values=True,
        json_encoders={
            datetime: lambda v: v.isoformat()
        }
    )


class EnrollmentStats(BaseModel):
    """Enrollment statistics model."""
    course_id: Optional[str] = Field(None, description="Course ID (if course-specific)")
    user_id: Optional[str] = Field(None, description="User ID (if user-specific)")
    total_enrollments: int = Field(default=0, description="Total enrollments")
    active_enrollments: int = Field(default=0, description="Active enrollments")
    completed_enrollments: int = Field(default=0, description="Completed enrollments")
    dropped_enrollments: int = Field(default=0, description="Dropped enrollments")
    average_completion_rate: Optional[float] = Field(None, ge=0, le=100, description="Average completion rate")
    average_final_grade: Optional[float] = Field(None, ge=0, le=100, description="Average final grade")
    
    # Pydantic v2 Configuration
    model_config = ConfigDict(
        from_attributes=True,
        validate_assignment=True,
        json_encoders={
            datetime: lambda v: v.isoformat()
        }
    )


class BulkEnrollment(BaseModel):
    """Bulk enrollment model."""
    user_ids: List[str] = Field(..., min_items=1, max_items=100, description="List of user IDs to enroll")
    course_id: str = Field(..., description="Course ID")
    role: EnrollmentRole = Field(default=EnrollmentRole.STUDENT, description="Enrollment role")
    status: EnrollmentStatus = Field(default=EnrollmentStatus.ACTIVE, description="Enrollment status")
    
    # Pydantic v2 Configuration
    model_config = ConfigDict(
        from_attributes=True,
        validate_assignment=True,
        use_enum_values=True,
        json_encoders={
            datetime: lambda v: v.isoformat()
        }
    )
    
    @field_validator('user_ids')
    @classmethod
    def validate_user_ids(cls, v: List[str]) -> List[str]:
        """Validate user IDs are unique."""
        if len(v) != len(set(v)):
            raise ValueError('User IDs must be unique')
        return v