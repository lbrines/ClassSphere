"""
Unit tests for CourseRepository.
"""
import pytest
from unittest.mock import AsyncMock, MagicMock, patch
from datetime import datetime, timedelta
from bson import ObjectId

from src.app.repositories.course_repository import CourseRepository
from src.app.models.course import CourseStatus, CourseLevel
from src.app.exceptions.base import ConflictError, DatabaseError


class TestCourseRepository:
    """Test CourseRepository functionality."""
    
    @pytest.fixture
    def repository(self):
        """Create course repository instance."""
        return CourseRepository()
    
    @pytest.fixture
    def mock_collection(self):
        """Create mock collection."""
        return AsyncMock()
    
    @pytest.fixture
    def sample_course_data(self):
        """Sample course data for testing."""
        return {
            'title': 'Introduction to Python',
            'description': 'Learn Python programming',
            'code': 'CS101',
            'level': CourseLevel.BEGINNER.value,
            'status': CourseStatus.DRAFT.value,
            'instructor_id': str(ObjectId()),
            'credits': 3
        }
    
    @pytest.mark.asyncio
    async def test_create_course_success(self, repository, mock_collection, sample_course_data):
        """Test successful course creation."""
        repository._collection = mock_collection
        
        # Mock exists to return False (no conflict)
        repository.exists = AsyncMock(return_value=False)
        repository.create = AsyncMock(return_value=str(ObjectId()))
        
        result_id = await repository.create_course(sample_course_data)
        
        assert isinstance(result_id, str)
        repository.exists.assert_called_once_with({'code': sample_course_data['code']})
        repository.create.assert_called_once_with(sample_course_data)
    
    @pytest.mark.asyncio
    async def test_create_course_code_conflict(self, repository, mock_collection, sample_course_data):
        """Test course creation with code conflict."""
        repository._collection = mock_collection
        
        # Mock exists to return True (conflict)
        repository.exists = AsyncMock(return_value=True)
        
        with pytest.raises(ConflictError) as exc_info:
            await repository.create_course(sample_course_data)
        
        assert f"Course with code {sample_course_data['code']} already exists" in str(exc_info.value)
    
    @pytest.mark.asyncio
    async def test_get_course_by_code_success(self, repository, mock_collection):
        """Test successful get course by code."""
        repository._collection = mock_collection
        
        test_code = 'CS101'
        test_course = {
            '_id': ObjectId(),
            'code': test_code,
            'title': 'Test Course'
        }
        
        repository.get_by_field = AsyncMock(return_value=test_course)
        
        result = await repository.get_course_by_code(test_code)
        
        assert result == test_course
        repository.get_by_field.assert_called_once_with('code', test_code.upper())
    
    @pytest.mark.asyncio
    async def test_get_courses_by_instructor_success(self, repository, mock_collection):
        """Test successful get courses by instructor."""
        repository._collection = mock_collection
        
        test_instructor_id = str(ObjectId())
        test_courses = [
            {'_id': ObjectId(), 'title': 'Course 1'},
            {'_id': ObjectId(), 'title': 'Course 2'}
        ]
        
        repository.get_many = AsyncMock(return_value=test_courses)
        
        result = await repository.get_courses_by_instructor(test_instructor_id, skip=0, limit=10)
        
        assert result == test_courses
        repository.get_many.assert_called_once_with(
            filter_dict={'instructor_id': test_instructor_id},
            skip=0,
            limit=10,
            sort=[('created_at', -1)]
        )
    
    @pytest.mark.asyncio
    async def test_get_courses_by_status_success(self, repository, mock_collection):
        """Test successful get courses by status."""
        repository._collection = mock_collection
        
        test_courses = [
            {'_id': ObjectId(), 'title': 'Active Course 1'},
            {'_id': ObjectId(), 'title': 'Active Course 2'}
        ]
        
        repository.get_many = AsyncMock(return_value=test_courses)
        
        result = await repository.get_courses_by_status(CourseStatus.ACTIVE, skip=0, limit=10)
        
        assert result == test_courses
        repository.get_many.assert_called_once_with(
            filter_dict={'status': CourseStatus.ACTIVE.value},
            skip=0,
            limit=10,
            sort=[('created_at', -1)]
        )
    
    @pytest.mark.asyncio
    async def test_get_courses_by_level_success(self, repository, mock_collection):
        """Test successful get courses by level."""
        repository._collection = mock_collection
        
        test_courses = [
            {'_id': ObjectId(), 'title': 'Beginner Course 1'},
            {'_id': ObjectId(), 'title': 'Beginner Course 2'}
        ]
        
        repository.get_many = AsyncMock(return_value=test_courses)
        
        result = await repository.get_courses_by_level(CourseLevel.BEGINNER, skip=0, limit=10)
        
        assert result == test_courses
        repository.get_many.assert_called_once_with(
            filter_dict={'level': CourseLevel.BEGINNER.value},
            skip=0,
            limit=10,
            sort=[('title', 1)]
        )
    
    @pytest.mark.asyncio
    async def test_get_courses_by_department_success(self, repository, mock_collection):
        """Test successful get courses by department."""
        repository._collection = mock_collection
        
        test_courses = [
            {'_id': ObjectId(), 'title': 'CS Course 1'},
            {'_id': ObjectId(), 'title': 'CS Course 2'}
        ]
        
        repository.get_many = AsyncMock(return_value=test_courses)
        
        result = await repository.get_courses_by_department('Computer Science', skip=0, limit=10)
        
        assert result == test_courses
        repository.get_many.assert_called_once_with(
            filter_dict={'department': 'Computer Science'},
            skip=0,
            limit=10,
            sort=[('title', 1)]
        )
    
    @pytest.mark.asyncio
    async def test_search_courses_success(self, repository, mock_collection):
        """Test successful course search."""
        repository._collection = mock_collection
        
        test_courses = [
            {'_id': ObjectId(), 'title': 'Python Programming'},
            {'_id': ObjectId(), 'title': 'Advanced Python'}
        ]
        
        repository.get_many = AsyncMock(return_value=test_courses)
        
        result = await repository.search_courses('python', skip=0, limit=10)
        
        assert result == test_courses
        repository.get_many.assert_called_once()
        
        # Check filter_dict contains regex search
        call_args = repository.get_many.call_args
        filter_dict = call_args[1]['filter_dict']
        assert '$or' in filter_dict
        assert len(filter_dict['$or']) == 3  # title, description, code
    
    @pytest.mark.asyncio
    async def test_get_active_courses_success(self, repository, mock_collection):
        """Test successful get active courses."""
        repository._collection = mock_collection
        
        test_courses = [
            {'_id': ObjectId(), 'title': 'Active Course 1'},
            {'_id': ObjectId(), 'title': 'Active Course 2'}
        ]
        
        repository.get_courses_by_status = AsyncMock(return_value=test_courses)
        
        result = await repository.get_active_courses(skip=0, limit=10)
        
        assert result == test_courses
        repository.get_courses_by_status.assert_called_once_with(CourseStatus.ACTIVE, 0, 10)
    
    @pytest.mark.asyncio
    async def test_get_courses_by_date_range_success(self, repository, mock_collection):
        """Test successful get courses by date range."""
        repository._collection = mock_collection
        
        start_date = datetime(2023, 1, 1)
        end_date = datetime(2023, 12, 31)
        test_courses = [
            {'_id': ObjectId(), 'title': 'Course in Range 1'},
            {'_id': ObjectId(), 'title': 'Course in Range 2'}
        ]
        
        repository.get_many = AsyncMock(return_value=test_courses)
        
        result = await repository.get_courses_by_date_range(start_date, end_date, skip=0, limit=10)
        
        assert result == test_courses
        repository.get_many.assert_called_once()
        
        # Check filter_dict contains date range
        call_args = repository.get_many.call_args
        filter_dict = call_args[1]['filter_dict']
        assert 'start_date' in filter_dict
        assert 'end_date' in filter_dict
    
    @pytest.mark.asyncio
    async def test_update_course_status_success(self, repository, mock_collection):
        """Test successful course status update."""
        repository._collection = mock_collection
        
        test_course_id = str(ObjectId())
        
        repository.update_by_id = AsyncMock(return_value=True)
        
        result = await repository.update_course_status(test_course_id, CourseStatus.ACTIVE)
        
        assert result is True
        repository.update_by_id.assert_called_once_with(test_course_id, {'status': CourseStatus.ACTIVE.value})
    
    @pytest.mark.asyncio
    async def test_update_course_instructor_success(self, repository, mock_collection):
        """Test successful course instructor update."""
        repository._collection = mock_collection
        
        test_course_id = str(ObjectId())
        test_instructor_id = str(ObjectId())
        
        repository.update_by_id = AsyncMock(return_value=True)
        
        result = await repository.update_course_instructor(test_course_id, test_instructor_id)
        
        assert result is True
        repository.update_by_id.assert_called_once_with(test_course_id, {'instructor_id': test_instructor_id})
    
    @pytest.mark.asyncio
    async def test_get_course_stats_success(self, repository, mock_collection):
        """Test successful course stats retrieval."""
        repository._collection = mock_collection
        
        test_course_id = str(ObjectId())
        test_stats = {
            'course_id': test_course_id,
            'total_students': 25,
            'active_students': 20,
            'completed_assignments': 10,
            'average_grade': 85.5,
            'completion_rate': 80.0
        }
        
        repository.aggregate = AsyncMock(return_value=[test_stats])
        
        result = await repository.get_course_stats(test_course_id)
        
        assert result == test_stats
        repository.aggregate.assert_called_once()
        
        # Check pipeline structure
        call_args = repository.aggregate.call_args
        pipeline = call_args[0][0]
        assert len(pipeline) > 0
        assert pipeline[0]['$match']['_id'] is not None
    
    @pytest.mark.asyncio
    async def test_get_course_stats_not_found(self, repository, mock_collection):
        """Test course stats when course not found."""
        repository._collection = mock_collection
        
        test_course_id = str(ObjectId())
        
        repository.aggregate = AsyncMock(return_value=[])
        
        result = await repository.get_course_stats(test_course_id)
        
        assert result == {}
    
    @pytest.mark.asyncio
    async def test_get_courses_with_stats_success(self, repository, mock_collection):
        """Test successful get courses with stats."""
        repository._collection = mock_collection
        
        test_courses = [
            {
                '_id': ObjectId(),
                'title': 'Course 1',
                'student_count': 25,
                'assignment_count': 10
            },
            {
                '_id': ObjectId(),
                'title': 'Course 2',
                'student_count': 30,
                'assignment_count': 12
            }
        ]
        
        repository.aggregate = AsyncMock(return_value=test_courses)
        
        result = await repository.get_courses_with_stats(skip=0, limit=10)
        
        assert result == test_courses
        repository.aggregate.assert_called_once()
    
    @pytest.mark.asyncio
    async def test_get_popular_courses_success(self, repository, mock_collection):
        """Test successful get popular courses."""
        repository._collection = mock_collection
        
        test_courses = [
            {'_id': ObjectId(), 'title': 'Popular Course 1', 'enrollment_count': 100},
            {'_id': ObjectId(), 'title': 'Popular Course 2', 'enrollment_count': 95}
        ]
        
        repository.aggregate = AsyncMock(return_value=test_courses)
        
        result = await repository.get_popular_courses(limit=5)
        
        assert result == test_courses
        repository.aggregate.assert_called_once()
    
    @pytest.mark.asyncio
    async def test_get_courses_by_credits_success(self, repository, mock_collection):
        """Test successful get courses by credits."""
        repository._collection = mock_collection
        
        test_courses = [
            {'_id': ObjectId(), 'title': '3 Credit Course 1'},
            {'_id': ObjectId(), 'title': '3 Credit Course 2'}
        ]
        
        repository.get_many = AsyncMock(return_value=test_courses)
        
        result = await repository.get_courses_by_credits(3, skip=0, limit=10)
        
        assert result == test_courses
        repository.get_many.assert_called_once_with(
            filter_dict={'credits': 3},
            skip=0,
            limit=10,
            sort=[('title', 1)]
        )
    
    @pytest.mark.asyncio
    async def test_bulk_update_status_success(self, repository, mock_collection):
        """Test successful bulk status update."""
        repository._collection = mock_collection
        
        test_course_ids = [str(ObjectId()), str(ObjectId())]
        
        repository.bulk_update = AsyncMock(return_value=2)
        
        result = await repository.bulk_update_status(test_course_ids, CourseStatus.ACTIVE)
        
        assert result == 2
        repository.bulk_update.assert_called_once()
        
        # Check filter_dict and update_data
        call_args = repository.bulk_update.call_args
        filter_dict = call_args[0][0]
        update_data = call_args[0][1]
        
        assert '_id' in filter_dict
        assert '$in' in filter_dict['_id']
        assert update_data['status'] == CourseStatus.ACTIVE.value
    
    @pytest.mark.asyncio
    async def test_create_course_indexes_success(self, repository, mock_collection):
        """Test successful course indexes creation."""
        repository._collection = mock_collection
        
        repository.create_indexes = AsyncMock()
        
        await repository.create_course_indexes()
        
        repository.create_indexes.assert_called_once()
        
        # Check that indexes were provided
        call_args = repository.create_indexes.call_args
        indexes = call_args[0][0]
        assert len(indexes) > 0
        
        # Check for specific indexes
        index_specs = [index[0] for index in indexes]
        assert ('code', 1) in index_specs
        assert ('instructor_id', 1) in index_specs
        assert ('status', 1) in index_specs
        assert ('level', 1) in index_specs
        assert ('department', 1) in index_specs
        assert ('credits', 1) in index_specs