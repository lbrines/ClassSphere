"""
Dashboard Educativo - Exception Handling
Context-Aware Implementation - Day 3-4 Critical
Implements Template Method Pattern for exceptions
"""

from typing import Optional, Dict, Any
from fastapi import HTTPException, status
from ..core.context_logger import log_context_status


class BaseAPIException(HTTPException):
    """
    Base API Exception with Template Method Pattern
    Implements _build_message() template method
    """
    
    def __init__(
        self,
        status_code: int,
        detail: Optional[str] = None,
        headers: Optional[Dict[str, Any]] = None,
        context_id: Optional[str] = None
    ):
        self.context_id = context_id or f"exception-{self.__class__.__name__}"
        self.detail = self._build_message(detail)
        super().__init__(status_code=status_code, detail=self.detail, headers=headers)
    
    def _build_message(self, detail: Optional[str] = None) -> str:
        """
        Template method for building exception messages
        Override in subclasses for specific message formatting
        """
        if detail:
            return detail
        return f"An error occurred: {self.__class__.__name__}"


class AuthenticationError(BaseAPIException):
    """Authentication error with context tracking"""
    
    def __init__(self, detail: Optional[str] = None, context_id: Optional[str] = None):
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=detail,
            headers={"WWW-Authenticate": "Bearer"},
            context_id=context_id
        )
    
    def _build_message(self, detail: Optional[str] = None) -> str:
        """Build authentication error message"""
        if detail:
            return f"Authentication failed: {detail}"
        return "Authentication required"


class TokenExpiredError(BaseAPIException):
    """Token expired error with context tracking"""
    
    def __init__(self, detail: Optional[str] = None, context_id: Optional[str] = None):
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=detail,
            headers={"WWW-Authenticate": "Bearer"},
            context_id=context_id
        )
    
    def _build_message(self, detail: Optional[str] = None) -> str:
        """Build token expired error message"""
        if detail:
            return f"Token expired: {detail}"
        return "Access token has expired"


class OAuthError(BaseAPIException):
    """OAuth error with context tracking"""
    
    def __init__(self, detail: Optional[str] = None, context_id: Optional[str] = None):
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=detail,
            context_id=context_id
        )
    
    def _build_message(self, detail: Optional[str] = None) -> str:
        """Build OAuth error message"""
        if detail:
            return f"OAuth error: {detail}"
        return "OAuth authentication failed"


class GoogleAPIError(BaseAPIException):
    """Google API error with context tracking"""
    
    def __init__(self, detail: Optional[str] = None, context_id: Optional[str] = None):
        super().__init__(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail=detail,
            context_id=context_id
        )
    
    def _build_message(self, detail: Optional[str] = None) -> str:
        """Build Google API error message"""
        if detail:
            return f"Google API error: {detail}"
        return "Google API service unavailable"


async def log_exception_context(
    exception: BaseAPIException,
    phase: str = "auth",
    task: str = "exception_handling"
) -> None:
    """Log exception context for tracking"""
    await log_context_status(
        context_id=exception.context_id,
        priority="CRITICAL",
        status="failed",
        position="middle",
        message=f"Exception occurred: {exception.detail}",
        phase=phase,
        task=task
    )