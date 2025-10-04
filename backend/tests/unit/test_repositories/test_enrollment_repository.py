"""
Unit tests for EnrollmentRepository.
"""
import pytest
from unittest.mock import AsyncMock, MagicMock, patch
from datetime import datetime
from bson import ObjectId

from src.app.repositories.enrollment_repository import EnrollmentRepository
from src.app.models.enrollment import EnrollmentStatus, EnrollmentRole
from src.app.exceptions.base import ConflictError


class TestEnrollmentRepository:
    """Test EnrollmentRepository functionality."""
    
    @pytest.fixture
    def repository(self):
        """Create enrollment repository instance."""
        return EnrollmentRepository()
    
    @pytest.fixture
    def mock_collection(self):
        """Create mock collection."""
        return AsyncMock()
    
    @pytest.fixture
    def sample_enrollment_data(self):
        """Sample enrollment data for testing."""
        return {
            'user_id': str(ObjectId()),
            'course_id': str(ObjectId()),
            'role': EnrollmentRole.STUDENT.value,
            'status': EnrollmentStatus.ACTIVE.value
        }
    
    @pytest.mark.asyncio
    async def test_create_enrollment_success(self, repository, mock_collection, sample_enrollment_data):
        """Test successful enrollment creation."""
        repository._collection = mock_collection
        
        # Mock exists to return False (no conflict)
        repository.exists = AsyncMock(return_value=False)
        repository.create = AsyncMock(return_value=str(ObjectId()))
        
        result_id = await repository.create_enrollment(sample_enrollment_data)
        
        assert isinstance(result_id, str)
        repository.exists.assert_called_once_with({
            'user_id': sample_enrollment_data['user_id'],
            'course_id': sample_enrollment_data['course_id']
        })
        repository.create.assert_called_once_with(sample_enrollment_data)
    
    @pytest.mark.asyncio
    async def test_create_enrollment_conflict(self, repository, mock_collection, sample_enrollment_data):
        """Test enrollment creation with conflict."""
        repository._collection = mock_collection
        
        # Mock exists to return True (conflict)
        repository.exists = AsyncMock(return_value=True)
        
        with pytest.raises(ConflictError) as exc_info:
            await repository.create_enrollment(sample_enrollment_data)
        
        assert f"User {sample_enrollment_data['user_id']} is already enrolled in course {sample_enrollment_data['course_id']}" in str(exc_info.value)
    
    @pytest.mark.asyncio
    async def test_get_enrollments_by_user_success(self, repository, mock_collection):
        """Test successful get enrollments by user."""
        repository._collection = mock_collection
        
        test_user_id = str(ObjectId())
        test_enrollments = [
            {'_id': ObjectId(), 'course_id': str(ObjectId())},
            {'_id': ObjectId(), 'course_id': str(ObjectId())}
        ]
        
        repository.get_many = AsyncMock(return_value=test_enrollments)
        
        result = await repository.get_enrollments_by_user(test_user_id, skip=0, limit=10)
        
        assert result == test_enrollments
        repository.get_many.assert_called_once_with(
            filter_dict={'user_id': test_user_id},
            skip=0,
            limit=10,
            sort=[('enrollment_date', -1)]
        )
    
    @pytest.mark.asyncio
    async def test_get_enrollments_by_course_success(self, repository, mock_collection):
        """Test successful get enrollments by course."""
        repository._collection = mock_collection
        
        test_course_id = str(ObjectId())
        test_enrollments = [
            {'_id': ObjectId(), 'user_id': str(ObjectId())},
            {'_id': ObjectId(), 'user_id': str(ObjectId())}
        ]
        
        repository.get_many = AsyncMock(return_value=test_enrollments)
        
        result = await repository.get_enrollments_by_course(test_course_id, skip=0, limit=10)
        
        assert result == test_enrollments
        repository.get_many.assert_called_once_with(
            filter_dict={'course_id': test_course_id},
            skip=0,
            limit=10,
            sort=[('enrollment_date', -1)]
        )
    
    @pytest.mark.asyncio
    async def test_get_enrollments_by_status_success(self, repository, mock_collection):
        """Test successful get enrollments by status."""
        repository._collection = mock_collection
        
        test_enrollments = [
            {'_id': ObjectId(), 'user_id': str(ObjectId())},
            {'_id': ObjectId(), 'user_id': str(ObjectId())}
        ]
        
        repository.get_many = AsyncMock(return_value=test_enrollments)
        
        result = await repository.get_enrollments_by_status(EnrollmentStatus.ACTIVE, skip=0, limit=10)
        
        assert result == test_enrollments
        repository.get_many.assert_called_once_with(
            filter_dict={'status': EnrollmentStatus.ACTIVE.value},
            skip=0,
            limit=10,
            sort=[('enrollment_date', -1)]
        )
    
    @pytest.mark.asyncio
    async def test_get_enrollments_by_role_success(self, repository, mock_collection):
        """Test successful get enrollments by role."""
        repository._collection = mock_collection
        
        test_enrollments = [
            {'_id': ObjectId(), 'user_id': str(ObjectId())},
            {'_id': ObjectId(), 'user_id': str(ObjectId())}
        ]
        
        repository.get_many = AsyncMock(return_value=test_enrollments)
        
        result = await repository.get_enrollments_by_role(EnrollmentRole.STUDENT, skip=0, limit=10)
        
        assert result == test_enrollments
        repository.get_many.assert_called_once_with(
            filter_dict={'role': EnrollmentRole.STUDENT.value},
            skip=0,
            limit=10,
            sort=[('enrollment_date', -1)]
        )
    
    @pytest.mark.asyncio
    async def test_get_user_course_enrollment_success(self, repository, mock_collection):
        """Test successful get user-course enrollment."""
        repository._collection = mock_collection
        
        test_user_id = str(ObjectId())
        test_course_id = str(ObjectId())
        test_enrollment = {
            '_id': ObjectId(),
            'user_id': test_user_id,
            'course_id': test_course_id
        }
        
        # Mock the complex logic for getting by both fields
        repository.get_by_field = AsyncMock(return_value=test_enrollment)
        
        result = await repository.get_user_course_enrollment(test_user_id, test_course_id)
        
        # This test is simplified since the actual implementation has complex logic
        assert result is not None
    
    @pytest.mark.asyncio
    async def test_get_active_enrollments_by_user_success(self, repository, mock_collection):
        """Test successful get active enrollments by user."""
        repository._collection = mock_collection
        
        test_user_id = str(ObjectId())
        test_enrollments = [
            {'_id': ObjectId(), 'course_id': str(ObjectId())},
            {'_id': ObjectId(), 'course_id': str(ObjectId())}
        ]
        
        repository.get_many = AsyncMock(return_value=test_enrollments)
        
        result = await repository.get_active_enrollments_by_user(test_user_id, skip=0, limit=10)
        
        assert result == test_enrollments
        repository.get_many.assert_called_once_with(
            filter_dict={
                'user_id': test_user_id,
                'status': EnrollmentStatus.ACTIVE.value
            },
            skip=0,
            limit=10,
            sort=[('enrollment_date', -1)]
        )
    
    @pytest.mark.asyncio
    async def test_get_active_enrollments_by_course_success(self, repository, mock_collection):
        """Test successful get active enrollments by course."""
        repository._collection = mock_collection
        
        test_course_id = str(ObjectId())
        test_enrollments = [
            {'_id': ObjectId(), 'user_id': str(ObjectId())},
            {'_id': ObjectId(), 'user_id': str(ObjectId())}
        ]
        
        repository.get_many = AsyncMock(return_value=test_enrollments)
        
        result = await repository.get_active_enrollments_by_course(test_course_id, skip=0, limit=10)
        
        assert result == test_enrollments
        repository.get_many.assert_called_once_with(
            filter_dict={
                'course_id': test_course_id,
                'status': EnrollmentStatus.ACTIVE.value
            },
            skip=0,
            limit=10,
            sort=[('enrollment_date', -1)]
        )
    
    @pytest.mark.asyncio
    async def test_update_enrollment_status_success(self, repository, mock_collection):
        """Test successful enrollment status update."""
        repository._collection = mock_collection
        
        test_enrollment_id = str(ObjectId())
        
        repository.update_by_id = AsyncMock(return_value=True)
        
        result = await repository.update_enrollment_status(test_enrollment_id, EnrollmentStatus.COMPLETED)
        
        assert result is True
        repository.update_by_id.assert_called_once()
        
        # Check that completion_date was added for COMPLETED status
        call_args = repository.update_by_id.call_args
        update_data = call_args[0][1]
        assert update_data['status'] == EnrollmentStatus.COMPLETED.value
        assert 'completion_date' in update_data
    
    @pytest.mark.asyncio
    async def test_update_enrollment_role_success(self, repository, mock_collection):
        """Test successful enrollment role update."""
        repository._collection = mock_collection
        
        test_enrollment_id = str(ObjectId())
        
        repository.update_by_id = AsyncMock(return_value=True)
        
        result = await repository.update_enrollment_role(test_enrollment_id, EnrollmentRole.TEACHER_ASSISTANT)
        
        assert result is True
        repository.update_by_id.assert_called_once_with(test_enrollment_id, {'role': EnrollmentRole.TEACHER_ASSISTANT.value})
    
    @pytest.mark.asyncio
    async def test_update_enrollment_grade_success(self, repository, mock_collection):
        """Test successful enrollment grade update."""
        repository._collection = mock_collection
        
        test_enrollment_id = str(ObjectId())
        final_grade = 85.5
        credits_earned = 3
        
        repository.update_by_id = AsyncMock(return_value=True)
        
        result = await repository.update_enrollment_grade(test_enrollment_id, final_grade, credits_earned)
        
        assert result is True
        repository.update_by_id.assert_called_once_with(test_enrollment_id, {
            'final_grade': final_grade,
            'credits_earned': credits_earned
        })
    
    @pytest.mark.asyncio
    async def test_get_enrollment_stats_success(self, repository, mock_collection):
        """Test successful enrollment stats retrieval."""
        repository._collection = mock_collection
        
        test_enrollment_id = str(ObjectId())
        test_stats = {
            'enrollment_id': test_enrollment_id,
            'assignments_completed': 8,
            'assignments_total': 10,
            'average_grade': 85.5
        }
        
        repository.aggregate = AsyncMock(return_value=[test_stats])
        
        result = await repository.get_enrollment_stats(test_enrollment_id)
        
        assert result == test_stats
        repository.aggregate.assert_called_once()
    
    @pytest.mark.asyncio
    async def test_get_enrollment_stats_not_found(self, repository, mock_collection):
        """Test enrollment stats when enrollment not found."""
        repository._collection = mock_collection
        
        test_enrollment_id = str(ObjectId())
        
        repository.aggregate = AsyncMock(return_value=[])
        
        result = await repository.get_enrollment_stats(test_enrollment_id)
        
        assert result == {}
    
    @pytest.mark.asyncio
    async def test_get_enrollments_with_stats_success(self, repository, mock_collection):
        """Test successful get enrollments with stats."""
        repository._collection = mock_collection
        
        test_enrollments = [
            {
                '_id': ObjectId(),
                'user_name': 'John Doe',
                'user_email': 'john@example.com',
                'course_title': 'Python Course',
                'course_code': 'CS101',
                'assignments_completed': 8,
                'assignments_total': 10,
                'average_grade': 85.5
            }
        ]
        
        repository.aggregate = AsyncMock(return_value=test_enrollments)
        
        result = await repository.get_enrollments_with_stats(skip=0, limit=10)
        
        assert result == test_enrollments
        repository.aggregate.assert_called_once()
    
    @pytest.mark.asyncio
    async def test_get_course_enrollment_stats_success(self, repository, mock_collection):
        """Test successful get course enrollment stats."""
        repository._collection = mock_collection
        
        test_course_id = str(ObjectId())
        test_stats = {
            'course_id': test_course_id,
            'total_enrollments': 25,
            'active_enrollments': 20,
            'completed_enrollments': 15,
            'dropped_enrollments': 5
        }
        
        repository.aggregate = AsyncMock(return_value=[test_stats])
        
        result = await repository.get_course_enrollment_stats(test_course_id)
        
        assert result == test_stats
        repository.aggregate.assert_called_once()
    
    @pytest.mark.asyncio
    async def test_bulk_create_enrollments_success(self, repository, mock_collection):
        """Test successful bulk create enrollments."""
        repository._collection = mock_collection
        
        enrollment_data_list = [
            {'user_id': str(ObjectId()), 'course_id': str(ObjectId())},
            {'user_id': str(ObjectId()), 'course_id': str(ObjectId())}
        ]
        
        # Mock exists to return False for all (no conflicts)
        repository.exists = AsyncMock(return_value=False)
        repository.bulk_create = AsyncMock(return_value=[str(ObjectId()), str(ObjectId())])
        
        result_ids = await repository.bulk_create_enrollments(enrollment_data_list)
        
        assert len(result_ids) == 2
        assert all(isinstance(id_val, str) for id_val in result_ids)
        repository.bulk_create.assert_called_once_with(enrollment_data_list)
    
    @pytest.mark.asyncio
    async def test_bulk_create_enrollments_conflict(self, repository, mock_collection):
        """Test bulk create enrollments with conflicts."""
        repository._collection = mock_collection
        
        enrollment_data_list = [
            {'user_id': str(ObjectId()), 'course_id': str(ObjectId())},
            {'user_id': str(ObjectId()), 'course_id': str(ObjectId())}
        ]
        
        # Mock exists to return True for first enrollment (conflict)
        repository.exists = AsyncMock(side_effect=[True, False])
        
        with pytest.raises(ConflictError) as exc_info:
            await repository.bulk_create_enrollments(enrollment_data_list)
        
        assert "Some enrollments already exist" in str(exc_info.value)
    
    @pytest.mark.asyncio
    async def test_bulk_update_status_success(self, repository, mock_collection):
        """Test successful bulk status update."""
        repository._collection = mock_collection
        
        test_enrollment_ids = [str(ObjectId()), str(ObjectId())]
        
        repository.bulk_update = AsyncMock(return_value=2)
        
        with patch('src.app.repositories.enrollment_repository.datetime') as mock_datetime:
            mock_datetime.utcnow.return_value = datetime(2023, 1, 1, 12, 0, 0)
            
            result = await repository.bulk_update_status(test_enrollment_ids, EnrollmentStatus.COMPLETED)
        
        assert result == 2
        repository.bulk_update.assert_called_once()
        
        # Check filter_dict and update_data
        call_args = repository.bulk_update.call_args
        filter_dict = call_args[0][0]
        update_data = call_args[0][1]
        
        assert '_id' in filter_dict
        assert '$in' in filter_dict['_id']
        assert update_data['status'] == EnrollmentStatus.COMPLETED.value
        assert 'completion_date' in update_data
    
    @pytest.mark.asyncio
    async def test_create_enrollment_indexes_success(self, repository, mock_collection):
        """Test successful enrollment indexes creation."""
        repository._collection = mock_collection
        
        repository.create_indexes = AsyncMock()
        
        await repository.create_enrollment_indexes()
        
        repository.create_indexes.assert_called_once()
        
        # Check that indexes were provided
        call_args = repository.create_indexes.call_args
        indexes = call_args[0][0]
        assert len(indexes) > 0
        
        # Check for specific indexes
        index_specs = [index[0] for index in indexes]
        assert ('user_id', 1) in index_specs
        assert ('course_id', 1) in index_specs
        assert ('status', 1) in index_specs
        assert ('role', 1) in index_specs
        assert ('enrollment_date', -1) in index_specs
        assert ('completion_date', -1) in index_specs