"""
Assignment models using Pydantic v2 with ConfigDict.
"""
from datetime import datetime
from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field, field_validator, ConfigDict
from enum import Enum


class AssignmentType(str, Enum):
    """Assignment type enum."""
    HOMEWORK = "homework"
    PROJECT = "project"
    EXAM = "exam"
    QUIZ = "quiz"
    ESSAY = "essay"
    PRESENTATION = "presentation"


class AssignmentStatus(str, Enum):
    """Assignment status enum."""
    DRAFT = "draft"
    PUBLISHED = "published"
    CLOSED = "closed"
    GRADED = "graded"


class AssignmentBase(BaseModel):
    """Base assignment model."""
    title: str = Field(..., min_length=3, max_length=200, description="Assignment title")
    description: str = Field(..., min_length=10, max_length=2000, description="Assignment description")
    assignment_type: AssignmentType = Field(default=AssignmentType.HOMEWORK, description="Assignment type")
    status: AssignmentStatus = Field(default=AssignmentStatus.DRAFT, description="Assignment status")
    
    # Required fields
    course_id: str = Field(..., description="Course ID")
    instructor_id: str = Field(..., description="Instructor user ID")
    due_date: datetime = Field(..., description="Assignment due date")
    max_points: float = Field(..., ge=0, le=1000, description="Maximum points")
    
    # Optional fields
    instructions: Optional[str] = Field(default=None, max_length=5000, description="Assignment instructions")
    attachments: Optional[List[str]] = Field(default=None, description="Attachment URLs")
    rubric: Optional[Dict[str, Any]] = Field(default=None, description="Grading rubric")
    late_submission_allowed: bool = Field(default=True, description="Allow late submissions")
    late_penalty_percentage: Optional[float] = Field(default=None, ge=0, le=100, description="Late penalty percentage")
    
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
    
    @field_validator('title')
    @classmethod
    def validate_title(cls, v: str) -> str:
        """Validate assignment title."""
        if not v.strip():
            raise ValueError('Assignment title cannot be empty')
        return v.strip()
    
    @field_validator('due_date')
    @classmethod
    def validate_due_date(cls, v: datetime) -> datetime:
        """Validate due date is in the future."""
        if v <= datetime.utcnow():
            raise ValueError('Due date must be in the future')
        return v
    
    @field_validator('late_penalty_percentage')
    @classmethod
    def validate_late_penalty(cls, v: Optional[float], info) -> Optional[float]:
        """Validate late penalty percentage."""
        if v is not None:
            late_allowed = info.data.get('late_submission_allowed', True)
            if not late_allowed and v > 0:
                raise ValueError('Late penalty cannot be set when late submissions are not allowed')
        return v


class AssignmentCreate(AssignmentBase):
    """Assignment creation model."""
    pass


class AssignmentUpdate(BaseModel):
    """Assignment update model."""
    title: Optional[str] = Field(None, min_length=3, max_length=200, description="Assignment title")
    description: Optional[str] = Field(None, min_length=10, max_length=2000, description="Assignment description")
    assignment_type: Optional[AssignmentType] = Field(None, description="Assignment type")
    status: Optional[AssignmentStatus] = Field(None, description="Assignment status")
    due_date: Optional[datetime] = Field(None, description="Assignment due date")
    max_points: Optional[float] = Field(None, ge=0, le=1000, description="Maximum points")
    instructions: Optional[str] = Field(None, max_length=5000, description="Assignment instructions")
    attachments: Optional[List[str]] = Field(None, description="Attachment URLs")
    rubric: Optional[Dict[str, Any]] = Field(None, description="Grading rubric")
    late_submission_allowed: Optional[bool] = Field(None, description="Allow late submissions")
    late_penalty_percentage: Optional[float] = Field(None, ge=0, le=100, description="Late penalty percentage")
    
    # Pydantic v2 Configuration
    model_config = ConfigDict(
        from_attributes=True,
        validate_assignment=True,
        use_enum_values=True,
        json_encoders={
            datetime: lambda v: v.isoformat()
        }
    )
    
    @field_validator('title')
    @classmethod
    def validate_title(cls, v: Optional[str]) -> Optional[str]:
        """Validate assignment title."""
        if v is not None and not v.strip():
            raise ValueError('Assignment title cannot be empty')
        return v.strip() if v else v
    
    @field_validator('due_date')
    @classmethod
    def validate_due_date(cls, v: Optional[datetime]) -> Optional[datetime]:
        """Validate due date is in the future."""
        if v is not None and v <= datetime.utcnow():
            raise ValueError('Due date must be in the future')
        return v


class AssignmentResponse(AssignmentBase):
    """Assignment response model."""
    id: str = Field(..., description="Assignment unique identifier")
    submission_count: int = Field(default=0, description="Number of submissions")
    graded_count: int = Field(default=0, description="Number of graded submissions")
    average_grade: Optional[float] = Field(None, ge=0, le=1000, description="Average grade")
    
    # Pydantic v2 Configuration
    model_config = ConfigDict(
        from_attributes=True,
        validate_assignment=True,
        use_enum_values=True,
        json_encoders={
            datetime: lambda v: v.isoformat()
        }
    )


class AssignmentList(BaseModel):
    """Assignment list model."""
    assignments: List[AssignmentResponse] = Field(..., description="List of assignments")
    total: int = Field(..., description="Total number of assignments")
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


class AssignmentSearch(BaseModel):
    """Assignment search model."""
    query: Optional[str] = Field(None, max_length=200, description="Search query")
    course_id: Optional[str] = Field(None, description="Course filter")
    assignment_type: Optional[AssignmentType] = Field(None, description="Assignment type filter")
    status: Optional[AssignmentStatus] = Field(None, description="Assignment status filter")
    instructor_id: Optional[str] = Field(None, description="Instructor filter")
    due_before: Optional[datetime] = Field(None, description="Due date filter (before)")
    due_after: Optional[datetime] = Field(None, description="Due date filter (after)")
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


class AssignmentStats(BaseModel):
    """Assignment statistics model."""
    assignment_id: str = Field(..., description="Assignment unique identifier")
    total_submissions: int = Field(default=0, description="Total submissions")
    on_time_submissions: int = Field(default=0, description="On-time submissions")
    late_submissions: int = Field(default=0, description="Late submissions")
    graded_submissions: int = Field(default=0, description="Graded submissions")
    average_grade: Optional[float] = Field(None, ge=0, le=1000, description="Average grade")
    completion_rate: Optional[float] = Field(None, ge=0, le=100, description="Completion rate percentage")
    
    # Pydantic v2 Configuration
    model_config = ConfigDict(
        from_attributes=True,
        validate_assignment=True,
        json_encoders={
            datetime: lambda v: v.isoformat()
        }
    )