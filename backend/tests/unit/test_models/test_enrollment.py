"""
Unit tests for Enrollment models.
"""
import pytest
from datetime import datetime, timedelta
from pydantic import ValidationError

from src.app.models.enrollment import (
    EnrollmentStatus,
    EnrollmentRole,
    EnrollmentBase,
    EnrollmentCreate,
    EnrollmentUpdate,
    EnrollmentResponse,
    EnrollmentList,
    EnrollmentSearch,
    EnrollmentStats,
    BulkEnrollment
)


class TestEnrollmentEnums:
    """Test enrollment enums."""
    
    def test_enrollment_status_enum(self):
        """Test EnrollmentStatus enum values."""
        assert EnrollmentStatus.PENDING == "pending"
        assert EnrollmentStatus.ACTIVE == "active"
        assert EnrollmentStatus.COMPLETED == "completed"
        assert EnrollmentStatus.DROPPED == "dropped"
        assert EnrollmentStatus.SUSPENDED == "suspended"
    
    def test_enrollment_role_enum(self):
        """Test EnrollmentRole enum values."""
        assert EnrollmentRole.STUDENT == "student"
        assert EnrollmentRole.TEACHER_ASSISTANT == "teacher_assistant"
        assert EnrollmentRole.OBSERVER == "observer"


class TestEnrollmentBase:
    """Test EnrollmentBase model."""
    
    def test_enrollment_base_valid_data(self):
        """Test EnrollmentBase with valid data."""
        enrollment_date = datetime.utcnow()
        completion_date = datetime.utcnow() + timedelta(days=90)
        
        enrollment_data = {
            "user_id": "user-123",
            "course_id": "course-456",
            "role": EnrollmentRole.STUDENT,
            "status": EnrollmentStatus.ACTIVE,
            "enrollment_date": enrollment_date,
            "completion_date": completion_date,
            "final_grade": 85.5,
            "credits_earned": 3
        }
        
        enrollment = EnrollmentBase(**enrollment_data)
        
        assert enrollment.user_id == "user-123"
        assert enrollment.course_id == "course-456"
        assert enrollment.role == EnrollmentRole.STUDENT
        assert enrollment.status == EnrollmentStatus.ACTIVE
        assert enrollment.enrollment_date == enrollment_date
        assert enrollment.completion_date == completion_date
        assert enrollment.final_grade == 85.5
        assert enrollment.credits_earned == 3
        assert enrollment.created_at is not None
        assert enrollment.updated_at is not None
    
    def test_enrollment_base_minimal_data(self):
        """Test EnrollmentBase with minimal required data."""
        enrollment_data = {
            "user_id": "user-123",
            "course_id": "course-456"
        }
        
        enrollment = EnrollmentBase(**enrollment_data)
        
        assert enrollment.user_id == "user-123"
        assert enrollment.course_id == "course-456"
        assert enrollment.role == EnrollmentRole.STUDENT  # Default
        assert enrollment.status == EnrollmentStatus.PENDING  # Default
        assert enrollment.enrollment_date is not None  # Default to now
        assert enrollment.completion_date is None
        assert enrollment.final_grade is None
        assert enrollment.credits_earned is None
    
    def test_enrollment_base_final_grade_validation(self):
        """Test EnrollmentBase final_grade validation."""
        # Invalid final_grade
        with pytest.raises(ValidationError) as exc_info:
            EnrollmentBase(
                user_id="user-123",
                course_id="course-456",
                final_grade=-1.0
            )
        assert "greater than or equal to 0" in str(exc_info.value)
        
        with pytest.raises(ValidationError) as exc_info:
            EnrollmentBase(
                user_id="user-123",
                course_id="course-456",
                final_grade=101.0
            )
        assert "less than or equal to 100" in str(exc_info.value)
    
    def test_enrollment_base_credits_validation(self):
        """Test EnrollmentBase credits_earned validation."""
        # Invalid credits_earned
        with pytest.raises(ValidationError) as exc_info:
            EnrollmentBase(
                user_id="user-123",
                course_id="course-456",
                credits_earned=-1
            )
        assert "greater than or equal to 0" in str(exc_info.value)
        
        with pytest.raises(ValidationError) as exc_info:
            EnrollmentBase(
                user_id="user-123",
                course_id="course-456",
                credits_earned=11
            )
        assert "less than or equal to 10" in str(exc_info.value)
    
    def test_enrollment_base_completion_date_validation(self):
        """Test EnrollmentBase completion_date validation."""
        enrollment_date = datetime.utcnow()
        completion_date = datetime.utcnow() - timedelta(days=1)  # Before enrollment
        
        with pytest.raises(ValidationError) as exc_info:
            EnrollmentBase(
                user_id="user-123",
                course_id="course-456",
                enrollment_date=enrollment_date,
                completion_date=completion_date
            )
        assert "Completion date must be after enrollment date" in str(exc_info.value)


class TestEnrollmentCreate:
    """Test EnrollmentCreate model."""
    
    def test_enrollment_create_inheritance(self):
        """Test EnrollmentCreate inherits from EnrollmentBase."""
        enrollment_data = {
            "user_id": "user-123",
            "course_id": "course-456",
            "role": EnrollmentRole.TEACHER_ASSISTANT,
            "status": EnrollmentStatus.ACTIVE
        }
        
        enrollment = EnrollmentCreate(**enrollment_data)
        
        assert isinstance(enrollment, EnrollmentBase)
        assert enrollment.user_id == "user-123"
        assert enrollment.course_id == "course-456"
        assert enrollment.role == EnrollmentRole.TEACHER_ASSISTANT
        assert enrollment.status == EnrollmentStatus.ACTIVE


class TestEnrollmentUpdate:
    """Test EnrollmentUpdate model."""
    
    def test_enrollment_update_all_optional(self):
        """Test EnrollmentUpdate with all optional fields."""
        completion_date = datetime.utcnow() + timedelta(days=90)
        
        enrollment_data = {
            "role": EnrollmentRole.OBSERVER,
            "status": EnrollmentStatus.COMPLETED,
            "completion_date": completion_date,
            "final_grade": 92.5,
            "credits_earned": 4
        }
        
        enrollment = EnrollmentUpdate(**enrollment_data)
        
        assert enrollment.role == EnrollmentRole.OBSERVER
        assert enrollment.status == EnrollmentStatus.COMPLETED
        assert enrollment.completion_date == completion_date
        assert enrollment.final_grade == 92.5
        assert enrollment.credits_earned == 4
    
    def test_enrollment_update_empty(self):
        """Test EnrollmentUpdate with no fields."""
        enrollment = EnrollmentUpdate()
        
        assert enrollment.role is None
        assert enrollment.status is None
        assert enrollment.completion_date is None
        assert enrollment.final_grade is None
        assert enrollment.credits_earned is None


class TestEnrollmentResponse:
    """Test EnrollmentResponse model."""
    
    def test_enrollment_response_inheritance(self):
        """Test EnrollmentResponse inherits from EnrollmentBase."""
        enrollment_data = {
            "id": "enrollment-123",
            "user_id": "user-123",
            "course_id": "course-456",
            "user_name": "John Doe",
            "user_email": "john@example.com",
            "course_title": "Python Programming",
            "course_code": "CS101",
            "assignments_completed": 8,
            "assignments_total": 10,
            "average_grade": 88.5
        }
        
        enrollment = EnrollmentResponse(**enrollment_data)
        
        assert isinstance(enrollment, EnrollmentBase)
        assert enrollment.id == "enrollment-123"
        assert enrollment.user_id == "user-123"
        assert enrollment.course_id == "course-456"
        assert enrollment.user_name == "John Doe"
        assert enrollment.user_email == "john@example.com"
        assert enrollment.course_title == "Python Programming"
        assert enrollment.course_code == "CS101"
        assert enrollment.assignments_completed == 8
        assert enrollment.assignments_total == 10
        assert enrollment.average_grade == 88.5


class TestEnrollmentList:
    """Test EnrollmentList model."""
    
    def test_enrollment_list_valid_data(self):
        """Test EnrollmentList with valid data."""
        enrollments = [
            EnrollmentResponse(
                id="enrollment-1",
                user_id="user-1",
                course_id="course-1"
            ),
            EnrollmentResponse(
                id="enrollment-2",
                user_id="user-2",
                course_id="course-2"
            )
        ]
        
        enrollment_list = EnrollmentList(
            enrollments=enrollments,
            total=2,
            page=1,
            size=20
        )
        
        assert len(enrollment_list.enrollments) == 2
        assert enrollment_list.total == 2
        assert enrollment_list.page == 1
        assert enrollment_list.size == 20


class TestEnrollmentSearch:
    """Test EnrollmentSearch model."""
    
    def test_enrollment_search_valid_data(self):
        """Test EnrollmentSearch with valid data."""
        enrolled_after = datetime.utcnow() - timedelta(days=30)
        enrolled_before = datetime.utcnow()
        
        search = EnrollmentSearch(
            user_id="user-123",
            course_id="course-456",
            role=EnrollmentRole.STUDENT,
            status=EnrollmentStatus.ACTIVE,
            enrolled_after=enrolled_after,
            enrolled_before=enrolled_before,
            page=2,
            size=10
        )
        
        assert search.user_id == "user-123"
        assert search.course_id == "course-456"
        assert search.role == EnrollmentRole.STUDENT
        assert search.status == EnrollmentStatus.ACTIVE
        assert search.enrolled_after == enrolled_after
        assert search.enrolled_before == enrolled_before
        assert search.page == 2
        assert search.size == 10
    
    def test_enrollment_search_defaults(self):
        """Test EnrollmentSearch with default values."""
        search = EnrollmentSearch()
        
        assert search.user_id is None
        assert search.course_id is None
        assert search.role is None
        assert search.status is None
        assert search.enrolled_after is None
        assert search.enrolled_before is None
        assert search.page == 1
        assert search.size == 20


class TestEnrollmentStats:
    """Test EnrollmentStats model."""
    
    def test_enrollment_stats_valid_data(self):
        """Test EnrollmentStats with valid data."""
        stats = EnrollmentStats(
            course_id="course-123",
            user_id="user-456",
            total_enrollments=100,
            active_enrollments=80,
            completed_enrollments=60,
            dropped_enrollments=10,
            average_completion_rate=75.0,
            average_final_grade=85.5
        )
        
        assert stats.course_id == "course-123"
        assert stats.user_id == "user-456"
        assert stats.total_enrollments == 100
        assert stats.active_enrollments == 80
        assert stats.completed_enrollments == 60
        assert stats.dropped_enrollments == 10
        assert stats.average_completion_rate == 75.0
        assert stats.average_final_grade == 85.5
    
    def test_enrollment_stats_defaults(self):
        """Test EnrollmentStats with default values."""
        stats = EnrollmentStats()
        
        assert stats.course_id is None
        assert stats.user_id is None
        assert stats.total_enrollments == 0
        assert stats.active_enrollments == 0
        assert stats.completed_enrollments == 0
        assert stats.dropped_enrollments == 0
        assert stats.average_completion_rate is None
        assert stats.average_final_grade is None


class TestBulkEnrollment:
    """Test BulkEnrollment model."""
    
    def test_bulk_enrollment_valid_data(self):
        """Test BulkEnrollment with valid data."""
        user_ids = ["user-1", "user-2", "user-3"]
        
        bulk_enrollment = BulkEnrollment(
            user_ids=user_ids,
            course_id="course-123",
            role=EnrollmentRole.STUDENT,
            status=EnrollmentStatus.ACTIVE
        )
        
        assert bulk_enrollment.user_ids == user_ids
        assert bulk_enrollment.course_id == "course-123"
        assert bulk_enrollment.role == EnrollmentRole.STUDENT
        assert bulk_enrollment.status == EnrollmentStatus.ACTIVE
    
    def test_bulk_enrollment_minimal_data(self):
        """Test BulkEnrollment with minimal required data."""
        user_ids = ["user-1"]
        
        bulk_enrollment = BulkEnrollment(
            user_ids=user_ids,
            course_id="course-123"
        )
        
        assert bulk_enrollment.user_ids == user_ids
        assert bulk_enrollment.course_id == "course-123"
        assert bulk_enrollment.role == EnrollmentRole.STUDENT  # Default
        assert bulk_enrollment.status == EnrollmentStatus.ACTIVE  # Default
    
    def test_bulk_enrollment_user_ids_validation(self):
        """Test BulkEnrollment user_ids validation."""
        # Empty user_ids
        with pytest.raises(ValidationError) as exc_info:
            BulkEnrollment(user_ids=[], course_id="course-123")
        assert "at least 1 item" in str(exc_info.value)
        
        # Too many user_ids
        user_ids = [f"user-{i}" for i in range(101)]
        with pytest.raises(ValidationError) as exc_info:
            BulkEnrollment(user_ids=user_ids, course_id="course-123")
        assert "at most 100 items" in str(exc_info.value)
        
        # Duplicate user_ids
        with pytest.raises(ValidationError) as exc_info:
            BulkEnrollment(user_ids=["user-1", "user-1"], course_id="course-123")
        assert "User IDs must be unique" in str(exc_info.value)
    
    def test_bulk_enrollment_defaults(self):
        """Test BulkEnrollment with default values."""
        user_ids = ["user-1", "user-2"]
        
        bulk_enrollment = BulkEnrollment(
            user_ids=user_ids,
            course_id="course-123"
        )
        
        assert bulk_enrollment.user_ids == user_ids
        assert bulk_enrollment.course_id == "course-123"
        assert bulk_enrollment.role == EnrollmentRole.STUDENT
        assert bulk_enrollment.status == EnrollmentStatus.ACTIVE