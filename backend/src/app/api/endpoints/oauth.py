"""
Endpoints de OAuth 2.0 Google
"""
from fastapi import APIRouter, HTTPException, status, Query
from pydantic import BaseModel
from typing import Optional
from app.services.google_service import GoogleOAuthService
from app.services.auth_service import AuthService
from app.core.security import create_access_token, create_refresh_token
from app.models.user import User, UserRole
from app.core.config import settings

router = APIRouter(prefix="/api/v1/oauth", tags=["oauth"])


class OAuthUrlResponse(BaseModel):
    """Respuesta con URL de autorización"""
    authorization_url: str
    state: str


class OAuthCallbackRequest(BaseModel):
    """Request para callback de OAuth"""
    code: str
    state: str
    code_verifier: str


class OAuthTokenResponse(BaseModel):
    """Respuesta de token OAuth"""
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    expires_in: int
    user: User


@router.post("/google/url", response_model=OAuthUrlResponse)
async def get_google_auth_url(
    state: Optional[str] = Query(None, description="Estado opcional para CSRF protection")
):
    """Obtener URL de autorización Google con PKCE"""
    google_service = GoogleOAuthService()
    
    try:
        auth_url, code_verifier = google_service.get_authorization_url(state)
        
        # En un entorno real, deberías almacenar el code_verifier
        # asociado al state en Redis o base de datos
        # Por ahora, lo incluimos en la respuesta para testing
        return OAuthUrlResponse(
            authorization_url=auth_url,
            state=state or "default-state"
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error generating authorization URL: {str(e)}"
        )


@router.post("/google/callback", response_model=OAuthTokenResponse)
async def google_oauth_callback(
    request: OAuthCallbackRequest
):
    """Callback de OAuth Google"""
    google_service = GoogleOAuthService()
    auth_service = AuthService()
    
    try:
        # Intercambiar código por token
        credentials = google_service.exchange_code_for_token(
            request.code,
            request.code_verifier
        )
        
        if not credentials:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Failed to exchange code for token"
            )
        
        # Obtener información del usuario
        user_info = google_service.get_user_info(credentials)
        
        if not user_info:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Failed to get user information"
            )
        
        # Verificar si el usuario existe o crear uno nuevo
        email = user_info['email']
        existing_user = await auth_service.get_user_by_email(email)
        
        if existing_user:
            user = existing_user
        else:
            # Crear nuevo usuario (en un entorno real, esto sería más complejo)
            # Por ahora, asignamos rol de teacher por defecto
            user = User(
                id=f"google-{user_info['id']}",
                email=email,
                name=user_info['name'],
                role=UserRole.TEACHER,
                is_active=True
            )
        
        # Crear tokens JWT
        access_token = create_access_token(data={"sub": user.email})
        refresh_token = create_refresh_token(data={"sub": user.email})
        
        return OAuthTokenResponse(
            access_token=access_token,
            refresh_token=refresh_token,
            expires_in=1800,
            user=user
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"OAuth callback error: {str(e)}"
        )


@router.get("/google/mode")
async def get_google_mode():
    """Obtener modo de Google (real/mock)"""
    return {
        "mode": "real" if settings.google_client_id else "mock",
        "client_id_configured": bool(settings.google_client_id),
        "redirect_uri": settings.google_redirect_uri
    }
