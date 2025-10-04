"""
Unit tests for SubmissionRepository.
"""
import pytest
from unittest.mock import AsyncMock, MagicMock, patch
from datetime import datetime
from bson import ObjectId

from src.app.repositories.submission_repository import SubmissionRepository
from src.app.models.submission import SubmissionStatus, SubmissionType
from src.app.exceptions.base import ConflictError


class TestSubmissionRepository:
    """Test SubmissionRepository functionality."""
    
    @pytest.fixture
    def repository(self):
        """Create submission repository instance."""
        return SubmissionRepository()
    
    @pytest.fixture
    def mock_collection(self):
        """Create mock collection."""
        return AsyncMock()
    
    @pytest.fixture
    def sample_submission_data(self):
        """Sample submission data for testing."""
        return {
            'assignment_id': str(ObjectId()),
            'student_id': str(ObjectId()),
            'submission_type': SubmissionType.TEXT.value,
            'status': SubmissionStatus.DRAFT.value,
            'content': 'Test submission content'
        }
    
    @pytest.mark.asyncio
    async def test_create_submission_success(self, repository, mock_collection, sample_submission_data):
        """Test successful submission creation."""
        repository._collection = mock_collection
        
        # Mock exists to return False (no conflict)
        repository.exists = AsyncMock(return_value=False)
        repository.create = AsyncMock(return_value=str(ObjectId()))
        
        result_id = await repository.create_submission(sample_submission_data)
        
        assert isinstance(result_id, str)
        repository.exists.assert_called_once_with({
            'assignment_id': sample_submission_data['assignment_id'],
            'student_id': sample_submission_data['student_id']
        })
        repository.create.assert_called_once_with(sample_submission_data)
    
    @pytest.mark.asyncio
    async def test_create_submission_conflict(self, repository, mock_collection, sample_submission_data):
        """Test submission creation with conflict."""
        repository._collection = mock_collection
        
        # Mock exists to return True (conflict)
        repository.exists = AsyncMock(return_value=True)
        
        with pytest.raises(ConflictError) as exc_info:
            await repository.create_submission(sample_submission_data)
        
        assert f"Student {sample_submission_data['student_id']} already has a submission for assignment {sample_submission_data['assignment_id']}" in str(exc_info.value)
    
    @pytest.mark.asyncio
    async def test_get_submissions_by_assignment_success(self, repository, mock_collection):
        """Test successful get submissions by assignment."""
        repository._collection = mock_collection
        
        test_assignment_id = str(ObjectId())
        test_submissions = [
            {'_id': ObjectId(), 'student_id': str(ObjectId())},
            {'_id': ObjectId(), 'student_id': str(ObjectId())}
        ]
        
        repository.get_many = AsyncMock(return_value=test_submissions)
        
        result = await repository.get_submissions_by_assignment(test_assignment_id, skip=0, limit=10)
        
        assert result == test_submissions
        repository.get_many.assert_called_once_with(
            filter_dict={'assignment_id': test_assignment_id},
            skip=0,
            limit=10,
            sort=[('submitted_at', -1)]
        )
    
    @pytest.mark.asyncio
    async def test_get_submissions_by_student_success(self, repository, mock_collection):
        """Test successful get submissions by student."""
        repository._collection = mock_collection
        
        test_student_id = str(ObjectId())
        test_submissions = [
            {'_id': ObjectId(), 'assignment_id': str(ObjectId())},
            {'_id': ObjectId(), 'assignment_id': str(ObjectId())}
        ]
        
        repository.get_many = AsyncMock(return_value=test_submissions)
        
        result = await repository.get_submissions_by_student(test_student_id, skip=0, limit=10)
        
        assert result == test_submissions
        repository.get_many.assert_called_once_with(
            filter_dict={'student_id': test_student_id},
            skip=0,
            limit=10,
            sort=[('submitted_at', -1)]
        )
    
    @pytest.mark.asyncio
    async def test_get_submissions_by_status_success(self, repository, mock_collection):
        """Test successful get submissions by status."""
        repository._collection = mock_collection
        
        test_submissions = [
            {'_id': ObjectId(), 'assignment_id': str(ObjectId())},
            {'_id': ObjectId(), 'assignment_id': str(ObjectId())}
        ]
        
        repository.get_many = AsyncMock(return_value=test_submissions)
        
        result = await repository.get_submissions_by_status(SubmissionStatus.SUBMITTED, skip=0, limit=10)
        
        assert result == test_submissions
        repository.get_many.assert_called_once_with(
            filter_dict={'status': SubmissionStatus.SUBMITTED.value},
            skip=0,
            limit=10,
            sort=[('submitted_at', -1)]
        )
    
    @pytest.mark.asyncio
    async def test_get_submissions_by_type_success(self, repository, mock_collection):
        """Test successful get submissions by type."""
        repository._collection = mock_collection
        
        test_submissions = [
            {'_id': ObjectId(), 'assignment_id': str(ObjectId())},
            {'_id': ObjectId(), 'assignment_id': str(ObjectId())}
        ]
        
        repository.get_many = AsyncMock(return_value=test_submissions)
        
        result = await repository.get_submissions_by_type(SubmissionType.TEXT, skip=0, limit=10)
        
        assert result == test_submissions
        repository.get_many.assert_called_once_with(
            filter_dict={'submission_type': SubmissionType.TEXT.value},
            skip=0,
            limit=10,
            sort=[('submitted_at', -1)]
        )
    
    @pytest.mark.asyncio
    async def test_get_late_submissions_success(self, repository, mock_collection):
        """Test successful get late submissions."""
        repository._collection = mock_collection
        
        test_submissions = [
            {'_id': ObjectId(), 'assignment_id': str(ObjectId()), 'is_late': True},
            {'_id': ObjectId(), 'assignment_id': str(ObjectId()), 'is_late': True}
        ]
        
        repository.get_many = AsyncMock(return_value=test_submissions)
        
        result = await repository.get_late_submissions(skip=0, limit=10)
        
        assert result == test_submissions
        repository.get_many.assert_called_once_with(
            filter_dict={'is_late': True},
            skip=0,
            limit=10,
            sort=[('submitted_at', -1)]
        )
    
    @pytest.mark.asyncio
    async def test_get_graded_submissions_success(self, repository, mock_collection):
        """Test successful get graded submissions."""
        repository._collection = mock_collection
        
        test_submissions = [
            {'_id': ObjectId(), 'assignment_id': str(ObjectId()), 'grade': 85.0},
            {'_id': ObjectId(), 'assignment_id': str(ObjectId()), 'grade': 90.0}
        ]
        
        repository.get_many = AsyncMock(return_value=test_submissions)
        
        result = await repository.get_graded_submissions(skip=0, limit=10)
        
        assert result == test_submissions
        repository.get_many.assert_called_once_with(
            filter_dict={'grade': {'$ne': None}},
            skip=0,
            limit=10,
            sort=[('graded_at', -1)]
        )
    
    @pytest.mark.asyncio
    async def test_get_ungraded_submissions_success(self, repository, mock_collection):
        """Test successful get ungraded submissions."""
        repository._collection = mock_collection
        
        test_submissions = [
            {'_id': ObjectId(), 'assignment_id': str(ObjectId()), 'grade': None},
            {'_id': ObjectId(), 'assignment_id': str(ObjectId()), 'grade': None}
        ]
        
        repository.get_many = AsyncMock(return_value=test_submissions)
        
        result = await repository.get_ungraded_submissions(skip=0, limit=10)
        
        assert result == test_submissions
        repository.get_many.assert_called_once_with(
            filter_dict={'grade': None},
            skip=0,
            limit=10,
            sort=[('submitted_at', 1)]
        )
    
    @pytest.mark.asyncio
    async def test_update_submission_status_success(self, repository, mock_collection):
        """Test successful submission status update."""
        repository._collection = mock_collection
        
        test_submission_id = str(ObjectId())
        
        repository.update_by_id = AsyncMock(return_value=True)
        
        with patch('src.app.repositories.submission_repository.datetime') as mock_datetime:
            mock_datetime.utcnow.return_value = datetime(2023, 1, 1, 12, 0, 0)
            
            result = await repository.update_submission_status(test_submission_id, SubmissionStatus.SUBMITTED)
        
        assert result is True
        repository.update_by_id.assert_called_once()
        
        # Check that submitted_at was added for SUBMITTED status
        call_args = repository.update_by_id.call_args
        update_data = call_args[0][1]
        assert update_data['status'] == SubmissionStatus.SUBMITTED.value
        assert 'submitted_at' in update_data
    
    @pytest.mark.asyncio
    async def test_grade_submission_success(self, repository, mock_collection):
        """Test successful submission grading."""
        repository._collection = mock_collection
        
        test_submission_id = str(ObjectId())
        grade = 85.0
        feedback = "Good work!"
        graded_by = str(ObjectId())
        
        repository.update_by_id = AsyncMock(return_value=True)
        
        with patch('src.app.repositories.submission_repository.datetime') as mock_datetime:
            mock_datetime.utcnow.return_value = datetime(2023, 1, 1, 12, 0, 0)
            
            result = await repository.grade_submission(test_submission_id, grade, feedback, graded_by)
        
        assert result is True
        repository.update_by_id.assert_called_once()
        
        # Check that grading data was added
        call_args = repository.update_by_id.call_args
        update_data = call_args[0][1]
        assert update_data['grade'] == grade
        assert update_data['feedback'] == feedback
        assert update_data['graded_by'] == graded_by
        assert update_data['status'] == SubmissionStatus.GRADED.value
        assert 'graded_at' in update_data
    
    @pytest.mark.asyncio
    async def test_get_submission_stats_success(self, repository, mock_collection):
        """Test successful submission stats retrieval."""
        repository._collection = mock_collection
        
        test_submission_id = str(ObjectId())
        test_stats = {
            'submission_id': test_submission_id,
            'assignment_title': 'Python Assignment',
            'assignment_due_date': datetime(2023, 1, 1),
            'student_name': 'John Doe',
            'student_email': 'john@example.com',
            'percentage': 85.0,
            'final_grade': 85.0
        }
        
        repository.aggregate = AsyncMock(return_value=[test_stats])
        
        result = await repository.get_submission_stats(test_submission_id)
        
        assert result == test_stats
        repository.aggregate.assert_called_once()
    
    @pytest.mark.asyncio
    async def test_get_submission_stats_not_found(self, repository, mock_collection):
        """Test submission stats when submission not found."""
        repository._collection = mock_collection
        
        test_submission_id = str(ObjectId())
        
        repository.aggregate = AsyncMock(return_value=[])
        
        result = await repository.get_submission_stats(test_submission_id)
        
        assert result == {}
    
    @pytest.mark.asyncio
    async def test_get_submissions_with_stats_success(self, repository, mock_collection):
        """Test successful get submissions with stats."""
        repository._collection = mock_collection
        
        test_submissions = [
            {
                '_id': ObjectId(),
                'assignment_title': 'Python Assignment',
                'assignment_due_date': datetime(2023, 1, 1),
                'student_name': 'John Doe',
                'student_email': 'john@example.com',
                'percentage': 85.0,
                'final_grade': 85.0
            }
        ]
        
        repository.aggregate = AsyncMock(return_value=test_submissions)
        
        result = await repository.get_submissions_with_stats(skip=0, limit=10)
        
        assert result == test_submissions
        repository.aggregate.assert_called_once()
    
    @pytest.mark.asyncio
    async def test_get_assignment_submission_stats_success(self, repository, mock_collection):
        """Test successful get assignment submission stats."""
        repository._collection = mock_collection
        
        test_assignment_id = str(ObjectId())
        test_stats = {
            'assignment_id': test_assignment_id,
            'total_submissions': 25,
            'submitted_submissions': 20,
            'late_submissions': 5,
            'graded_submissions': 18,
            'average_grade': 85.5,
            'completion_rate': 80.0
        }
        
        repository.aggregate = AsyncMock(return_value=[test_stats])
        
        result = await repository.get_assignment_submission_stats(test_assignment_id)
        
        assert result == test_stats
        repository.aggregate.assert_called_once()
    
    @pytest.mark.asyncio
    async def test_get_student_submission_stats_success(self, repository, mock_collection):
        """Test successful get student submission stats."""
        repository._collection = mock_collection
        
        test_student_id = str(ObjectId())
        test_stats = {
            'student_id': test_student_id,
            'total_submissions': 15,
            'submitted_submissions': 12,
            'late_submissions': 2,
            'graded_submissions': 10,
            'average_grade': 88.0,
            'completion_rate': 80.0
        }
        
        repository.aggregate = AsyncMock(return_value=[test_stats])
        
        result = await repository.get_student_submission_stats(test_student_id)
        
        assert result == test_stats
        repository.aggregate.assert_called_once()
    
    @pytest.mark.asyncio
    async def test_get_submissions_by_date_range_success(self, repository, mock_collection):
        """Test successful get submissions by date range."""
        repository._collection = mock_collection
        
        start_date = datetime(2023, 1, 1)
        end_date = datetime(2023, 12, 31)
        test_submissions = [
            {'_id': ObjectId(), 'assignment_id': str(ObjectId())},
            {'_id': ObjectId(), 'assignment_id': str(ObjectId())}
        ]
        
        repository.get_many = AsyncMock(return_value=test_submissions)
        
        result = await repository.get_submissions_by_date_range(start_date, end_date, skip=0, limit=10)
        
        assert result == test_submissions
        repository.get_many.assert_called_once()
        
        # Check filter_dict contains date range
        call_args = repository.get_many.call_args
        filter_dict = call_args[1]['filter_dict']
        assert 'submitted_at' in filter_dict
    
    @pytest.mark.asyncio
    async def test_bulk_grade_submissions_success(self, repository, mock_collection):
        """Test successful bulk grade submissions."""
        repository._collection = mock_collection
        
        test_submission_ids = [str(ObjectId()), str(ObjectId())]
        grade = 85.0
        feedback = "Good work!"
        graded_by = str(ObjectId())
        
        repository.bulk_update = AsyncMock(return_value=2)
        
        with patch('src.app.repositories.submission_repository.datetime') as mock_datetime:
            mock_datetime.utcnow.return_value = datetime(2023, 1, 1, 12, 0, 0)
            
            result = await repository.bulk_grade_submissions(test_submission_ids, grade, feedback, graded_by)
        
        assert result == 2
        repository.bulk_update.assert_called_once()
        
        # Check filter_dict and update_data
        call_args = repository.bulk_update.call_args
        filter_dict = call_args[0][0]
        update_data = call_args[0][1]
        
        assert '_id' in filter_dict
        assert '$in' in filter_dict['_id']
        assert update_data['grade'] == grade
        assert update_data['feedback'] == feedback
        assert update_data['graded_by'] == graded_by
        assert update_data['status'] == SubmissionStatus.GRADED.value
        assert 'graded_at' in update_data
    
    @pytest.mark.asyncio
    async def test_bulk_create_submissions_success(self, repository, mock_collection):
        """Test successful bulk create submissions."""
        repository._collection = mock_collection
        
        submission_data_list = [
            {'assignment_id': str(ObjectId()), 'student_id': str(ObjectId())},
            {'assignment_id': str(ObjectId()), 'student_id': str(ObjectId())}
        ]
        
        # Mock exists to return False for all (no conflicts)
        repository.exists = AsyncMock(return_value=False)
        repository.bulk_create = AsyncMock(return_value=[str(ObjectId()), str(ObjectId())])
        
        result_ids = await repository.bulk_create_submissions(submission_data_list)
        
        assert len(result_ids) == 2
        assert all(isinstance(id_val, str) for id_val in result_ids)
        repository.bulk_create.assert_called_once_with(submission_data_list)
    
    @pytest.mark.asyncio
    async def test_bulk_create_submissions_conflict(self, repository, mock_collection):
        """Test bulk create submissions with conflicts."""
        repository._collection = mock_collection
        
        submission_data_list = [
            {'assignment_id': str(ObjectId()), 'student_id': str(ObjectId())},
            {'assignment_id': str(ObjectId()), 'student_id': str(ObjectId())}
        ]
        
        # Mock exists to return True for first submission (conflict)
        repository.exists = AsyncMock(side_effect=[True, False])
        
        with pytest.raises(ConflictError) as exc_info:
            await repository.bulk_create_submissions(submission_data_list)
        
        assert "Some submissions already exist" in str(exc_info.value)
    
    @pytest.mark.asyncio
    async def test_create_submission_indexes_success(self, repository, mock_collection):
        """Test successful submission indexes creation."""
        repository._collection = mock_collection
        
        repository.create_indexes = AsyncMock()
        
        await repository.create_submission_indexes()
        
        repository.create_indexes.assert_called_once()
        
        # Check that indexes were provided
        call_args = repository.create_indexes.call_args
        indexes = call_args[0][0]
        assert len(indexes) > 0
        
        # Check for specific indexes
        index_specs = [index[0] for index in indexes]
        assert ('assignment_id', 1) in index_specs
        assert ('student_id', 1) in index_specs
        assert ('status', 1) in index_specs
        assert ('submission_type', 1) in index_specs
        assert ('submitted_at', -1) in index_specs
        assert ('graded_at', -1) in index_specs
        assert ('is_late', 1) in index_specs
        assert ('grade', 1) in index_specs