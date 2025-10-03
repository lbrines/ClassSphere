"""
Exception modules for the application.
"""
from .base import (
    BaseAPIException,
    ValidationError,
    NotFoundError,
    ConflictError,
    UnauthorizedError,
    ForbiddenError,
    BadRequestError,
    InternalServerError,
    ServiceUnavailableError,
    DatabaseError,
    CacheError,
    ExternalServiceError,
    ConfigurationError,
    MigrationError,
    DeprecatedAPIError
)

from .auth import (
    AuthenticationError,
    TokenExpiredError,
    TokenInvalidError,
    TokenRevokedError,
    InsufficientPermissionsError,
    UserNotFoundError,
    UserInactiveError,
    UserSuspendedError,
    PasswordMismatchError,
    PasswordTooWeakError,
    EmailNotVerifiedError,
    AccountLockedError,
    SessionExpiredError,
    SessionInvalidError,
    RateLimitExceededError
)

from .oauth import (
    OAuthError,
    OAuthProviderError,
    OAuthTokenError,
    OAuthAuthorizationError,
    OAuthScopeError,
    OAuthRedirectError,
    GoogleAPIError,
    GoogleAPIConnectionError,
    GoogleAPIAuthenticationError,
    GoogleAPIAuthorizationError,
    GoogleAPIRateLimitError,
    GoogleAPINotFoundError,
    GoogleAPIBadRequestError,
    GoogleAPIServerError,
    GoogleAPITimeoutError,
    GoogleClassroomError,
    GoogleClassroomCourseError,
    GoogleClassroomStudentError,
    GoogleClassroomAssignmentError
)

__all__ = [
    # Base exceptions
    "BaseAPIException",
    "ValidationError",
    "NotFoundError",
    "ConflictError",
    "UnauthorizedError",
    "ForbiddenError",
    "BadRequestError",
    "InternalServerError",
    "ServiceUnavailableError",
    "DatabaseError",
    "CacheError",
    "ExternalServiceError",
    "ConfigurationError",
    "MigrationError",
    "DeprecatedAPIError",
    
    # Authentication exceptions
    "AuthenticationError",
    "TokenExpiredError",
    "TokenInvalidError",
    "TokenRevokedError",
    "InsufficientPermissionsError",
    "UserNotFoundError",
    "UserInactiveError",
    "UserSuspendedError",
    "PasswordMismatchError",
    "PasswordTooWeakError",
    "EmailNotVerifiedError",
    "AccountLockedError",
    "SessionExpiredError",
    "SessionInvalidError",
    "RateLimitExceededError",
    
    # OAuth exceptions
    "OAuthError",
    "OAuthProviderError",
    "OAuthTokenError",
    "OAuthAuthorizationError",
    "OAuthScopeError",
    "OAuthRedirectError",
    "GoogleAPIError",
    "GoogleAPIConnectionError",
    "GoogleAPIAuthenticationError",
    "GoogleAPIAuthorizationError",
    "GoogleAPIRateLimitError",
    "GoogleAPINotFoundError",
    "GoogleAPIBadRequestError",
    "GoogleAPIServerError",
    "GoogleAPITimeoutError",
    "GoogleClassroomError",
    "GoogleClassroomCourseError",
    "GoogleClassroomStudentError",
    "GoogleClassroomAssignmentError"
]