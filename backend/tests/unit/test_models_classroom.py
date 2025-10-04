"""Tests for Google Classroom models with Pydantic v2."""

import pytest
from datetime import datetime
from pydantic import ValidationError

from src.app.models.classroom import (
    CourseState,
    StudentRole,
    CourseBase,
    CourseCreate,
    CourseUpdate,
    CourseResponse,
    StudentBase,
    StudentResponse,
    TeacherBase,
    TeacherResponse,
    CourseWorkType,
    CourseWorkState,
    CourseWorkBase,
    CourseWorkResponse,
    SubmissionState,
    StudentSubmissionBase,
    StudentSubmissionResponse,
    ClassroomMetrics,
    ClassroomSyncStatus
)


class TestEnumerations:
    """Test enumeration values."""

    def test_course_state(self):
        """Test CourseState enumeration."""
        assert CourseState.ACTIVE == "ACTIVE"
        assert CourseState.ARCHIVED == "ARCHIVED"
        assert CourseState.PROVISIONED == "PROVISIONED"
        assert CourseState.DECLINED == "DECLINED"
        assert CourseState.SUSPENDED == "SUSPENDED"

    def test_student_role(self):
        """Test StudentRole enumeration."""
        assert StudentRole.STUDENT == "STUDENT"
        assert StudentRole.TEACHER == "TEACHER"

    def test_course_work_type(self):
        """Test CourseWorkType enumeration."""
        assert CourseWorkType.ASSIGNMENT == "ASSIGNMENT"
        assert CourseWorkType.SHORT_ANSWER_QUESTION == "SHORT_ANSWER_QUESTION"
        assert CourseWorkType.MULTIPLE_CHOICE_QUESTION == "MULTIPLE_CHOICE_QUESTION"

    def test_course_work_state(self):
        """Test CourseWorkState enumeration."""
        assert CourseWorkState.PUBLISHED == "PUBLISHED"
        assert CourseWorkState.DRAFT == "DRAFT"
        assert CourseWorkState.DELETED == "DELETED"

    def test_submission_state(self):
        """Test SubmissionState enumeration."""
        assert SubmissionState.NEW == "NEW"
        assert SubmissionState.CREATED == "CREATED"
        assert SubmissionState.TURNED_IN == "TURNED_IN"
        assert SubmissionState.RETURNED == "RETURNED"
        assert SubmissionState.RECLAIMED_BY_STUDENT == "RECLAIMED_BY_STUDENT"


class TestCourseBase:
    """Test CourseBase model."""

    def test_valid_course_base(self):
        """Test valid course base model."""
        course = CourseBase(
            name="Mathematics 101",
            section="A",
            description="Introduction to Mathematics",
            description_heading="Welcome to Math",
            room="Room 201",
            owner_id="teacher_123",
            course_state=CourseState.ACTIVE
        )

        assert course.name == "Mathematics 101"
        assert course.section == "A"
        assert course.description == "Introduction to Mathematics"
        assert course.owner_id == "teacher_123"
        assert course.course_state == CourseState.ACTIVE

    def test_name_validation(self):
        """Test course name validation."""
        # Valid name
        course = CourseBase(
            name="  Mathematics 101  ",
            owner_id="teacher_123"
        )
        assert course.name == "Mathematics 101"

        # Empty name
        with pytest.raises(ValidationError, match="Course name cannot be empty"):
            CourseBase(
                name="",
                owner_id="teacher_123"
            )

        # Whitespace-only name
        with pytest.raises(ValidationError, match="Course name cannot be empty"):
            CourseBase(
                name="   ",
                owner_id="teacher_123"
            )

        # Too long name (Google Classroom limit: 750 characters)
        with pytest.raises(ValidationError, match="Course name must be less than 750 characters"):
            CourseBase(
                name="A" * 751,
                owner_id="teacher_123"
            )

    def test_section_validation(self):
        """Test section validation."""
        # Valid section
        course = CourseBase(
            name="Math 101",
            section="  Section A  ",
            owner_id="teacher_123"
        )
        assert course.section == "Section A"

        # Empty section becomes None
        course = CourseBase(
            name="Math 101",
            section="   ",
            owner_id="teacher_123"
        )
        assert course.section is None

        # Too long section (Google Classroom limit: 2800 characters)
        with pytest.raises(ValidationError, match="Section must be less than 2800 characters"):
            CourseBase(
                name="Math 101",
                section="A" * 2801,
                owner_id="teacher_123"
            )

    def test_defaults(self):
        """Test default values."""
        course = CourseBase(
            name="Math 101",
            owner_id="teacher_123"
        )

        assert course.section is None
        assert course.description is None
        assert course.description_heading is None
        assert course.room is None
        assert course.course_state == CourseState.ACTIVE

    def test_config_dict(self):
        """Test ConfigDict configuration."""
        course = CourseBase(
            name="Math 101",
            owner_id="teacher_123"
        )

        config = course.model_config
        assert config['from_attributes'] is True
        assert config['str_strip_whitespace'] is True
        assert config['validate_assignment'] is True
        assert config['extra'] == "allow"  # For Google API compatibility


class TestCourseCreate:
    """Test CourseCreate model."""

    def test_valid_course_create(self):
        """Test valid course creation."""
        course = CourseCreate(
            name="Math 101",
            owner_id="teacher_123",
            enrollment_code="ABC123"
        )

        assert course.name == "Math 101"
        assert course.enrollment_code == "ABC123"

    def test_enrollment_code_validation(self):
        """Test enrollment code validation."""
        # Valid enrollment code
        course = CourseCreate(
            name="Math 101",
            owner_id="teacher_123",
            enrollment_code="  abc123  "
        )
        assert course.enrollment_code == "ABC123"  # Should be uppercase

        # Too short enrollment code
        with pytest.raises(ValidationError, match="Enrollment code must be 6-7 characters"):
            CourseCreate(
                name="Math 101",
                owner_id="teacher_123",
                enrollment_code="ABC12"
            )

        # Too long enrollment code
        with pytest.raises(ValidationError, match="Enrollment code must be 6-7 characters"):
            CourseCreate(
                name="Math 101",
                owner_id="teacher_123",
                enrollment_code="ABC12345"
            )

        # None enrollment code is valid
        course = CourseCreate(
            name="Math 101",
            owner_id="teacher_123",
            enrollment_code=None
        )
        assert course.enrollment_code is None


class TestCourseUpdate:
    """Test CourseUpdate model."""

    def test_valid_course_update(self):
        """Test valid course update."""
        update = CourseUpdate(
            name="Updated Math 101",
            section="Updated Section",
            description="Updated description",
            course_state=CourseState.ARCHIVED
        )

        assert update.name == "Updated Math 101"
        assert update.section == "Updated Section"
        assert update.course_state == CourseState.ARCHIVED

    def test_partial_update(self):
        """Test partial course update."""
        update = CourseUpdate(name="Only Name Updated")

        assert update.name == "Only Name Updated"
        assert update.section is None
        assert update.description is None

    def test_empty_update(self):
        """Test empty course update."""
        update = CourseUpdate()

        assert update.name is None
        assert update.section is None
        assert update.description is None
        assert update.course_state is None


class TestCourseResponse:
    """Test CourseResponse model."""

    def test_valid_course_response(self):
        """Test valid course response."""
        now = datetime.now()
        course = CourseResponse(
            id="course_123",
            name="Math 101",
            owner_id="teacher_123",
            creation_time=now,
            update_time=now,
            enrollment_code="ABC123",
            calendar_id="calendar_123",
            guardiansEnabled=True
        )

        assert course.id == "course_123"
        assert course.name == "Math 101"
        assert course.creation_time == now
        assert course.enrollment_code == "ABC123"
        assert course.guardiansEnabled is True

    def test_optional_fields(self):
        """Test optional fields in response."""
        course = CourseResponse(
            id="course_123",
            name="Math 101",
            owner_id="teacher_123"
        )

        assert course.creation_time is None
        assert course.update_time is None
        assert course.enrollment_code is None
        assert course.calendar_id is None
        assert course.teacher_folder is None
        assert course.guardiansEnabled is None

    def test_datetime_serialization(self):
        """Test datetime serialization."""
        now = datetime.now()
        course = CourseResponse(
            id="course_123",
            name="Math 101",
            owner_id="teacher_123",
            creation_time=now
        )

        # Test that datetime serialization method exists
        assert hasattr(course, 'serialize_datetime')

        # Test datetime serialization
        result = course.serialize_datetime(now)
        assert result == now.isoformat()

        # Test None serialization
        result = course.serialize_datetime(None)
        assert result is None


class TestStudentModels:
    """Test Student models."""

    def test_student_base(self):
        """Test StudentBase model."""
        student = StudentBase(
            course_id="course_123",
            user_id="user_123",
            profile={"name": "Student Name"}
        )

        assert student.course_id == "course_123"
        assert student.user_id == "user_123"
        assert student.profile["name"] == "Student Name"

    def test_student_response(self):
        """Test StudentResponse model."""
        student = StudentResponse(
            course_id="course_123",
            user_id="user_123",
            student_id="google_student_123",
            full_name="Test Student",
            email_address="student@example.com",
            photo_url="https://example.com/photo.jpg"
        )

        assert student.course_id == "course_123"
        assert student.student_id == "google_student_123"
        assert student.full_name == "Test Student"
        assert student.email_address == "student@example.com"


class TestTeacherModels:
    """Test Teacher models."""

    def test_teacher_base(self):
        """Test TeacherBase model."""
        teacher = TeacherBase(
            course_id="course_123",
            user_id="user_123"
        )

        assert teacher.course_id == "course_123"
        assert teacher.user_id == "user_123"

    def test_teacher_response(self):
        """Test TeacherResponse model."""
        teacher = TeacherResponse(
            course_id="course_123",
            user_id="user_123",
            teacher_id="google_teacher_123",
            full_name="Test Teacher",
            email_address="teacher@example.com",
            photo_url="https://example.com/photo.jpg"
        )

        assert teacher.course_id == "course_123"
        assert teacher.teacher_id == "google_teacher_123"
        assert teacher.full_name == "Test Teacher"
        assert teacher.email_address == "teacher@example.com"


class TestCourseWorkBase:
    """Test CourseWorkBase model."""

    def test_valid_course_work_base(self):
        """Test valid course work base."""
        work = CourseWorkBase(
            course_id="course_123",
            title="Assignment 1",
            description="Complete the math problems",
            work_type=CourseWorkType.ASSIGNMENT,
            state=CourseWorkState.PUBLISHED,
            max_points=100.0
        )

        assert work.course_id == "course_123"
        assert work.title == "Assignment 1"
        assert work.work_type == CourseWorkType.ASSIGNMENT
        assert work.max_points == 100.0

    def test_title_validation(self):
        """Test title validation."""
        # Valid title
        work = CourseWorkBase(
            course_id="course_123",
            title="  Assignment 1  "
        )
        assert work.title == "Assignment 1"

        # Empty title
        with pytest.raises(ValidationError, match="Course work title cannot be empty"):
            CourseWorkBase(
                course_id="course_123",
                title=""
            )

        # Too long title (Google Classroom limit: 3000 characters)
        with pytest.raises(ValidationError, match="Title must be less than 3000 characters"):
            CourseWorkBase(
                course_id="course_123",
                title="A" * 3001
            )

    def test_max_points_validation(self):
        """Test max points validation."""
        # Valid points
        work = CourseWorkBase(
            course_id="course_123",
            title="Assignment 1",
            max_points=85.5
        )
        assert work.max_points == 85.5

        # Negative points
        with pytest.raises(ValidationError, match="Max points cannot be negative"):
            CourseWorkBase(
                course_id="course_123",
                title="Assignment 1",
                max_points=-10.0
            )

        # Too high points
        with pytest.raises(ValidationError, match="Max points cannot exceed 10000"):
            CourseWorkBase(
                course_id="course_123",
                title="Assignment 1",
                max_points=10001.0
            )

        # None is valid
        work = CourseWorkBase(
            course_id="course_123",
            title="Assignment 1",
            max_points=None
        )
        assert work.max_points is None

    def test_defaults(self):
        """Test default values."""
        work = CourseWorkBase(
            course_id="course_123",
            title="Assignment 1"
        )

        assert work.description is None
        assert work.work_type == CourseWorkType.ASSIGNMENT
        assert work.state == CourseWorkState.DRAFT
        assert work.max_points is None


class TestCourseWorkResponse:
    """Test CourseWorkResponse model."""

    def test_valid_course_work_response(self):
        """Test valid course work response."""
        now = datetime.now()
        work = CourseWorkResponse(
            id="work_123",
            course_id="course_123",
            title="Assignment 1",
            creation_time=now,
            update_time=now,
            due_date=now,
            due_time="23:59",
            materials=[{"link": {"url": "https://example.com"}}]
        )

        assert work.id == "work_123"
        assert work.course_id == "course_123"
        assert work.creation_time == now
        assert work.due_time == "23:59"
        assert len(work.materials) == 1


class TestStudentSubmissionModels:
    """Test StudentSubmission models."""

    def test_student_submission_base(self):
        """Test StudentSubmissionBase model."""
        submission = StudentSubmissionBase(
            course_id="course_123",
            course_work_id="work_123",
            user_id="user_123",
            state=SubmissionState.TURNED_IN
        )

        assert submission.course_id == "course_123"
        assert submission.course_work_id == "work_123"
        assert submission.user_id == "user_123"
        assert submission.state == SubmissionState.TURNED_IN

    def test_student_submission_response(self):
        """Test StudentSubmissionResponse model."""
        now = datetime.now()
        submission = StudentSubmissionResponse(
            id="submission_123",
            course_id="course_123",
            course_work_id="work_123",
            user_id="user_123",
            state=SubmissionState.RETURNED,
            creation_time=now,
            update_time=now,
            late=True,
            draft_grade=85.0,
            assigned_grade=88.0
        )

        assert submission.id == "submission_123"
        assert submission.state == SubmissionState.RETURNED
        assert submission.late is True
        assert submission.draft_grade == 85.0
        assert submission.assigned_grade == 88.0


class TestClassroomMetrics:
    """Test ClassroomMetrics model."""

    def test_valid_classroom_metrics(self):
        """Test valid classroom metrics."""
        now = datetime.now()
        metrics = ClassroomMetrics(
            course_id="course_123",
            total_students=25,
            total_teachers=2,
            total_assignments=10,
            total_submissions=200,
            completion_rate=85.5,
            average_grade=87.3,
            active_students=23,
            last_activity=now
        )

        assert metrics.course_id == "course_123"
        assert metrics.total_students == 25
        assert metrics.completion_rate == 85.5
        assert metrics.average_grade == 87.3
        assert metrics.last_activity == now

    def test_completion_rate_validation(self):
        """Test completion rate validation."""
        # Valid completion rate
        metrics = ClassroomMetrics(
            course_id="course_123",
            completion_rate=95.5
        )
        assert metrics.completion_rate == 95.5

        # Negative completion rate
        with pytest.raises(ValidationError, match="Completion rate must be between 0 and 100"):
            ClassroomMetrics(
                course_id="course_123",
                completion_rate=-5.0
            )

        # Too high completion rate
        with pytest.raises(ValidationError, match="Completion rate must be between 0 and 100"):
            ClassroomMetrics(
                course_id="course_123",
                completion_rate=105.0
            )

    def test_average_grade_validation(self):
        """Test average grade validation."""
        # Valid average grade
        metrics = ClassroomMetrics(
            course_id="course_123",
            average_grade=85.5
        )
        assert metrics.average_grade == 85.5

        # None is valid
        metrics = ClassroomMetrics(
            course_id="course_123",
            average_grade=None
        )
        assert metrics.average_grade is None

        # Negative average grade
        with pytest.raises(ValidationError, match="Average grade cannot be negative"):
            ClassroomMetrics(
                course_id="course_123",
                average_grade=-10.0
            )

    def test_defaults(self):
        """Test default values."""
        metrics = ClassroomMetrics(course_id="course_123")

        assert metrics.total_students == 0
        assert metrics.total_teachers == 0
        assert metrics.total_assignments == 0
        assert metrics.total_submissions == 0
        assert metrics.completion_rate == 0.0
        assert metrics.average_grade is None
        assert metrics.active_students == 0
        assert metrics.last_activity is None


class TestClassroomSyncStatus:
    """Test ClassroomSyncStatus model."""

    def test_valid_sync_status(self):
        """Test valid sync status."""
        now = datetime.now()
        status = ClassroomSyncStatus(
            course_id="course_123",
            last_sync=now,
            sync_status="completed",
            error_message=None,
            records_synced=150
        )

        assert status.course_id == "course_123"
        assert status.last_sync == now
        assert status.sync_status == "completed"
        assert status.error_message is None
        assert status.records_synced == 150

    def test_sync_error(self):
        """Test sync status with error."""
        status = ClassroomSyncStatus(
            course_id="course_123",
            sync_status="failed",
            error_message="API quota exceeded",
            records_synced=0
        )

        assert status.sync_status == "failed"
        assert status.error_message == "API quota exceeded"
        assert status.records_synced == 0

    def test_defaults(self):
        """Test default values."""
        status = ClassroomSyncStatus(course_id="course_123")

        assert status.last_sync is None
        assert status.sync_status == "pending"
        assert status.error_message is None
        assert status.records_synced == 0


class TestModelSerialization:
    """Test model serialization and validation."""

    def test_course_serialization(self):
        """Test course model serialization."""
        course = CourseBase(
            name="Math 101",
            owner_id="teacher_123"
        )

        # Test model dump
        data = course.model_dump()
        assert data["name"] == "Math 101"
        assert data["owner_id"] == "teacher_123"
        assert data["course_state"] == CourseState.ACTIVE

        # Test model validation
        validated = CourseBase.model_validate(data)
        assert validated.name == course.name
        assert validated.owner_id == course.owner_id
        assert validated.course_state == course.course_state

    def test_metrics_serialization(self):
        """Test metrics model serialization."""
        now = datetime.now()
        metrics = ClassroomMetrics(
            course_id="course_123",
            total_students=25,
            last_activity=now
        )

        # Test model dump
        data = metrics.model_dump()
        assert data["course_id"] == "course_123"
        assert data["total_students"] == 25

        # Test model validation
        validated = ClassroomMetrics.model_validate(data)
        assert validated.course_id == metrics.course_id
        assert validated.total_students == metrics.total_students