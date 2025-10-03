"""
OAuth and Google API exceptions.
"""
from typing import Optional, Dict, Any


class OAuthError(Exception):
    """Base OAuth error."""
    
    def __init__(
        self,
        message: str = "OAuth error occurred",
        error_code: str = "OAUTH_ERROR",
        provider: Optional[str] = None,
        details: Optional[Dict[str, Any]] = None
    ):
        self.message = message
        self.error_code = error_code
        self.provider = provider
        self.details = details or {}
        super().__init__(self.message)


class OAuthProviderError(OAuthError):
    """OAuth provider error."""
    
    def __init__(
        self,
        message: str = "OAuth provider error",
        error_code: str = "OAUTH_PROVIDER_ERROR",
        provider: Optional[str] = None,
        provider_error: Optional[str] = None,
        details: Optional[Dict[str, Any]] = None
    ):
        self.provider_error = provider_error
        if provider_error:
            message = f"{message}: {provider_error}"
        super().__init__(message, error_code, provider, details)


class OAuthTokenError(OAuthError):
    """OAuth token error."""
    
    def __init__(
        self,
        message: str = "OAuth token error",
        error_code: str = "OAUTH_TOKEN_ERROR",
        provider: Optional[str] = None,
        token_type: Optional[str] = None,
        details: Optional[Dict[str, Any]] = None
    ):
        self.token_type = token_type
        if token_type:
            message = f"{message}: {token_type}"
        super().__init__(message, error_code, provider, details)


class OAuthAuthorizationError(OAuthError):
    """OAuth authorization error."""
    
    def __init__(
        self,
        message: str = "OAuth authorization failed",
        error_code: str = "OAUTH_AUTHORIZATION_ERROR",
        provider: Optional[str] = None,
        authorization_code: Optional[str] = None,
        details: Optional[Dict[str, Any]] = None
    ):
        self.authorization_code = authorization_code
        if authorization_code:
            message = f"{message}: {authorization_code}"
        super().__init__(message, error_code, provider, details)


class OAuthScopeError(OAuthError):
    """OAuth scope error."""
    
    def __init__(
        self,
        message: str = "OAuth scope error",
        error_code: str = "OAUTH_SCOPE_ERROR",
        provider: Optional[str] = None,
        required_scope: Optional[str] = None,
        granted_scopes: Optional[list] = None,
        details: Optional[Dict[str, Any]] = None
    ):
        self.required_scope = required_scope
        self.granted_scopes = granted_scopes or []
        if required_scope:
            message = f"{message}: {required_scope}"
        super().__init__(message, error_code, provider, details)


class OAuthRedirectError(OAuthError):
    """OAuth redirect error."""
    
    def __init__(
        self,
        message: str = "OAuth redirect error",
        error_code: str = "OAUTH_REDIRECT_ERROR",
        provider: Optional[str] = None,
        redirect_uri: Optional[str] = None,
        details: Optional[Dict[str, Any]] = None
    ):
        self.redirect_uri = redirect_uri
        if redirect_uri:
            message = f"{message}: {redirect_uri}"
        super().__init__(message, error_code, provider, details)


class GoogleAPIError(Exception):
    """Base Google API error."""
    
    def __init__(
        self,
        message: str = "Google API error occurred",
        error_code: str = "GOOGLE_API_ERROR",
        api_endpoint: Optional[str] = None,
        status_code: Optional[int] = None,
        details: Optional[Dict[str, Any]] = None
    ):
        self.message = message
        self.error_code = error_code
        self.api_endpoint = api_endpoint
        self.status_code = status_code
        self.details = details or {}
        super().__init__(self.message)


class GoogleAPIConnectionError(GoogleAPIError):
    """Google API connection error."""
    
    def __init__(
        self,
        message: str = "Failed to connect to Google API",
        error_code: str = "GOOGLE_API_CONNECTION_ERROR",
        api_endpoint: Optional[str] = None,
        details: Optional[Dict[str, Any]] = None
    ):
        super().__init__(message, error_code, api_endpoint, None, details)


class GoogleAPIAuthenticationError(GoogleAPIError):
    """Google API authentication error."""
    
    def __init__(
        self,
        message: str = "Google API authentication failed",
        error_code: str = "GOOGLE_API_AUTH_ERROR",
        api_endpoint: Optional[str] = None,
        details: Optional[Dict[str, Any]] = None
    ):
        super().__init__(message, error_code, api_endpoint, 401, details)


class GoogleAPIAuthorizationError(GoogleAPIError):
    """Google API authorization error."""
    
    def __init__(
        self,
        message: str = "Google API authorization failed",
        error_code: str = "GOOGLE_API_AUTHZ_ERROR",
        api_endpoint: Optional[str] = None,
        required_scopes: Optional[list] = None,
        details: Optional[Dict[str, Any]] = None
    ):
        self.required_scopes = required_scopes or []
        if required_scopes:
            message = f"{message}: {', '.join(required_scopes)}"
        super().__init__(message, error_code, api_endpoint, 403, details)


class GoogleAPIRateLimitError(GoogleAPIError):
    """Google API rate limit error."""
    
    def __init__(
        self,
        message: str = "Google API rate limit exceeded",
        error_code: str = "GOOGLE_API_RATE_LIMIT_ERROR",
        api_endpoint: Optional[str] = None,
        retry_after: Optional[int] = None,
        details: Optional[Dict[str, Any]] = None
    ):
        self.retry_after = retry_after
        if retry_after:
            message = f"{message}, retry after {retry_after} seconds"
        super().__init__(message, error_code, api_endpoint, 429, details)


class GoogleAPINotFoundError(GoogleAPIError):
    """Google API not found error."""
    
    def __init__(
        self,
        message: str = "Google API resource not found",
        error_code: str = "GOOGLE_API_NOT_FOUND_ERROR",
        api_endpoint: Optional[str] = None,
        resource_id: Optional[str] = None,
        details: Optional[Dict[str, Any]] = None
    ):
        self.resource_id = resource_id
        if resource_id:
            message = f"{message}: {resource_id}"
        super().__init__(message, error_code, api_endpoint, 404, details)


class GoogleAPIBadRequestError(GoogleAPIError):
    """Google API bad request error."""
    
    def __init__(
        self,
        message: str = "Google API bad request",
        error_code: str = "GOOGLE_API_BAD_REQUEST_ERROR",
        api_endpoint: Optional[str] = None,
        validation_errors: Optional[list] = None,
        details: Optional[Dict[str, Any]] = None
    ):
        self.validation_errors = validation_errors or []
        if validation_errors:
            message = f"{message}: {', '.join(validation_errors)}"
        super().__init__(message, error_code, api_endpoint, 400, details)


class GoogleAPIServerError(GoogleAPIError):
    """Google API server error."""
    
    def __init__(
        self,
        message: str = "Google API server error",
        error_code: str = "GOOGLE_API_SERVER_ERROR",
        api_endpoint: Optional[str] = None,
        status_code: Optional[int] = None,
        details: Optional[Dict[str, Any]] = None
    ):
        super().__init__(message, error_code, api_endpoint, status_code or 500, details)


class GoogleAPITimeoutError(GoogleAPIError):
    """Google API timeout error."""
    
    def __init__(
        self,
        message: str = "Google API request timeout",
        error_code: str = "GOOGLE_API_TIMEOUT_ERROR",
        api_endpoint: Optional[str] = None,
        timeout_duration: Optional[int] = None,
        details: Optional[Dict[str, Any]] = None
    ):
        self.timeout_duration = timeout_duration
        if timeout_duration:
            message = f"{message} after {timeout_duration} seconds"
        super().__init__(message, error_code, api_endpoint, 408, details)


class GoogleClassroomError(GoogleAPIError):
    """Google Classroom specific error."""
    
    def __init__(
        self,
        message: str = "Google Classroom API error",
        error_code: str = "GOOGLE_CLASSROOM_ERROR",
        classroom_resource: Optional[str] = None,
        details: Optional[Dict[str, Any]] = None
    ):
        self.classroom_resource = classroom_resource
        if classroom_resource:
            message = f"{message}: {classroom_resource}"
        super().__init__(message, error_code, "classroom.googleapis.com", None, details)


class GoogleClassroomCourseError(GoogleClassroomError):
    """Google Classroom course error."""
    
    def __init__(
        self,
        message: str = "Google Classroom course error",
        error_code: str = "GOOGLE_CLASSROOM_COURSE_ERROR",
        course_id: Optional[str] = None,
        details: Optional[Dict[str, Any]] = None
    ):
        self.course_id = course_id
        if course_id:
            message = f"{message}: {course_id}"
        super().__init__(message, error_code, "courses", details)


class GoogleClassroomStudentError(GoogleClassroomError):
    """Google Classroom student error."""
    
    def __init__(
        self,
        message: str = "Google Classroom student error",
        error_code: str = "GOOGLE_CLASSROOM_STUDENT_ERROR",
        student_id: Optional[str] = None,
        course_id: Optional[str] = None,
        details: Optional[Dict[str, Any]] = None
    ):
        self.student_id = student_id
        self.course_id = course_id
        if student_id:
            message = f"{message}: {student_id}"
        if course_id:
            message = f"{message} in course {course_id}"
        super().__init__(message, error_code, "students", details)


class GoogleClassroomAssignmentError(GoogleClassroomError):
    """Google Classroom assignment error."""
    
    def __init__(
        self,
        message: str = "Google Classroom assignment error",
        error_code: str = "GOOGLE_CLASSROOM_ASSIGNMENT_ERROR",
        assignment_id: Optional[str] = None,
        course_id: Optional[str] = None,
        details: Optional[Dict[str, Any]] = None
    ):
        self.assignment_id = assignment_id
        self.course_id = course_id
        if assignment_id:
            message = f"{message}: {assignment_id}"
        if course_id:
            message = f"{message} in course {course_id}"
        super().__init__(message, error_code, "assignments", details)