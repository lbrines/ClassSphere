"""
Unit tests for Assignment models.
"""
import pytest
from datetime import datetime, timedelta
from pydantic import ValidationError

from src.app.models.assignment import (
    AssignmentType,
    AssignmentStatus,
    AssignmentBase,
    AssignmentCreate,
    AssignmentUpdate,
    AssignmentResponse,
    AssignmentList,
    AssignmentSearch,
    AssignmentStats
)


class TestAssignmentEnums:
    """Test assignment enums."""
    
    def test_assignment_type_enum(self):
        """Test AssignmentType enum values."""
        assert AssignmentType.HOMEWORK == "homework"
        assert AssignmentType.PROJECT == "project"
        assert AssignmentType.EXAM == "exam"
        assert AssignmentType.QUIZ == "quiz"
        assert AssignmentType.ESSAY == "essay"
        assert AssignmentType.PRESENTATION == "presentation"
    
    def test_assignment_status_enum(self):
        """Test AssignmentStatus enum values."""
        assert AssignmentStatus.DRAFT == "draft"
        assert AssignmentStatus.PUBLISHED == "published"
        assert AssignmentStatus.CLOSED == "closed"
        assert AssignmentStatus.GRADED == "graded"


class TestAssignmentBase:
    """Test AssignmentBase model."""
    
    def test_assignment_base_valid_data(self):
        """Test AssignmentBase with valid data."""
        due_date = datetime.utcnow() + timedelta(days=7)
        
        assignment_data = {
            "title": "Python Programming Assignment",
            "description": "Create a Python program that demonstrates object-oriented programming",
            "assignment_type": AssignmentType.HOMEWORK,
            "status": AssignmentStatus.DRAFT,
            "course_id": "course-123",
            "instructor_id": "instructor-456",
            "due_date": due_date,
            "max_points": 100.0,
            "instructions": "Follow the provided guidelines",
            "attachments": ["https://example.com/file1.pdf", "https://example.com/file2.docx"],
            "rubric": {"criteria": "points", "code_quality": 30, "functionality": 50, "documentation": 20},
            "late_submission_allowed": True,
            "late_penalty_percentage": 10.0
        }
        
        assignment = AssignmentBase(**assignment_data)
        
        assert assignment.title == "Python Programming Assignment"
        assert assignment.description == "Create a Python program that demonstrates object-oriented programming"
        assert assignment.assignment_type == AssignmentType.HOMEWORK
        assert assignment.status == AssignmentStatus.DRAFT
        assert assignment.course_id == "course-123"
        assert assignment.instructor_id == "instructor-456"
        assert assignment.due_date == due_date
        assert assignment.max_points == 100.0
        assert assignment.instructions == "Follow the provided guidelines"
        assert len(assignment.attachments) == 2
        assert assignment.rubric["criteria"] == "points"
        assert assignment.late_submission_allowed is True
        assert assignment.late_penalty_percentage == 10.0
        assert assignment.created_at is not None
        assert assignment.updated_at is not None
    
    def test_assignment_base_minimal_data(self):
        """Test AssignmentBase with minimal required data."""
        due_date = datetime.utcnow() + timedelta(days=7)
        
        assignment_data = {
            "title": "Test Assignment",
            "description": "A test assignment description",
            "course_id": "course-123",
            "instructor_id": "instructor-456",
            "due_date": due_date,
            "max_points": 50.0
        }
        
        assignment = AssignmentBase(**assignment_data)
        
        assert assignment.title == "Test Assignment"
        assert assignment.description == "A test assignment description"
        assert assignment.course_id == "course-123"
        assert assignment.instructor_id == "instructor-456"
        assert assignment.due_date == due_date
        assert assignment.max_points == 50.0
        assert assignment.assignment_type == AssignmentType.HOMEWORK  # Default
        assert assignment.status == AssignmentStatus.DRAFT  # Default
        assert assignment.instructions is None
        assert assignment.attachments is None
        assert assignment.rubric is None
        assert assignment.late_submission_allowed is True  # Default
        assert assignment.late_penalty_percentage is None
    
    def test_assignment_base_title_validation(self):
        """Test AssignmentBase title validation."""
        due_date = datetime.utcnow() + timedelta(days=7)
        
        # Empty title
        with pytest.raises(ValidationError) as exc_info:
            AssignmentBase(
                title="",
                description="Test description",
                course_id="course-123",
                instructor_id="instructor-456",
                due_date=due_date,
                max_points=50.0
            )
        assert "String should have at least 3 characters" in str(exc_info.value)
        
        # Title too short
        with pytest.raises(ValidationError) as exc_info:
            AssignmentBase(
                title="AB",
                description="Test description",
                course_id="course-123",
                instructor_id="instructor-456",
                due_date=due_date,
                max_points=50.0
            )
        assert "at least 3 characters" in str(exc_info.value)
        
        # Title too long
        with pytest.raises(ValidationError) as exc_info:
            AssignmentBase(
                title="A" * 201,
                description="Test description",
                course_id="course-123",
                instructor_id="instructor-456",
                due_date=due_date,
                max_points=50.0
            )
        assert "at most 200 characters" in str(exc_info.value)
    
    def test_assignment_base_description_validation(self):
        """Test AssignmentBase description validation."""
        due_date = datetime.utcnow() + timedelta(days=7)
        
        # Description too short
        with pytest.raises(ValidationError) as exc_info:
            AssignmentBase(
                title="Test Assignment",
                description="Short",
                course_id="course-123",
                instructor_id="instructor-456",
                due_date=due_date,
                max_points=50.0
            )
        assert "at least 10 characters" in str(exc_info.value)
        
        # Description too long
        with pytest.raises(ValidationError) as exc_info:
            AssignmentBase(
                title="Test Assignment",
                description="A" * 2001,
                course_id="course-123",
                instructor_id="instructor-456",
                due_date=due_date,
                max_points=50.0
            )
        assert "at most 2000 characters" in str(exc_info.value)
    
    def test_assignment_base_due_date_validation(self):
        """Test AssignmentBase due_date validation."""
        # Due date in the past
        past_date = datetime.utcnow() - timedelta(days=1)
        
        with pytest.raises(ValidationError) as exc_info:
            AssignmentBase(
                title="Test Assignment",
                description="Test description",
                course_id="course-123",
                instructor_id="instructor-456",
                due_date=past_date,
                max_points=50.0
            )
        assert "Due date must be in the future" in str(exc_info.value)
    
    def test_assignment_base_max_points_validation(self):
        """Test AssignmentBase max_points validation."""
        due_date = datetime.utcnow() + timedelta(days=7)
        
        # Invalid max_points
        with pytest.raises(ValidationError) as exc_info:
            AssignmentBase(
                title="Test Assignment",
                description="Test description",
                course_id="course-123",
                instructor_id="instructor-456",
                due_date=due_date,
                max_points=-1.0
            )
        assert "greater than or equal to 0" in str(exc_info.value)
        
        with pytest.raises(ValidationError) as exc_info:
            AssignmentBase(
                title="Test Assignment",
                description="Test description",
                course_id="course-123",
                instructor_id="instructor-456",
                due_date=due_date,
                max_points=1001.0
            )
        assert "less than or equal to 1000" in str(exc_info.value)
    
    def test_assignment_base_late_penalty_validation(self):
        """Test AssignmentBase late_penalty_percentage validation."""
        due_date = datetime.utcnow() + timedelta(days=7)
        
        # Late penalty when late submissions not allowed
        with pytest.raises(ValidationError) as exc_info:
            AssignmentBase(
                title="Test Assignment",
                description="Test description",
                course_id="course-123",
                instructor_id="instructor-456",
                due_date=due_date,
                max_points=50.0,
                late_submission_allowed=False,
                late_penalty_percentage=10.0
            )
        assert "Late penalty cannot be set when late submissions are not allowed" in str(exc_info.value)
        
        # Valid case: late penalty when late submissions allowed
        assignment = AssignmentBase(
            title="Test Assignment",
            description="Test description",
            course_id="course-123",
            instructor_id="instructor-456",
            due_date=due_date,
            max_points=50.0,
            late_submission_allowed=True,
            late_penalty_percentage=10.0
        )
        assert assignment.late_penalty_percentage == 10.0


class TestAssignmentCreate:
    """Test AssignmentCreate model."""
    
    def test_assignment_create_inheritance(self):
        """Test AssignmentCreate inherits from AssignmentBase."""
        due_date = datetime.utcnow() + timedelta(days=7)
        
        assignment_data = {
            "title": "Create Assignment",
            "description": "Assignment for creation testing",
            "course_id": "course-123",
            "instructor_id": "instructor-456",
            "due_date": due_date,
            "max_points": 75.0,
            "assignment_type": AssignmentType.PROJECT
        }
        
        assignment = AssignmentCreate(**assignment_data)
        
        assert isinstance(assignment, AssignmentBase)
        assert assignment.title == "Create Assignment"
        assert assignment.description == "Assignment for creation testing"
        assert assignment.course_id == "course-123"
        assert assignment.instructor_id == "instructor-456"
        assert assignment.due_date == due_date
        assert assignment.max_points == 75.0
        assert assignment.assignment_type == AssignmentType.PROJECT


class TestAssignmentUpdate:
    """Test AssignmentUpdate model."""
    
    def test_assignment_update_all_optional(self):
        """Test AssignmentUpdate with all optional fields."""
        due_date = datetime.utcnow() + timedelta(days=14)
        
        assignment_data = {
            "title": "Updated Assignment",
            "description": "Updated assignment description",
            "assignment_type": AssignmentType.EXAM,
            "status": AssignmentStatus.PUBLISHED,
            "due_date": due_date,
            "max_points": 150.0,
            "instructions": "Updated instructions",
            "attachments": ["https://example.com/updated.pdf"],
            "rubric": {"updated": "criteria"},
            "late_submission_allowed": False,
            "late_penalty_percentage": 0.0
        }
        
        assignment = AssignmentUpdate(**assignment_data)
        
        assert assignment.title == "Updated Assignment"
        assert assignment.description == "Updated assignment description"
        assert assignment.assignment_type == AssignmentType.EXAM
        assert assignment.status == AssignmentStatus.PUBLISHED
        assert assignment.due_date == due_date
        assert assignment.max_points == 150.0
        assert assignment.instructions == "Updated instructions"
        assert len(assignment.attachments) == 1
        assert assignment.rubric["updated"] == "criteria"
        assert assignment.late_submission_allowed is False
        assert assignment.late_penalty_percentage == 0.0
    
    def test_assignment_update_empty(self):
        """Test AssignmentUpdate with no fields."""
        assignment = AssignmentUpdate()
        
        assert assignment.title is None
        assert assignment.description is None
        assert assignment.assignment_type is None
        assert assignment.status is None
        assert assignment.due_date is None
        assert assignment.max_points is None
        assert assignment.instructions is None
        assert assignment.attachments is None
        assert assignment.rubric is None
        assert assignment.late_submission_allowed is None
        assert assignment.late_penalty_percentage is None


class TestAssignmentResponse:
    """Test AssignmentResponse model."""
    
    def test_assignment_response_inheritance(self):
        """Test AssignmentResponse inherits from AssignmentBase."""
        due_date = datetime.utcnow() + timedelta(days=7)
        
        assignment_data = {
            "id": "assignment-123",
            "title": "Response Assignment",
            "description": "Assignment for response testing",
            "course_id": "course-123",
            "instructor_id": "instructor-456",
            "due_date": due_date,
            "max_points": 100.0,
            "submission_count": 25,
            "graded_count": 20,
            "average_grade": 85.5
        }
        
        assignment = AssignmentResponse(**assignment_data)
        
        assert isinstance(assignment, AssignmentBase)
        assert assignment.id == "assignment-123"
        assert assignment.title == "Response Assignment"
        assert assignment.description == "Assignment for response testing"
        assert assignment.course_id == "course-123"
        assert assignment.instructor_id == "instructor-456"
        assert assignment.due_date == due_date
        assert assignment.max_points == 100.0
        assert assignment.submission_count == 25
        assert assignment.graded_count == 20
        assert assignment.average_grade == 85.5


class TestAssignmentList:
    """Test AssignmentList model."""
    
    def test_assignment_list_valid_data(self):
        """Test AssignmentList with valid data."""
        due_date = datetime.utcnow() + timedelta(days=7)
        
        assignments = [
            AssignmentResponse(
                id="assignment-1",
                title="Assignment 1",
                description="Description 1",
                course_id="course-1",
                instructor_id="instructor-1",
                due_date=due_date,
                max_points=50.0
            ),
            AssignmentResponse(
                id="assignment-2",
                title="Assignment 2",
                description="Description 2",
                course_id="course-2",
                instructor_id="instructor-2",
                due_date=due_date,
                max_points=75.0
            )
        ]
        
        assignment_list = AssignmentList(
            assignments=assignments,
            total=2,
            page=1,
            size=20
        )
        
        assert len(assignment_list.assignments) == 2
        assert assignment_list.total == 2
        assert assignment_list.page == 1
        assert assignment_list.size == 20


class TestAssignmentSearch:
    """Test AssignmentSearch model."""
    
    def test_assignment_search_valid_data(self):
        """Test AssignmentSearch with valid data."""
        due_after = datetime.utcnow()
        due_before = datetime.utcnow() + timedelta(days=30)
        
        search = AssignmentSearch(
            query="Python",
            course_id="course-123",
            assignment_type=AssignmentType.HOMEWORK,
            status=AssignmentStatus.PUBLISHED,
            instructor_id="instructor-456",
            due_after=due_after,
            due_before=due_before,
            page=2,
            size=10
        )
        
        assert search.query == "Python"
        assert search.course_id == "course-123"
        assert search.assignment_type == AssignmentType.HOMEWORK
        assert search.status == AssignmentStatus.PUBLISHED
        assert search.instructor_id == "instructor-456"
        assert search.due_after == due_after
        assert search.due_before == due_before
        assert search.page == 2
        assert search.size == 10
    
    def test_assignment_search_defaults(self):
        """Test AssignmentSearch with default values."""
        search = AssignmentSearch()
        
        assert search.query is None
        assert search.course_id is None
        assert search.assignment_type is None
        assert search.status is None
        assert search.instructor_id is None
        assert search.due_before is None
        assert search.due_after is None
        assert search.page == 1
        assert search.size == 20


class TestAssignmentStats:
    """Test AssignmentStats model."""
    
    def test_assignment_stats_valid_data(self):
        """Test AssignmentStats with valid data."""
        stats = AssignmentStats(
            assignment_id="assignment-123",
            total_submissions=50,
            on_time_submissions=40,
            late_submissions=10,
            graded_submissions=45,
            average_grade=87.5,
            completion_rate=90.0
        )
        
        assert stats.assignment_id == "assignment-123"
        assert stats.total_submissions == 50
        assert stats.on_time_submissions == 40
        assert stats.late_submissions == 10
        assert stats.graded_submissions == 45
        assert stats.average_grade == 87.5
        assert stats.completion_rate == 90.0
    
    def test_assignment_stats_defaults(self):
        """Test AssignmentStats with default values."""
        stats = AssignmentStats(assignment_id="assignment-123")
        
        assert stats.assignment_id == "assignment-123"
        assert stats.total_submissions == 0
        assert stats.on_time_submissions == 0
        assert stats.late_submissions == 0
        assert stats.graded_submissions == 0
        assert stats.average_grade is None
        assert stats.completion_rate is None