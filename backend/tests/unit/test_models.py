import pytest
from src.app.models.user import User, UserRole, UserCreate, UserUpdate, UserInDB
from pydantic import ValidationError

class TestUserModels:
    def test_user_role_enum(self):
        """Test UserRole enum values."""
        assert UserRole.ADMIN.value == "admin"
        assert UserRole.COORDINATOR.value == "coordinador"
        assert UserRole.TEACHER.value == "teacher"
        assert UserRole.STUDENT.value == "estudiante"
    
    def test_user_create_valid(self):
        """Test UserCreate model with valid data."""
        user_data = {
            "email": "test@example.com",
            "name": "Test User",
            "role": UserRole.STUDENT,
            "password": "password123"
        }
        
        user = UserCreate(**user_data)
        assert user.email == "test@example.com"
        assert user.name == "Test User"
        assert user.role == UserRole.STUDENT
        assert user.password == "password123"
    
    def test_user_create_invalid_email(self):
        """Test UserCreate model with invalid email."""
        user_data = {
            "email": "invalid-email",
            "name": "Test User",
            "role": UserRole.STUDENT,
            "password": "password123"
        }
        
        with pytest.raises(ValidationError):
            UserCreate(**user_data)
    
    def test_user_create_missing_fields(self):
        """Test UserCreate model with missing required fields."""
        with pytest.raises(ValidationError):
            UserCreate(email="test@example.com")
    
    def test_user_update_partial(self):
        """Test UserUpdate model with partial data."""
        user_data = {
            "name": "Updated Name"
        }
        
        user = UserUpdate(**user_data)
        assert user.name == "Updated Name"
        assert user.role is None
        assert user.is_active is None
    
    def test_user_update_all_fields(self):
        """Test UserUpdate model with all fields."""
        user_data = {
            "name": "Updated Name",
            "role": UserRole.TEACHER,
            "is_active": False
        }
        
        user = UserUpdate(**user_data)
        assert user.name == "Updated Name"
        assert user.role == UserRole.TEACHER
        assert user.is_active == False
    
    def test_user_in_db_model(self):
        """Test UserInDB model structure."""
        user_data = {
            "id": "123e4567-e89b-12d3-a456-426614174000",
            "email": "test@example.com",
            "name": "Test User",
            "role": UserRole.STUDENT,
            "google_id": "google123",
            "is_active": True,
            "created_at": "2025-01-27T12:00:00Z",
            "updated_at": "2025-01-27T12:00:00Z",
            "last_login": "2025-01-27T12:00:00Z"
        }
        
        user = UserInDB(**user_data)
        assert user.email == "test@example.com"
        assert user.name == "Test User"
        assert user.role == UserRole.STUDENT
        assert user.google_id == "google123"
        assert user.is_active == True
    
    def test_user_default_role(self):
        """Test that UserCreate defaults to STUDENT role."""
        user_data = {
            "email": "test@example.com",
            "name": "Test User",
            "password": "password123"
        }
        
        user = UserCreate(**user_data)
        assert user.role == UserRole.STUDENT
