"""
Base exceptions and common error handling.
"""
from typing import Optional, Dict, Any


class BaseAPIException(Exception):
    """Base API exception."""
    
    def __init__(
        self,
        message: str,
        error_code: str,
        status_code: int = 500,
        details: Optional[Dict[str, Any]] = None
    ):
        self.message = message
        self.error_code = error_code
        self.status_code = status_code
        self.details = details or {}
        super().__init__(self.message)


class ValidationError(BaseAPIException):
    """Validation error."""
    
    def __init__(
        self,
        message: str = "Validation error",
        error_code: str = "VALIDATION_ERROR",
        field: Optional[str] = None,
        value: Optional[Any] = None,
        details: Optional[Dict[str, Any]] = None
    ):
        self.field = field
        self.value = value
        if field:
            message = f"{message} in field '{field}'"
        if value is not None:
            message = f"{message}: {value}"
        super().__init__(message, error_code, 400, details)


class NotFoundError(BaseAPIException):
    """Resource not found error."""
    
    def __init__(
        self,
        message: str = "Resource not found",
        error_code: str = "NOT_FOUND_ERROR",
        resource_type: Optional[str] = None,
        resource_id: Optional[str] = None,
        details: Optional[Dict[str, Any]] = None
    ):
        self.resource_type = resource_type
        self.resource_id = resource_id
        if resource_type:
            message = f"{resource_type} not found"
        if resource_id:
            message = f"{message}: {resource_id}"
        super().__init__(message, error_code, 404, details)


class ConflictError(BaseAPIException):
    """Resource conflict error."""
    
    def __init__(
        self,
        message: str = "Resource conflict",
        error_code: str = "CONFLICT_ERROR",
        resource_type: Optional[str] = None,
        resource_id: Optional[str] = None,
        details: Optional[Dict[str, Any]] = None
    ):
        self.resource_type = resource_type
        self.resource_id = resource_id
        if resource_type:
            message = f"{resource_type} conflict"
        if resource_id:
            message = f"{message}: {resource_id}"
        super().__init__(message, error_code, 409, details)


class UnauthorizedError(BaseAPIException):
    """Unauthorized error."""
    
    def __init__(
        self,
        message: str = "Unauthorized access",
        error_code: str = "UNAUTHORIZED_ERROR",
        details: Optional[Dict[str, Any]] = None
    ):
        super().__init__(message, error_code, 401, details)


class ForbiddenError(BaseAPIException):
    """Forbidden error."""
    
    def __init__(
        self,
        message: str = "Access forbidden",
        error_code: str = "FORBIDDEN_ERROR",
        required_permission: Optional[str] = None,
        details: Optional[Dict[str, Any]] = None
    ):
        self.required_permission = required_permission
        if required_permission:
            message = f"{message}: {required_permission}"
        super().__init__(message, error_code, 403, details)


class BadRequestError(BaseAPIException):
    """Bad request error."""
    
    def __init__(
        self,
        message: str = "Bad request",
        error_code: str = "BAD_REQUEST_ERROR",
        details: Optional[Dict[str, Any]] = None
    ):
        super().__init__(message, error_code, 400, details)


class InternalServerError(BaseAPIException):
    """Internal server error."""
    
    def __init__(
        self,
        message: str = "Internal server error",
        error_code: str = "INTERNAL_SERVER_ERROR",
        details: Optional[Dict[str, Any]] = None
    ):
        super().__init__(message, error_code, 500, details)


class ServiceUnavailableError(BaseAPIException):
    """Service unavailable error."""
    
    def __init__(
        self,
        message: str = "Service unavailable",
        error_code: str = "SERVICE_UNAVAILABLE_ERROR",
        service_name: Optional[str] = None,
        retry_after: Optional[int] = None,
        details: Optional[Dict[str, Any]] = None
    ):
        self.service_name = service_name
        self.retry_after = retry_after
        if service_name:
            message = f"{service_name} service unavailable"
        if retry_after:
            message = f"{message}, retry after {retry_after} seconds"
        super().__init__(message, error_code, 503, details)


class DatabaseError(BaseAPIException):
    """Database error."""
    
    def __init__(
        self,
        message: str = "Database error",
        error_code: str = "DATABASE_ERROR",
        operation: Optional[str] = None,
        table: Optional[str] = None,
        details: Optional[Dict[str, Any]] = None
    ):
        self.operation = operation
        self.table = table
        if operation:
            message = f"Database {operation} error"
        if table:
            message = f"{message} on table '{table}'"
        super().__init__(message, error_code, 500, details)


class CacheError(BaseAPIException):
    """Cache error."""
    
    def __init__(
        self,
        message: str = "Cache error",
        error_code: str = "CACHE_ERROR",
        operation: Optional[str] = None,
        key: Optional[str] = None,
        details: Optional[Dict[str, Any]] = None
    ):
        self.operation = operation
        self.key = key
        if operation:
            message = f"Cache {operation} error"
        if key:
            message = f"{message} for key '{key}'"
        super().__init__(message, error_code, 500, details)


class ExternalServiceError(BaseAPIException):
    """External service error."""
    
    def __init__(
        self,
        message: str = "External service error",
        error_code: str = "EXTERNAL_SERVICE_ERROR",
        service_name: Optional[str] = None,
        endpoint: Optional[str] = None,
        status_code: Optional[int] = None,
        details: Optional[Dict[str, Any]] = None
    ):
        self.service_name = service_name
        self.endpoint = endpoint
        self.status_code = status_code
        if service_name:
            message = f"{service_name} service error"
        if endpoint:
            message = f"{message} at {endpoint}"
        if status_code:
            message = f"{message} (status: {status_code})"
        super().__init__(message, error_code, 502, details)


class ConfigurationError(BaseAPIException):
    """Configuration error."""
    
    def __init__(
        self,
        message: str = "Configuration error",
        error_code: str = "CONFIGURATION_ERROR",
        config_key: Optional[str] = None,
        details: Optional[Dict[str, Any]] = None
    ):
        self.config_key = config_key
        if config_key:
            message = f"{message} for '{config_key}'"
        super().__init__(message, error_code, 500, details)


class MigrationError(BaseAPIException):
    """Migration error."""
    
    def __init__(
        self,
        message: str = "Migration error",
        error_code: str = "MIGRATION_ERROR",
        migration_name: Optional[str] = None,
        from_version: Optional[str] = None,
        to_version: Optional[str] = None,
        details: Optional[Dict[str, Any]] = None
    ):
        self.migration_name = migration_name
        self.from_version = from_version
        self.to_version = to_version
        if migration_name:
            message = f"{message} in '{migration_name}'"
        if from_version and to_version:
            message = f"{message} from {from_version} to {to_version}"
        super().__init__(message, error_code, 500, details)


class DeprecatedAPIError(BaseAPIException):
    """Deprecated API error."""
    
    def __init__(
        self,
        message: str = "API endpoint is deprecated",
        error_code: str = "DEPRECATED_API_ERROR",
        endpoint: Optional[str] = None,
        alternative_endpoint: Optional[str] = None,
        deprecation_date: Optional[str] = None,
        removal_date: Optional[str] = None,
        details: Optional[Dict[str, Any]] = None
    ):
        self.endpoint = endpoint
        self.alternative_endpoint = alternative_endpoint
        self.deprecation_date = deprecation_date
        self.removal_date = removal_date
        if endpoint:
            message = f"API endpoint '{endpoint}' is deprecated"
        if alternative_endpoint:
            message = f"{message}, use '{alternative_endpoint}' instead"
        if deprecation_date:
            message = f"{message} (deprecated since {deprecation_date})"
        if removal_date:
            message = f"{message}, will be removed on {removal_date}"
        super().__init__(message, error_code, 410, details)