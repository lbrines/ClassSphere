"""Tests for exceptions module with Template Method Pattern."""

import pytest
from src.app.core.exceptions import (
    BaseAPIException,
    AuthenticationError,
    TokenExpiredError,
    OAuthError,
    GoogleAPIError,
    NotFoundError,
    ConflictError,
    ValidationError,
    ServiceUnavailableError,
    DatabaseError,
    CacheError,
    ExternalServiceError,
    DeprecatedAPIError,
    GoogleClassroomError
)


class TestBaseAPIException:
    """Test BaseAPIException Template Method Pattern."""

    def test_default_message_construction(self):
        """Test default message construction."""
        exc = BaseAPIException()
        assert exc.message == "An error occurred"
        assert exc.status_code == 500

    def test_custom_message_priority(self):
        """Test custom message takes priority over default."""
        custom_message = "Custom error message"
        exc = BaseAPIException(message=custom_message)
        assert exc.message == custom_message

    def test_custom_message_with_parameters(self):
        """Test custom message with additional parameters."""
        custom_message = "Custom error"
        exc = BaseAPIException(
            message=custom_message,
            user_id="123",
            action="create"
        )
        assert "Custom error" in exc.message
        assert "user_id: 123" in exc.message
        assert "action: create" in exc.message

    def test_automatic_message_construction(self):
        """Test automatic message construction hook."""
        # Create a custom exception to test hook method
        class TestException(BaseAPIException):
            default_message = "Test error"

            def _construct_automatic_message(self, default_message, **kwargs):
                resource = kwargs.get('resource', 'unknown')
                return f"Test error for {resource}"

        exc = TestException(resource="user")
        assert exc.message == "Test error for user"

    def test_template_method_flow(self):
        """Test complete template method flow."""
        exc = BaseAPIException(
            message=None,  # No custom message
            status_code=400
        )
        assert exc.message == "An error occurred"
        assert exc.status_code == 400

    def test_details_storage(self):
        """Test that additional parameters are stored in details."""
        exc = BaseAPIException(
            user_id="123",
            action="delete",
            timestamp="2023-01-01"
        )
        assert exc.details["user_id"] == "123"
        assert exc.details["action"] == "delete"
        assert exc.details["timestamp"] == "2023-01-01"


class TestAuthenticationError:
    """Test AuthenticationError."""

    def test_default_authentication_error(self):
        """Test default authentication error."""
        exc = AuthenticationError()
        assert exc.message == "Authentication failed"
        assert exc.status_code == 401

    def test_custom_authentication_error(self):
        """Test custom authentication error."""
        exc = AuthenticationError(message="Invalid credentials")
        assert exc.message == "Invalid credentials"
        assert exc.status_code == 401

    def test_authentication_error_with_params(self):
        """Test authentication error with parameters."""
        exc = AuthenticationError(
            message="Login failed",
            user_id="123",
            reason="password_expired"
        )
        assert "Login failed" in exc.message
        assert "user_id: 123" in exc.message
        assert "reason: password_expired" in exc.message


class TestTokenExpiredError:
    """Test TokenExpiredError with Template Method Pattern."""

    def test_default_token_expired(self):
        """Test default token expired error."""
        exc = TokenExpiredError()
        assert exc.message == "Token has expired"
        assert exc.status_code == 401

    def test_custom_token_expired(self):
        """Test custom token expired error."""
        exc = TokenExpiredError(message="Access token invalid")
        assert exc.message == "Access token invalid"

    def test_automatic_token_construction(self):
        """Test automatic token message construction."""
        exc = TokenExpiredError(
            token_type="Access token",
            expired_at="2023-01-01T10:00:00Z"
        )
        assert "Access token has expired" in exc.message
        assert "2023-01-01T10:00:00Z" in exc.message

    def test_token_type_only(self):
        """Test token expired with only token type."""
        exc = TokenExpiredError(token_type="Refresh token")
        assert exc.message == "Refresh token has expired"


class TestOAuthError:
    """Test OAuthError with Template Method Pattern."""

    def test_default_oauth_error(self):
        """Test default OAuth error."""
        exc = OAuthError()
        assert exc.message == "OAuth authentication failed"
        assert exc.status_code == 401

    def test_oauth_error_with_provider(self):
        """Test OAuth error with provider."""
        exc = OAuthError(provider="Google")
        assert exc.message == "Google authentication failed"

    def test_oauth_error_with_provider_and_code(self):
        """Test OAuth error with provider and error code."""
        exc = OAuthError(
            provider="Google",
            error_code="invalid_grant"
        )
        assert "Google authentication failed" in exc.message
        assert "invalid_grant" in exc.message

    def test_oauth_custom_message_priority(self):
        """Test OAuth custom message takes priority."""
        exc = OAuthError(
            message="Custom OAuth error",
            provider="Google",
            error_code="invalid_grant"
        )
        assert "Custom OAuth error" in exc.message
        assert "provider: Google" in exc.message


class TestGoogleAPIError:
    """Test GoogleAPIError with Template Method Pattern."""

    def test_default_google_api_error(self):
        """Test default Google API error."""
        exc = GoogleAPIError()
        assert exc.message == "Google API error"
        assert exc.status_code == 502

    def test_google_api_quota_exceeded(self):
        """Test Google API quota exceeded."""
        exc = GoogleAPIError(
            api_name="Classroom API",
            quota_exceeded=True
        )
        assert exc.message == "Classroom API quota exceeded"

    def test_google_api_with_error_code(self):
        """Test Google API error with error code."""
        exc = GoogleAPIError(
            api_name="Drive API",
            error_code="403"
        )
        assert "Drive API error" in exc.message
        assert "403" in exc.message


class TestNotFoundError:
    """Test NotFoundError with Template Method Pattern."""

    def test_default_not_found(self):
        """Test default not found error."""
        exc = NotFoundError()
        assert exc.message == "Resource not found"
        assert exc.status_code == 404

    def test_not_found_with_resource_type(self):
        """Test not found with resource type."""
        exc = NotFoundError(resource_type="User")
        assert exc.message == "User not found"

    def test_not_found_with_resource_and_id(self):
        """Test not found with resource type and ID."""
        exc = NotFoundError(
            resource_type="Course",
            resource_id="123"
        )
        assert exc.message == "Course not found: 123"

    def test_not_found_custom_message_priority(self):
        """Test not found custom message priority."""
        exc = NotFoundError(
            message="Custom not found",
            resource_type="User",
            resource_id="456"
        )
        assert "Custom not found" in exc.message
        assert "resource_type: User" in exc.message


class TestConflictError:
    """Test ConflictError with Template Method Pattern."""

    def test_default_conflict(self):
        """Test default conflict error."""
        exc = ConflictError()
        assert exc.message == "Resource conflict"
        assert exc.status_code == 409

    def test_conflict_with_resource_type(self):
        """Test conflict with resource type."""
        exc = ConflictError(resource_type="User")
        assert exc.message == "User already exists"

    def test_conflict_with_field(self):
        """Test conflict with resource type and field."""
        exc = ConflictError(
            resource_type="User",
            conflict_field="email"
        )
        assert exc.message == "User with email already exists"


class TestValidationError:
    """Test ValidationError with Template Method Pattern."""

    def test_default_validation_error(self):
        """Test default validation error."""
        exc = ValidationError()
        assert exc.message == "Validation failed"
        assert exc.status_code == 422

    def test_validation_with_field(self):
        """Test validation error with field."""
        exc = ValidationError(field_name="email")
        assert exc.message == "Validation failed for email"

    def test_validation_with_field_and_type(self):
        """Test validation error with field and type."""
        exc = ValidationError(
            field_name="password",
            validation_type="too_short"
        )
        assert exc.message == "Validation failed for password: too_short"


class TestServiceUnavailableError:
    """Test ServiceUnavailableError with Template Method Pattern."""

    def test_default_service_unavailable(self):
        """Test default service unavailable error."""
        exc = ServiceUnavailableError()
        assert exc.message == "Service temporarily unavailable"
        assert exc.status_code == 503

    def test_service_unavailable_with_name(self):
        """Test service unavailable with service name."""
        exc = ServiceUnavailableError(service_name="Redis")
        assert exc.message == "Redis temporarily unavailable"

    def test_service_unavailable_with_retry(self):
        """Test service unavailable with retry after."""
        exc = ServiceUnavailableError(
            service_name="Database",
            retry_after=60
        )
        assert "Database temporarily unavailable" in exc.message
        assert "60 seconds" in exc.message


class TestDatabaseError:
    """Test DatabaseError with Template Method Pattern."""

    def test_default_database_error(self):
        """Test default database error."""
        exc = DatabaseError()
        assert exc.message == "Database operation failed"
        assert exc.status_code == 500

    def test_database_error_with_operation(self):
        """Test database error with operation."""
        exc = DatabaseError(operation="insert")
        assert exc.message == "Database insert failed"

    def test_database_error_with_operation_and_table(self):
        """Test database error with operation and table."""
        exc = DatabaseError(
            operation="update",
            table="users"
        )
        assert exc.message == "Database update failed for users"


class TestCacheError:
    """Test CacheError with Template Method Pattern."""

    def test_default_cache_error(self):
        """Test default cache error."""
        exc = CacheError()
        assert exc.message == "Cache operation failed"
        assert exc.status_code == 500

    def test_cache_error_with_operation(self):
        """Test cache error with operation."""
        exc = CacheError(operation="get")
        assert exc.message == "Cache get failed"

    def test_cache_error_with_key(self):
        """Test cache error with operation and key."""
        exc = CacheError(
            operation="set",
            cache_key="user:123"
        )
        assert "Cache set failed for key: user:123" in exc.message


class TestExternalServiceError:
    """Test ExternalServiceError with Template Method Pattern."""

    def test_default_external_service_error(self):
        """Test default external service error."""
        exc = ExternalServiceError()
        assert exc.message == "External service error"
        assert exc.status_code == 502

    def test_external_service_with_name(self):
        """Test external service error with service name."""
        exc = ExternalServiceError(service_name="Google API")
        assert exc.message == "Google API service error"

    def test_external_service_with_endpoint_and_status(self):
        """Test external service error with endpoint and status."""
        exc = ExternalServiceError(
            service_name="REST API",
            endpoint="/api/users",
            status_code=500
        )
        assert "REST API service error" in exc.message
        assert "/api/users" in exc.message
        assert "HTTP 500" in exc.message


class TestDeprecatedAPIError:
    """Test DeprecatedAPIError with Template Method Pattern."""

    def test_default_deprecated_api_error(self):
        """Test default deprecated API error."""
        exc = DeprecatedAPIError()
        assert exc.message == "Deprecated API usage"
        assert exc.status_code == 410

    def test_deprecated_api_with_version(self):
        """Test deprecated API error with version."""
        exc = DeprecatedAPIError(api_version="v1")
        assert exc.message == "API version v1 is deprecated"

    def test_deprecated_api_complete_info(self):
        """Test deprecated API error with complete information."""
        exc = DeprecatedAPIError(
            api_version="v1",
            replacement_version="v2",
            sunset_date="2024-01-01"
        )
        assert "API version v1 is deprecated" in exc.message
        assert "use version v2" in exc.message
        assert "sunset: 2024-01-01" in exc.message


class TestGoogleClassroomError:
    """Test GoogleClassroomError with Template Method Pattern."""

    def test_default_classroom_error(self):
        """Test default Google Classroom error."""
        exc = GoogleClassroomError()
        assert exc.message == "Google Classroom error"
        assert exc.status_code == 502

    def test_classroom_error_with_operation(self):
        """Test Google Classroom error with operation."""
        exc = GoogleClassroomError(operation="list_courses")
        assert exc.message == "Google Classroom list_courses failed"

    def test_classroom_error_complete(self):
        """Test Google Classroom error with complete information."""
        exc = GoogleClassroomError(
            operation="get_course",
            course_id="123456",
            error_code="403"
        )
        assert "Google Classroom get_course failed" in exc.message
        assert "course 123456" in exc.message
        assert "403" in exc.message

    def test_classroom_custom_message_priority(self):
        """Test Google Classroom custom message priority."""
        exc = GoogleClassroomError(
            message="Custom classroom error",
            operation="create_course",
            course_id="789"
        )
        assert "Custom classroom error" in exc.message
        assert "operation: create_course" in exc.message