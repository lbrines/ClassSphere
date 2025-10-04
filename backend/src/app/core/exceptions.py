"""Custom exceptions with Template Method Pattern for consistent message construction."""

from typing import Any, Dict, Optional


class BaseAPIException(Exception):
    """Base exception class implementing Template Method Pattern for message construction."""

    def __init__(
        self,
        message: Optional[str] = None,
        status_code: int = 500,
        **kwargs: Any
    ):
        self.status_code = status_code
        self.details = kwargs

        # Template Method Pattern: construct message using template method
        default_message = getattr(self, 'default_message', 'An error occurred')
        self.message = self._build_message(message, default_message, **kwargs)
        super().__init__(self.message)

    def _build_message(self, custom_message: Optional[str], default_message: str, **kwargs: Any) -> str:
        """Template method for message construction."""
        if custom_message and custom_message != default_message:
            # Prioritize custom message with additional parameters
            return self._construct_custom_with_params(custom_message, **kwargs)
        return self._construct_automatic_message(default_message, **kwargs)

    def _construct_custom_with_params(self, custom_message: str, **kwargs: Any) -> str:
        """Hook method for custom message construction with parameters."""
        if kwargs:
            # Add relevant parameters to custom message
            param_info = ", ".join(f"{k}: {v}" for k, v in kwargs.items() if v is not None)
            if param_info:
                return f"{custom_message} ({param_info})"
        return custom_message

    def _construct_automatic_message(self, default_message: str, **kwargs: Any) -> str:
        """Hook method for automatic message construction."""
        return default_message


class AuthenticationError(BaseAPIException):
    """Authentication failed exception."""

    default_message = "Authentication failed"

    def __init__(self, message: Optional[str] = None, **kwargs: Any):
        super().__init__(message, status_code=401, **kwargs)


class TokenExpiredError(AuthenticationError):
    """Token expired exception."""

    default_message = "Token has expired"

    def _construct_automatic_message(self, default_message: str, **kwargs: Any) -> str:
        """Custom automatic message construction for token expiration."""
        token_type = kwargs.get('token_type', 'Token')
        expired_at = kwargs.get('expired_at')

        message = f"{token_type} has expired"
        if expired_at:
            message = f"{message} at {expired_at}"

        return message


class OAuthError(AuthenticationError):
    """OAuth authentication error."""

    default_message = "OAuth authentication failed"

    def _construct_automatic_message(self, default_message: str, **kwargs: Any) -> str:
        """Custom automatic message construction for OAuth errors."""
        provider = kwargs.get('provider')
        error_code = kwargs.get('error_code')

        if provider:
            message = f"{provider} authentication failed"
        else:
            message = default_message

        if error_code:
            message = f"{message} (code: {error_code})"

        return message


class GoogleAPIError(BaseAPIException):
    """Google API error."""

    default_message = "Google API error"

    def __init__(self, message: Optional[str] = None, **kwargs: Any):
        super().__init__(message, status_code=502, **kwargs)

    def _construct_automatic_message(self, default_message: str, **kwargs: Any) -> str:
        """Custom automatic message construction for Google API errors."""
        api_name = kwargs.get('api_name', 'Google API')
        error_code = kwargs.get('error_code')
        quota_exceeded = kwargs.get('quota_exceeded', False)

        if quota_exceeded:
            return f"{api_name} quota exceeded"

        message = f"{api_name} error"
        if error_code:
            message = f"{message} (code: {error_code})"

        return message


class NotFoundError(BaseAPIException):
    """Resource not found exception."""

    default_message = "Resource not found"

    def __init__(self, message: Optional[str] = None, **kwargs: Any):
        super().__init__(message, status_code=404, **kwargs)

    def _construct_automatic_message(self, default_message: str, **kwargs: Any) -> str:
        """Custom automatic message construction for not found errors."""
        resource_type = kwargs.get('resource_type')
        resource_id = kwargs.get('resource_id')

        if resource_type:
            message = f"{resource_type} not found"
        else:
            message = default_message

        if resource_id:
            message = f"{message}: {resource_id}"

        return message


class ConflictError(BaseAPIException):
    """Resource conflict exception."""

    default_message = "Resource conflict"

    def __init__(self, message: Optional[str] = None, **kwargs: Any):
        super().__init__(message, status_code=409, **kwargs)

    def _construct_automatic_message(self, default_message: str, **kwargs: Any) -> str:
        """Custom automatic message construction for conflict errors."""
        resource_type = kwargs.get('resource_type')
        conflict_field = kwargs.get('conflict_field')

        if resource_type and conflict_field:
            return f"{resource_type} with {conflict_field} already exists"
        elif resource_type:
            return f"{resource_type} already exists"

        return default_message


class ValidationError(BaseAPIException):
    """Validation error exception."""

    default_message = "Validation failed"

    def __init__(self, message: Optional[str] = None, **kwargs: Any):
        super().__init__(message, status_code=422, **kwargs)

    def _construct_automatic_message(self, default_message: str, **kwargs: Any) -> str:
        """Custom automatic message construction for validation errors."""
        field_name = kwargs.get('field_name')
        validation_type = kwargs.get('validation_type')

        if field_name and validation_type:
            return f"Validation failed for {field_name}: {validation_type}"
        elif field_name:
            return f"Validation failed for {field_name}"

        return default_message


class ServiceUnavailableError(BaseAPIException):
    """Service unavailable exception."""

    default_message = "Service temporarily unavailable"

    def __init__(self, message: Optional[str] = None, **kwargs: Any):
        super().__init__(message, status_code=503, **kwargs)

    def _construct_automatic_message(self, default_message: str, **kwargs: Any) -> str:
        """Custom automatic message construction for service unavailable errors."""
        service_name = kwargs.get('service_name')
        retry_after = kwargs.get('retry_after')

        if service_name:
            message = f"{service_name} temporarily unavailable"
        else:
            message = default_message

        if retry_after:
            message = f"{message} (retry after {retry_after} seconds)"

        return message


class DatabaseError(BaseAPIException):
    """Database operation error."""

    default_message = "Database operation failed"

    def __init__(self, message: Optional[str] = None, **kwargs: Any):
        super().__init__(message, status_code=500, **kwargs)

    def _construct_automatic_message(self, default_message: str, **kwargs: Any) -> str:
        """Custom automatic message construction for database errors."""
        operation = kwargs.get('operation')
        table = kwargs.get('table')

        if operation and table:
            return f"Database {operation} failed for {table}"
        elif operation:
            return f"Database {operation} failed"

        return default_message


class CacheError(BaseAPIException):
    """Cache operation error."""

    default_message = "Cache operation failed"

    def __init__(self, message: Optional[str] = None, **kwargs: Any):
        super().__init__(message, status_code=500, **kwargs)

    def _construct_automatic_message(self, default_message: str, **kwargs: Any) -> str:
        """Custom automatic message construction for cache errors."""
        operation = kwargs.get('operation')
        cache_key = kwargs.get('cache_key')

        if operation and cache_key:
            return f"Cache {operation} failed for key: {cache_key}"
        elif operation:
            return f"Cache {operation} failed"

        return default_message


class ExternalServiceError(BaseAPIException):
    """External service error."""

    default_message = "External service error"

    def __init__(self, message: Optional[str] = None, **kwargs: Any):
        # Extract status_code if it's meant for HTTP status, not our exception status
        http_status_code = kwargs.pop('status_code', None)
        if http_status_code:
            kwargs['http_status_code'] = http_status_code
        super().__init__(message, status_code=502, **kwargs)

    def _construct_automatic_message(self, default_message: str, **kwargs: Any) -> str:
        """Custom automatic message construction for external service errors."""
        service_name = kwargs.get('service_name')
        endpoint = kwargs.get('endpoint')
        http_status_code = kwargs.get('http_status_code')

        if service_name:
            message = f"{service_name} service error"
        else:
            message = default_message

        if endpoint:
            message = f"{message} at {endpoint}"

        if http_status_code:
            message = f"{message} (HTTP {http_status_code})"

        return message


class DeprecatedAPIError(BaseAPIException):
    """Deprecated API usage error."""

    default_message = "Deprecated API usage"

    def __init__(self, message: Optional[str] = None, **kwargs: Any):
        super().__init__(message, status_code=410, **kwargs)

    def _construct_automatic_message(self, default_message: str, **kwargs: Any) -> str:
        """Custom automatic message construction for deprecated API errors."""
        api_version = kwargs.get('api_version')
        replacement_version = kwargs.get('replacement_version')
        sunset_date = kwargs.get('sunset_date')

        message = default_message

        if api_version:
            message = f"API version {api_version} is deprecated"

        if replacement_version:
            message = f"{message}, use version {replacement_version}"

        if sunset_date:
            message = f"{message} (sunset: {sunset_date})"

        return message


class GoogleClassroomError(GoogleAPIError):
    """Google Classroom specific error."""

    default_message = "Google Classroom error"

    def _construct_automatic_message(self, default_message: str, **kwargs: Any) -> str:
        """Custom automatic message construction for Google Classroom errors."""
        course_id = kwargs.get('course_id')
        operation = kwargs.get('operation')
        error_code = kwargs.get('error_code')

        if operation:
            message = f"Google Classroom {operation} failed"
        else:
            message = default_message

        if course_id:
            message = f"{message} for course {course_id}"

        if error_code:
            message = f"{message} (code: {error_code})"

        return message