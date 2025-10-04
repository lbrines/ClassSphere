"""Service factory for dual mode switching (Google/Mock)."""

from typing import Union, Type, Any
from ..core.config import settings
from ..core.exceptions import ServiceUnavailableError
from .auth_service import AuthService
from .oauth_service import OAuthService


class ServiceFactory:
    """Factory for creating services based on current mode."""
    
    @staticmethod
    def get_auth_service() -> AuthService:
        """Get authentication service instance."""
        return AuthService()
    
    @staticmethod
    def get_oauth_service() -> Union[OAuthService, 'MockOAuthService']:
        """Get OAuth service based on current mode."""
        if settings.google_mode:
            return OAuthService()
        else:
            return MockOAuthService()
    
    @staticmethod
    def get_classroom_service() -> Union[Any, 'MockClassroomService']:
        """Get classroom service based on current mode."""
        if settings.google_mode:
            # This will be implemented in Phase 2
            raise ServiceUnavailableError(
                "Google Classroom service not yet implemented",
                service_name="Google Classroom"
            )
        else:
            return MockClassroomService()
    
    @staticmethod
    def is_google_mode() -> bool:
        """Check if currently in Google mode."""
        return settings.google_mode
    
    @staticmethod
    def is_mock_mode() -> bool:
        """Check if currently in Mock mode."""
        return settings.mock_mode
    
    @staticmethod
    def switch_to_google_mode():
        """Switch to Google mode."""
        settings.google_mode = True
        settings.mock_mode = False
    
    @staticmethod
    def switch_to_mock_mode():
        """Switch to Mock mode."""
        settings.google_mode = False
        settings.mock_mode = True


class MockOAuthService:
    """Mock OAuth service for development and testing."""
    
    def __init__(self):
        self.provider = "mock"
    
    def generate_oauth_url(self, state: str = None) -> str:
        """Generate mock OAuth URL."""
        return f"http://localhost:3000/auth/mock/callback?state={state or 'mock_state'}"
    
    async def exchange_code_for_token(self, code: str, state: str = None):
        """Mock token exchange."""
        from ..models.oauth import OAuthTokenResponse
        from datetime import datetime, timedelta
        
        return OAuthTokenResponse(
            id="mock_token_123",
            provider="mock",
            token_type="Bearer",
            expires_at=datetime.utcnow() + timedelta(hours=1),
            scope="mock_scope",
            created_at=datetime.utcnow(),
            updated_at=None
        )
    
    async def refresh_access_token(self, refresh_token: str):
        """Mock token refresh."""
        return await self.exchange_code_for_token("mock_code")
    
    async def get_user_profile(self, access_token: str):
        """Mock user profile retrieval."""
        from ..models.oauth import GoogleOAuthProfile
        
        return GoogleOAuthProfile(
            id="mock_user_123",
            email="mock@example.com",
            name="Mock User",
            given_name="Mock",
            family_name="User",
            verified_email=True
        )
    
    async def validate_token(self, access_token: str) -> bool:
        """Mock token validation."""
        return access_token.startswith("mock_")
    
    def get_classroom_service(self, access_token: str):
        """Mock classroom service."""
        return MockClassroomService()


class MockClassroomService:
    """Mock Google Classroom service for development and testing."""
    
    def __init__(self):
        self.service_name = "Mock Classroom"
    
    async def list_courses(self, page_size: int = 10, page_token: str = None):
        """Mock course listing."""
        return {
            "courses": [
                {
                    "id": "mock_course_1",
                    "name": "Mock Course 1",
                    "section": "Mock Section",
                    "descriptionHeading": "Mock Description",
                    "room": "Mock Room",
                    "ownerId": "mock_teacher_1",
                    "courseState": "ACTIVE",
                    "creationTime": "2024-01-01T00:00:00Z",
                    "updateTime": "2024-01-01T00:00:00Z",
                    "enrollmentCode": "mock_code_1"
                }
            ],
            "nextPageToken": None
        }
    
    async def get_course(self, course_id: str):
        """Mock course retrieval."""
        return {
            "id": course_id,
            "name": f"Mock Course {course_id}",
            "section": "Mock Section",
            "descriptionHeading": "Mock Description",
            "room": "Mock Room",
            "ownerId": "mock_teacher_1",
            "courseState": "ACTIVE",
            "creationTime": "2024-01-01T00:00:00Z",
            "updateTime": "2024-01-01T00:00:00Z",
            "enrollmentCode": f"mock_code_{course_id}"
        }
    
    async def list_course_work(self, course_id: str, page_size: int = 10):
        """Mock course work listing."""
        return {
            "courseWork": [
                {
                    "id": "mock_work_1",
                    "title": "Mock Assignment 1",
                    "description": "Mock assignment description",
                    "maxPoints": 100,
                    "workType": "ASSIGNMENT",
                    "state": "PUBLISHED",
                    "creationTime": "2024-01-01T00:00:00Z",
                    "updateTime": "2024-01-01T00:00:00Z",
                    "dueDate": {"year": 2024, "month": 12, "day": 31},
                    "dueTime": {"hours": 23, "minutes": 59}
                }
            ]
        }
    
    async def list_students(self, course_id: str, page_size: int = 10):
        """Mock student listing."""
        return {
            "students": [
                {
                    "userId": "mock_student_1",
                    "courseId": course_id,
                    "profile": {
                        "id": "mock_student_1",
                        "name": {
                            "givenName": "Mock",
                            "familyName": "Student"
                        },
                        "emailAddress": "mock.student@example.com"
                    },
                    "courseRole": "STUDENT"
                }
            ]
        }