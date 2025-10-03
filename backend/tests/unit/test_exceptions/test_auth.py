"""
Unit tests for authentication exceptions.
"""
import pytest
from src.app.exceptions.auth import (
    AuthenticationError, TokenExpiredError, TokenInvalidError,
    TokenRevokedError, InsufficientPermissionsError, UserNotFoundError,
    UserInactiveError, UserSuspendedError, PasswordMismatchError,
    PasswordTooWeakError, EmailNotVerifiedError, AccountLockedError,
    SessionExpiredError, SessionInvalidError, RateLimitExceededError
)


class TestAuthenticationError:
    """Test AuthenticationError exception."""
    
    def test_authentication_error_default(self):
        """Test AuthenticationError with default values."""
        error = AuthenticationError()
        
        assert str(error) == "Authentication failed"
        assert error.message == "Authentication failed"
        assert error.error_code == "AUTH_ERROR"
        assert error.details == {}
    
    def test_authentication_error_custom(self):
        """Test AuthenticationError with custom values."""
        details = {"user_id": "user123", "attempt": 3}
        error = AuthenticationError(
            message="Custom auth error",
            error_code="CUSTOM_AUTH_ERROR",
            details=details
        )
        
        assert str(error) == "Custom auth error"
        assert error.message == "Custom auth error"
        assert error.error_code == "CUSTOM_AUTH_ERROR"
        assert error.details == details


class TestTokenExpiredError:
    """Test TokenExpiredError exception."""
    
    def test_token_expired_error_default(self):
        """Test TokenExpiredError with default values."""
        error = TokenExpiredError()
        
        assert str(error) == "Token has expired"
        assert error.message == "Token has expired"
        assert error.error_code == "TOKEN_EXPIRED"
        assert error.details == {}
    
    def test_token_expired_error_custom(self):
        """Test TokenExpiredError with custom values."""
        details = {"expired_at": "2023-01-01T00:00:00Z"}
        error = TokenExpiredError(
            message="Custom token expired",
            error_code="CUSTOM_TOKEN_EXPIRED",
            details=details
        )
        
        assert str(error) == "Custom token expired"
        assert error.message == "Custom token expired"
        assert error.error_code == "CUSTOM_TOKEN_EXPIRED"
        assert error.details == details


class TestTokenInvalidError:
    """Test TokenInvalidError exception."""
    
    def test_token_invalid_error_default(self):
        """Test TokenInvalidError with default values."""
        error = TokenInvalidError()
        
        assert str(error) == "Token is invalid"
        assert error.message == "Token is invalid"
        assert error.error_code == "TOKEN_INVALID"
        assert error.details == {}
    
    def test_token_invalid_error_custom(self):
        """Test TokenInvalidError with custom values."""
        details = {"token_format": "invalid"}
        error = TokenInvalidError(
            message="Custom token invalid",
            error_code="CUSTOM_TOKEN_INVALID",
            details=details
        )
        
        assert str(error) == "Custom token invalid"
        assert error.message == "Custom token invalid"
        assert error.error_code == "CUSTOM_TOKEN_INVALID"
        assert error.details == details


class TestTokenRevokedError:
    """Test TokenRevokedError exception."""
    
    def test_token_revoked_error_default(self):
        """Test TokenRevokedError with default values."""
        error = TokenRevokedError()
        
        assert str(error) == "Token has been revoked"
        assert error.message == "Token has been revoked"
        assert error.error_code == "TOKEN_REVOKED"
        assert error.details == {}
    
    def test_token_revoked_error_custom(self):
        """Test TokenRevokedError with custom values."""
        details = {"revoked_at": "2023-01-01T00:00:00Z"}
        error = TokenRevokedError(
            message="Custom token revoked",
            error_code="CUSTOM_TOKEN_REVOKED",
            details=details
        )
        
        assert str(error) == "Custom token revoked"
        assert error.message == "Custom token revoked"
        assert error.error_code == "CUSTOM_TOKEN_REVOKED"
        assert error.details == details


class TestInsufficientPermissionsError:
    """Test InsufficientPermissionsError exception."""
    
    def test_insufficient_permissions_error_default(self):
        """Test InsufficientPermissionsError with default values."""
        error = InsufficientPermissionsError()
        
        assert str(error) == "Insufficient permissions"
        assert error.message == "Insufficient permissions"
        assert error.error_code == "INSUFFICIENT_PERMISSIONS"
        assert error.details == {}
        assert error.required_permission is None
    
    def test_insufficient_permissions_error_with_permission(self):
        """Test InsufficientPermissionsError with required permission."""
        error = InsufficientPermissionsError(
            required_permission="read:admin_data"
        )
        
        assert str(error) == "Insufficient permissions: read:admin_data"
        assert error.message == "Insufficient permissions: read:admin_data"
        assert error.error_code == "INSUFFICIENT_PERMISSIONS"
        assert error.required_permission == "read:admin_data"
    
    def test_insufficient_permissions_error_custom(self):
        """Test InsufficientPermissionsError with custom values."""
        details = {"user_permissions": ["read:own_data"]}
        error = InsufficientPermissionsError(
            message="Custom insufficient permissions",
            error_code="CUSTOM_INSUFFICIENT_PERMISSIONS",
            required_permission="write:admin_data",
            details=details
        )
        
        assert str(error) == "Custom insufficient permissions: write:admin_data"
        assert error.message == "Custom insufficient permissions: write:admin_data"
        assert error.error_code == "CUSTOM_INSUFFICIENT_PERMISSIONS"
        assert error.required_permission == "write:admin_data"
        assert error.details == details


class TestUserNotFoundError:
    """Test UserNotFoundError exception."""
    
    def test_user_not_found_error_default(self):
        """Test UserNotFoundError with default values."""
        error = UserNotFoundError()
        
        assert str(error) == "User not found"
        assert error.message == "User not found"
        assert error.error_code == "USER_NOT_FOUND"
        assert error.details == {}
        assert error.user_id is None
    
    def test_user_not_found_error_with_user_id(self):
        """Test UserNotFoundError with user ID."""
        error = UserNotFoundError(user_id="user123")
        
        assert str(error) == "User not found: user123"
        assert error.message == "User not found: user123"
        assert error.error_code == "USER_NOT_FOUND"
        assert error.user_id == "user123"
    
    def test_user_not_found_error_custom(self):
        """Test UserNotFoundError with custom values."""
        details = {"search_criteria": "email"}
        error = UserNotFoundError(
            message="Custom user not found",
            error_code="CUSTOM_USER_NOT_FOUND",
            user_id="user123",
            details=details
        )
        
        assert str(error) == "Custom user not found: user123"
        assert error.message == "Custom user not found: user123"
        assert error.error_code == "CUSTOM_USER_NOT_FOUND"
        assert error.user_id == "user123"
        assert error.details == details


class TestUserInactiveError:
    """Test UserInactiveError exception."""
    
    def test_user_inactive_error_default(self):
        """Test UserInactiveError with default values."""
        error = UserInactiveError()
        
        assert str(error) == "User account is inactive"
        assert error.message == "User account is inactive"
        assert error.error_code == "USER_INACTIVE"
        assert error.details == {}
        assert error.user_id is None
    
    def test_user_inactive_error_with_user_id(self):
        """Test UserInactiveError with user ID."""
        error = UserInactiveError(user_id="user123")
        
        assert str(error) == "User account is inactive: user123"
        assert error.message == "User account is inactive: user123"
        assert error.error_code == "USER_INACTIVE"
        assert error.user_id == "user123"
    
    def test_user_inactive_error_custom(self):
        """Test UserInactiveError with custom values."""
        details = {"inactive_since": "2023-01-01T00:00:00Z"}
        error = UserInactiveError(
            message="Custom user inactive",
            error_code="CUSTOM_USER_INACTIVE",
            user_id="user123",
            details=details
        )
        
        assert str(error) == "Custom user inactive: user123"
        assert error.message == "Custom user inactive: user123"
        assert error.error_code == "CUSTOM_USER_INACTIVE"
        assert error.user_id == "user123"
        assert error.details == details


class TestUserSuspendedError:
    """Test UserSuspendedError exception."""
    
    def test_user_suspended_error_default(self):
        """Test UserSuspendedError with default values."""
        error = UserSuspendedError()
        
        assert str(error) == "User account is suspended"
        assert error.message == "User account is suspended"
        assert error.error_code == "USER_SUSPENDED"
        assert error.details == {}
        assert error.user_id is None
    
    def test_user_suspended_error_with_user_id(self):
        """Test UserSuspendedError with user ID."""
        error = UserSuspendedError(user_id="user123")
        
        assert str(error) == "User account is suspended: user123"
        assert error.message == "User account is suspended: user123"
        assert error.error_code == "USER_SUSPENDED"
        assert error.user_id == "user123"
    
    def test_user_suspended_error_custom(self):
        """Test UserSuspendedError with custom values."""
        details = {"suspended_until": "2023-12-31T23:59:59Z"}
        error = UserSuspendedError(
            message="Custom user suspended",
            error_code="CUSTOM_USER_SUSPENDED",
            user_id="user123",
            details=details
        )
        
        assert str(error) == "Custom user suspended: user123"
        assert error.message == "Custom user suspended: user123"
        assert error.error_code == "CUSTOM_USER_SUSPENDED"
        assert error.user_id == "user123"
        assert error.details == details


class TestPasswordMismatchError:
    """Test PasswordMismatchError exception."""
    
    def test_password_mismatch_error_default(self):
        """Test PasswordMismatchError with default values."""
        error = PasswordMismatchError()
        
        assert str(error) == "Password does not match"
        assert error.message == "Password does not match"
        assert error.error_code == "PASSWORD_MISMATCH"
        assert error.details == {}
    
    def test_password_mismatch_error_custom(self):
        """Test PasswordMismatchError with custom values."""
        details = {"attempt": 3}
        error = PasswordMismatchError(
            message="Custom password mismatch",
            error_code="CUSTOM_PASSWORD_MISMATCH",
            details=details
        )
        
        assert str(error) == "Custom password mismatch"
        assert error.message == "Custom password mismatch"
        assert error.error_code == "CUSTOM_PASSWORD_MISMATCH"
        assert error.details == details


class TestPasswordTooWeakError:
    """Test PasswordTooWeakError exception."""
    
    def test_password_too_weak_error_default(self):
        """Test PasswordTooWeakError with default values."""
        error = PasswordTooWeakError()
        
        assert str(error) == "Password is too weak"
        assert error.message == "Password is too weak"
        assert error.error_code == "PASSWORD_TOO_WEAK"
        assert error.details == {}
    
    def test_password_too_weak_error_custom(self):
        """Test PasswordTooWeakError with custom values."""
        details = {"missing_requirements": ["uppercase", "special_char"]}
        error = PasswordTooWeakError(
            message="Custom password too weak",
            error_code="CUSTOM_PASSWORD_TOO_WEAK",
            details=details
        )
        
        assert str(error) == "Custom password too weak"
        assert error.message == "Custom password too weak"
        assert error.error_code == "CUSTOM_PASSWORD_TOO_WEAK"
        assert error.details == details


class TestEmailNotVerifiedError:
    """Test EmailNotVerifiedError exception."""
    
    def test_email_not_verified_error_default(self):
        """Test EmailNotVerifiedError with default values."""
        error = EmailNotVerifiedError()
        
        assert str(error) == "Email address is not verified"
        assert error.message == "Email address is not verified"
        assert error.error_code == "EMAIL_NOT_VERIFIED"
        assert error.details == {}
        assert error.email is None
    
    def test_email_not_verified_error_with_email(self):
        """Test EmailNotVerifiedError with email."""
        error = EmailNotVerifiedError(email="test@example.com")
        
        assert str(error) == "Email address is not verified: test@example.com"
        assert error.message == "Email address is not verified: test@example.com"
        assert error.error_code == "EMAIL_NOT_VERIFIED"
        assert error.email == "test@example.com"
    
    def test_email_not_verified_error_custom(self):
        """Test EmailNotVerifiedError with custom values."""
        details = {"verification_sent_at": "2023-01-01T00:00:00Z"}
        error = EmailNotVerifiedError(
            message="Custom email not verified",
            error_code="CUSTOM_EMAIL_NOT_VERIFIED",
            email="test@example.com",
            details=details
        )
        
        assert str(error) == "Custom email not verified: test@example.com"
        assert error.message == "Custom email not verified: test@example.com"
        assert error.error_code == "CUSTOM_EMAIL_NOT_VERIFIED"
        assert error.email == "test@example.com"
        assert error.details == details


class TestAccountLockedError:
    """Test AccountLockedError exception."""
    
    def test_account_locked_error_default(self):
        """Test AccountLockedError with default values."""
        error = AccountLockedError()
        
        assert str(error) == "Account is locked due to too many failed attempts"
        assert error.message == "Account is locked due to too many failed attempts"
        assert error.error_code == "ACCOUNT_LOCKED"
        assert error.details == {}
        assert error.user_id is None
        assert error.lockout_duration is None
    
    def test_account_locked_error_with_user_id(self):
        """Test AccountLockedError with user ID."""
        error = AccountLockedError(user_id="user123")
        
        assert str(error) == "Account is locked due to too many failed attempts: user123"
        assert error.message == "Account is locked due to too many failed attempts: user123"
        assert error.error_code == "ACCOUNT_LOCKED"
        assert error.user_id == "user123"
    
    def test_account_locked_error_with_duration(self):
        """Test AccountLockedError with lockout duration."""
        error = AccountLockedError(lockout_duration=30)
        
        assert str(error) == "Account is locked due to too many failed attempts (locked for 30 minutes)"
        assert error.message == "Account is locked due to too many failed attempts (locked for 30 minutes)"
        assert error.error_code == "ACCOUNT_LOCKED"
        assert error.lockout_duration == 30
    
    def test_account_locked_error_with_both(self):
        """Test AccountLockedError with user ID and duration."""
        error = AccountLockedError(user_id="user123", lockout_duration=30)
        
        assert str(error) == "Account is locked due to too many failed attempts: user123 (locked for 30 minutes)"
        assert error.message == "Account is locked due to too many failed attempts: user123 (locked for 30 minutes)"
        assert error.error_code == "ACCOUNT_LOCKED"
        assert error.user_id == "user123"
        assert error.lockout_duration == 30


class TestSessionExpiredError:
    """Test SessionExpiredError exception."""
    
    def test_session_expired_error_default(self):
        """Test SessionExpiredError with default values."""
        error = SessionExpiredError()
        
        assert str(error) == "Session has expired"
        assert error.message == "Session has expired"
        assert error.error_code == "SESSION_EXPIRED"
        assert error.details == {}
        assert error.session_id is None
    
    def test_session_expired_error_with_session_id(self):
        """Test SessionExpiredError with session ID."""
        error = SessionExpiredError(session_id="session123")
        
        assert str(error) == "Session has expired: session123"
        assert error.message == "Session has expired: session123"
        assert error.error_code == "SESSION_EXPIRED"
        assert error.session_id == "session123"
    
    def test_session_expired_error_custom(self):
        """Test SessionExpiredError with custom values."""
        details = {"expired_at": "2023-01-01T00:00:00Z"}
        error = SessionExpiredError(
            message="Custom session expired",
            error_code="CUSTOM_SESSION_EXPIRED",
            session_id="session123",
            details=details
        )
        
        assert str(error) == "Custom session expired: session123"
        assert error.message == "Custom session expired: session123"
        assert error.error_code == "CUSTOM_SESSION_EXPIRED"
        assert error.session_id == "session123"
        assert error.details == details


class TestSessionInvalidError:
    """Test SessionInvalidError exception."""
    
    def test_session_invalid_error_default(self):
        """Test SessionInvalidError with default values."""
        error = SessionInvalidError()
        
        assert str(error) == "Session is invalid"
        assert error.message == "Session is invalid"
        assert error.error_code == "SESSION_INVALID"
        assert error.details == {}
        assert error.session_id is None
    
    def test_session_invalid_error_with_session_id(self):
        """Test SessionInvalidError with session ID."""
        error = SessionInvalidError(session_id="session123")
        
        assert str(error) == "Session is invalid: session123"
        assert error.message == "Session is invalid: session123"
        assert error.error_code == "SESSION_INVALID"
        assert error.session_id == "session123"
    
    def test_session_invalid_error_custom(self):
        """Test SessionInvalidError with custom values."""
        details = {"invalid_reason": "tampered"}
        error = SessionInvalidError(
            message="Custom session invalid",
            error_code="CUSTOM_SESSION_INVALID",
            session_id="session123",
            details=details
        )
        
        assert str(error) == "Custom session invalid: session123"
        assert error.message == "Custom session invalid: session123"
        assert error.error_code == "CUSTOM_SESSION_INVALID"
        assert error.session_id == "session123"
        assert error.details == details


class TestRateLimitExceededError:
    """Test RateLimitExceededError exception."""
    
    def test_rate_limit_exceeded_error_default(self):
        """Test RateLimitExceededError with default values."""
        error = RateLimitExceededError()
        
        assert str(error) == "Rate limit exceeded"
        assert error.message == "Rate limit exceeded"
        assert error.error_code == "RATE_LIMIT_EXCEEDED"
        assert error.details == {}
        assert error.retry_after is None
    
    def test_rate_limit_exceeded_error_with_retry_after(self):
        """Test RateLimitExceededError with retry after."""
        error = RateLimitExceededError(retry_after=60)
        
        assert str(error) == "Rate limit exceeded, retry after 60 seconds"
        assert error.message == "Rate limit exceeded, retry after 60 seconds"
        assert error.error_code == "RATE_LIMIT_EXCEEDED"
        assert error.retry_after == 60
    
    def test_rate_limit_exceeded_error_custom(self):
        """Test RateLimitExceededError with custom values."""
        details = {"limit": 100, "window": 3600}
        error = RateLimitExceededError(
            message="Custom rate limit exceeded",
            error_code="CUSTOM_RATE_LIMIT_EXCEEDED",
            retry_after=120,
            details=details
        )
        
        assert str(error) == "Custom rate limit exceeded, retry after 120 seconds"
        assert error.message == "Custom rate limit exceeded, retry after 120 seconds"
        assert error.error_code == "CUSTOM_RATE_LIMIT_EXCEEDED"
        assert error.retry_after == 120
        assert error.details == details