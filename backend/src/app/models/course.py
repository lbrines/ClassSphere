"""
Course models using Pydantic v2 with ConfigDict.
"""
from datetime import datetime
from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field, field_validator, ConfigDict
from enum import Enum


class CourseStatus(str, Enum):
    """Course status enum."""
    DRAFT = "draft"
    ACTIVE = "active"
    ARCHIVED = "archived"
    COMPLETED = "completed"


class CourseLevel(str, Enum):
    """Course level enum."""
    BEGINNER = "beginner"
    INTERMEDIATE = "intermediate"
    ADVANCED = "advanced"


class CourseBase(BaseModel):
    """Base course model."""
    title: str = Field(..., min_length=3, max_length=200, description="Course title")
    description: str = Field(..., min_length=10, max_length=1000, description="Course description")
    code: str = Field(..., min_length=3, max_length=20, description="Course code")
    level: CourseLevel = Field(default=CourseLevel.BEGINNER, description="Course level")
    status: CourseStatus = Field(default=CourseStatus.DRAFT, description="Course status")
    
    # Optional fields
    instructor_id: Optional[str] = Field(default=None, description="Instructor user ID")
    max_students: Optional[int] = Field(default=None, ge=1, le=1000, description="Maximum number of students")
    credits: Optional[int] = Field(default=None, ge=1, le=10, description="Course credits")
    department: Optional[str] = Field(default=None, max_length=100, description="Department")
    
    # Dates
    start_date: Optional[datetime] = Field(default=None, description="Course start date")
    end_date: Optional[datetime] = Field(default=None, description="Course end date")
    
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
        """Validate course title."""
        if not v.strip():
            raise ValueError('Course title cannot be empty')
        return v.strip()
    
    @field_validator('code')
    @classmethod
    def validate_code(cls, v: str) -> str:
        """Validate course code format."""
        if not v.strip():
            raise ValueError('Course code cannot be empty')
        # Course code should be uppercase and alphanumeric
        code = v.strip().upper()
        if not code.replace('-', '').replace('_', '').isalnum():
            raise ValueError('Course code must be alphanumeric (with - or _ allowed)')
        return code
    
    @field_validator('end_date')
    @classmethod
    def validate_end_date(cls, v: Optional[datetime], info) -> Optional[datetime]:
        """Validate end date is after start date."""
        if v is not None:
            start_date = info.data.get('start_date')
            if start_date is not None and v <= start_date:
                raise ValueError('End date must be after start date')
        return v


class CourseCreate(CourseBase):
    """Course creation model."""
    pass


class CourseUpdate(BaseModel):
    """Course update model."""
    title: Optional[str] = Field(None, min_length=3, max_length=200, description="Course title")
    description: Optional[str] = Field(None, min_length=10, max_length=1000, description="Course description")
    code: Optional[str] = Field(None, min_length=3, max_length=20, description="Course code")
    level: Optional[CourseLevel] = Field(None, description="Course level")
    status: Optional[CourseStatus] = Field(None, description="Course status")
    instructor_id: Optional[str] = Field(None, description="Instructor user ID")
    max_students: Optional[int] = Field(None, ge=1, le=1000, description="Maximum number of students")
    credits: Optional[int] = Field(None, ge=1, le=10, description="Course credits")
    department: Optional[str] = Field(None, max_length=100, description="Department")
    start_date: Optional[datetime] = Field(None, description="Course start date")
    end_date: Optional[datetime] = Field(None, description="Course end date")
    
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
        """Validate course title."""
        if v is not None and not v.strip():
            raise ValueError('Course title cannot be empty')
        return v.strip() if v else v
    
    @field_validator('code')
    @classmethod
    def validate_code(cls, v: Optional[str]) -> Optional[str]:
        """Validate course code format."""
        if v is not None:
            if not v.strip():
                raise ValueError('Course code cannot be empty')
            # Course code should be uppercase and alphanumeric
            code = v.strip().upper()
            if not code.replace('-', '').replace('_', '').isalnum():
                raise ValueError('Course code must be alphanumeric (with - or _ allowed)')
            return code
        return v


class CourseResponse(CourseBase):
    """Course response model."""
    id: str = Field(..., description="Course unique identifier")
    student_count: int = Field(default=0, description="Number of enrolled students")
    assignment_count: int = Field(default=0, description="Number of assignments")
    
    # Pydantic v2 Configuration
    model_config = ConfigDict(
        from_attributes=True,
        validate_assignment=True,
        use_enum_values=True,
        json_encoders={
            datetime: lambda v: v.isoformat()
        }
    )


class CourseList(BaseModel):
    """Course list model."""
    courses: List[CourseResponse] = Field(..., description="List of courses")
    total: int = Field(..., description="Total number of courses")
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


class CourseSearch(BaseModel):
    """Course search model."""
    query: Optional[str] = Field(None, max_length=200, description="Search query")
    level: Optional[CourseLevel] = Field(None, description="Course level filter")
    status: Optional[CourseStatus] = Field(None, description="Course status filter")
    department: Optional[str] = Field(None, max_length=100, description="Department filter")
    instructor_id: Optional[str] = Field(None, description="Instructor filter")
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


class CourseStats(BaseModel):
    """Course statistics model."""
    course_id: str = Field(..., description="Course unique identifier")
    total_students: int = Field(default=0, description="Total enrolled students")
    active_students: int = Field(default=0, description="Active students")
    completed_assignments: int = Field(default=0, description="Completed assignments")
    average_grade: Optional[float] = Field(None, ge=0, le=100, description="Average grade")
    completion_rate: Optional[float] = Field(None, ge=0, le=100, description="Completion rate percentage")
    
    # Pydantic v2 Configuration
    model_config = ConfigDict(
        from_attributes=True,
        validate_assignment=True,
        json_encoders={
            datetime: lambda v: v.isoformat()
        }
    )