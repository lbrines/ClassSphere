"""
Endpoints OAuth 2.0
"""
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import JSONResponse

from app.models.auth import GoogleOAuthRequest, AuthResponse
from app.services.google_oauth_service import GoogleOAuthService
from app.services.auth_service import AuthService
from app.middleware.auth import get_auth_service


router = APIRouter(prefix="/api/v1/oauth", tags=["oauth"])


@router.get("/google/url")
async def get_google_auth_url():
    """Obtener URL de autorización de Google con PKCE"""
    try:
        google_service = GoogleOAuthService()
        auth_data = google_service.get_authorization_url()

        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content={
                "authorization_url": auth_data["authorization_url"],
                "code_verifier": auth_data["code_verifier"],
                "state": auth_data["state"]
            }
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to generate authorization URL: {str(e)}"
        )


@router.post("/google/callback", response_model=AuthResponse)
async def google_oauth_callback(
    oauth_request: GoogleOAuthRequest,
    auth_service: AuthService = Depends(get_auth_service)
):
    """Callback para OAuth de Google"""
    try:
        google_service = GoogleOAuthService()

        # Intercambiar código por tokens
        token_data = await google_service.exchange_code_for_tokens(
            oauth_request.authorization_code,
            oauth_request.code_verifier
        )

        # Obtener información del usuario
        google_user_info = await google_service.get_user_info(
            token_data["access_token"]
        )

        # Crear o actualizar usuario en la base de datos
        user = auth_service.create_or_update_google_user(google_user_info)

        # Generar tokens JWT de la aplicación
        app_tokens = auth_service.create_tokens(user)

        return AuthResponse(user=user, token=app_tokens)

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"OAuth callback failed: {str(e)}"
        )


@router.post("/google/refresh")
async def refresh_google_token(refresh_token: str):
    """Renovar token de Google"""
    try:
        google_service = GoogleOAuthService()
        token_data = await google_service.refresh_access_token(refresh_token)

        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content=token_data
        )

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Token refresh failed: {str(e)}"
        )