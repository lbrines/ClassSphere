"""
Authentication and authorization exceptions.
"""
from typing import Optional, Dict, Any


class AuthenticationError(Exception):
    """Base authentication error."""
    
    def __init__(
        self,
        message: str = "Authentication failed",
        error_code: str = "AUTH_ERROR",
        details: Optional[Dict[str, Any]] = None
    ):
        self.message = message
        self.error_code = error_code
        self.details = details or {}
        super().__init__(self.message)


class TokenExpiredError(AuthenticationError):
    """Token expired error."""
    
    def __init__(
        self,
        message: str = "Token has expired",
        error_code: str = "TOKEN_EXPIRED",
        details: Optional[Dict[str, Any]] = None
    ):
        super().__init__(message, error_code, details)


class TokenInvalidError(AuthenticationError):
    """Token invalid error."""
    
    def __init__(
        self,
        message: str = "Token is invalid",
        error_code: str = "TOKEN_INVALID",
        details: Optional[Dict[str, Any]] = None
    ):
        super().__init__(message, error_code, details)


class TokenRevokedError(AuthenticationError):
    """Token revoked error."""
    
    def __init__(
        self,
        message: str = "Token has been revoked",
        error_code: str = "TOKEN_REVOKED",
        details: Optional[Dict[str, Any]] = None
    ):
        super().__init__(message, error_code, details)


class InsufficientPermissionsError(AuthenticationError):
    """Insufficient permissions error."""
    
    def __init__(
        self,
        message: str = "Insufficient permissions",
        error_code: str = "INSUFFICIENT_PERMISSIONS",
        required_permission: Optional[str] = None,
        details: Optional[Dict[str, Any]] = None
    ):
        self.required_permission = required_permission
        if required_permission:
            message = f"{message}: {required_permission}"
        super().__init__(message, error_code, details)


class UserNotFoundError(AuthenticationError):
    """User not found error."""
    
    def __init__(
        self,
        message: str = "User not found",
        error_code: str = "USER_NOT_FOUND",
        user_id: Optional[str] = None,
        details: Optional[Dict[str, Any]] = None
    ):
        self.user_id = user_id
        if user_id:
            message = f"{message}: {user_id}"
        super().__init__(message, error_code, details)


class UserInactiveError(AuthenticationError):
    """User inactive error."""
    
    def __init__(
        self,
        message: str = "User account is inactive",
        error_code: str = "USER_INACTIVE",
        user_id: Optional[str] = None,
        details: Optional[Dict[str, Any]] = None
    ):
        self.user_id = user_id
        if user_id:
            message = f"{message}: {user_id}"
        super().__init__(message, error_code, details)


class UserSuspendedError(AuthenticationError):
    """User suspended error."""
    
    def __init__(
        self,
        message: str = "User account is suspended",
        error_code: str = "USER_SUSPENDED",
        user_id: Optional[str] = None,
        details: Optional[Dict[str, Any]] = None
    ):
        self.user_id = user_id
        if user_id:
            message = f"{message}: {user_id}"
        super().__init__(message, error_code, details)


class PasswordMismatchError(AuthenticationError):
    """Password mismatch error."""
    
    def __init__(
        self,
        message: str = "Password does not match",
        error_code: str = "PASSWORD_MISMATCH",
        details: Optional[Dict[str, Any]] = None
    ):
        super().__init__(message, error_code, details)


class PasswordTooWeakError(AuthenticationError):
    """Password too weak error."""
    
    def __init__(
        self,
        message: str = "Password is too weak",
        error_code: str = "PASSWORD_TOO_WEAK",
        details: Optional[Dict[str, Any]] = None
    ):
        super().__init__(message, error_code, details)


class EmailNotVerifiedError(AuthenticationError):
    """Email not verified error."""
    
    def __init__(
        self,
        message: str = "Email address is not verified",
        error_code: str = "EMAIL_NOT_VERIFIED",
        email: Optional[str] = None,
        details: Optional[Dict[str, Any]] = None
    ):
        self.email = email
        if email:
            message = f"{message}: {email}"
        super().__init__(message, error_code, details)


class AccountLockedError(AuthenticationError):
    """Account locked error."""
    
    def __init__(
        self,
        message: str = "Account is locked due to too many failed attempts",
        error_code: str = "ACCOUNT_LOCKED",
        user_id: Optional[str] = None,
        lockout_duration: Optional[int] = None,
        details: Optional[Dict[str, Any]] = None
    ):
        self.user_id = user_id
        self.lockout_duration = lockout_duration
        if user_id:
            message = f"{message}: {user_id}"
        if lockout_duration:
            message = f"{message} (locked for {lockout_duration} minutes)"
        super().__init__(message, error_code, details)


class SessionExpiredError(AuthenticationError):
    """Session expired error."""
    
    def __init__(
        self,
        message: str = "Session has expired",
        error_code: str = "SESSION_EXPIRED",
        session_id: Optional[str] = None,
        details: Optional[Dict[str, Any]] = None
    ):
        self.session_id = session_id
        if session_id:
            message = f"{message}: {session_id}"
        super().__init__(message, error_code, details)


class SessionInvalidError(AuthenticationError):
    """Session invalid error."""
    
    def __init__(
        self,
        message: str = "Session is invalid",
        error_code: str = "SESSION_INVALID",
        session_id: Optional[str] = None,
        details: Optional[Dict[str, Any]] = None
    ):
        self.session_id = session_id
        if session_id:
            message = f"{message}: {session_id}"
        super().__init__(message, error_code, details)


class RateLimitExceededError(AuthenticationError):
    """Rate limit exceeded error."""
    
    def __init__(
        self,
        message: str = "Rate limit exceeded",
        error_code: str = "RATE_LIMIT_EXCEEDED",
        retry_after: Optional[int] = None,
        details: Optional[Dict[str, Any]] = None
    ):
        self.retry_after = retry_after
        if retry_after:
            message = f"{message}, retry after {retry_after} seconds"
        super().__init__(message, error_code, details)