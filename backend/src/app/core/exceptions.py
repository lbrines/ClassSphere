"""
Custom exceptions for ClassSphere application.
"""
from fastapi import HTTPException, status


class ClassSphereException(Exception):
    """Base exception for ClassSphere application."""
    pass


class AuthenticationError(ClassSphereException):
    """Exception raised for authentication failures."""
    pass


class AuthorizationError(ClassSphereException):
    """Exception raised for authorization failures."""
    pass


class NotFoundError(ClassSphereException):
    """Exception raised when a resource is not found."""
    pass


class ValidationError(ClassSphereException):
    """Exception raised for validation errors."""
    pass


class ExternalServiceError(ClassSphereException):
    """Exception raised for external service failures."""
    pass


# HTTP Exception factories
def authentication_exception(detail: str = "Could not validate credentials"):
    """Create HTTP 401 Unauthorized exception."""
    return HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail=detail,
        headers={"WWW-Authenticate": "Bearer"},
    )


def authorization_exception(detail: str = "Not enough permissions"):
    """Create HTTP 403 Forbidden exception."""
    return HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail=detail,
    )


def not_found_exception(detail: str = "Resource not found"):
    """Create HTTP 404 Not Found exception."""
    return HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=detail,
    )


def validation_exception(detail: str = "Validation error"):
    """Create HTTP 422 Unprocessable Entity exception."""
    return HTTPException(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        detail=detail,
    )