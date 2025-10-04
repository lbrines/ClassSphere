"""
Unit tests for AssignmentRepository.
"""
import pytest
from unittest.mock import AsyncMock, MagicMock, patch
from datetime import datetime, timedelta
from bson import ObjectId

from src.app.repositories.assignment_repository import AssignmentRepository
from src.app.models.assignment import AssignmentType, AssignmentStatus


class TestAssignmentRepository:
    """Test AssignmentRepository functionality."""
    
    @pytest.fixture
    def repository(self):
        """Create assignment repository instance."""
        return AssignmentRepository()
    
    @pytest.fixture
    def mock_collection(self):
        """Create mock collection."""
        return AsyncMock()
    
    @pytest.fixture
    def sample_assignment_data(self):
        """Sample assignment data for testing."""
        return {
            'title': 'Python Assignment',
            'description': 'Complete Python exercises',
            'assignment_type': AssignmentType.HOMEWORK.value,
            'status': AssignmentStatus.DRAFT.value,
            'course_id': str(ObjectId()),
            'instructor_id': str(ObjectId()),
            'due_date': datetime.utcnow() + timedelta(days=7),
            'max_points': 100.0
        }
    
    @pytest.mark.asyncio
    async def test_create_assignment_success(self, repository, mock_collection, sample_assignment_data):
        """Test successful assignment creation."""
        repository._collection = mock_collection
        repository.create = AsyncMock(return_value=str(ObjectId()))
        
        result_id = await repository.create_assignment(sample_assignment_data)
        
        assert isinstance(result_id, str)
        repository.create.assert_called_once_with(sample_assignment_data)
    
    @pytest.mark.asyncio
    async def test_get_assignments_by_course_success(self, repository, mock_collection):
        """Test successful get assignments by course."""
        repository._collection = mock_collection
        
        test_course_id = str(ObjectId())
        test_assignments = [
            {'_id': ObjectId(), 'title': 'Assignment 1'},
            {'_id': ObjectId(), 'title': 'Assignment 2'}
        ]
        
        repository.get_many = AsyncMock(return_value=test_assignments)
        
        result = await repository.get_assignments_by_course(test_course_id, skip=0, limit=10)
        
        assert result == test_assignments
        repository.get_many.assert_called_once_with(
            filter_dict={'course_id': test_course_id},
            skip=0,
            limit=10,
            sort=[('due_date', 1)]
        )
    
    @pytest.mark.asyncio
    async def test_get_assignments_by_instructor_success(self, repository, mock_collection):
        """Test successful get assignments by instructor."""
        repository._collection = mock_collection
        
        test_instructor_id = str(ObjectId())
        test_assignments = [
            {'_id': ObjectId(), 'title': 'Instructor Assignment 1'},
            {'_id': ObjectId(), 'title': 'Instructor Assignment 2'}
        ]
        
        repository.get_many = AsyncMock(return_value=test_assignments)
        
        result = await repository.get_assignments_by_instructor(test_instructor_id, skip=0, limit=10)
        
        assert result == test_assignments
        repository.get_many.assert_called_once_with(
            filter_dict={'instructor_id': test_instructor_id},
            skip=0,
            limit=10,
            sort=[('created_at', -1)]
        )
    
    @pytest.mark.asyncio
    async def test_get_assignments_by_type_success(self, repository, mock_collection):
        """Test successful get assignments by type."""
        repository._collection = mock_collection
        
        test_assignments = [
            {'_id': ObjectId(), 'title': 'Homework 1'},
            {'_id': ObjectId(), 'title': 'Homework 2'}
        ]
        
        repository.get_many = AsyncMock(return_value=test_assignments)
        
        result = await repository.get_assignments_by_type(AssignmentType.HOMEWORK, skip=0, limit=10)
        
        assert result == test_assignments
        repository.get_many.assert_called_once_with(
            filter_dict={'assignment_type': AssignmentType.HOMEWORK.value},
            skip=0,
            limit=10,
            sort=[('due_date', 1)]
        )
    
    @pytest.mark.asyncio
    async def test_get_assignments_by_status_success(self, repository, mock_collection):
        """Test successful get assignments by status."""
        repository._collection = mock_collection
        
        test_assignments = [
            {'_id': ObjectId(), 'title': 'Published Assignment 1'},
            {'_id': ObjectId(), 'title': 'Published Assignment 2'}
        ]
        
        repository.get_many = AsyncMock(return_value=test_assignments)
        
        result = await repository.get_assignments_by_status(AssignmentStatus.PUBLISHED, skip=0, limit=10)
        
        assert result == test_assignments
        repository.get_many.assert_called_once_with(
            filter_dict={'status': AssignmentStatus.PUBLISHED.value},
            skip=0,
            limit=10,
            sort=[('due_date', 1)]
        )
    
    @pytest.mark.asyncio
    async def test_get_upcoming_assignments_success(self, repository, mock_collection):
        """Test successful get upcoming assignments."""
        repository._collection = mock_collection
        
        test_assignments = [
            {'_id': ObjectId(), 'title': 'Upcoming Assignment 1'},
            {'_id': ObjectId(), 'title': 'Upcoming Assignment 2'}
        ]
        
        repository.get_many = AsyncMock(return_value=test_assignments)
        
        result = await repository.get_upcoming_assignments(days_ahead=7, skip=0, limit=10)
        
        assert result == test_assignments
        repository.get_many.assert_called_once()
        
        # Check filter_dict contains date and status filters
        call_args = repository.get_many.call_args
        filter_dict = call_args[1]['filter_dict']
        assert 'due_date' in filter_dict
        assert 'status' in filter_dict
    
    @pytest.mark.asyncio
    async def test_get_overdue_assignments_success(self, repository, mock_collection):
        """Test successful get overdue assignments."""
        repository._collection = mock_collection
        
        test_assignments = [
            {'_id': ObjectId(), 'title': 'Overdue Assignment 1'},
            {'_id': ObjectId(), 'title': 'Overdue Assignment 2'}
        ]
        
        repository.get_many = AsyncMock(return_value=test_assignments)
        
        result = await repository.get_overdue_assignments(skip=0, limit=10)
        
        assert result == test_assignments
        repository.get_many.assert_called_once()
        
        # Check filter_dict contains overdue conditions
        call_args = repository.get_many.call_args
        filter_dict = call_args[1]['filter_dict']
        assert 'due_date' in filter_dict
        assert 'status' in filter_dict
    
    @pytest.mark.asyncio
    async def test_search_assignments_success(self, repository, mock_collection):
        """Test successful assignment search."""
        repository._collection = mock_collection
        
        test_assignments = [
            {'_id': ObjectId(), 'title': 'Python Assignment'},
            {'_id': ObjectId(), 'title': 'Advanced Python'}
        ]
        
        repository.get_many = AsyncMock(return_value=test_assignments)
        
        result = await repository.search_assignments('python', skip=0, limit=10)
        
        assert result == test_assignments
        repository.get_many.assert_called_once()
        
        # Check filter_dict contains regex search
        call_args = repository.get_many.call_args
        filter_dict = call_args[1]['filter_dict']
        assert '$or' in filter_dict
        assert len(filter_dict['$or']) == 2  # title, description
    
    @pytest.mark.asyncio
    async def test_get_assignments_by_date_range_success(self, repository, mock_collection):
        """Test successful get assignments by date range."""
        repository._collection = mock_collection
        
        start_date = datetime(2023, 1, 1)
        end_date = datetime(2023, 12, 31)
        test_assignments = [
            {'_id': ObjectId(), 'title': 'Assignment in Range 1'},
            {'_id': ObjectId(), 'title': 'Assignment in Range 2'}
        ]
        
        repository.get_many = AsyncMock(return_value=test_assignments)
        
        result = await repository.get_assignments_by_date_range(start_date, end_date, skip=0, limit=10)
        
        assert result == test_assignments
        repository.get_many.assert_called_once()
        
        # Check filter_dict contains date range
        call_args = repository.get_many.call_args
        filter_dict = call_args[1]['filter_dict']
        assert 'due_date' in filter_dict
    
    @pytest.mark.asyncio
    async def test_update_assignment_status_success(self, repository, mock_collection):
        """Test successful assignment status update."""
        repository._collection = mock_collection
        
        test_assignment_id = str(ObjectId())
        
        repository.update_by_id = AsyncMock(return_value=True)
        
        result = await repository.update_assignment_status(test_assignment_id, AssignmentStatus.PUBLISHED)
        
        assert result is True
        repository.update_by_id.assert_called_once_with(test_assignment_id, {'status': AssignmentStatus.PUBLISHED.value})
    
    @pytest.mark.asyncio
    async def test_update_assignment_due_date_success(self, repository, mock_collection):
        """Test successful assignment due date update."""
        repository._collection = mock_collection
        
        test_assignment_id = str(ObjectId())
        new_due_date = datetime.utcnow() + timedelta(days=14)
        
        repository.update_by_id = AsyncMock(return_value=True)
        
        result = await repository.update_assignment_due_date(test_assignment_id, new_due_date)
        
        assert result is True
        repository.update_by_id.assert_called_once_with(test_assignment_id, {'due_date': new_due_date})
    
    @pytest.mark.asyncio
    async def test_get_assignment_stats_success(self, repository, mock_collection):
        """Test successful assignment stats retrieval."""
        repository._collection = mock_collection
        
        test_assignment_id = str(ObjectId())
        test_stats = {
            'assignment_id': test_assignment_id,
            'total_submissions': 25,
            'on_time_submissions': 20,
            'late_submissions': 5,
            'graded_submissions': 22,
            'average_grade': 85.5,
            'completion_rate': 88.0
        }
        
        repository.aggregate = AsyncMock(return_value=[test_stats])
        
        result = await repository.get_assignment_stats(test_assignment_id)
        
        assert result == test_stats
        repository.aggregate.assert_called_once()
    
    @pytest.mark.asyncio
    async def test_get_assignment_stats_not_found(self, repository, mock_collection):
        """Test assignment stats when assignment not found."""
        repository._collection = mock_collection
        
        test_assignment_id = str(ObjectId())
        
        repository.aggregate = AsyncMock(return_value=[])
        
        result = await repository.get_assignment_stats(test_assignment_id)
        
        assert result == {}
    
    @pytest.mark.asyncio
    async def test_get_assignments_with_stats_success(self, repository, mock_collection):
        """Test successful get assignments with stats."""
        repository._collection = mock_collection
        
        test_assignments = [
            {
                '_id': ObjectId(),
                'title': 'Assignment 1',
                'submission_count': 25,
                'graded_count': 22,
                'average_grade': 85.5
            },
            {
                '_id': ObjectId(),
                'title': 'Assignment 2',
                'submission_count': 30,
                'graded_count': 28,
                'average_grade': 88.0
            }
        ]
        
        repository.aggregate = AsyncMock(return_value=test_assignments)
        
        result = await repository.get_assignments_with_stats(skip=0, limit=10)
        
        assert result == test_assignments
        repository.aggregate.assert_called_once()
    
    @pytest.mark.asyncio
    async def test_get_assignments_by_points_range_success(self, repository, mock_collection):
        """Test successful get assignments by points range."""
        repository._collection = mock_collection
        
        test_assignments = [
            {'_id': ObjectId(), 'title': '50 Point Assignment'},
            {'_id': ObjectId(), 'title': '75 Point Assignment'}
        ]
        
        repository.get_many = AsyncMock(return_value=test_assignments)
        
        result = await repository.get_assignments_by_points_range(50.0, 100.0, skip=0, limit=10)
        
        assert result == test_assignments
        repository.get_many.assert_called_once_with(
            filter_dict={'max_points': {'$gte': 50.0, '$lte': 100.0}},
            skip=0,
            limit=10,
            sort=[('max_points', -1)]
        )
    
    @pytest.mark.asyncio
    async def test_get_late_assignments_by_course_success(self, repository, mock_collection):
        """Test successful get late assignments by course."""
        repository._collection = mock_collection
        
        test_course_id = str(ObjectId())
        test_assignments = [
            {'_id': ObjectId(), 'title': 'Late Assignment 1'},
            {'_id': ObjectId(), 'title': 'Late Assignment 2'}
        ]
        
        repository.get_many = AsyncMock(return_value=test_assignments)
        
        result = await repository.get_late_assignments_by_course(test_course_id, skip=0, limit=10)
        
        assert result == test_assignments
        repository.get_many.assert_called_once()
        
        # Check filter_dict contains course and overdue conditions
        call_args = repository.get_many.call_args
        filter_dict = call_args[1]['filter_dict']
        assert filter_dict['course_id'] == test_course_id
        assert 'due_date' in filter_dict
        assert 'status' in filter_dict
    
    @pytest.mark.asyncio
    async def test_bulk_update_status_success(self, repository, mock_collection):
        """Test successful bulk status update."""
        repository._collection = mock_collection
        
        test_assignment_ids = [str(ObjectId()), str(ObjectId())]
        
        repository.bulk_update = AsyncMock(return_value=2)
        
        result = await repository.bulk_update_status(test_assignment_ids, AssignmentStatus.PUBLISHED)
        
        assert result == 2
        repository.bulk_update.assert_called_once()
        
        # Check filter_dict and update_data
        call_args = repository.bulk_update.call_args
        filter_dict = call_args[0][0]
        update_data = call_args[0][1]
        
        assert '_id' in filter_dict
        assert '$in' in filter_dict['_id']
        assert update_data['status'] == AssignmentStatus.PUBLISHED.value
    
    @pytest.mark.asyncio
    async def test_get_assignments_by_course_and_status_success(self, repository, mock_collection):
        """Test successful get assignments by course and status."""
        repository._collection = mock_collection
        
        test_course_id = str(ObjectId())
        test_assignments = [
            {'_id': ObjectId(), 'title': 'Published Assignment 1'},
            {'_id': ObjectId(), 'title': 'Published Assignment 2'}
        ]
        
        repository.get_many = AsyncMock(return_value=test_assignments)
        
        result = await repository.get_assignments_by_course_and_status(test_course_id, AssignmentStatus.PUBLISHED, skip=0, limit=10)
        
        assert result == test_assignments
        repository.get_many.assert_called_once_with(
            filter_dict={
                'course_id': test_course_id,
                'status': AssignmentStatus.PUBLISHED.value
            },
            skip=0,
            limit=10,
            sort=[('due_date', 1)]
        )
    
    @pytest.mark.asyncio
    async def test_create_assignment_indexes_success(self, repository, mock_collection):
        """Test successful assignment indexes creation."""
        repository._collection = mock_collection
        
        repository.create_indexes = AsyncMock()
        
        await repository.create_assignment_indexes()
        
        repository.create_indexes.assert_called_once()
        
        # Check that indexes were provided
        call_args = repository.create_indexes.call_args
        indexes = call_args[0][0]
        assert len(indexes) > 0
        
        # Check for specific indexes
        index_specs = [index[0] for index in indexes]
        assert ('course_id', 1) in index_specs
        assert ('instructor_id', 1) in index_specs
        assert ('assignment_type', 1) in index_specs
        assert ('status', 1) in index_specs
        assert ('due_date', 1) in index_specs
        assert ('max_points', 1) in index_specs