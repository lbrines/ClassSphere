"""
Unit tests for UserRepository.
"""
import pytest
from unittest.mock import AsyncMock, MagicMock, patch
from datetime import datetime
from bson import ObjectId

from src.app.repositories.user_repository import UserRepository
from src.app.models.user import UserRole, UserStatus
from src.app.exceptions.base import ConflictError, DatabaseError


class TestUserRepository:
    """Test UserRepository functionality."""
    
    @pytest.fixture
    def repository(self):
        """Create user repository instance."""
        return UserRepository()
    
    @pytest.fixture
    def mock_collection(self):
        """Create mock collection."""
        return AsyncMock()
    
    @pytest.fixture
    def sample_user_data(self):
        """Sample user data for testing."""
        return {
            'email': 'test@example.com',
            'name': 'Test User',
            'role': UserRole.STUDENT.value,
            'status': UserStatus.ACTIVE.value
        }
    
    @pytest.mark.asyncio
    async def test_create_user_success(self, repository, mock_collection, sample_user_data):
        """Test successful user creation."""
        repository._collection = mock_collection
        
        # Mock exists to return False (no conflict)
        repository.exists = AsyncMock(return_value=False)
        repository.create = AsyncMock(return_value=str(ObjectId()))
        
        result_id = await repository.create_user(sample_user_data)
        
        assert isinstance(result_id, str)
        repository.exists.assert_called_once_with({'email': sample_user_data['email']})
        repository.create.assert_called_once_with(sample_user_data)
    
    @pytest.mark.asyncio
    async def test_create_user_email_conflict(self, repository, mock_collection, sample_user_data):
        """Test user creation with email conflict."""
        repository._collection = mock_collection
        
        # Mock exists to return True (conflict)
        repository.exists = AsyncMock(return_value=True)
        
        with pytest.raises(ConflictError) as exc_info:
            await repository.create_user(sample_user_data)
        
        assert f"User with email {sample_user_data['email']} already exists" in str(exc_info.value)
    
    @pytest.mark.asyncio
    async def test_get_user_by_email_success(self, repository, mock_collection):
        """Test successful get user by email."""
        repository._collection = mock_collection
        
        test_email = 'test@example.com'
        test_user = {
            '_id': ObjectId(),
            'email': test_email,
            'name': 'Test User'
        }
        
        repository.get_by_field = AsyncMock(return_value=test_user)
        
        result = await repository.get_user_by_email(test_email)
        
        assert result == test_user
        repository.get_by_field.assert_called_once_with('email', test_email.lower())
    
    @pytest.mark.asyncio
    async def test_get_user_by_email_not_found(self, repository, mock_collection):
        """Test get user by email when not found."""
        repository._collection = mock_collection
        
        repository.get_by_field = AsyncMock(return_value=None)
        
        result = await repository.get_user_by_email('nonexistent@example.com')
        
        assert result is None
    
    @pytest.mark.asyncio
    async def test_get_user_by_google_id_success(self, repository, mock_collection):
        """Test successful get user by Google ID."""
        repository._collection = mock_collection
        
        test_google_id = 'google123'
        test_user = {
            '_id': ObjectId(),
            'google_id': test_google_id,
            'name': 'Test User'
        }
        
        repository.get_by_field = AsyncMock(return_value=test_user)
        
        result = await repository.get_user_by_google_id(test_google_id)
        
        assert result == test_user
        repository.get_by_field.assert_called_once_with('google_id', test_google_id)
    
    @pytest.mark.asyncio
    async def test_get_users_by_role_success(self, repository, mock_collection):
        """Test successful get users by role."""
        repository._collection = mock_collection
        
        test_users = [
            {'_id': ObjectId(), 'name': 'Student 1'},
            {'_id': ObjectId(), 'name': 'Student 2'}
        ]
        
        repository.get_many = AsyncMock(return_value=test_users)
        
        result = await repository.get_users_by_role(UserRole.STUDENT, skip=0, limit=10)
        
        assert result == test_users
        repository.get_many.assert_called_once_with(
            filter_dict={'role': UserRole.STUDENT.value},
            skip=0,
            limit=10,
            sort=[('created_at', -1)]
        )
    
    @pytest.mark.asyncio
    async def test_get_users_by_status_success(self, repository, mock_collection):
        """Test successful get users by status."""
        repository._collection = mock_collection
        
        test_users = [
            {'_id': ObjectId(), 'name': 'Active User 1'},
            {'_id': ObjectId(), 'name': 'Active User 2'}
        ]
        
        repository.get_many = AsyncMock(return_value=test_users)
        
        result = await repository.get_users_by_status(UserStatus.ACTIVE, skip=0, limit=10)
        
        assert result == test_users
        repository.get_many.assert_called_once_with(
            filter_dict={'status': UserStatus.ACTIVE.value},
            skip=0,
            limit=10,
            sort=[('created_at', -1)]
        )
    
    @pytest.mark.asyncio
    async def test_search_users_success(self, repository, mock_collection):
        """Test successful user search."""
        repository._collection = mock_collection
        
        test_users = [
            {'_id': ObjectId(), 'name': 'John Doe'},
            {'_id': ObjectId(), 'name': 'Jane Doe'}
        ]
        
        repository.get_many = AsyncMock(return_value=test_users)
        
        result = await repository.search_users('john', skip=0, limit=10)
        
        assert result == test_users
        repository.get_many.assert_called_once()
        
        # Check filter_dict contains regex search
        call_args = repository.get_many.call_args
        filter_dict = call_args[1]['filter_dict']
        assert '$or' in filter_dict
        assert len(filter_dict['$or']) == 2
    
    @pytest.mark.asyncio
    async def test_update_user_status_success(self, repository, mock_collection):
        """Test successful user status update."""
        repository._collection = mock_collection
        
        test_user_id = str(ObjectId())
        
        repository.update_by_id = AsyncMock(return_value=True)
        
        result = await repository.update_user_status(test_user_id, UserStatus.INACTIVE)
        
        assert result is True
        repository.update_by_id.assert_called_once_with(test_user_id, {'status': UserStatus.INACTIVE.value})
    
    @pytest.mark.asyncio
    async def test_update_user_role_success(self, repository, mock_collection):
        """Test successful user role update."""
        repository._collection = mock_collection
        
        test_user_id = str(ObjectId())
        
        repository.update_by_id = AsyncMock(return_value=True)
        
        result = await repository.update_user_role(test_user_id, UserRole.TEACHER)
        
        assert result is True
        repository.update_by_id.assert_called_once_with(test_user_id, {'role': UserRole.TEACHER.value})
    
    @pytest.mark.asyncio
    async def test_update_last_login_success(self, repository, mock_collection):
        """Test successful last login update."""
        repository._collection = mock_collection
        
        test_user_id = str(ObjectId())
        
        repository.update_by_id = AsyncMock(return_value=True)
        
        with patch('src.app.repositories.user_repository.datetime') as mock_datetime:
            mock_datetime.utcnow.return_value = datetime(2023, 1, 1, 12, 0, 0)
            
            result = await repository.update_last_login(test_user_id)
        
        assert result is True
        repository.update_by_id.assert_called_once()
        
        # Check that last_login was set
        call_args = repository.update_by_id.call_args
        update_data = call_args[0][1]
        assert 'last_login' in update_data
    
    @pytest.mark.asyncio
    async def test_get_user_stats_success(self, repository, mock_collection):
        """Test successful user stats retrieval."""
        repository._collection = mock_collection
        
        test_user_id = str(ObjectId())
        test_stats = {
            'user_id': test_user_id,
            'total_logins': 10,
            'courses_enrolled': 3,
            'assignments_completed': 15,
            'average_grade': 85.5
        }
        
        repository.aggregate = AsyncMock(return_value=[test_stats])
        
        result = await repository.get_user_stats(test_user_id)
        
        assert result == test_stats
        repository.aggregate.assert_called_once()
        
        # Check pipeline structure
        call_args = repository.aggregate.call_args
        pipeline = call_args[0][0]
        assert len(pipeline) > 0
        assert pipeline[0]['$match']['_id'] is not None
    
    @pytest.mark.asyncio
    async def test_get_user_stats_not_found(self, repository, mock_collection):
        """Test user stats when user not found."""
        repository._collection = mock_collection
        
        test_user_id = str(ObjectId())
        
        repository.aggregate = AsyncMock(return_value=[])
        
        result = await repository.get_user_stats(test_user_id)
        
        assert result == {}
    
    @pytest.mark.asyncio
    async def test_get_active_users_count_success(self, repository, mock_collection):
        """Test successful active users count."""
        repository._collection = mock_collection
        
        repository.count = AsyncMock(return_value=42)
        
        result = await repository.get_active_users_count()
        
        assert result == 42
        repository.count.assert_called_once_with({'status': UserStatus.ACTIVE.value})
    
    @pytest.mark.asyncio
    async def test_get_users_by_department_success(self, repository, mock_collection):
        """Test successful get users by department."""
        repository._collection = mock_collection
        
        test_users = [
            {'_id': ObjectId(), 'name': 'CS Student 1'},
            {'_id': ObjectId(), 'name': 'CS Student 2'}
        ]
        
        repository.get_many = AsyncMock(return_value=test_users)
        
        result = await repository.get_users_by_department('Computer Science', skip=0, limit=10)
        
        assert result == test_users
        repository.get_many.assert_called_once_with(
            filter_dict={'department': 'Computer Science'},
            skip=0,
            limit=10,
            sort=[('name', 1)]
        )
    
    @pytest.mark.asyncio
    async def test_bulk_update_status_success(self, repository, mock_collection):
        """Test successful bulk status update."""
        repository._collection = mock_collection
        
        test_user_ids = [str(ObjectId()), str(ObjectId())]
        
        repository.bulk_update = AsyncMock(return_value=2)
        
        result = await repository.bulk_update_status(test_user_ids, UserStatus.INACTIVE)
        
        assert result == 2
        repository.bulk_update.assert_called_once()
        
        # Check filter_dict and update_data
        call_args = repository.bulk_update.call_args
        filter_dict = call_args[0][0]
        update_data = call_args[0][1]
        
        assert '_id' in filter_dict
        assert '$in' in filter_dict['_id']
        assert update_data['status'] == UserStatus.INACTIVE.value
    
    @pytest.mark.asyncio
    async def test_create_user_indexes_success(self, repository, mock_collection):
        """Test successful user indexes creation."""
        repository._collection = mock_collection
        
        repository.create_indexes = AsyncMock()
        
        await repository.create_user_indexes()
        
        repository.create_indexes.assert_called_once()
        
        # Check that indexes were provided
        call_args = repository.create_indexes.call_args
        indexes = call_args[0][0]
        assert len(indexes) > 0
        
        # Check for specific indexes
        index_specs = [index[0] for index in indexes]
        assert ('email', 1) in index_specs
        assert ('google_id', 1) in index_specs
        assert ('role', 1) in index_specs
        assert ('status', 1) in index_specs