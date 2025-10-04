"""
Unit tests for Course models.
"""
import pytest
from datetime import datetime, timedelta
from pydantic import ValidationError

from src.app.models.course import (
    CourseStatus,
    CourseLevel,
    CourseBase,
    CourseCreate,
    CourseUpdate,
    CourseResponse,
    CourseList,
    CourseSearch,
    CourseStats
)


class TestCourseEnums:
    """Test course enums."""
    
    def test_course_status_enum(self):
        """Test CourseStatus enum values."""
        assert CourseStatus.DRAFT == "draft"
        assert CourseStatus.ACTIVE == "active"
        assert CourseStatus.ARCHIVED == "archived"
        assert CourseStatus.COMPLETED == "completed"
    
    def test_course_level_enum(self):
        """Test CourseLevel enum values."""
        assert CourseLevel.BEGINNER == "beginner"
        assert CourseLevel.INTERMEDIATE == "intermediate"
        assert CourseLevel.ADVANCED == "advanced"


class TestCourseBase:
    """Test CourseBase model."""
    
    def test_course_base_valid_data(self):
        """Test CourseBase with valid data."""
        course_data = {
            "title": "Introduction to Python",
            "description": "Learn the basics of Python programming language",
            "code": "CS101",
            "level": CourseLevel.BEGINNER,
            "status": CourseStatus.DRAFT,
            "instructor_id": "instructor-123",
            "max_students": 30,
            "credits": 3,
            "department": "Computer Science",
            "start_date": datetime.utcnow() + timedelta(days=30),
            "end_date": datetime.utcnow() + timedelta(days=120)
        }
        
        course = CourseBase(**course_data)
        
        assert course.title == "Introduction to Python"
        assert course.description == "Learn the basics of Python programming language"
        assert course.code == "CS101"
        assert course.level == CourseLevel.BEGINNER
        assert course.status == CourseStatus.DRAFT
        assert course.instructor_id == "instructor-123"
        assert course.max_students == 30
        assert course.credits == 3
        assert course.department == "Computer Science"
        assert course.start_date is not None
        assert course.end_date is not None
        assert course.created_at is not None
        assert course.updated_at is not None
    
    def test_course_base_minimal_data(self):
        """Test CourseBase with minimal required data."""
        course_data = {
            "title": "Test Course",
            "description": "A test course description",
            "code": "TEST-101"
        }
        
        course = CourseBase(**course_data)
        
        assert course.title == "Test Course"
        assert course.description == "A test course description"
        assert course.code == "TEST-101"
        assert course.level == CourseLevel.BEGINNER  # Default
        assert course.status == CourseStatus.DRAFT  # Default
        assert course.instructor_id is None
        assert course.max_students is None
        assert course.credits is None
        assert course.department is None
        assert course.start_date is None
        assert course.end_date is None
    
    def test_course_base_title_validation(self):
        """Test CourseBase title validation."""
        # Empty title
        with pytest.raises(ValidationError) as exc_info:
            CourseBase(title="", description="Test description", code="TEST-101")
        assert "String should have at least 3 characters" in str(exc_info.value)
        
        # Whitespace only title
        with pytest.raises(ValidationError) as exc_info:
            CourseBase(title="   ", description="Test description", code="TEST-101")
        assert "Course title cannot be empty" in str(exc_info.value)
        
        # Title too short
        with pytest.raises(ValidationError) as exc_info:
            CourseBase(title="AB", description="Test description", code="TEST-101")
        assert "at least 3 characters" in str(exc_info.value)
        
        # Title too long
        with pytest.raises(ValidationError) as exc_info:
            CourseBase(title="A" * 201, description="Test description", code="TEST-101")
        assert "at most 200 characters" in str(exc_info.value)
    
    def test_course_base_code_validation(self):
        """Test CourseBase code validation."""
        # Empty code
        with pytest.raises(ValidationError) as exc_info:
            CourseBase(title="Test Course", description="Test description", code="")
        assert "String should have at least 3 characters" in str(exc_info.value)
        
        # Code too short
        with pytest.raises(ValidationError) as exc_info:
            CourseBase(title="Test Course", description="Test description", code="AB")
        assert "at least 3 characters" in str(exc_info.value)
        
        # Code too long
        with pytest.raises(ValidationError) as exc_info:
            CourseBase(title="Test Course", description="Test description", code="A" * 21)
        assert "at most 20 characters" in str(exc_info.value)
        
        # Invalid characters in code
        with pytest.raises(ValidationError) as exc_info:
            CourseBase(title="Test Course", description="Test description", code="CS@101")
        assert "Course code must be alphanumeric" in str(exc_info.value)
        
        # Valid code with special characters
        course = CourseBase(title="Test Course", description="Test description", code="CS-101")
        assert course.code == "CS-101"
        
        course = CourseBase(title="Test Course", description="Test description", code="cs_101")
        assert course.code == "CS_101"  # Should be uppercase
    
    def test_course_base_description_validation(self):
        """Test CourseBase description validation."""
        # Description too short
        with pytest.raises(ValidationError) as exc_info:
            CourseBase(title="Test Course", description="Short", code="TEST-101")
        assert "at least 10 characters" in str(exc_info.value)
        
        # Description too long
        with pytest.raises(ValidationError) as exc_info:
            CourseBase(title="Test Course", description="A" * 1001, code="TEST-101")
        assert "at most 1000 characters" in str(exc_info.value)
    
    def test_course_base_max_students_validation(self):
        """Test CourseBase max_students validation."""
        # Invalid max_students
        with pytest.raises(ValidationError) as exc_info:
            CourseBase(title="Test Course", description="Test description", code="TEST-101", max_students=0)
        assert "greater than or equal to 1" in str(exc_info.value)
        
        with pytest.raises(ValidationError) as exc_info:
            CourseBase(title="Test Course", description="Test description", code="TEST-101", max_students=1001)
        assert "less than or equal to 1000" in str(exc_info.value)
    
    def test_course_base_credits_validation(self):
        """Test CourseBase credits validation."""
        # Invalid credits
        with pytest.raises(ValidationError) as exc_info:
            CourseBase(title="Test Course", description="Test description", code="TEST-101", credits=0)
        assert "greater than or equal to 1" in str(exc_info.value)
        
        with pytest.raises(ValidationError) as exc_info:
            CourseBase(title="Test Course", description="Test description", code="TEST-101", credits=11)
        assert "less than or equal to 10" in str(exc_info.value)
    
    def test_course_base_end_date_validation(self):
        """Test CourseBase end_date validation."""
        start_date = datetime.utcnow() + timedelta(days=30)
        end_date = datetime.utcnow() + timedelta(days=20)  # Before start_date
        
        with pytest.raises(ValidationError) as exc_info:
            CourseBase(
                title="Test Course",
                description="Test description",
                code="TEST-101",
                start_date=start_date,
                end_date=end_date
            )
        assert "End date must be after start date" in str(exc_info.value)


class TestCourseCreate:
    """Test CourseCreate model."""
    
    def test_course_create_inheritance(self):
        """Test CourseCreate inherits from CourseBase."""
        course_data = {
            "title": "Advanced Python",
            "description": "Advanced Python programming concepts",
            "code": "CS201",
            "level": CourseLevel.ADVANCED,
            "status": CourseStatus.ACTIVE
        }
        
        course = CourseCreate(**course_data)
        
        assert isinstance(course, CourseBase)
        assert course.title == "Advanced Python"
        assert course.description == "Advanced Python programming concepts"
        assert course.code == "CS201"
        assert course.level == CourseLevel.ADVANCED
        assert course.status == CourseStatus.ACTIVE


class TestCourseUpdate:
    """Test CourseUpdate model."""
    
    def test_course_update_all_optional(self):
        """Test CourseUpdate with all optional fields."""
        course_data = {
            "title": "Updated Course",
            "description": "Updated description",
            "code": "UPD-101",
            "level": CourseLevel.INTERMEDIATE,
            "status": CourseStatus.ACTIVE,
            "instructor_id": "instructor-456",
            "max_students": 25,
            "credits": 4,
            "department": "Updated Department"
        }
        
        course = CourseUpdate(**course_data)
        
        assert course.title == "Updated Course"
        assert course.description == "Updated description"
        assert course.code == "UPD-101"
        assert course.level == CourseLevel.INTERMEDIATE
        assert course.status == CourseStatus.ACTIVE
        assert course.instructor_id == "instructor-456"
        assert course.max_students == 25
        assert course.credits == 4
        assert course.department == "Updated Department"
    
    def test_course_update_empty(self):
        """Test CourseUpdate with no fields."""
        course = CourseUpdate()
        
        assert course.title is None
        assert course.description is None
        assert course.code is None
        assert course.level is None
        assert course.status is None
        assert course.instructor_id is None
        assert course.max_students is None
        assert course.credits is None
        assert course.department is None
    
    def test_course_update_title_validation(self):
        """Test CourseUpdate title validation."""
        # Empty title
        with pytest.raises(ValidationError) as exc_info:
            CourseUpdate(title="")
        assert "String should have at least 3 characters" in str(exc_info.value)
        
        # Whitespace only title
        with pytest.raises(ValidationError) as exc_info:
            CourseUpdate(title="   ")
        assert "Course title cannot be empty" in str(exc_info.value)


class TestCourseResponse:
    """Test CourseResponse model."""
    
    def test_course_response_inheritance(self):
        """Test CourseResponse inherits from CourseBase."""
        course_data = {
            "id": "course-123",
            "title": "Response Course",
            "description": "Course for response testing",
            "code": "RESP-101",
            "student_count": 15,
            "assignment_count": 5
        }
        
        course = CourseResponse(**course_data)
        
        assert isinstance(course, CourseBase)
        assert course.id == "course-123"
        assert course.title == "Response Course"
        assert course.description == "Course for response testing"
        assert course.code == "RESP-101"
        assert course.student_count == 15
        assert course.assignment_count == 5


class TestCourseList:
    """Test CourseList model."""
    
    def test_course_list_valid_data(self):
        """Test CourseList with valid data."""
        courses = [
            CourseResponse(
                id="course-1",
                title="Course 1",
                description="Description 1",
                code="CS1"
            ),
            CourseResponse(
                id="course-2",
                title="Course 2",
                description="Description 2",
                code="CS2"
            )
        ]
        
        course_list = CourseList(
            courses=courses,
            total=2,
            page=1,
            size=20
        )
        
        assert len(course_list.courses) == 2
        assert course_list.total == 2
        assert course_list.page == 1
        assert course_list.size == 20
    
    def test_course_list_pagination_validation(self):
        """Test CourseList pagination validation."""
        # Invalid page
        with pytest.raises(ValidationError) as exc_info:
            CourseList(courses=[], total=0, page=0, size=20)
        assert "greater than or equal to 1" in str(exc_info.value)
        
        # Invalid size
        with pytest.raises(ValidationError) as exc_info:
            CourseList(courses=[], total=0, page=1, size=0)
        assert "greater than or equal to 1" in str(exc_info.value)
        
        with pytest.raises(ValidationError) as exc_info:
            CourseList(courses=[], total=0, page=1, size=101)
        assert "less than or equal to 100" in str(exc_info.value)


class TestCourseSearch:
    """Test CourseSearch model."""
    
    def test_course_search_valid_data(self):
        """Test CourseSearch with valid data."""
        search = CourseSearch(
            query="Python",
            level=CourseLevel.BEGINNER,
            status=CourseStatus.ACTIVE,
            department="Computer Science",
            instructor_id="instructor-123",
            page=2,
            size=10
        )
        
        assert search.query == "Python"
        assert search.level == CourseLevel.BEGINNER
        assert search.status == CourseStatus.ACTIVE
        assert search.department == "Computer Science"
        assert search.instructor_id == "instructor-123"
        assert search.page == 2
        assert search.size == 10
    
    def test_course_search_defaults(self):
        """Test CourseSearch with default values."""
        search = CourseSearch()
        
        assert search.query is None
        assert search.level is None
        assert search.status is None
        assert search.department is None
        assert search.instructor_id is None
        assert search.page == 1
        assert search.size == 20


class TestCourseStats:
    """Test CourseStats model."""
    
    def test_course_stats_valid_data(self):
        """Test CourseStats with valid data."""
        stats = CourseStats(
            course_id="course-123",
            total_students=50,
            active_students=45,
            completed_assignments=120,
            average_grade=85.5,
            completion_rate=90.0
        )
        
        assert stats.course_id == "course-123"
        assert stats.total_students == 50
        assert stats.active_students == 45
        assert stats.completed_assignments == 120
        assert stats.average_grade == 85.5
        assert stats.completion_rate == 90.0
    
    def test_course_stats_defaults(self):
        """Test CourseStats with default values."""
        stats = CourseStats(course_id="course-123")
        
        assert stats.course_id == "course-123"
        assert stats.total_students == 0
        assert stats.active_students == 0
        assert stats.completed_assignments == 0
        assert stats.average_grade is None
        assert stats.completion_rate is None
    
    def test_course_stats_grade_validation(self):
        """Test CourseStats grade validation."""
        # Invalid average_grade
        with pytest.raises(ValidationError) as exc_info:
            CourseStats(course_id="course-123", average_grade=-1.0)
        assert "greater than or equal to 0" in str(exc_info.value)
        
        with pytest.raises(ValidationError) as exc_info:
            CourseStats(course_id="course-123", average_grade=101.0)
        assert "less than or equal to 100" in str(exc_info.value)
        
        # Invalid completion_rate
        with pytest.raises(ValidationError) as exc_info:
            CourseStats(course_id="course-123", completion_rate=-1.0)
        assert "greater than or equal to 0" in str(exc_info.value)
        
        with pytest.raises(ValidationError) as exc_info:
            CourseStats(course_id="course-123", completion_rate=101.0)
        assert "less than or equal to 100" in str(exc_info.value)