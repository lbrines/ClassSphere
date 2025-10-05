"""
OAuth endpoints for Google authentication.
"""
import asyncio
from typing import Dict, Any, Optional
from urllib.parse import urlencode

from fastapi import APIRouter, Depends, HTTPException, status, Query
from fastapi.responses import RedirectResponse
from pydantic import BaseModel

from ...core.config import settings
from ...core.exceptions import ExternalServiceError
from ...services.oauth_service import OAuthService
from ...models.user import UserResponse


router = APIRouter(prefix="/auth", tags=["oauth"])


class OAuthInitResponse(BaseModel):
    """OAuth initialization response model."""
    auth_url: str
    state: str


def get_oauth_service() -> OAuthService:
    """Dependency to get OAuth service instance."""
    return OAuthService()


@router.get("/google", response_model=Dict[str, Any])
async def google_oauth_init(
    oauth_service: OAuthService = Depends(get_oauth_service)
) -> Dict[str, Any]:
    """
    Initialize Google OAuth flow.

    Args:
        oauth_service: OAuth service instance

    Returns:
        Google OAuth authorization URL and state

    Raises:
        HTTPException: If OAuth initialization fails
    """
    try:
        # Generate OAuth URL with timeout
        auth_url = await asyncio.wait_for(
            oauth_service.get_google_auth_url(),
            timeout=2.0
        )

        return {
            "success": True,
            "data": {
                "auth_url": auth_url,
                "message": "Redirect to this URL for Google authentication"
            },
            "message": "Google OAuth initialization successful"
        }

    except asyncio.TimeoutError:
        raise HTTPException(
            status_code=status.HTTP_408_REQUEST_TIMEOUT,
            detail="OAuth initialization timeout"
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"OAuth initialization failed: {str(e)}"
        )


@router.get("/google/callback")
async def google_oauth_callback(
    code: Optional[str] = Query(None),
    state: Optional[str] = Query(None),
    error: Optional[str] = Query(None),
    oauth_service: OAuthService = Depends(get_oauth_service)
):
    """
    Handle Google OAuth callback.

    Args:
        code: Authorization code from Google
        state: State parameter for CSRF protection
        error: Error parameter from Google
        oauth_service: OAuth service instance

    Returns:
        Redirect to frontend with token or error

    Raises:
        HTTPException: If OAuth callback fails
    """
    # Handle OAuth errors
    if error:
        error_params = urlencode({"error": error})
        return RedirectResponse(
            url=f"http://localhost:3000/auth/callback?{error_params}",
            status_code=302
        )

    if not code:
        error_params = urlencode({"error": "missing_code"})
        return RedirectResponse(
            url=f"http://localhost:3000/auth/callback?{error_params}",
            status_code=302
        )

    try:
        # Authenticate with Google with timeout
        user, jwt_token = await asyncio.wait_for(
            oauth_service.authenticate_with_google(code, state),
            timeout=10.0
        )

        # Redirect to frontend with token
        success_params = urlencode({
            "token": jwt_token,
            "user_id": user.id,
            "email": user.email,
            "name": user.name,
            "role": user.role.value
        })

        return RedirectResponse(
            url=f"http://localhost:3000/auth/callback?{success_params}",
            status_code=302
        )

    except asyncio.TimeoutError:
        error_params = urlencode({"error": "timeout"})
        return RedirectResponse(
            url=f"http://localhost:3000/auth/callback?{error_params}",
            status_code=302
        )
    except ExternalServiceError as e:
        error_params = urlencode({"error": "google_error", "message": str(e)})
        return RedirectResponse(
            url=f"http://localhost:3000/auth/callback?{error_params}",
            status_code=302
        )
    except Exception as e:
        error_params = urlencode({"error": "internal_error", "message": str(e)})
        return RedirectResponse(
            url=f"http://localhost:3000/auth/callback?{error_params}",
            status_code=302
        )


@router.post("/refresh", response_model=Dict[str, Any])
async def refresh_token() -> Dict[str, Any]:
    """
    Refresh JWT token (placeholder for future implementation).

    Returns:
        Refresh token response
    """
    return {
        "success": False,
        "data": None,
        "message": "Token refresh not implemented yet"
    }