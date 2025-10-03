"""
Unit tests for user models.
"""
import pytest
from datetime import datetime
from pydantic import ValidationError
from src.app.models.user import (
    UserRole, UserStatus, UserBase, UserCreate, UserUpdate,
    UserResponse, UserLogin, UserProfile, UserStats, UserSearch
)


class TestUserEnums:
    """Test user enums."""
    
    def test_user_role_enum(self):
        """Test UserRole enum values."""
        assert UserRole.ADMIN == "admin"
        assert UserRole.TEACHER == "teacher"
        assert UserRole.STUDENT == "student"
        assert UserRole.COORDINATOR == "coordinator"
    
    def test_user_status_enum(self):
        """Test UserStatus enum values."""
        assert UserStatus.ACTIVE == "active"
        assert UserStatus.INACTIVE == "inactive"
        assert UserStatus.PENDING == "pending"
        assert UserStatus.SUSPENDED == "suspended"


class TestUserBase:
    """Test UserBase model."""
    
    def test_user_base_valid_data(self):
        """Test UserBase with valid data."""
        user = UserBase(
            email="test@example.com",
            name="Test User",
            role=UserRole.STUDENT,
            status=UserStatus.ACTIVE
        )
        
        assert user.email == "test@example.com"
        assert user.name == "Test User"
        assert user.role == UserRole.STUDENT
        assert user.status == UserStatus.ACTIVE
        assert user.google_id is None
        assert user.avatar_url is None
        assert user.phone is None
        assert user.department is None
        assert user.grade_level is None
        assert isinstance(user.created_at, datetime)
        assert isinstance(user.updated_at, datetime)
        assert user.last_login is None
    
    def test_user_base_with_optional_fields(self):
        """Test UserBase with optional fields."""
        user = UserBase(
            email="test@example.com",
            name="Test User",
            google_id="google123",
            avatar_url="https://example.com/avatar.jpg",
            phone="+1234567890",
            department="Computer Science",
            grade_level="12"
        )
        
        assert user.google_id == "google123"
        assert user.avatar_url == "https://example.com/avatar.jpg"
        assert user.phone == "+1234567890"
        assert user.department == "Computer Science"
        assert user.grade_level == "12"
    
    def test_user_base_email_validation(self):
        """Test UserBase email validation."""
        # Valid email
        user = UserBase(email="test@example.com", name="Test User")
        assert user.email == "test@example.com"
        
        # Invalid email
        with pytest.raises(ValidationError) as exc_info:
            UserBase(email="invalid-email", name="Test User")
        assert "Invalid email format" in str(exc_info.value)
        
        # Email normalization
        user = UserBase(email="TEST@EXAMPLE.COM", name="Test User")
        assert user.email == "test@example.com"
    
    def test_user_base_name_validation(self):
        """Test UserBase name validation."""
        # Valid name
        user = UserBase(email="test@example.com", name="Test User")
        assert user.name == "Test User"
        
        # Empty name - Pydantic v2 validates min_length first
        with pytest.raises(ValidationError) as exc_info:
            UserBase(email="test@example.com", name="")
        # Pydantic v2 gives a different error message for min_length
        assert "String should have at least 2 characters" in str(exc_info.value)
        
        # Name normalization
        user = UserBase(email="test@example.com", name="  test user  ")
        assert user.name == "Test User"
    
    def test_user_base_model_config(self):
        """Test UserBase model configuration."""
        user = UserBase(email="test@example.com", name="Test User")
        
        # Test model_dump
        data = user.model_dump()
        assert "email" in data
        assert "name" in data
        assert "created_at" in data
        assert "updated_at" in data
        
        # Test model_dump with exclude
        data = user.model_dump(exclude={"created_at", "updated_at"})
        assert "created_at" not in data
        assert "updated_at" not in data


class TestUserCreate:
    """Test UserCreate model."""
    
    def test_user_create_valid_data(self):
        """Test UserCreate with valid data."""
        user = UserCreate(
            email="test@example.com",
            name="Test User",
            password="SecurePass123!",
            confirm_password="SecurePass123!"
        )
        
        assert user.email == "test@example.com"
        assert user.name == "Test User"
        assert user.password == "SecurePass123!"
        assert user.confirm_password == "SecurePass123!"
        assert user.role == UserRole.STUDENT
        assert user.status == UserStatus.ACTIVE
    
    def test_user_create_password_validation(self):
        """Test UserCreate password validation."""
        # Valid password
        user = UserCreate(
            email="test@example.com",
            name="Test User",
            password="SecurePass123!",
            confirm_password="SecurePass123!"
        )
        assert user.password == "SecurePass123!"
        
        # Password too short - Pydantic v2 validates min_length first
        with pytest.raises(ValidationError) as exc_info:
            UserCreate(
                email="test@example.com",
                name="Test User",
                password="short",
                confirm_password="short"
            )
        # Pydantic v2 gives a different error message for min_length
        assert "String should have at least 8 characters" in str(exc_info.value)
        
        # Password without uppercase
        with pytest.raises(ValidationError) as exc_info:
            UserCreate(
                email="test@example.com",
                name="Test User",
                password="securepass123!",
                confirm_password="securepass123!"
            )
        assert "Password must contain uppercase" in str(exc_info.value)
        
        # Password without lowercase - Pydantic v2 gives combined error message
        with pytest.raises(ValidationError) as exc_info:
            UserCreate(
                email="test@example.com",
                name="Test User",
                password="SECUREPASS123!",
                confirm_password="SECUREPASS123!"
            )
        # Pydantic v2 gives a combined error message for all missing requirements
        assert "Password must contain uppercase, lowercase, digit and special character" in str(exc_info.value)
        
        # Password without digit - Pydantic v2 gives combined error message
        with pytest.raises(ValidationError) as exc_info:
            UserCreate(
                email="test@example.com",
                name="Test User",
                password="SecurePass!",
                confirm_password="SecurePass!"
            )
        # Pydantic v2 gives a combined error message for all missing requirements
        assert "Password must contain uppercase, lowercase, digit and special character" in str(exc_info.value)
        
        # Password without special character - Pydantic v2 gives combined error message
        with pytest.raises(ValidationError) as exc_info:
            UserCreate(
                email="test@example.com",
                name="Test User",
                password="SecurePass123",
                confirm_password="SecurePass123"
            )
        # Pydantic v2 gives a combined error message for all missing requirements
        assert "Password must contain uppercase, lowercase, digit and special character" in str(exc_info.value)
    
    def test_user_create_password_confirmation(self):
        """Test UserCreate password confirmation."""
        # Matching passwords
        user = UserCreate(
            email="test@example.com",
            name="Test User",
            password="SecurePass123!",
            confirm_password="SecurePass123!"
        )
        assert user.confirm_password == "SecurePass123!"
        
        # Non-matching passwords
        with pytest.raises(ValidationError) as exc_info:
            UserCreate(
                email="test@example.com",
                name="Test User",
                password="SecurePass123!",
                confirm_password="DifferentPass123!"
            )
        assert "Passwords do not match" in str(exc_info.value)


class TestUserUpdate:
    """Test UserUpdate model."""
    
    def test_user_update_valid_data(self):
        """Test UserUpdate with valid data."""
        user = UserUpdate(
            name="Updated User",
            role=UserRole.TEACHER,
            phone="+1234567890"
        )
        
        assert user.name == "Updated User"
        assert user.role == UserRole.TEACHER
        assert user.phone == "+1234567890"
        assert user.status is None
        assert user.department is None
    
    def test_user_update_name_validation(self):
        """Test UserUpdate name validation."""
        # Valid name
        user = UserUpdate(name="Updated User")
        assert user.name == "Updated User"
        
        # Empty name - Pydantic v2 validates min_length first
        with pytest.raises(ValidationError) as exc_info:
            UserUpdate(name="")
        # Pydantic v2 gives a different error message for min_length
        assert "String should have at least 2 characters" in str(exc_info.value)
        
        # Name normalization
        user = UserUpdate(name="  updated user  ")
        assert user.name == "Updated User"
    
    def test_user_update_all_none(self):
        """Test UserUpdate with all None values."""
        user = UserUpdate()
        
        assert user.name is None
        assert user.role is None
        assert user.status is None
        assert user.phone is None
        assert user.department is None
        assert user.grade_level is None
        assert user.avatar_url is None


class TestUserResponse:
    """Test UserResponse model."""
    
    def test_user_response_valid_data(self):
        """Test UserResponse with valid data."""
        user = UserResponse(
            user_id="user123",
            email="test@example.com",
            name="Test User",
            role=UserRole.STUDENT,
            status=UserStatus.ACTIVE,
            permissions=["read:own_courses"],
            is_verified=True
        )
        
        assert user.user_id == "user123"
        assert user.email == "test@example.com"
        assert user.name == "Test User"
        assert user.role == UserRole.STUDENT
        assert user.status == UserStatus.ACTIVE
        assert user.permissions == ["read:own_courses"]
        assert user.is_verified is True


class TestUserLogin:
    """Test UserLogin model."""
    
    def test_user_login_valid_data(self):
        """Test UserLogin with valid data."""
        login = UserLogin(
            email="test@example.com",
            password="SecurePass123!",
            remember_me=True
        )
        
        assert login.email == "test@example.com"
        assert login.password == "SecurePass123!"
        assert login.remember_me is True
    
    def test_user_login_email_validation(self):
        """Test UserLogin email validation."""
        # Valid email
        login = UserLogin(email="test@example.com", password="password")
        assert login.email == "test@example.com"
        
        # Invalid email
        with pytest.raises(ValidationError) as exc_info:
            UserLogin(email="invalid-email", password="password")
        assert "Invalid email format" in str(exc_info.value)
        
        # Email normalization
        login = UserLogin(email="TEST@EXAMPLE.COM", password="password")
        assert login.email == "test@example.com"


class TestUserProfile:
    """Test UserProfile model."""
    
    def test_user_profile_valid_data(self):
        """Test UserProfile with valid data."""
        profile = UserProfile(
            user_id="user123",
            name="Test User",
            role=UserRole.STUDENT,
            avatar_url="https://example.com/avatar.jpg",
            department="Computer Science",
            grade_level="12"
        )
        
        assert profile.user_id == "user123"
        assert profile.name == "Test User"
        assert profile.role == UserRole.STUDENT
        assert profile.avatar_url == "https://example.com/avatar.jpg"
        assert profile.department == "Computer Science"
        assert profile.grade_level == "12"


class TestUserStats:
    """Test UserStats model."""
    
    def test_user_stats_valid_data(self):
        """Test UserStats with valid data."""
        stats = UserStats(
            user_id="user123",
            total_logins=10,
            last_login=datetime.utcnow(),
            courses_enrolled=5,
            assignments_completed=20,
            average_grade=85.5
        )
        
        assert stats.user_id == "user123"
        assert stats.total_logins == 10
        assert isinstance(stats.last_login, datetime)
        assert stats.courses_enrolled == 5
        assert stats.assignments_completed == 20
        assert stats.average_grade == 85.5
    
    def test_user_stats_default_values(self):
        """Test UserStats with default values."""
        stats = UserStats(user_id="user123")
        
        assert stats.user_id == "user123"
        assert stats.total_logins == 0
        assert stats.last_login is None
        assert stats.courses_enrolled == 0
        assert stats.assignments_completed == 0
        assert stats.average_grade is None


class TestUserSearch:
    """Test UserSearch model."""
    
    def test_user_search_valid_data(self):
        """Test UserSearch with valid data."""
        search = UserSearch(
            query="test user",
            role=UserRole.STUDENT,
            status=UserStatus.ACTIVE,
            department="Computer Science",
            limit=50,
            offset=10
        )
        
        assert search.query == "test user"
        assert search.role == UserRole.STUDENT
        assert search.status == UserStatus.ACTIVE
        assert search.department == "Computer Science"
        assert search.limit == 50
        assert search.offset == 10
    
    def test_user_search_query_validation(self):
        """Test UserSearch query validation."""
        # Valid query
        search = UserSearch(query="test user")
        assert search.query == "test user"
        
        # Empty query - Pydantic v2 validates min_length first
        with pytest.raises(ValidationError) as exc_info:
            UserSearch(query="")
        # Pydantic v2 gives a different error message for min_length
        assert "String should have at least 1 character" in str(exc_info.value)
        
        # Query normalization
        search = UserSearch(query="  test user  ")
        assert search.query == "test user"
    
    def test_user_search_limit_validation(self):
        """Test UserSearch limit validation."""
        # Valid limit
        search = UserSearch(query="test", limit=20)
        assert search.limit == 20
        
        # Limit too low
        with pytest.raises(ValidationError) as exc_info:
            UserSearch(query="test", limit=0)
        assert "greater than or equal to 1" in str(exc_info.value)
        
        # Limit too high
        with pytest.raises(ValidationError) as exc_info:
            UserSearch(query="test", limit=101)
        assert "less than or equal to 100" in str(exc_info.value)
    
    def test_user_search_offset_validation(self):
        """Test UserSearch offset validation."""
        # Valid offset
        search = UserSearch(query="test", offset=10)
        assert search.offset == 10
        
        # Negative offset
        with pytest.raises(ValidationError) as exc_info:
            UserSearch(query="test", offset=-1)
        assert "greater than or equal to 0" in str(exc_info.value)
    
    def test_user_search_default_values(self):
        """Test UserSearch with default values."""
        search = UserSearch(query="test")
        
        assert search.query == "test"
        assert search.role is None
        assert search.status is None
        assert search.department is None
        assert search.limit == 20
        assert search.offset == 0