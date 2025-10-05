"""
Servicio OAuth 2.0 para Google con PKCE
"""
import base64
import hashlib
import secrets
import urllib.parse
from typing import Dict, Optional

import httpx
from fastapi import HTTPException, status

from app.core.config import settings
from app.models.auth import GoogleUserInfo


class GoogleOAuthService:
    """Servicio para OAuth 2.0 de Google con PKCE"""

    def __init__(self):
        self.client_id = settings.google_client_id
        self.client_secret = settings.google_client_secret
        self.redirect_uri = settings.google_redirect_uri

        # URLs de Google OAuth
        self.auth_base_url = "https://accounts.google.com/o/oauth2/v2/auth"
        self.token_url = "https://oauth2.googleapis.com/token"
        self.userinfo_url = "https://www.googleapis.com/oauth2/v2/userinfo"

        # Scopes requeridos
        self.scopes = [
            "openid",
            "email",
            "profile",
            "https://www.googleapis.com/auth/classroom.courses.readonly",
            "https://www.googleapis.com/auth/classroom.rosters.readonly"
        ]

    def generate_pkce_challenge(self) -> tuple[str, str]:
        """Generar código verificador y challenge para PKCE"""
        # Código verificador (43-128 caracteres)
        code_verifier = base64.urlsafe_b64encode(secrets.token_bytes(96)).decode('utf-8')
        code_verifier = code_verifier.rstrip('=')[:128]

        # Challenge (SHA256 del código verificador, codificado en base64url)
        code_challenge = hashlib.sha256(code_verifier.encode()).digest()
        code_challenge_b64 = base64.urlsafe_b64encode(code_challenge).decode('utf-8')
        code_challenge_b64 = code_challenge_b64.rstrip('=')

        return code_verifier, code_challenge_b64

    def get_authorization_url(self) -> Dict[str, str]:
        """Obtener URL de autorización de Google con PKCE"""
        code_verifier, code_challenge = self.generate_pkce_challenge()

        params = {
            "client_id": self.client_id,
            "redirect_uri": self.redirect_uri,
            "scope": " ".join(self.scopes),
            "response_type": "code",
            "access_type": "offline",
            "prompt": "consent",
            "code_challenge": code_challenge,
            "code_challenge_method": "S256",
            "state": secrets.token_urlsafe(32)
        }

        auth_url = f"{self.auth_base_url}?{urllib.parse.urlencode(params)}"

        return {
            "authorization_url": auth_url,
            "code_verifier": code_verifier,
            "state": params["state"]
        }

    async def exchange_code_for_tokens(
        self,
        authorization_code: str,
        code_verifier: str
    ) -> Dict[str, str]:
        """Intercambiar código de autorización por tokens de acceso"""
        data = {
            "client_id": self.client_id,
            "client_secret": self.client_secret,
            "code": authorization_code,
            "grant_type": "authorization_code",
            "redirect_uri": self.redirect_uri,
            "code_verifier": code_verifier
        }

        async with httpx.AsyncClient() as client:
            try:
                response = await client.post(
                    self.token_url,
                    data=data,
                    headers={"Content-Type": "application/x-www-form-urlencoded"}
                )
                response.raise_for_status()

                token_data = response.json()

                if "error" in token_data:
                    raise HTTPException(
                        status_code=status.HTTP_400_BAD_REQUEST,
                        detail=f"OAuth error: {token_data.get('error_description', token_data['error'])}"
                    )

                return token_data

            except httpx.HTTPError as e:
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail=f"Failed to exchange code for tokens: {str(e)}"
                )

    async def get_user_info(self, access_token: str) -> GoogleUserInfo:
        """Obtener información del usuario desde Google"""
        headers = {"Authorization": f"Bearer {access_token}"}

        async with httpx.AsyncClient() as client:
            try:
                response = await client.get(
                    self.userinfo_url,
                    headers=headers
                )
                response.raise_for_status()

                user_data = response.json()

                return GoogleUserInfo(
                    google_id=user_data["id"],
                    email=user_data["email"],
                    first_name=user_data.get("given_name", ""),
                    last_name=user_data.get("family_name", ""),
                    avatar_url=user_data.get("picture")
                )

            except httpx.HTTPError as e:
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail=f"Failed to get user info: {str(e)}"
                )

    async def refresh_access_token(self, refresh_token: str) -> Dict[str, str]:
        """Renovar token de acceso usando refresh token"""
        data = {
            "client_id": self.client_id,
            "client_secret": self.client_secret,
            "refresh_token": refresh_token,
            "grant_type": "refresh_token"
        }

        async with httpx.AsyncClient() as client:
            try:
                response = await client.post(
                    self.token_url,
                    data=data,
                    headers={"Content-Type": "application/x-www-form-urlencoded"}
                )
                response.raise_for_status()

                token_data = response.json()

                if "error" in token_data:
                    raise HTTPException(
                        status_code=status.HTTP_400_BAD_REQUEST,
                        detail=f"Token refresh error: {token_data.get('error_description', token_data['error'])}"
                    )

                return token_data

            except httpx.HTTPError as e:
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail=f"Failed to refresh token: {str(e)}"
                )