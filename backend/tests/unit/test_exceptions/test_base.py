"""
Unit tests for base exceptions.
"""
import pytest
from src.app.exceptions.base import (
    BaseAPIException, ValidationError, NotFoundError, ConflictError,
    UnauthorizedError, ForbiddenError, BadRequestError, InternalServerError,
    ServiceUnavailableError, DatabaseError, CacheError, ExternalServiceError,
    ConfigurationError, MigrationError, DeprecatedAPIError
)


class TestBaseAPIException:
    """Test BaseAPIException exception."""
    
    def test_base_api_exception_default(self):
        """Test BaseAPIException with default values."""
        error = BaseAPIException("Test error", "TEST_ERROR")
        
        assert str(error) == "Test error"
        assert error.message == "Test error"
        assert error.error_code == "TEST_ERROR"
        assert error.status_code == 500
        assert error.details == {}
    
    def test_base_api_exception_custom(self):
        """Test BaseAPIException with custom values."""
        details = {"field": "value"}
        error = BaseAPIException(
            message="Custom error",
            error_code="CUSTOM_ERROR",
            status_code=400,
            details=details
        )
        
        assert str(error) == "Custom error"
        assert error.message == "Custom error"
        assert error.error_code == "CUSTOM_ERROR"
        assert error.status_code == 400
        assert error.details == details


class TestValidationError:
    """Test ValidationError exception."""
    
    def test_validation_error_default(self):
        """Test ValidationError with default values."""
        error = ValidationError()
        
        assert str(error) == "Validation error"
        assert error.message == "Validation error"
        assert error.error_code == "VALIDATION_ERROR"
        assert error.status_code == 400
        assert error.field is None
        assert error.value is None
        assert error.details == {}
    
    def test_validation_error_with_field(self):
        """Test ValidationError with field."""
        error = ValidationError(field="email")
        
        assert str(error) == "Validation error in field 'email'"
        assert error.message == "Validation error in field 'email'"
        assert error.error_code == "VALIDATION_ERROR"
        assert error.field == "email"
    
    def test_validation_error_with_value(self):
        """Test ValidationError with value."""
        error = ValidationError(value="invalid@")
        
        assert str(error) == "Validation error: invalid@"
        assert error.message == "Validation error: invalid@"
        assert error.error_code == "VALIDATION_ERROR"
        assert error.value == "invalid@"
    
    def test_validation_error_with_both(self):
        """Test ValidationError with field and value."""
        error = ValidationError(field="email", value="invalid@")
        
        assert str(error) == "Validation error in field 'email': invalid@"
        assert error.message == "Validation error in field 'email': invalid@"
        assert error.error_code == "VALIDATION_ERROR"
        assert error.field == "email"
        assert error.value == "invalid@"
    
    def test_validation_error_custom(self):
        """Test ValidationError with custom values."""
        details = {"constraint": "email_format"}
        error = ValidationError(
            message="Custom validation error",
            error_code="CUSTOM_VALIDATION_ERROR",
            field="email",
            value="invalid@",
            details=details
        )
        
        assert str(error) == "Custom validation error in field 'email': invalid@"
        assert error.message == "Custom validation error in field 'email': invalid@"
        assert error.error_code == "CUSTOM_VALIDATION_ERROR"
        assert error.field == "email"
        assert error.value == "invalid@"
        assert error.details == details


class TestNotFoundError:
    """Test NotFoundError exception."""
    
    def test_not_found_error_default(self):
        """Test NotFoundError with default values."""
        error = NotFoundError()
        
        assert str(error) == "Resource not found"
        assert error.message == "Resource not found"
        assert error.error_code == "NOT_FOUND_ERROR"
        assert error.status_code == 404
        assert error.resource_type is None
        assert error.resource_id is None
        assert error.details == {}
    
    def test_not_found_error_with_resource_type(self):
        """Test NotFoundError with resource type."""
        error = NotFoundError(resource_type="User")
        
        assert str(error) == "User not found"
        assert error.message == "User not found"
        assert error.error_code == "NOT_FOUND_ERROR"
        assert error.resource_type == "User"
    
    def test_not_found_error_with_resource_id(self):
        """Test NotFoundError with resource ID."""
        error = NotFoundError(resource_id="user123")
        
        assert str(error) == "Resource not found: user123"
        assert error.message == "Resource not found: user123"
        assert error.error_code == "NOT_FOUND_ERROR"
        assert error.resource_id == "user123"
    
    def test_not_found_error_with_both(self):
        """Test NotFoundError with resource type and ID."""
        error = NotFoundError(resource_type="User", resource_id="user123")
        
        assert str(error) == "User not found: user123"
        assert error.message == "User not found: user123"
        assert error.error_code == "NOT_FOUND_ERROR"
        assert error.resource_type == "User"
        assert error.resource_id == "user123"
    
    def test_not_found_error_custom(self):
        """Test NotFoundError with custom values."""
        details = {"search_criteria": "email"}
        error = NotFoundError(
            message="Custom not found error",
            error_code="CUSTOM_NOT_FOUND_ERROR",
            resource_type="User",
            resource_id="user123",
            details=details
        )
        
        assert str(error) == "Custom not found error: user123"
        assert error.message == "Custom not found error: user123"
        assert error.error_code == "CUSTOM_NOT_FOUND_ERROR"
        assert error.resource_type == "User"
        assert error.resource_id == "user123"
        assert error.details == details


class TestConflictError:
    """Test ConflictError exception."""
    
    def test_conflict_error_default(self):
        """Test ConflictError with default values."""
        error = ConflictError()
        
        assert str(error) == "Resource conflict"
        assert error.message == "Resource conflict"
        assert error.error_code == "CONFLICT_ERROR"
        assert error.status_code == 409
        assert error.resource_type is None
        assert error.resource_id is None
        assert error.details == {}
    
    def test_conflict_error_with_resource_type(self):
        """Test ConflictError with resource type."""
        error = ConflictError(resource_type="User")
        
        assert str(error) == "User conflict"
        assert error.message == "User conflict"
        assert error.error_code == "CONFLICT_ERROR"
        assert error.resource_type == "User"
    
    def test_conflict_error_with_resource_id(self):
        """Test ConflictError with resource ID."""
        error = ConflictError(resource_id="user123")
        
        assert str(error) == "Resource conflict: user123"
        assert error.message == "Resource conflict: user123"
        assert error.error_code == "CONFLICT_ERROR"
        assert error.resource_id == "user123"
    
    def test_conflict_error_custom(self):
        """Test ConflictError with custom values."""
        details = {"conflict_reason": "duplicate_email"}
        error = ConflictError(
            message="Custom conflict error",
            error_code="CUSTOM_CONFLICT_ERROR",
            resource_type="User",
            resource_id="user123",
            details=details
        )
        
        assert str(error) == "Custom conflict error: user123"
        assert error.message == "Custom conflict error: user123"
        assert error.error_code == "CUSTOM_CONFLICT_ERROR"
        assert error.resource_type == "User"
        assert error.resource_id == "user123"
        assert error.details == details


class TestUnauthorizedError:
    """Test UnauthorizedError exception."""
    
    def test_unauthorized_error_default(self):
        """Test UnauthorizedError with default values."""
        error = UnauthorizedError()
        
        assert str(error) == "Unauthorized access"
        assert error.message == "Unauthorized access"
        assert error.error_code == "UNAUTHORIZED_ERROR"
        assert error.status_code == 401
        assert error.details == {}
    
    def test_unauthorized_error_custom(self):
        """Test UnauthorizedError with custom values."""
        details = {"required_auth": "bearer_token"}
        error = UnauthorizedError(
            message="Custom unauthorized error",
            error_code="CUSTOM_UNAUTHORIZED_ERROR",
            details=details
        )
        
        assert str(error) == "Custom unauthorized error"
        assert error.message == "Custom unauthorized error"
        assert error.error_code == "CUSTOM_UNAUTHORIZED_ERROR"
        assert error.status_code == 401
        assert error.details == details


class TestForbiddenError:
    """Test ForbiddenError exception."""
    
    def test_forbidden_error_default(self):
        """Test ForbiddenError with default values."""
        error = ForbiddenError()
        
        assert str(error) == "Access forbidden"
        assert error.message == "Access forbidden"
        assert error.error_code == "FORBIDDEN_ERROR"
        assert error.status_code == 403
        assert error.required_permission is None
        assert error.details == {}
    
    def test_forbidden_error_with_permission(self):
        """Test ForbiddenError with required permission."""
        error = ForbiddenError(required_permission="admin")
        
        assert str(error) == "Access forbidden: admin"
        assert error.message == "Access forbidden: admin"
        assert error.error_code == "FORBIDDEN_ERROR"
        assert error.required_permission == "admin"
    
    def test_forbidden_error_custom(self):
        """Test ForbiddenError with custom values."""
        details = {"user_role": "student"}
        error = ForbiddenError(
            message="Custom forbidden error",
            error_code="CUSTOM_FORBIDDEN_ERROR",
            required_permission="admin",
            details=details
        )
        
        assert str(error) == "Custom forbidden error: admin"
        assert error.message == "Custom forbidden error: admin"
        assert error.error_code == "CUSTOM_FORBIDDEN_ERROR"
        assert error.status_code == 403
        assert error.required_permission == "admin"
        assert error.details == details


class TestBadRequestError:
    """Test BadRequestError exception."""
    
    def test_bad_request_error_default(self):
        """Test BadRequestError with default values."""
        error = BadRequestError()
        
        assert str(error) == "Bad request"
        assert error.message == "Bad request"
        assert error.error_code == "BAD_REQUEST_ERROR"
        assert error.status_code == 400
        assert error.details == {}
    
    def test_bad_request_error_custom(self):
        """Test BadRequestError with custom values."""
        details = {"invalid_field": "email"}
        error = BadRequestError(
            message="Custom bad request error",
            error_code="CUSTOM_BAD_REQUEST_ERROR",
            details=details
        )
        
        assert str(error) == "Custom bad request error"
        assert error.message == "Custom bad request error"
        assert error.error_code == "CUSTOM_BAD_REQUEST_ERROR"
        assert error.status_code == 400
        assert error.details == details


class TestInternalServerError:
    """Test InternalServerError exception."""
    
    def test_internal_server_error_default(self):
        """Test InternalServerError with default values."""
        error = InternalServerError()
        
        assert str(error) == "Internal server error"
        assert error.message == "Internal server error"
        assert error.error_code == "INTERNAL_SERVER_ERROR"
        assert error.status_code == 500
        assert error.details == {}
    
    def test_internal_server_error_custom(self):
        """Test InternalServerError with custom values."""
        details = {"error_id": "err123"}
        error = InternalServerError(
            message="Custom internal server error",
            error_code="CUSTOM_INTERNAL_SERVER_ERROR",
            details=details
        )
        
        assert str(error) == "Custom internal server error"
        assert error.message == "Custom internal server error"
        assert error.error_code == "CUSTOM_INTERNAL_SERVER_ERROR"
        assert error.status_code == 500
        assert error.details == details


class TestServiceUnavailableError:
    """Test ServiceUnavailableError exception."""
    
    def test_service_unavailable_error_default(self):
        """Test ServiceUnavailableError with default values."""
        error = ServiceUnavailableError()
        
        assert str(error) == "Service unavailable"
        assert error.message == "Service unavailable"
        assert error.error_code == "SERVICE_UNAVAILABLE_ERROR"
        assert error.status_code == 503
        assert error.service_name is None
        assert error.retry_after is None
        assert error.details == {}
    
    def test_service_unavailable_error_with_service_name(self):
        """Test ServiceUnavailableError with service name."""
        error = ServiceUnavailableError(service_name="database")
        
        assert str(error) == "database service unavailable"
        assert error.message == "database service unavailable"
        assert error.error_code == "SERVICE_UNAVAILABLE_ERROR"
        assert error.service_name == "database"
    
    def test_service_unavailable_error_with_retry_after(self):
        """Test ServiceUnavailableError with retry after."""
        error = ServiceUnavailableError(retry_after=60)
        
        assert str(error) == "Service unavailable, retry after 60 seconds"
        assert error.message == "Service unavailable, retry after 60 seconds"
        assert error.error_code == "SERVICE_UNAVAILABLE_ERROR"
        assert error.retry_after == 60
    
    def test_service_unavailable_error_with_both(self):
        """Test ServiceUnavailableError with service name and retry after."""
        error = ServiceUnavailableError(service_name="database", retry_after=60)
        
        assert str(error) == "database service unavailable, retry after 60 seconds"
        assert error.message == "database service unavailable, retry after 60 seconds"
        assert error.error_code == "SERVICE_UNAVAILABLE_ERROR"
        assert error.service_name == "database"
        assert error.retry_after == 60
    
    def test_service_unavailable_error_custom(self):
        """Test ServiceUnavailableError with custom values."""
        details = {"maintenance_window": "2023-01-01T00:00:00Z"}
        error = ServiceUnavailableError(
            message="Custom service unavailable error",
            error_code="CUSTOM_SERVICE_UNAVAILABLE_ERROR",
            service_name="database",
            retry_after=120,
            details=details
        )
        
        assert str(error) == "Custom service unavailable error, retry after 120 seconds"
        assert error.message == "Custom service unavailable error, retry after 120 seconds"
        assert error.error_code == "CUSTOM_SERVICE_UNAVAILABLE_ERROR"
        assert error.service_name == "database"
        assert error.retry_after == 120
        assert error.details == details


class TestDatabaseError:
    """Test DatabaseError exception."""
    
    def test_database_error_default(self):
        """Test DatabaseError with default values."""
        error = DatabaseError()
        
        assert str(error) == "Database error"
        assert error.message == "Database error"
        assert error.error_code == "DATABASE_ERROR"
        assert error.status_code == 500
        assert error.operation is None
        assert error.table is None
        assert error.details == {}
    
    def test_database_error_with_operation(self):
        """Test DatabaseError with operation."""
        error = DatabaseError(operation="insert")
        
        assert str(error) == "Database insert error"
        assert error.message == "Database insert error"
        assert error.error_code == "DATABASE_ERROR"
        assert error.operation == "insert"
    
    def test_database_error_with_table(self):
        """Test DatabaseError with table."""
        error = DatabaseError(table="users")
        
        assert str(error) == "Database error on table 'users'"
        assert error.message == "Database error on table 'users'"
        assert error.error_code == "DATABASE_ERROR"
        assert error.table == "users"
    
    def test_database_error_with_both(self):
        """Test DatabaseError with operation and table."""
        error = DatabaseError(operation="insert", table="users")
        
        assert str(error) == "Database insert error on table 'users'"
        assert error.message == "Database insert error on table 'users'"
        assert error.error_code == "DATABASE_ERROR"
        assert error.operation == "insert"
        assert error.table == "users"
    
    def test_database_error_custom(self):
        """Test DatabaseError with custom values."""
        details = {"query": "SELECT * FROM users"}
        error = DatabaseError(
            message="Custom database error",
            error_code="CUSTOM_DATABASE_ERROR",
            operation="select",
            table="users",
            details=details
        )
        
        assert str(error) == "Custom database error on table 'users'"
        assert error.message == "Custom database error on table 'users'"
        assert error.error_code == "CUSTOM_DATABASE_ERROR"
        assert error.operation == "select"
        assert error.table == "users"
        assert error.details == details


class TestCacheError:
    """Test CacheError exception."""
    
    def test_cache_error_default(self):
        """Test CacheError with default values."""
        error = CacheError()
        
        assert str(error) == "Cache error"
        assert error.message == "Cache error"
        assert error.error_code == "CACHE_ERROR"
        assert error.status_code == 500
        assert error.operation is None
        assert error.key is None
        assert error.details == {}
    
    def test_cache_error_with_operation(self):
        """Test CacheError with operation."""
        error = CacheError(operation="get")
        
        assert str(error) == "Cache get error"
        assert error.message == "Cache get error"
        assert error.error_code == "CACHE_ERROR"
        assert error.operation == "get"
    
    def test_cache_error_with_key(self):
        """Test CacheError with key."""
        error = CacheError(key="user:123")
        
        assert str(error) == "Cache error for key 'user:123'"
        assert error.message == "Cache error for key 'user:123'"
        assert error.error_code == "CACHE_ERROR"
        assert error.key == "user:123"
    
    def test_cache_error_with_both(self):
        """Test CacheError with operation and key."""
        error = CacheError(operation="get", key="user:123")
        
        assert str(error) == "Cache get error for key 'user:123'"
        assert error.message == "Cache get error for key 'user:123'"
        assert error.error_code == "CACHE_ERROR"
        assert error.operation == "get"
        assert error.key == "user:123"
    
    def test_cache_error_custom(self):
        """Test CacheError with custom values."""
        details = {"ttl": 3600}
        error = CacheError(
            message="Custom cache error",
            error_code="CUSTOM_CACHE_ERROR",
            operation="set",
            key="user:123",
            details=details
        )
        
        assert str(error) == "Custom cache error for key 'user:123'"
        assert error.message == "Custom cache error for key 'user:123'"
        assert error.error_code == "CUSTOM_CACHE_ERROR"
        assert error.operation == "set"
        assert error.key == "user:123"
        assert error.details == details


class TestExternalServiceError:
    """Test ExternalServiceError exception."""
    
    def test_external_service_error_default(self):
        """Test ExternalServiceError with default values."""
        error = ExternalServiceError()
        
        assert str(error) == "External service error"
        assert error.message == "External service error"
        assert error.error_code == "EXTERNAL_SERVICE_ERROR"
        assert error.status_code == 502
        assert error.service_name is None
        assert error.endpoint is None
        assert error.status_code == 502
        assert error.details == {}
    
    def test_external_service_error_with_service_name(self):
        """Test ExternalServiceError with service name."""
        error = ExternalServiceError(service_name="google")
        
        assert str(error) == "google service error"
        assert error.message == "google service error"
        assert error.error_code == "EXTERNAL_SERVICE_ERROR"
        assert error.service_name == "google"
    
    def test_external_service_error_with_endpoint(self):
        """Test ExternalServiceError with endpoint."""
        error = ExternalServiceError(endpoint="https://api.google.com")
        
        assert str(error) == "External service error at https://api.google.com"
        assert error.message == "External service error at https://api.google.com"
        assert error.error_code == "EXTERNAL_SERVICE_ERROR"
        assert error.endpoint == "https://api.google.com"
    
    def test_external_service_error_with_status_code(self):
        """Test ExternalServiceError with status code."""
        error = ExternalServiceError(status_code=404)
        
        assert str(error) == "External service error (status: 404)"
        assert error.message == "External service error (status: 404)"
        assert error.error_code == "EXTERNAL_SERVICE_ERROR"
        assert error.status_code == 404
    
    def test_external_service_error_with_all(self):
        """Test ExternalServiceError with all parameters."""
        error = ExternalServiceError(
            service_name="google",
            endpoint="https://api.google.com",
            status_code=404
        )
        
        assert str(error) == "google service error at https://api.google.com (status: 404)"
        assert error.message == "google service error at https://api.google.com (status: 404)"
        assert error.error_code == "EXTERNAL_SERVICE_ERROR"
        assert error.service_name == "google"
        assert error.endpoint == "https://api.google.com"
        assert error.status_code == 404
    
    def test_external_service_error_custom(self):
        """Test ExternalServiceError with custom values."""
        details = {"response": "error_response"}
        error = ExternalServiceError(
            message="Custom external service error",
            error_code="CUSTOM_EXTERNAL_SERVICE_ERROR",
            service_name="google",
            endpoint="https://api.google.com",
            status_code=500,
            details=details
        )
        
        assert str(error) == "Custom external service error at https://api.google.com (status: 500)"
        assert error.message == "Custom external service error at https://api.google.com (status: 500)"
        assert error.error_code == "CUSTOM_EXTERNAL_SERVICE_ERROR"
        assert error.service_name == "google"
        assert error.endpoint == "https://api.google.com"
        assert error.status_code == 500
        assert error.details == details


class TestConfigurationError:
    """Test ConfigurationError exception."""
    
    def test_configuration_error_default(self):
        """Test ConfigurationError with default values."""
        error = ConfigurationError()
        
        assert str(error) == "Configuration error"
        assert error.message == "Configuration error"
        assert error.error_code == "CONFIGURATION_ERROR"
        assert error.status_code == 500
        assert error.config_key is None
        assert error.details == {}
    
    def test_configuration_error_with_config_key(self):
        """Test ConfigurationError with config key."""
        error = ConfigurationError(config_key="database_url")
        
        assert str(error) == "Configuration error for 'database_url'"
        assert error.message == "Configuration error for 'database_url'"
        assert error.error_code == "CONFIGURATION_ERROR"
        assert error.config_key == "database_url"
    
    def test_configuration_error_custom(self):
        """Test ConfigurationError with custom values."""
        details = {"expected_type": "string"}
        error = ConfigurationError(
            message="Custom configuration error",
            error_code="CUSTOM_CONFIGURATION_ERROR",
            config_key="database_url",
            details=details
        )
        
        assert str(error) == "Custom configuration error for 'database_url'"
        assert error.message == "Custom configuration error for 'database_url'"
        assert error.error_code == "CUSTOM_CONFIGURATION_ERROR"
        assert error.config_key == "database_url"
        assert error.details == details


class TestMigrationError:
    """Test MigrationError exception."""
    
    def test_migration_error_default(self):
        """Test MigrationError with default values."""
        error = MigrationError()
        
        assert str(error) == "Migration error"
        assert error.message == "Migration error"
        assert error.error_code == "MIGRATION_ERROR"
        assert error.status_code == 500
        assert error.migration_name is None
        assert error.from_version is None
        assert error.to_version is None
        assert error.details == {}
    
    def test_migration_error_with_migration_name(self):
        """Test MigrationError with migration name."""
        error = MigrationError(migration_name="add_users_table")
        
        assert str(error) == "Migration error in 'add_users_table'"
        assert error.message == "Migration error in 'add_users_table'"
        assert error.error_code == "MIGRATION_ERROR"
        assert error.migration_name == "add_users_table"
    
    def test_migration_error_with_versions(self):
        """Test MigrationError with from and to versions."""
        error = MigrationError(from_version="1.0", to_version="2.0")
        
        assert str(error) == "Migration error from 1.0 to 2.0"
        assert error.message == "Migration error from 1.0 to 2.0"
        assert error.error_code == "MIGRATION_ERROR"
        assert error.from_version == "1.0"
        assert error.to_version == "2.0"
    
    def test_migration_error_with_all(self):
        """Test MigrationError with all parameters."""
        error = MigrationError(
            migration_name="add_users_table",
            from_version="1.0",
            to_version="2.0"
        )
        
        assert str(error) == "Migration error in 'add_users_table' from 1.0 to 2.0"
        assert error.message == "Migration error in 'add_users_table' from 1.0 to 2.0"
        assert error.error_code == "MIGRATION_ERROR"
        assert error.migration_name == "add_users_table"
        assert error.from_version == "1.0"
        assert error.to_version == "2.0"
    
    def test_migration_error_custom(self):
        """Test MigrationError with custom values."""
        details = {"step": "create_table"}
        error = MigrationError(
            message="Custom migration error",
            error_code="CUSTOM_MIGRATION_ERROR",
            migration_name="add_users_table",
            from_version="1.0",
            to_version="2.0",
            details=details
        )
        
        assert str(error) == "Custom migration error in 'add_users_table' from 1.0 to 2.0"
        assert error.message == "Custom migration error in 'add_users_table' from 1.0 to 2.0"
        assert error.error_code == "CUSTOM_MIGRATION_ERROR"
        assert error.migration_name == "add_users_table"
        assert error.from_version == "1.0"
        assert error.to_version == "2.0"
        assert error.details == details


class TestDeprecatedAPIError:
    """Test DeprecatedAPIError exception."""
    
    def test_deprecated_api_error_default(self):
        """Test DeprecatedAPIError with default values."""
        error = DeprecatedAPIError()
        
        assert str(error) == "API endpoint is deprecated"
        assert error.message == "API endpoint is deprecated"
        assert error.error_code == "DEPRECATED_API_ERROR"
        assert error.status_code == 410
        assert error.endpoint is None
        assert error.alternative_endpoint is None
        assert error.deprecation_date is None
        assert error.removal_date is None
        assert error.details == {}
    
    def test_deprecated_api_error_with_endpoint(self):
        """Test DeprecatedAPIError with endpoint."""
        error = DeprecatedAPIError(endpoint="/api/v1/users")
        
        assert str(error) == "API endpoint '/api/v1/users' is deprecated"
        assert error.message == "API endpoint '/api/v1/users' is deprecated"
        assert error.error_code == "DEPRECATED_API_ERROR"
        assert error.endpoint == "/api/v1/users"
    
    def test_deprecated_api_error_with_alternative(self):
        """Test DeprecatedAPIError with alternative endpoint."""
        error = DeprecatedAPIError(
            endpoint="/api/v1/users",
            alternative_endpoint="/api/v2/users"
        )
        
        assert str(error) == "API endpoint '/api/v1/users' is deprecated, use '/api/v2/users' instead"
        assert error.message == "API endpoint '/api/v1/users' is deprecated, use '/api/v2/users' instead"
        assert error.error_code == "DEPRECATED_API_ERROR"
        assert error.endpoint == "/api/v1/users"
        assert error.alternative_endpoint == "/api/v2/users"
    
    def test_deprecated_api_error_with_dates(self):
        """Test DeprecatedAPIError with deprecation and removal dates."""
        error = DeprecatedAPIError(
            endpoint="/api/v1/users",
            deprecation_date="2023-01-01",
            removal_date="2024-01-01"
        )
        
        assert str(error) == "API endpoint '/api/v1/users' is deprecated (deprecated since 2023-01-01), will be removed on 2024-01-01"
        assert error.message == "API endpoint '/api/v1/users' is deprecated (deprecated since 2023-01-01), will be removed on 2024-01-01"
        assert error.error_code == "DEPRECATED_API_ERROR"
        assert error.endpoint == "/api/v1/users"
        assert error.deprecation_date == "2023-01-01"
        assert error.removal_date == "2024-01-01"
    
    def test_deprecated_api_error_with_all(self):
        """Test DeprecatedAPIError with all parameters."""
        error = DeprecatedAPIError(
            endpoint="/api/v1/users",
            alternative_endpoint="/api/v2/users",
            deprecation_date="2023-01-01",
            removal_date="2024-01-01"
        )
        
        assert str(error) == "API endpoint '/api/v1/users' is deprecated (deprecated since 2023-01-01), use '/api/v2/users' instead, will be removed on 2024-01-01"
        assert error.message == "API endpoint '/api/v1/users' is deprecated (deprecated since 2023-01-01), use '/api/v2/users' instead, will be removed on 2024-01-01"
        assert error.error_code == "DEPRECATED_API_ERROR"
        assert error.endpoint == "/api/v1/users"
        assert error.alternative_endpoint == "/api/v2/users"
        assert error.deprecation_date == "2023-01-01"
        assert error.removal_date == "2024-01-01"
    
    def test_deprecated_api_error_custom(self):
        """Test DeprecatedAPIError with custom values."""
        details = {"replacement_guide": "https://docs.example.com/migration"}
        error = DeprecatedAPIError(
            message="Custom deprecated API error",
            error_code="CUSTOM_DEPRECATED_API_ERROR",
            endpoint="/api/v1/users",
            alternative_endpoint="/api/v2/users",
            deprecation_date="2023-01-01",
            removal_date="2024-01-01",
            details=details
        )
        
        assert str(error) == "Custom deprecated API error (deprecated since 2023-01-01), use '/api/v2/users' instead, will be removed on 2024-01-01"
        assert error.message == "Custom deprecated API error (deprecated since 2023-01-01), use '/api/v2/users' instead, will be removed on 2024-01-01"
        assert error.error_code == "CUSTOM_DEPRECATED_API_ERROR"
        assert error.endpoint == "/api/v1/users"
        assert error.alternative_endpoint == "/api/v2/users"
        assert error.deprecation_date == "2023-01-01"
        assert error.removal_date == "2024-01-01"
        assert error.details == details