"""Tests for ServiceFactory."""

import pytest
from unittest.mock import patch, MagicMock

from src.app.services.service_factory import ServiceFactory, MockOAuthService, MockClassroomService
from src.app.services.auth_service import AuthService
from src.app.services.oauth_service import OAuthService
from src.app.core.exceptions import ServiceUnavailableError


class TestServiceFactory:
    """Test cases for ServiceFactory."""

    def test_get_auth_service(self):
        """Test getting auth service."""
        service = ServiceFactory.get_auth_service()
        assert isinstance(service, AuthService)

    @patch('src.app.services.service_factory.settings')
    def test_get_oauth_service_google_mode(self, mock_settings):
        """Test getting OAuth service in Google mode."""
        mock_settings.google_mode = True
        mock_settings.mock_mode = False
        
        service = ServiceFactory.get_oauth_service()
        assert isinstance(service, OAuthService)

    @patch('src.app.services.service_factory.settings')
    def test_get_oauth_service_mock_mode(self, mock_settings):
        """Test getting OAuth service in Mock mode."""
        mock_settings.google_mode = False
        mock_settings.mock_mode = True
        
        service = ServiceFactory.get_oauth_service()
        assert isinstance(service, MockOAuthService)

    @patch('src.app.services.service_factory.settings')
    def test_get_classroom_service_mock_mode(self, mock_settings):
        """Test getting classroom service in Mock mode."""
        mock_settings.google_mode = False
        mock_settings.mock_mode = True
        
        service = ServiceFactory.get_classroom_service()
        assert isinstance(service, MockClassroomService)

    @patch('src.app.services.service_factory.settings')
    def test_get_classroom_service_google_mode(self, mock_settings):
        """Test getting classroom service in Google mode."""
        mock_settings.google_mode = True
        mock_settings.mock_mode = False
        
        with pytest.raises(ServiceUnavailableError, match="Google Classroom service not yet implemented"):
            ServiceFactory.get_classroom_service()

    @patch('src.app.services.service_factory.settings')
    def test_is_google_mode(self, mock_settings):
        """Test checking Google mode."""
        mock_settings.google_mode = True
        assert ServiceFactory.is_google_mode() is True
        
        mock_settings.google_mode = False
        assert ServiceFactory.is_google_mode() is False

    @patch('src.app.services.service_factory.settings')
    def test_is_mock_mode(self, mock_settings):
        """Test checking Mock mode."""
        mock_settings.mock_mode = True
        assert ServiceFactory.is_mock_mode() is True
        
        mock_settings.mock_mode = False
        assert ServiceFactory.is_mock_mode() is False

    @patch('src.app.services.service_factory.settings')
    def test_switch_to_google_mode(self, mock_settings):
        """Test switching to Google mode."""
        ServiceFactory.switch_to_google_mode()
        
        assert mock_settings.google_mode is True
        assert mock_settings.mock_mode is False

    @patch('src.app.services.service_factory.settings')
    def test_switch_to_mock_mode(self, mock_settings):
        """Test switching to Mock mode."""
        ServiceFactory.switch_to_mock_mode()
        
        assert mock_settings.google_mode is False
        assert mock_settings.mock_mode is True


class TestMockOAuthService:
    """Test cases for MockOAuthService."""

    @pytest.fixture
    def mock_oauth_service(self):
        """Create MockOAuthService instance."""
        return MockOAuthService()

    def test_mock_oauth_service_initialization(self, mock_oauth_service):
        """Test MockOAuthService initialization."""
        assert mock_oauth_service.provider == "mock"

    def test_generate_oauth_url(self, mock_oauth_service):
        """Test generating mock OAuth URL."""
        url = mock_oauth_service.generate_oauth_url()
        assert "http://localhost:3000/auth/mock/callback" in url
        assert "state=mock_state" in url

    def test_generate_oauth_url_with_custom_state(self, mock_oauth_service):
        """Test generating mock OAuth URL with custom state."""
        custom_state = "custom_state_123"
        url = mock_oauth_service.generate_oauth_url(custom_state)
        assert f"state={custom_state}" in url

    @pytest.mark.asyncio
    async def test_exchange_code_for_token(self, mock_oauth_service):
        """Test mock token exchange."""
        result = await mock_oauth_service.exchange_code_for_token("mock_code")
        
        assert result.id == "mock_token_123"
        assert result.provider == "mock"
        assert result.token_type == "Bearer"
        assert result.scope == "mock_scope"

    @pytest.mark.asyncio
    async def test_refresh_access_token(self, mock_oauth_service):
        """Test mock token refresh."""
        result = await mock_oauth_service.refresh_access_token("mock_refresh_token")
        
        assert result.id == "mock_token_123"
        assert result.provider == "mock"

    @pytest.mark.asyncio
    async def test_get_user_profile(self, mock_oauth_service):
        """Test mock user profile retrieval."""
        result = await mock_oauth_service.get_user_profile("mock_token")
        
        assert result.id == "mock_user_123"
        assert result.email == "mock@example.com"
        assert result.name == "Mock User"
        assert result.given_name == "Mock"
        assert result.family_name == "User"
        assert result.verified_email is True

    @pytest.mark.asyncio
    async def test_validate_token_valid(self, mock_oauth_service):
        """Test mock token validation with valid token."""
        result = await mock_oauth_service.validate_token("mock_valid_token")
        assert result is True

    @pytest.mark.asyncio
    async def test_validate_token_invalid(self, mock_oauth_service):
        """Test mock token validation with invalid token."""
        result = await mock_oauth_service.validate_token("invalid_token")
        assert result is False

    def test_get_classroom_service(self, mock_oauth_service):
        """Test getting mock classroom service."""
        service = mock_oauth_service.get_classroom_service("mock_token")
        assert isinstance(service, MockClassroomService)


class TestMockClassroomService:
    """Test cases for MockClassroomService."""

    @pytest.fixture
    def mock_classroom_service(self):
        """Create MockClassroomService instance."""
        return MockClassroomService()

    def test_mock_classroom_service_initialization(self, mock_classroom_service):
        """Test MockClassroomService initialization."""
        assert mock_classroom_service.service_name == "Mock Classroom"

    @pytest.mark.asyncio
    async def test_list_courses(self, mock_classroom_service):
        """Test mock course listing."""
        result = await mock_classroom_service.list_courses()
        
        assert "courses" in result
        assert len(result["courses"]) == 1
        assert result["courses"][0]["id"] == "mock_course_1"
        assert result["courses"][0]["name"] == "Mock Course 1"
        assert result["nextPageToken"] is None

    @pytest.mark.asyncio
    async def test_list_courses_with_page_size(self, mock_classroom_service):
        """Test mock course listing with page size."""
        result = await mock_classroom_service.list_courses(page_size=5)
        
        assert "courses" in result
        assert len(result["courses"]) == 1

    @pytest.mark.asyncio
    async def test_get_course(self, mock_classroom_service):
        """Test mock course retrieval."""
        course_id = "test_course_123"
        result = await mock_classroom_service.get_course(course_id)
        
        assert result["id"] == course_id
        assert result["name"] == f"Mock Course {course_id}"
        assert result["section"] == "Mock Section"
        assert result["courseState"] == "ACTIVE"

    @pytest.mark.asyncio
    async def test_list_course_work(self, mock_classroom_service):
        """Test mock course work listing."""
        course_id = "test_course_123"
        result = await mock_classroom_service.list_course_work(course_id)
        
        assert "courseWork" in result
        assert len(result["courseWork"]) == 1
        assert result["courseWork"][0]["id"] == "mock_work_1"
        assert result["courseWork"][0]["title"] == "Mock Assignment 1"
        assert result["courseWork"][0]["maxPoints"] == 100

    @pytest.mark.asyncio
    async def test_list_students(self, mock_classroom_service):
        """Test mock student listing."""
        course_id = "test_course_123"
        result = await mock_classroom_service.list_students(course_id)
        
        assert "students" in result
        assert len(result["students"]) == 1
        assert result["students"][0]["userId"] == "mock_student_1"
        assert result["students"][0]["courseId"] == course_id
        assert result["students"][0]["courseRole"] == "STUDENT"