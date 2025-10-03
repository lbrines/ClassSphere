"""
Unit tests for OAuth exceptions.
"""
import pytest
from src.app.exceptions.oauth import (
    OAuthError, OAuthProviderError, OAuthTokenError,
    OAuthAuthorizationError, OAuthScopeError, OAuthRedirectError,
    GoogleAPIError, GoogleAPIConnectionError, GoogleAPIAuthenticationError,
    GoogleAPIAuthorizationError, GoogleAPIRateLimitError, GoogleAPINotFoundError,
    GoogleAPIBadRequestError, GoogleAPIServerError, GoogleAPITimeoutError,
    GoogleClassroomError, GoogleClassroomCourseError, GoogleClassroomStudentError,
    GoogleClassroomAssignmentError
)


class TestOAuthError:
    """Test OAuthError exception."""
    
    def test_oauth_error_default(self):
        """Test OAuthError with default values."""
        error = OAuthError()
        
        assert str(error) == "OAuth error occurred"
        assert error.message == "OAuth error occurred"
        assert error.error_code == "OAUTH_ERROR"
        assert error.provider is None
        assert error.details == {}
    
    def test_oauth_error_with_provider(self):
        """Test OAuthError with provider."""
        error = OAuthError(provider="google")
        
        assert str(error) == "OAuth error occurred"
        assert error.message == "OAuth error occurred"
        assert error.error_code == "OAUTH_ERROR"
        assert error.provider == "google"
        assert error.details == {}
    
    def test_oauth_error_custom(self):
        """Test OAuthError with custom values."""
        details = {"code": "invalid_request"}
        error = OAuthError(
            message="Custom OAuth error",
            error_code="CUSTOM_OAUTH_ERROR",
            provider="google",
            details=details
        )
        
        assert str(error) == "Custom OAuth error"
        assert error.message == "Custom OAuth error"
        assert error.error_code == "CUSTOM_OAUTH_ERROR"
        assert error.provider == "google"
        assert error.details == details


class TestOAuthProviderError:
    """Test OAuthProviderError exception."""
    
    def test_oauth_provider_error_default(self):
        """Test OAuthProviderError with default values."""
        error = OAuthProviderError()
        
        assert str(error) == "OAuth provider error"
        assert error.message == "OAuth provider error"
        assert error.error_code == "OAUTH_PROVIDER_ERROR"
        assert error.provider is None
        assert error.provider_error is None
        assert error.details == {}
    
    def test_oauth_provider_error_with_provider_error(self):
        """Test OAuthProviderError with provider error."""
        error = OAuthProviderError(provider_error="invalid_client")
        
        assert str(error) == "OAuth provider error: invalid_client"
        assert error.message == "OAuth provider error: invalid_client"
        assert error.error_code == "OAUTH_PROVIDER_ERROR"
        assert error.provider_error == "invalid_client"
    
    def test_oauth_provider_error_custom(self):
        """Test OAuthProviderError with custom values."""
        details = {"response": "error_response"}
        error = OAuthProviderError(
            message="Custom provider error",
            error_code="CUSTOM_PROVIDER_ERROR",
            provider="google",
            provider_error="invalid_grant",
            details=details
        )
        
        assert str(error) == "Custom provider error: invalid_grant"
        assert error.message == "Custom provider error: invalid_grant"
        assert error.error_code == "CUSTOM_PROVIDER_ERROR"
        assert error.provider == "google"
        assert error.provider_error == "invalid_grant"
        assert error.details == details


class TestOAuthTokenError:
    """Test OAuthTokenError exception."""
    
    def test_oauth_token_error_default(self):
        """Test OAuthTokenError with default values."""
        error = OAuthTokenError()
        
        assert str(error) == "OAuth token error"
        assert error.message == "OAuth token error"
        assert error.error_code == "OAUTH_TOKEN_ERROR"
        assert error.provider is None
        assert error.token_type is None
        assert error.details == {}
    
    def test_oauth_token_error_with_token_type(self):
        """Test OAuthTokenError with token type."""
        error = OAuthTokenError(token_type="access")
        
        assert str(error) == "OAuth token error: access"
        assert error.message == "OAuth token error: access"
        assert error.error_code == "OAUTH_TOKEN_ERROR"
        assert error.token_type == "access"
    
    def test_oauth_token_error_custom(self):
        """Test OAuthTokenError with custom values."""
        details = {"expires_at": "2023-01-01T00:00:00Z"}
        error = OAuthTokenError(
            message="Custom token error",
            error_code="CUSTOM_TOKEN_ERROR",
            provider="google",
            token_type="refresh",
            details=details
        )
        
        assert str(error) == "Custom token error: refresh"
        assert error.message == "Custom token error: refresh"
        assert error.error_code == "CUSTOM_TOKEN_ERROR"
        assert error.provider == "google"
        assert error.token_type == "refresh"
        assert error.details == details


class TestOAuthAuthorizationError:
    """Test OAuthAuthorizationError exception."""
    
    def test_oauth_authorization_error_default(self):
        """Test OAuthAuthorizationError with default values."""
        error = OAuthAuthorizationError()
        
        assert str(error) == "OAuth authorization failed"
        assert error.message == "OAuth authorization failed"
        assert error.error_code == "OAUTH_AUTHORIZATION_ERROR"
        assert error.provider is None
        assert error.authorization_code is None
        assert error.details == {}
    
    def test_oauth_authorization_error_with_code(self):
        """Test OAuthAuthorizationError with authorization code."""
        error = OAuthAuthorizationError(authorization_code="auth_code_123")
        
        assert str(error) == "OAuth authorization failed: auth_code_123"
        assert error.message == "OAuth authorization failed: auth_code_123"
        assert error.error_code == "OAUTH_AUTHORIZATION_ERROR"
        assert error.authorization_code == "auth_code_123"
    
    def test_oauth_authorization_error_custom(self):
        """Test OAuthAuthorizationError with custom values."""
        details = {"state": "state_123"}
        error = OAuthAuthorizationError(
            message="Custom authorization error",
            error_code="CUSTOM_AUTHORIZATION_ERROR",
            provider="google",
            authorization_code="auth_code_123",
            details=details
        )
        
        assert str(error) == "Custom authorization error: auth_code_123"
        assert error.message == "Custom authorization error: auth_code_123"
        assert error.error_code == "CUSTOM_AUTHORIZATION_ERROR"
        assert error.provider == "google"
        assert error.authorization_code == "auth_code_123"
        assert error.details == details


class TestOAuthScopeError:
    """Test OAuthScopeError exception."""
    
    def test_oauth_scope_error_default(self):
        """Test OAuthScopeError with default values."""
        error = OAuthScopeError()
        
        assert str(error) == "OAuth scope error"
        assert error.message == "OAuth scope error"
        assert error.error_code == "OAUTH_SCOPE_ERROR"
        assert error.provider is None
        assert error.required_scope is None
        assert error.granted_scopes == []
        assert error.details == {}
    
    def test_oauth_scope_error_with_required_scope(self):
        """Test OAuthScopeError with required scope."""
        error = OAuthScopeError(required_scope="admin")
        
        assert str(error) == "OAuth scope error: admin"
        assert error.message == "OAuth scope error: admin"
        assert error.error_code == "OAUTH_SCOPE_ERROR"
        assert error.required_scope == "admin"
    
    def test_oauth_scope_error_custom(self):
        """Test OAuthScopeError with custom values."""
        details = {"requested_scopes": ["admin", "user"]}
        error = OAuthScopeError(
            message="Custom scope error",
            error_code="CUSTOM_SCOPE_ERROR",
            provider="google",
            required_scope="admin",
            granted_scopes=["user"],
            details=details
        )
        
        assert str(error) == "Custom scope error: admin"
        assert error.message == "Custom scope error: admin"
        assert error.error_code == "CUSTOM_SCOPE_ERROR"
        assert error.provider == "google"
        assert error.required_scope == "admin"
        assert error.granted_scopes == ["user"]
        assert error.details == details


class TestOAuthRedirectError:
    """Test OAuthRedirectError exception."""
    
    def test_oauth_redirect_error_default(self):
        """Test OAuthRedirectError with default values."""
        error = OAuthRedirectError()
        
        assert str(error) == "OAuth redirect error"
        assert error.message == "OAuth redirect error"
        assert error.error_code == "OAUTH_REDIRECT_ERROR"
        assert error.provider is None
        assert error.redirect_uri is None
        assert error.details == {}
    
    def test_oauth_redirect_error_with_redirect_uri(self):
        """Test OAuthRedirectError with redirect URI."""
        error = OAuthRedirectError(redirect_uri="http://localhost:3000/callback")
        
        assert str(error) == "OAuth redirect error: http://localhost:3000/callback"
        assert error.message == "OAuth redirect error: http://localhost:3000/callback"
        assert error.error_code == "OAUTH_REDIRECT_ERROR"
        assert error.redirect_uri == "http://localhost:3000/callback"
    
    def test_oauth_redirect_error_custom(self):
        """Test OAuthRedirectError with custom values."""
        details = {"expected_uri": "http://localhost:3000/auth/callback"}
        error = OAuthRedirectError(
            message="Custom redirect error",
            error_code="CUSTOM_REDIRECT_ERROR",
            provider="google",
            redirect_uri="http://localhost:3000/callback",
            details=details
        )
        
        assert str(error) == "Custom redirect error: http://localhost:3000/callback"
        assert error.message == "Custom redirect error: http://localhost:3000/callback"
        assert error.error_code == "CUSTOM_REDIRECT_ERROR"
        assert error.provider == "google"
        assert error.redirect_uri == "http://localhost:3000/callback"
        assert error.details == details


class TestGoogleAPIError:
    """Test GoogleAPIError exception."""
    
    def test_google_api_error_default(self):
        """Test GoogleAPIError with default values."""
        error = GoogleAPIError()
        
        assert str(error) == "Google API error occurred"
        assert error.message == "Google API error occurred"
        assert error.error_code == "GOOGLE_API_ERROR"
        assert error.api_endpoint is None
        assert error.status_code is None
        assert error.details == {}
    
    def test_google_api_error_with_endpoint(self):
        """Test GoogleAPIError with API endpoint."""
        error = GoogleAPIError(api_endpoint="classroom.googleapis.com")
        
        assert str(error) == "Google API error occurred"
        assert error.message == "Google API error occurred"
        assert error.error_code == "GOOGLE_API_ERROR"
        assert error.api_endpoint == "classroom.googleapis.com"
    
    def test_google_api_error_with_status_code(self):
        """Test GoogleAPIError with status code."""
        error = GoogleAPIError(status_code=404)
        
        assert str(error) == "Google API error occurred"
        assert error.message == "Google API error occurred"
        assert error.error_code == "GOOGLE_API_ERROR"
        assert error.status_code == 404
    
    def test_google_api_error_custom(self):
        """Test GoogleAPIError with custom values."""
        details = {"response": "error_response"}
        error = GoogleAPIError(
            message="Custom Google API error",
            error_code="CUSTOM_GOOGLE_API_ERROR",
            api_endpoint="classroom.googleapis.com",
            status_code=500,
            details=details
        )
        
        assert str(error) == "Custom Google API error"
        assert error.message == "Custom Google API error"
        assert error.error_code == "CUSTOM_GOOGLE_API_ERROR"
        assert error.api_endpoint == "classroom.googleapis.com"
        assert error.status_code == 500
        assert error.details == details


class TestGoogleAPIConnectionError:
    """Test GoogleAPIConnectionError exception."""
    
    def test_google_api_connection_error_default(self):
        """Test GoogleAPIConnectionError with default values."""
        error = GoogleAPIConnectionError()
        
        assert str(error) == "Failed to connect to Google API"
        assert error.message == "Failed to connect to Google API"
        assert error.error_code == "GOOGLE_API_CONNECTION_ERROR"
        assert error.api_endpoint is None
        assert error.status_code is None
        assert error.details == {}
    
    def test_google_api_connection_error_with_endpoint(self):
        """Test GoogleAPIConnectionError with API endpoint."""
        error = GoogleAPIConnectionError(api_endpoint="classroom.googleapis.com")
        
        assert str(error) == "Failed to connect to Google API"
        assert error.message == "Failed to connect to Google API"
        assert error.error_code == "GOOGLE_API_CONNECTION_ERROR"
        assert error.api_endpoint == "classroom.googleapis.com"
    
    def test_google_api_connection_error_custom(self):
        """Test GoogleAPIConnectionError with custom values."""
        details = {"timeout": 30}
        error = GoogleAPIConnectionError(
            message="Custom connection error",
            error_code="CUSTOM_CONNECTION_ERROR",
            api_endpoint="classroom.googleapis.com",
            details=details
        )
        
        assert str(error) == "Custom connection error"
        assert error.message == "Custom connection error"
        assert error.error_code == "CUSTOM_CONNECTION_ERROR"
        assert error.api_endpoint == "classroom.googleapis.com"
        assert error.status_code is None
        assert error.details == details


class TestGoogleAPIAuthenticationError:
    """Test GoogleAPIAuthenticationError exception."""
    
    def test_google_api_authentication_error_default(self):
        """Test GoogleAPIAuthenticationError with default values."""
        error = GoogleAPIAuthenticationError()
        
        assert str(error) == "Google API authentication failed"
        assert error.message == "Google API authentication failed"
        assert error.error_code == "GOOGLE_API_AUTH_ERROR"
        assert error.api_endpoint is None
        assert error.status_code == 401
        assert error.details == {}
    
    def test_google_api_authentication_error_custom(self):
        """Test GoogleAPIAuthenticationError with custom values."""
        details = {"token_expired": True}
        error = GoogleAPIAuthenticationError(
            message="Custom authentication error",
            error_code="CUSTOM_AUTH_ERROR",
            api_endpoint="classroom.googleapis.com",
            details=details
        )
        
        assert str(error) == "Custom authentication error"
        assert error.message == "Custom authentication error"
        assert error.error_code == "CUSTOM_AUTH_ERROR"
        assert error.api_endpoint == "classroom.googleapis.com"
        assert error.status_code == 401
        assert error.details == details


class TestGoogleAPIAuthorizationError:
    """Test GoogleAPIAuthorizationError exception."""
    
    def test_google_api_authorization_error_default(self):
        """Test GoogleAPIAuthorizationError with default values."""
        error = GoogleAPIAuthorizationError()
        
        assert str(error) == "Google API authorization failed"
        assert error.message == "Google API authorization failed"
        assert error.error_code == "GOOGLE_API_AUTHZ_ERROR"
        assert error.api_endpoint is None
        assert error.status_code == 403
        assert error.required_scopes == []
        assert error.details == {}
    
    def test_google_api_authorization_error_with_scopes(self):
        """Test GoogleAPIAuthorizationError with required scopes."""
        error = GoogleAPIAuthorizationError(required_scopes=["admin", "user"])
        
        assert str(error) == "Google API authorization failed: admin, user"
        assert error.message == "Google API authorization failed: admin, user"
        assert error.error_code == "GOOGLE_API_AUTHZ_ERROR"
        assert error.required_scopes == ["admin", "user"]
    
    def test_google_api_authorization_error_custom(self):
        """Test GoogleAPIAuthorizationError with custom values."""
        details = {"current_scopes": ["user"]}
        error = GoogleAPIAuthorizationError(
            message="Custom authorization error",
            error_code="CUSTOM_AUTHZ_ERROR",
            api_endpoint="classroom.googleapis.com",
            required_scopes=["admin"],
            details=details
        )
        
        assert str(error) == "Custom authorization error: admin"
        assert error.message == "Custom authorization error: admin"
        assert error.error_code == "CUSTOM_AUTHZ_ERROR"
        assert error.api_endpoint == "classroom.googleapis.com"
        assert error.status_code == 403
        assert error.required_scopes == ["admin"]
        assert error.details == details


class TestGoogleAPIRateLimitError:
    """Test GoogleAPIRateLimitError exception."""
    
    def test_google_api_rate_limit_error_default(self):
        """Test GoogleAPIRateLimitError with default values."""
        error = GoogleAPIRateLimitError()
        
        assert str(error) == "Google API rate limit exceeded"
        assert error.message == "Google API rate limit exceeded"
        assert error.error_code == "GOOGLE_API_RATE_LIMIT_ERROR"
        assert error.api_endpoint is None
        assert error.status_code == 429
        assert error.retry_after is None
        assert error.details == {}
    
    def test_google_api_rate_limit_error_with_retry_after(self):
        """Test GoogleAPIRateLimitError with retry after."""
        error = GoogleAPIRateLimitError(retry_after=60)
        
        assert str(error) == "Google API rate limit exceeded, retry after 60 seconds"
        assert error.message == "Google API rate limit exceeded, retry after 60 seconds"
        assert error.error_code == "GOOGLE_API_RATE_LIMIT_ERROR"
        assert error.retry_after == 60
    
    def test_google_api_rate_limit_error_custom(self):
        """Test GoogleAPIRateLimitError with custom values."""
        details = {"limit": 100, "window": 3600}
        error = GoogleAPIRateLimitError(
            message="Custom rate limit error",
            error_code="CUSTOM_RATE_LIMIT_ERROR",
            api_endpoint="classroom.googleapis.com",
            retry_after=120,
            details=details
        )
        
        assert str(error) == "Custom rate limit error, retry after 120 seconds"
        assert error.message == "Custom rate limit error, retry after 120 seconds"
        assert error.error_code == "CUSTOM_RATE_LIMIT_ERROR"
        assert error.api_endpoint == "classroom.googleapis.com"
        assert error.status_code == 429
        assert error.retry_after == 120
        assert error.details == details


class TestGoogleAPINotFoundError:
    """Test GoogleAPINotFoundError exception."""
    
    def test_google_api_not_found_error_default(self):
        """Test GoogleAPINotFoundError with default values."""
        error = GoogleAPINotFoundError()
        
        assert str(error) == "Google API resource not found"
        assert error.message == "Google API resource not found"
        assert error.error_code == "GOOGLE_API_NOT_FOUND_ERROR"
        assert error.api_endpoint is None
        assert error.status_code == 404
        assert error.resource_id is None
        assert error.details == {}
    
    def test_google_api_not_found_error_with_resource_id(self):
        """Test GoogleAPINotFoundError with resource ID."""
        error = GoogleAPINotFoundError(resource_id="course123")
        
        assert str(error) == "Google API resource not found: course123"
        assert error.message == "Google API resource not found: course123"
        assert error.error_code == "GOOGLE_API_NOT_FOUND_ERROR"
        assert error.resource_id == "course123"
    
    def test_google_api_not_found_error_custom(self):
        """Test GoogleAPINotFoundError with custom values."""
        details = {"resource_type": "course"}
        error = GoogleAPINotFoundError(
            message="Custom not found error",
            error_code="CUSTOM_NOT_FOUND_ERROR",
            api_endpoint="classroom.googleapis.com",
            resource_id="course123",
            details=details
        )
        
        assert str(error) == "Custom not found error: course123"
        assert error.message == "Custom not found error: course123"
        assert error.error_code == "CUSTOM_NOT_FOUND_ERROR"
        assert error.api_endpoint == "classroom.googleapis.com"
        assert error.status_code == 404
        assert error.resource_id == "course123"
        assert error.details == details


class TestGoogleAPIBadRequestError:
    """Test GoogleAPIBadRequestError exception."""
    
    def test_google_api_bad_request_error_default(self):
        """Test GoogleAPIBadRequestError with default values."""
        error = GoogleAPIBadRequestError()
        
        assert str(error) == "Google API bad request"
        assert error.message == "Google API bad request"
        assert error.error_code == "GOOGLE_API_BAD_REQUEST_ERROR"
        assert error.api_endpoint is None
        assert error.status_code == 400
        assert error.validation_errors == []
        assert error.details == {}
    
    def test_google_api_bad_request_error_with_validation_errors(self):
        """Test GoogleAPIBadRequestError with validation errors."""
        error = GoogleAPIBadRequestError(validation_errors=["invalid_field", "missing_required"])
        
        assert str(error) == "Google API bad request: invalid_field, missing_required"
        assert error.message == "Google API bad request: invalid_field, missing_required"
        assert error.error_code == "GOOGLE_API_BAD_REQUEST_ERROR"
        assert error.validation_errors == ["invalid_field", "missing_required"]
    
    def test_google_api_bad_request_error_custom(self):
        """Test GoogleAPIBadRequestError with custom values."""
        details = {"request_body": "invalid_data"}
        error = GoogleAPIBadRequestError(
            message="Custom bad request error",
            error_code="CUSTOM_BAD_REQUEST_ERROR",
            api_endpoint="classroom.googleapis.com",
            validation_errors=["invalid_format"],
            details=details
        )
        
        assert str(error) == "Custom bad request error: invalid_format"
        assert error.message == "Custom bad request error: invalid_format"
        assert error.error_code == "CUSTOM_BAD_REQUEST_ERROR"
        assert error.api_endpoint == "classroom.googleapis.com"
        assert error.status_code == 400
        assert error.validation_errors == ["invalid_format"]
        assert error.details == details


class TestGoogleAPIServerError:
    """Test GoogleAPIServerError exception."""
    
    def test_google_api_server_error_default(self):
        """Test GoogleAPIServerError with default values."""
        error = GoogleAPIServerError()
        
        assert str(error) == "Google API server error"
        assert error.message == "Google API server error"
        assert error.error_code == "GOOGLE_API_SERVER_ERROR"
        assert error.api_endpoint is None
        assert error.status_code == 500
        assert error.details == {}
    
    def test_google_api_server_error_custom(self):
        """Test GoogleAPIServerError with custom values."""
        details = {"internal_error": "database_connection_failed"}
        error = GoogleAPIServerError(
            message="Custom server error",
            error_code="CUSTOM_SERVER_ERROR",
            api_endpoint="classroom.googleapis.com",
            status_code=503,
            details=details
        )
        
        assert str(error) == "Custom server error"
        assert error.message == "Custom server error"
        assert error.error_code == "CUSTOM_SERVER_ERROR"
        assert error.api_endpoint == "classroom.googleapis.com"
        assert error.status_code == 503
        assert error.details == details


class TestGoogleAPITimeoutError:
    """Test GoogleAPITimeoutError exception."""
    
    def test_google_api_timeout_error_default(self):
        """Test GoogleAPITimeoutError with default values."""
        error = GoogleAPITimeoutError()
        
        assert str(error) == "Google API request timeout"
        assert error.message == "Google API request timeout"
        assert error.error_code == "GOOGLE_API_TIMEOUT_ERROR"
        assert error.api_endpoint is None
        assert error.status_code == 408
        assert error.timeout_duration is None
        assert error.details == {}
    
    def test_google_api_timeout_error_with_duration(self):
        """Test GoogleAPITimeoutError with timeout duration."""
        error = GoogleAPITimeoutError(timeout_duration=30)
        
        assert str(error) == "Google API request timeout after 30 seconds"
        assert error.message == "Google API request timeout after 30 seconds"
        assert error.error_code == "GOOGLE_API_TIMEOUT_ERROR"
        assert error.timeout_duration == 30
    
    def test_google_api_timeout_error_custom(self):
        """Test GoogleAPITimeoutError with custom values."""
        details = {"request_id": "req123"}
        error = GoogleAPITimeoutError(
            message="Custom timeout error",
            error_code="CUSTOM_TIMEOUT_ERROR",
            api_endpoint="classroom.googleapis.com",
            timeout_duration=60,
            details=details
        )
        
        assert str(error) == "Custom timeout error after 60 seconds"
        assert error.message == "Custom timeout error after 60 seconds"
        assert error.error_code == "CUSTOM_TIMEOUT_ERROR"
        assert error.api_endpoint == "classroom.googleapis.com"
        assert error.status_code == 408
        assert error.timeout_duration == 60
        assert error.details == details


class TestGoogleClassroomError:
    """Test GoogleClassroomError exception."""
    
    def test_google_classroom_error_default(self):
        """Test GoogleClassroomError with default values."""
        error = GoogleClassroomError()
        
        assert str(error) == "Google Classroom API error"
        assert error.message == "Google Classroom API error"
        assert error.error_code == "GOOGLE_CLASSROOM_ERROR"
        assert error.api_endpoint == "classroom.googleapis.com"
        assert error.status_code is None
        assert error.classroom_resource is None
        assert error.details == {}
    
    def test_google_classroom_error_with_resource(self):
        """Test GoogleClassroomError with classroom resource."""
        error = GoogleClassroomError(classroom_resource="courses")
        
        assert str(error) == "Google Classroom API error: courses"
        assert error.message == "Google Classroom API error: courses"
        assert error.error_code == "GOOGLE_CLASSROOM_ERROR"
        assert error.classroom_resource == "courses"
    
    def test_google_classroom_error_custom(self):
        """Test GoogleClassroomError with custom values."""
        details = {"course_id": "course123"}
        error = GoogleClassroomError(
            message="Custom classroom error",
            error_code="CUSTOM_CLASSROOM_ERROR",
            classroom_resource="students",
            details=details
        )
        
        assert str(error) == "Custom classroom error: students"
        assert error.message == "Custom classroom error: students"
        assert error.error_code == "CUSTOM_CLASSROOM_ERROR"
        assert error.api_endpoint == "classroom.googleapis.com"
        assert error.classroom_resource == "students"
        assert error.details == details


class TestGoogleClassroomCourseError:
    """Test GoogleClassroomCourseError exception."""
    
    def test_google_classroom_course_error_default(self):
        """Test GoogleClassroomCourseError with default values."""
        error = GoogleClassroomCourseError()
        
        assert str(error) == "Google Classroom course error"
        assert error.message == "Google Classroom course error"
        assert error.error_code == "GOOGLE_CLASSROOM_COURSE_ERROR"
        assert error.api_endpoint == "classroom.googleapis.com"
        assert error.status_code is None
        assert error.classroom_resource == "courses"
        assert error.course_id is None
        assert error.details == {}
    
    def test_google_classroom_course_error_with_course_id(self):
        """Test GoogleClassroomCourseError with course ID."""
        error = GoogleClassroomCourseError(course_id="course123")
        
        assert str(error) == "Google Classroom course error: course123"
        assert error.message == "Google Classroom course error: course123"
        assert error.error_code == "GOOGLE_CLASSROOM_COURSE_ERROR"
        assert error.course_id == "course123"
    
    def test_google_classroom_course_error_custom(self):
        """Test GoogleClassroomCourseError with custom values."""
        details = {"operation": "create"}
        error = GoogleClassroomCourseError(
            message="Custom course error",
            error_code="CUSTOM_COURSE_ERROR",
            course_id="course123",
            details=details
        )
        
        assert str(error) == "Custom course error: course123"
        assert error.message == "Custom course error: course123"
        assert error.error_code == "CUSTOM_COURSE_ERROR"
        assert error.api_endpoint == "classroom.googleapis.com"
        assert error.classroom_resource == "courses"
        assert error.course_id == "course123"
        assert error.details == details


class TestGoogleClassroomStudentError:
    """Test GoogleClassroomStudentError exception."""
    
    def test_google_classroom_student_error_default(self):
        """Test GoogleClassroomStudentError with default values."""
        error = GoogleClassroomStudentError()
        
        assert str(error) == "Google Classroom student error"
        assert error.message == "Google Classroom student error"
        assert error.error_code == "GOOGLE_CLASSROOM_STUDENT_ERROR"
        assert error.api_endpoint == "classroom.googleapis.com"
        assert error.status_code is None
        assert error.classroom_resource == "students"
        assert error.student_id is None
        assert error.course_id is None
        assert error.details == {}
    
    def test_google_classroom_student_error_with_student_id(self):
        """Test GoogleClassroomStudentError with student ID."""
        error = GoogleClassroomStudentError(student_id="student123")
        
        assert str(error) == "Google Classroom student error: student123"
        assert error.message == "Google Classroom student error: student123"
        assert error.error_code == "GOOGLE_CLASSROOM_STUDENT_ERROR"
        assert error.student_id == "student123"
    
    def test_google_classroom_student_error_with_course_id(self):
        """Test GoogleClassroomStudentError with course ID."""
        error = GoogleClassroomStudentError(course_id="course123")
        
        assert str(error) == "Google Classroom student error in course course123"
        assert error.message == "Google Classroom student error in course course123"
        assert error.error_code == "GOOGLE_CLASSROOM_STUDENT_ERROR"
        assert error.course_id == "course123"
    
    def test_google_classroom_student_error_with_both(self):
        """Test GoogleClassroomStudentError with both student and course ID."""
        error = GoogleClassroomStudentError(student_id="student123", course_id="course123")
        
        assert str(error) == "Google Classroom student error: student123 in course course123"
        assert error.message == "Google Classroom student error: student123 in course course123"
        assert error.error_code == "GOOGLE_CLASSROOM_STUDENT_ERROR"
        assert error.student_id == "student123"
        assert error.course_id == "course123"
    
    def test_google_classroom_student_error_custom(self):
        """Test GoogleClassroomStudentError with custom values."""
        details = {"operation": "enroll"}
        error = GoogleClassroomStudentError(
            message="Custom student error",
            error_code="CUSTOM_STUDENT_ERROR",
            student_id="student123",
            course_id="course123",
            details=details
        )
        
        assert str(error) == "Custom student error: student123 in course course123"
        assert error.message == "Custom student error: student123 in course course123"
        assert error.error_code == "CUSTOM_STUDENT_ERROR"
        assert error.api_endpoint == "classroom.googleapis.com"
        assert error.classroom_resource == "students"
        assert error.student_id == "student123"
        assert error.course_id == "course123"
        assert error.details == details


class TestGoogleClassroomAssignmentError:
    """Test GoogleClassroomAssignmentError exception."""
    
    def test_google_classroom_assignment_error_default(self):
        """Test GoogleClassroomAssignmentError with default values."""
        error = GoogleClassroomAssignmentError()
        
        assert str(error) == "Google Classroom assignment error"
        assert error.message == "Google Classroom assignment error"
        assert error.error_code == "GOOGLE_CLASSROOM_ASSIGNMENT_ERROR"
        assert error.api_endpoint == "classroom.googleapis.com"
        assert error.status_code is None
        assert error.classroom_resource == "assignments"
        assert error.assignment_id is None
        assert error.course_id is None
        assert error.details == {}
    
    def test_google_classroom_assignment_error_with_assignment_id(self):
        """Test GoogleClassroomAssignmentError with assignment ID."""
        error = GoogleClassroomAssignmentError(assignment_id="assignment123")
        
        assert str(error) == "Google Classroom assignment error: assignment123"
        assert error.message == "Google Classroom assignment error: assignment123"
        assert error.error_code == "GOOGLE_CLASSROOM_ASSIGNMENT_ERROR"
        assert error.assignment_id == "assignment123"
    
    def test_google_classroom_assignment_error_with_course_id(self):
        """Test GoogleClassroomAssignmentError with course ID."""
        error = GoogleClassroomAssignmentError(course_id="course123")
        
        assert str(error) == "Google Classroom assignment error in course course123"
        assert error.message == "Google Classroom assignment error in course course123"
        assert error.error_code == "GOOGLE_CLASSROOM_ASSIGNMENT_ERROR"
        assert error.course_id == "course123"
    
    def test_google_classroom_assignment_error_with_both(self):
        """Test GoogleClassroomAssignmentError with both assignment and course ID."""
        error = GoogleClassroomAssignmentError(assignment_id="assignment123", course_id="course123")
        
        assert str(error) == "Google Classroom assignment error: assignment123 in course course123"
        assert error.message == "Google Classroom assignment error: assignment123 in course course123"
        assert error.error_code == "GOOGLE_CLASSROOM_ASSIGNMENT_ERROR"
        assert error.assignment_id == "assignment123"
        assert error.course_id == "course123"
    
    def test_google_classroom_assignment_error_custom(self):
        """Test GoogleClassroomAssignmentError with custom values."""
        details = {"operation": "grade"}
        error = GoogleClassroomAssignmentError(
            message="Custom assignment error",
            error_code="CUSTOM_ASSIGNMENT_ERROR",
            assignment_id="assignment123",
            course_id="course123",
            details=details
        )
        
        assert str(error) == "Custom assignment error: assignment123 in course course123"
        assert error.message == "Custom assignment error: assignment123 in course course123"
        assert error.error_code == "CUSTOM_ASSIGNMENT_ERROR"
        assert error.api_endpoint == "classroom.googleapis.com"
        assert error.classroom_resource == "assignments"
        assert error.assignment_id == "assignment123"
        assert error.course_id == "course123"
        assert error.details == details