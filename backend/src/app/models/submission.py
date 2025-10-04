"""
Submission models using Pydantic v2 with ConfigDict.
"""
from datetime import datetime
from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field, field_validator, ConfigDict
from enum import Enum


class SubmissionStatus(str, Enum):
    """Submission status enum."""
    DRAFT = "draft"
    SUBMITTED = "submitted"
    LATE = "late"
    GRADED = "graded"
    RETURNED = "returned"


class SubmissionType(str, Enum):
    """Submission type enum."""
    TEXT = "text"
    FILE = "file"
    URL = "url"
    MULTIPLE_CHOICE = "multiple_choice"
    CODE = "code"


class SubmissionBase(BaseModel):
    """Base submission model."""
    assignment_id: str = Field(..., description="Assignment ID")
    student_id: str = Field(..., description="Student user ID")
    submission_type: SubmissionType = Field(default=SubmissionType.TEXT, description="Submission type")
    status: SubmissionStatus = Field(default=SubmissionStatus.DRAFT, description="Submission status")
    
    # Content fields
    content: Optional[str] = Field(default=None, max_length=10000, description="Submission content")
    files: Optional[List[str]] = Field(default=None, description="File URLs")
    urls: Optional[List[str]] = Field(default=None, description="URL submissions")
    
    # Grading fields
    grade: Optional[float] = Field(default=None, ge=0, le=1000, description="Submission grade")
    max_points: Optional[float] = Field(default=None, ge=0, le=1000, description="Maximum points")
    feedback: Optional[str] = Field(default=None, max_length=2000, description="Instructor feedback")
    graded_by: Optional[str] = Field(default=None, description="Grader user ID")
    graded_at: Optional[datetime] = Field(default=None, description="Grading timestamp")
    
    # Timing fields
    submitted_at: Optional[datetime] = Field(default=None, description="Submission timestamp")
    due_date: Optional[datetime] = Field(default=None, description="Assignment due date")
    is_late: bool = Field(default=False, description="Is submission late")
    late_penalty: Optional[float] = Field(default=None, ge=0, le=100, description="Late penalty percentage")
    
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
    
    @field_validator('grade')
    @classmethod
    def validate_grade(cls, v: Optional[float], info) -> Optional[float]:
        """Validate grade is not greater than max points."""
        if v is not None:
            max_points = info.data.get('max_points')
            if max_points is not None and v > max_points:
                raise ValueError('Grade cannot exceed maximum points')
        return v
    
    @field_validator('submitted_at')
    @classmethod
    def validate_submitted_at(cls, v: Optional[datetime], info) -> Optional[datetime]:
        """Validate submission timestamp."""
        if v is not None:
            due_date = info.data.get('due_date')
            if due_date is not None:
                is_late = v > due_date
                info.data['is_late'] = is_late
        return v
    
    @field_validator('files')
    @classmethod
    def validate_files(cls, v: Optional[List[str]]) -> Optional[List[str]]:
        """Validate file URLs."""
        if v is not None:
            # Basic URL validation
            import re
            url_pattern = re.compile(
                r'^https?://'  # http:// or https://
                r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+[A-Z]{2,6}\.?|'  # domain...
                r'localhost|'  # localhost...
                r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'  # ...or ip
                r'(?::\d+)?'  # optional port
                r'(?:/?|[/?]\S+)$', re.IGNORECASE)
            
            for file_url in v:
                if not url_pattern.match(file_url):
                    raise ValueError(f'Invalid file URL: {file_url}')
        return v


class SubmissionCreate(SubmissionBase):
    """Submission creation model."""
    pass


class SubmissionUpdate(BaseModel):
    """Submission update model."""
    content: Optional[str] = Field(None, max_length=10000, description="Submission content")
    files: Optional[List[str]] = Field(None, description="File URLs")
    urls: Optional[List[str]] = Field(None, description="URL submissions")
    status: Optional[SubmissionStatus] = Field(None, description="Submission status")
    grade: Optional[float] = Field(None, ge=0, le=1000, description="Submission grade")
    feedback: Optional[str] = Field(None, max_length=2000, description="Instructor feedback")
    graded_by: Optional[str] = Field(None, description="Grader user ID")
    
    # Pydantic v2 Configuration
    model_config = ConfigDict(
        from_attributes=True,
        validate_assignment=True,
        use_enum_values=True,
        json_encoders={
            datetime: lambda v: v.isoformat()
        }
    )


class SubmissionResponse(SubmissionBase):
    """Submission response model."""
    id: str = Field(..., description="Submission unique identifier")
    
    # Assignment information
    assignment_title: Optional[str] = Field(None, description="Assignment title")
    assignment_due_date: Optional[datetime] = Field(None, description="Assignment due date")
    
    # Student information
    student_name: Optional[str] = Field(None, description="Student name")
    student_email: Optional[str] = Field(None, description="Student email")
    
    # Calculated fields
    percentage: Optional[float] = Field(None, ge=0, le=100, description="Grade percentage")
    final_grade: Optional[float] = Field(None, ge=0, le=1000, description="Final grade after penalties")
    
    # Pydantic v2 Configuration
    model_config = ConfigDict(
        from_attributes=True,
        validate_assignment=True,
        use_enum_values=True,
        json_encoders={
            datetime: lambda v: v.isoformat()
        }
    )


class SubmissionList(BaseModel):
    """Submission list model."""
    submissions: List[SubmissionResponse] = Field(..., description="List of submissions")
    total: int = Field(..., description="Total number of submissions")
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


class SubmissionSearch(BaseModel):
    """Submission search model."""
    assignment_id: Optional[str] = Field(None, description="Assignment filter")
    student_id: Optional[str] = Field(None, description="Student filter")
    status: Optional[SubmissionStatus] = Field(None, description="Status filter")
    submission_type: Optional[SubmissionType] = Field(None, description="Type filter")
    graded: Optional[bool] = Field(None, description="Graded filter")
    late: Optional[bool] = Field(None, description="Late submission filter")
    submitted_after: Optional[datetime] = Field(None, description="Submission date filter (after)")
    submitted_before: Optional[datetime] = Field(None, description="Submission date filter (before)")
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


class SubmissionStats(BaseModel):
    """Submission statistics model."""
    assignment_id: Optional[str] = Field(None, description="Assignment ID (if assignment-specific)")
    student_id: Optional[str] = Field(None, description="Student ID (if student-specific)")
    total_submissions: int = Field(default=0, description="Total submissions")
    submitted_submissions: int = Field(default=0, description="Submitted submissions")
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


class BulkSubmission(BaseModel):
    """Bulk submission model."""
    assignment_id: str = Field(..., description="Assignment ID")
    student_ids: List[str] = Field(..., min_items=1, max_items=100, description="List of student IDs")
    content: Optional[str] = Field(None, max_length=10000, description="Submission content")
    files: Optional[List[str]] = Field(None, description="File URLs")
    urls: Optional[List[str]] = Field(None, description="URL submissions")
    
    # Pydantic v2 Configuration
    model_config = ConfigDict(
        from_attributes=True,
        validate_assignment=True,
        use_enum_values=True,
        json_encoders={
            datetime: lambda v: v.isoformat()
        }
    )
    
    @field_validator('student_ids')
    @classmethod
    def validate_student_ids(cls, v: List[str]) -> List[str]:
        """Validate student IDs are unique."""
        if len(v) != len(set(v)):
            raise ValueError('Student IDs must be unique')
        return v