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
    
    def _build_message(self, custom_message: str, default_message: str, **kwargs) -> str:
        """Template method para construcción de mensajes."""
        if custom_message and custom_message != default_message:
            # Si hay mensaje personalizado, agregar parámetros adicionales si están disponibles
            resource_id = kwargs.get('resource_id')
            retry_after = kwargs.get('retry_after')
            table = kwargs.get('table')
            key = kwargs.get('key')
            endpoint = kwargs.get('endpoint')
            status_code = kwargs.get('status_code')
            alternative_endpoint = kwargs.get('alternative_endpoint')
            deprecation_date = kwargs.get('deprecation_date')
            removal_date = kwargs.get('removal_date')
            
            if resource_id:
                return f"{custom_message}: {resource_id}"
            elif retry_after:
                return f"{custom_message}, retry after {retry_after} seconds"
            elif table:
                return f"{custom_message} on table '{table}'"
            elif key:
                return f"{custom_message} for key '{key}'"
            elif alternative_endpoint or deprecation_date or removal_date:
                # Para DeprecatedAPIError con mensaje personalizado
                message = custom_message
                if deprecation_date:
                    message = f"{message} (deprecated since {deprecation_date})"
                if alternative_endpoint:
                    message = f"{message}, use '{alternative_endpoint}' instead"
                if removal_date:
                    message = f"{message}, will be removed on {removal_date}"
                return message
            elif endpoint and status_code:
                return f"{custom_message} at {endpoint} (status: {status_code})"
            elif endpoint:
                return f"{custom_message} at {endpoint}"
            elif status_code:
                return f"{custom_message} (status: {status_code})"
            
            return custom_message
        return self._construct_automatic_message(default_message, **kwargs)
    
    def _construct_automatic_message(self, default_message: str, **kwargs) -> str:
        """Hook method para construcción automática de mensajes."""
        return default_message


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
        final_message = self._build_message(
            custom_message=message,
            default_message="Resource not found",
            resource_type=resource_type,
            resource_id=resource_id
        )
        super().__init__(final_message, error_code, 404, details)
    
    def _construct_automatic_message(self, default_message: str, **kwargs) -> str:
        """Construye mensaje automático basado en resource_type y resource_id."""
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
        final_message = self._build_message(
            custom_message=message,
            default_message="Resource conflict",
            resource_type=resource_type,
            resource_id=resource_id
        )
        super().__init__(final_message, error_code, 409, details)
    
    def _construct_automatic_message(self, default_message: str, **kwargs) -> str:
        """Construye mensaje automático basado en resource_type y resource_id."""
        resource_type = kwargs.get('resource_type')
        resource_id = kwargs.get('resource_id')
        
        if resource_type:
            message = f"{resource_type} conflict"
        else:
            message = default_message
            
        if resource_id:
            message = f"{message}: {resource_id}"
            
        return message


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
        final_message = self._build_message(
            custom_message=message,
            default_message="Service unavailable",
            service_name=service_name,
            retry_after=retry_after
        )
        super().__init__(final_message, error_code, 503, details)
    
    def _construct_automatic_message(self, default_message: str, **kwargs) -> str:
        """Construye mensaje automático basado en service_name y retry_after."""
        service_name = kwargs.get('service_name')
        retry_after = kwargs.get('retry_after')
        
        if service_name:
            message = f"{service_name} service unavailable"
        else:
            message = default_message
            
        if retry_after:
            message = f"{message}, retry after {retry_after} seconds"
            
        return message


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
        final_message = self._build_message(
            custom_message=message,
            default_message="Database error",
            operation=operation,
            table=table
        )
        super().__init__(final_message, error_code, 500, details)
    
    def _construct_automatic_message(self, default_message: str, **kwargs) -> str:
        """Construye mensaje automático basado en operation y table."""
        operation = kwargs.get('operation')
        table = kwargs.get('table')
        
        if operation:
            message = f"Database {operation} error"
        else:
            message = default_message
            
        if table:
            message = f"{message} on table '{table}'"
            
        return message


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
        final_message = self._build_message(
            custom_message=message,
            default_message="Cache error",
            operation=operation,
            key=key
        )
        super().__init__(final_message, error_code, 500, details)
    
    def _construct_automatic_message(self, default_message: str, **kwargs) -> str:
        """Construye mensaje automático basado en operation y key."""
        operation = kwargs.get('operation')
        key = kwargs.get('key')
        
        if operation:
            message = f"Cache {operation} error"
        else:
            message = default_message
            
        if key:
            message = f"{message} for key '{key}'"
            
        return message


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
        final_message = self._build_message(
            custom_message=message,
            default_message="External service error",
            service_name=service_name,
            endpoint=endpoint,
            status_code=status_code
        )
        # Usar el status_code proporcionado si está disponible, sino usar 502
        http_status_code = status_code if status_code else 502
        super().__init__(final_message, error_code, http_status_code, details)
    
    def _construct_automatic_message(self, default_message: str, **kwargs) -> str:
        """Construye mensaje automático basado en service_name, endpoint y status_code."""
        service_name = kwargs.get('service_name')
        endpoint = kwargs.get('endpoint')
        status_code = kwargs.get('status_code')
        
        if service_name:
            message = f"{service_name} service error"
        else:
            message = default_message
            
        if endpoint:
            message = f"{message} at {endpoint}"
            
        if status_code:
            message = f"{message} (status: {status_code})"
            
        return message


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
        final_message = self._build_message(
            custom_message=message,
            default_message="API endpoint is deprecated",
            endpoint=endpoint,
            alternative_endpoint=alternative_endpoint,
            deprecation_date=deprecation_date,
            removal_date=removal_date
        )
        super().__init__(final_message, error_code, 410, details)
    
    def _construct_automatic_message(self, default_message: str, **kwargs) -> str:
        """Construye mensaje automático basado en endpoint, alternative_endpoint, deprecation_date y removal_date."""
        endpoint = kwargs.get('endpoint')
        alternative_endpoint = kwargs.get('alternative_endpoint')
        deprecation_date = kwargs.get('deprecation_date')
        removal_date = kwargs.get('removal_date')
        
        if endpoint:
            message = f"API endpoint '{endpoint}' is deprecated"
        else:
            message = default_message
            
        if deprecation_date:
            message = f"{message} (deprecated since {deprecation_date})"
            
        if alternative_endpoint:
            message = f"{message}, use '{alternative_endpoint}' instead"
            
        if removal_date:
            message = f"{message}, will be removed on {removal_date}"
            
        return message