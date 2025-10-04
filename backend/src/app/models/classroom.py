"""Google Classroom models with Pydantic v2."""

from datetime import datetime
from typing import Optional, List, Dict, Any
from enum import Enum

from pydantic import BaseModel, ConfigDict, field_validator, field_serializer, AnyUrl


class CourseState(str, Enum):
    """Course state enumeration."""
    COURSE_STATE_UNSPECIFIED = "COURSE_STATE_UNSPECIFIED"
    ACTIVE = "ACTIVE"
    ARCHIVED = "ARCHIVED"
    PROVISIONED = "PROVISIONED"
    DECLINED = "DECLINED"
    SUSPENDED = "SUSPENDED"


class StudentRole(str, Enum):
    """Student role enumeration."""
    STUDENT = "STUDENT"
    TEACHER = "TEACHER"


class CourseBase(BaseModel):
    """Base course model."""

    name: str
    section: Optional[str] = None
    description: Optional[str] = None
    description_heading: Optional[str] = None
    room: Optional[str] = None
    owner_id: str
    course_state: CourseState = CourseState.ACTIVE

    model_config = ConfigDict(
        from_attributes=True,
        str_strip_whitespace=True,
        validate_assignment=True,
        extra="allow"  # Allow extra fields for Google API compatibility
    )

    @field_validator("name")
    @classmethod
    def validate_name(cls, v: str) -> str:
        """Validate course name."""
        if not v or not v.strip():
            raise ValueError("Course name cannot be empty")
        if len(v.strip()) > 750:  # Google Classroom limit
            raise ValueError("Course name must be less than 750 characters")
        return v.strip()

    @field_validator("section")
    @classmethod
    def validate_section(cls, v: Optional[str]) -> Optional[str]:
        """Validate section name."""
        if v is None:
            return v
        if len(v.strip()) > 2800:  # Google Classroom limit
            raise ValueError("Section must be less than 2800 characters")
        return v.strip() if v.strip() else None


class CourseCreate(CourseBase):
    """Course creation model."""

    enrollment_code: Optional[str] = None

    @field_validator("enrollment_code")
    @classmethod
    def validate_enrollment_code(cls, v: Optional[str]) -> Optional[str]:
        """Validate enrollment code."""
        if v is None:
            return v
        # Enrollment codes are typically 6-7 characters
        if len(v.strip()) < 6 or len(v.strip()) > 7:
            raise ValueError("Enrollment code must be 6-7 characters")
        return v.strip().upper()


class CourseUpdate(BaseModel):
    """Course update model."""

    name: Optional[str] = None
    section: Optional[str] = None
    description: Optional[str] = None
    description_heading: Optional[str] = None
    room: Optional[str] = None
    course_state: Optional[CourseState] = None

    model_config = ConfigDict(
        from_attributes=True,
        str_strip_whitespace=True,
        validate_assignment=True,
        extra="allow"
    )


class CourseResponse(CourseBase):
    """Course response model."""

    id: str
    creation_time: Optional[datetime] = None
    update_time: Optional[datetime] = None
    enrollment_code: Optional[str] = None
    calendar_id: Optional[str] = None
    teacher_folder: Optional[Dict[str, Any]] = None
    guardiansEnabled: Optional[bool] = None

    model_config = ConfigDict(
        from_attributes=True,
        extra="allow"
    )

    @field_serializer('creation_time', 'update_time', when_used='json')
    def serialize_datetime(self, value: Optional[datetime]) -> Optional[str]:
        """Serialize datetime to ISO format."""
        return value.isoformat() if value else None


class StudentBase(BaseModel):
    """Base student model."""

    course_id: str
    user_id: str
    profile: Optional[Dict[str, Any]] = None

    model_config = ConfigDict(
        from_attributes=True,
        extra="allow"
    )


class StudentResponse(StudentBase):
    """Student response model."""

    student_id: Optional[str] = None  # Google user ID
    full_name: Optional[str] = None
    email_address: Optional[str] = None
    photo_url: Optional[AnyUrl] = None

    model_config = ConfigDict(
        from_attributes=True,
        extra="allow"
    )


class TeacherBase(BaseModel):
    """Base teacher model."""

    course_id: str
    user_id: str

    model_config = ConfigDict(
        from_attributes=True,
        extra="allow"
    )


class TeacherResponse(TeacherBase):
    """Teacher response model."""

    teacher_id: Optional[str] = None  # Google user ID
    full_name: Optional[str] = None
    email_address: Optional[str] = None
    photo_url: Optional[AnyUrl] = None

    model_config = ConfigDict(
        from_attributes=True,
        extra="allow"
    )


class CourseWorkType(str, Enum):
    """Course work type enumeration."""
    COURSE_WORK_TYPE_UNSPECIFIED = "COURSE_WORK_TYPE_UNSPECIFIED"
    ASSIGNMENT = "ASSIGNMENT"
    SHORT_ANSWER_QUESTION = "SHORT_ANSWER_QUESTION"
    MULTIPLE_CHOICE_QUESTION = "MULTIPLE_CHOICE_QUESTION"


class CourseWorkState(str, Enum):
    """Course work state enumeration."""
    COURSE_WORK_STATE_UNSPECIFIED = "COURSE_WORK_STATE_UNSPECIFIED"
    PUBLISHED = "PUBLISHED"
    DRAFT = "DRAFT"
    DELETED = "DELETED"


class CourseWorkBase(BaseModel):
    """Base course work model."""

    course_id: str
    title: str
    description: Optional[str] = None
    work_type: CourseWorkType = CourseWorkType.ASSIGNMENT
    state: CourseWorkState = CourseWorkState.DRAFT
    max_points: Optional[float] = None

    model_config = ConfigDict(
        from_attributes=True,
        str_strip_whitespace=True,
        validate_assignment=True,
        extra="allow"
    )

    @field_validator("title")
    @classmethod
    def validate_title(cls, v: str) -> str:
        """Validate course work title."""
        if not v or not v.strip():
            raise ValueError("Course work title cannot be empty")
        if len(v.strip()) > 3000:  # Google Classroom limit
            raise ValueError("Title must be less than 3000 characters")
        return v.strip()

    @field_validator("max_points")
    @classmethod
    def validate_max_points(cls, v: Optional[float]) -> Optional[float]:
        """Validate max points."""
        if v is None:
            return v
        if v < 0:
            raise ValueError("Max points cannot be negative")
        if v > 10000:  # Reasonable upper limit
            raise ValueError("Max points cannot exceed 10000")
        return v


class CourseWorkResponse(CourseWorkBase):
    """Course work response model."""

    id: str
    creation_time: Optional[datetime] = None
    update_time: Optional[datetime] = None
    due_date: Optional[datetime] = None
    due_time: Optional[str] = None
    materials: Optional[List[Dict[str, Any]]] = None

    model_config = ConfigDict(
        from_attributes=True,
        extra="allow"
    )
    
    @field_serializer('creation_time', 'update_time', 'due_date')
    def serialize_datetime(self, value: Optional[datetime]) -> Optional[str]:
        """Serialize datetime fields to ISO format."""
        return value.isoformat() if value else None


class SubmissionState(str, Enum):
    """Submission state enumeration."""
    SUBMISSION_STATE_UNSPECIFIED = "SUBMISSION_STATE_UNSPECIFIED"
    NEW = "NEW"
    CREATED = "CREATED"
    TURNED_IN = "TURNED_IN"
    RETURNED = "RETURNED"
    RECLAIMED_BY_STUDENT = "RECLAIMED_BY_STUDENT"


class StudentSubmissionBase(BaseModel):
    """Base student submission model."""

    course_id: str
    course_work_id: str
    user_id: str
    state: SubmissionState = SubmissionState.NEW

    model_config = ConfigDict(
        from_attributes=True,
        extra="allow"
    )


class StudentSubmissionResponse(StudentSubmissionBase):
    """Student submission response model."""

    id: str
    creation_time: Optional[datetime] = None
    update_time: Optional[datetime] = None
    late: Optional[bool] = None
    draft_grade: Optional[float] = None
    assigned_grade: Optional[float] = None
    submission_history: Optional[List[Dict[str, Any]]] = None

    model_config = ConfigDict(
        from_attributes=True,
        extra="allow"
    )
    
    @field_serializer('creation_time', 'update_time')
    def serialize_datetime(self, value: Optional[datetime]) -> Optional[str]:
        """Serialize datetime fields to ISO format."""
        return value.isoformat() if value else None


class ClassroomMetrics(BaseModel):
    """Classroom metrics model."""

    course_id: str
    total_students: int = 0
    total_teachers: int = 0
    total_assignments: int = 0
    total_submissions: int = 0
    completion_rate: float = 0.0
    average_grade: Optional[float] = None
    active_students: int = 0
    last_activity: Optional[datetime] = None

    model_config = ConfigDict(
        from_attributes=True
    )
    
    @field_serializer('last_activity')
    def serialize_datetime(self, value: Optional[datetime]) -> Optional[str]:
        """Serialize datetime fields to ISO format."""
        return value.isoformat() if value else None

    @field_validator("completion_rate")
    @classmethod
    def validate_completion_rate(cls, v: float) -> float:
        """Validate completion rate."""
        if v < 0.0 or v > 100.0:
            raise ValueError("Completion rate must be between 0 and 100")
        return v

    @field_validator("average_grade")
    @classmethod
    def validate_average_grade(cls, v: Optional[float]) -> Optional[float]:
        """Validate average grade."""
        if v is None:
            return v
        if v < 0:
            raise ValueError("Average grade cannot be negative")
        return v


class ClassroomSyncStatus(BaseModel):
    """Classroom sync status model."""

    course_id: str
    last_sync: Optional[datetime] = None
    sync_status: str = "pending"
    error_message: Optional[str] = None
    records_synced: int = 0

    model_config = ConfigDict(
        from_attributes=True
    )
    
    @field_serializer('last_sync')
    def serialize_datetime(self, value: Optional[datetime]) -> Optional[str]:
        """Serialize datetime fields to ISO format."""
        return value.isoformat() if value else None