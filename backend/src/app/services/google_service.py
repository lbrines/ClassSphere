"""
Servicio de Google OAuth con PKCE
"""
import secrets
import hashlib
import base64
from typing import Optional, Dict, Any
from urllib.parse import urlencode
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import Flow
from app.core.config import settings


class GoogleOAuthService:
    """Servicio de OAuth 2.0 Google con PKCE"""
    
    def __init__(self):
        self.client_config = {
            "web": {
                "client_id": settings.google_client_id,
                "client_secret": settings.google_client_secret,
                "auth_uri": "https://accounts.google.com/o/oauth2/auth",
                "token_uri": "https://oauth2.googleapis.com/token",
                "redirect_uris": [settings.google_redirect_uri]
            }
        }
    
    def generate_pkce_challenge(self) -> tuple[str, str]:
        """Generar code_verifier y code_challenge para PKCE"""
        # Generar code_verifier (43-128 caracteres)
        code_verifier = base64.urlsafe_b64encode(
            secrets.token_bytes(32)
        ).decode('utf-8').rstrip('=')
        
        # Generar code_challenge (SHA256 hash del code_verifier)
        code_challenge = base64.urlsafe_b64encode(
            hashlib.sha256(code_verifier.encode('utf-8')).digest()
        ).decode('utf-8').rstrip('=')
        
        return code_verifier, code_challenge
    
    def get_authorization_url(self, state: Optional[str] = None) -> tuple[str, str]:
        """Obtener URL de autorización con PKCE"""
        code_verifier, code_challenge = self.generate_pkce_challenge()
        
        # Crear flow
        flow = Flow.from_client_config(
            self.client_config,
            scopes=[
                'https://www.googleapis.com/auth/userinfo.email',
                'https://www.googleapis.com/auth/userinfo.profile',
                'https://www.googleapis.com/auth/classroom.courses.readonly'
            ]
        )
        flow.redirect_uri = settings.google_redirect_uri
        
        # Generar URL de autorización
        auth_url, _ = flow.authorization_url(
            access_type='offline',
            include_granted_scopes='true',
            state=state or secrets.token_urlsafe(32),
            code_challenge=code_challenge,
            code_challenge_method='S256'
        )
        
        return auth_url, code_verifier
    
    def exchange_code_for_token(
        self, 
        authorization_code: str, 
        code_verifier: str
    ) -> Optional[Credentials]:
        """Intercambiar código de autorización por token"""
        try:
            flow = Flow.from_client_config(
                self.client_config,
                scopes=[
                    'https://www.googleapis.com/auth/userinfo.email',
                    'https://www.googleapis.com/auth/userinfo.profile',
                    'https://www.googleapis.com/auth/classroom.courses.readonly'
                ]
            )
            flow.redirect_uri = settings.google_redirect_uri
            
            # Intercambiar código por token
            flow.fetch_token(
                code=authorization_code,
                code_verifier=code_verifier
            )
            
            return flow.credentials
            
        except Exception as e:
            print(f"Error exchanging code for token: {e}")
            return None
    
    def get_user_info(self, credentials: Credentials) -> Optional[Dict[str, Any]]:
        """Obtener información del usuario desde Google"""
        try:
            from googleapiclient.discovery import build
            
            service = build('oauth2', 'v2', credentials=credentials)
            user_info = service.userinfo().get().execute()
            
            return {
                'id': user_info.get('id'),
                'email': user_info.get('email'),
                'name': user_info.get('name'),
                'picture': user_info.get('picture'),
                'verified_email': user_info.get('verified_email', False)
            }
            
        except Exception as e:
            print(f"Error getting user info: {e}")
            return None
    
    def refresh_token(self, credentials: Credentials) -> Optional[Credentials]:
        """Refrescar token si es necesario"""
        try:
            if credentials.expired and credentials.refresh_token:
                credentials.refresh(Request())
                return credentials
            return credentials
        except Exception as e:
            print(f"Error refreshing token: {e}")
            return None
