"""
Authentication endpoints for ClassSphere API.
"""
import asyncio
from typing import Dict, Any

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel, EmailStr

from ...core.security import verify_token, AuthenticationError
from ...core.exceptions import authentication_exception
from ...services.auth_service import AuthService
from ...models.user import UserResponse


router = APIRouter(prefix="/auth", tags=["authentication"])
security = HTTPBearer()


class LoginRequest(BaseModel):
    """Login request model."""
    email: EmailStr
    password: str


class LoginResponse(BaseModel):
    """Login response model."""
    token: str
    user: UserResponse


def get_auth_service() -> AuthService:
    """Dependency to get auth service instance."""
    return AuthService()


async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    auth_service: AuthService = Depends(get_auth_service)
) -> UserResponse:
    """
    Get current user from JWT token.

    Args:
        credentials: HTTP authorization credentials
        auth_service: Authentication service

    Returns:
        Current user information

    Raises:
        HTTPException: If token is invalid
    """
    try:
        # Verify token with timeout
        payload = await asyncio.wait_for(
            verify_token(credentials.credentials),
            timeout=2.0
        )

        user_id = payload.get("sub")
        if user_id is None:
            raise authentication_exception("Invalid token payload")

        # Get user with timeout
        user = await asyncio.wait_for(
            auth_service.get_user_by_id(user_id),
            timeout=2.0
        )

        if user is None:
            raise authentication_exception("User not found")

        return UserResponse(
            id=user.id,
            email=user.email,
            name=user.name,
            role=user.role,
            is_active=user.is_active,
            created_at=user.created_at,
            updated_at=user.updated_at,
        )

    except asyncio.TimeoutError:
        raise authentication_exception("Authentication timeout")
    except AuthenticationError:
        raise authentication_exception("Invalid token")


@router.post("/login", response_model=Dict[str, Any])
async def login(
    login_request: LoginRequest,
    auth_service: AuthService = Depends(get_auth_service)
) -> Dict[str, Any]:
    """
    Authenticate user with email and password.

    Args:
        login_request: Login credentials
        auth_service: Authentication service

    Returns:
        Login response with token and user information

    Raises:
        HTTPException: If authentication fails
    """
    try:
        # Authenticate user with timeout
        user = await asyncio.wait_for(
            auth_service.authenticate_user(
                login_request.email,
                login_request.password
            ),
            timeout=5.0
        )

        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid credentials"
            )

        # Create token with timeout
        token = await asyncio.wait_for(
            auth_service.create_token(user),
            timeout=2.0
        )

        user_response = UserResponse(
            id=user.id,
            email=user.email,
            name=user.name,
            role=user.role,
            is_active=user.is_active,
            created_at=user.created_at,
            updated_at=user.updated_at,
        )

        return {
            "success": True,
            "data": {
                "token": token,
                "user": user_response.dict()
            },
            "message": "Login successful"
        }

    except asyncio.TimeoutError:
        raise HTTPException(
            status_code=status.HTTP_408_REQUEST_TIMEOUT,
            detail="Authentication timeout"
        )
    except AuthenticationError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(e)
        )


@router.get("/me", response_model=Dict[str, Any])
async def get_current_user_info(
    current_user: UserResponse = Depends(get_current_user)
) -> Dict[str, Any]:
    """
    Get current user information.

    Args:
        current_user: Current authenticated user

    Returns:
        Current user information
    """
    return {
        "success": True,
        "data": current_user.dict(),
        "message": "User information retrieved"
    }


@router.post("/verify", response_model=Dict[str, Any])
async def verify_token_endpoint(
    credentials: HTTPAuthorizationCredentials = Depends(security)
) -> Dict[str, Any]:
    """
    Verify JWT token validity.

    Args:
        credentials: HTTP authorization credentials

    Returns:
        Token verification result

    Raises:
        HTTPException: If token is invalid
    """
    try:
        # Verify token with timeout
        payload = await asyncio.wait_for(
            verify_token(credentials.credentials),
            timeout=2.0
        )

        return {
            "success": True,
            "data": {
                "valid": True,
                "user_id": payload.get("sub"),
                "email": payload.get("email"),
                "role": payload.get("role"),
                "expires": payload.get("exp")
            },
            "message": "Token is valid"
        }

    except asyncio.TimeoutError:
        raise authentication_exception("Token verification timeout")
    except AuthenticationError:
        raise authentication_exception("Invalid token")


@router.post("/logout", response_model=Dict[str, Any])
async def logout() -> Dict[str, Any]:
    """
    Logout endpoint (stateless - client should discard token).

    Returns:
        Logout confirmation
    """
    return {
        "success": True,
        "data": {"logged_out": True},
        "message": "Logout successful"
    }