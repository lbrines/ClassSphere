"""
Dashboard Educativo - Authentication API
Context-Aware Implementation - Phase 1 Critical
Implements JWT service with context tracking
"""

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPBearer
from datetime import datetime, timedelta
from typing import Dict, Any, Optional
from jose import JWTError, jwt
from passlib.context import CryptContext

from ...core.config import get_settings
from ...core.context_logger import context_logger
from ...core.exceptions import AuthenticationError, TokenExpiredError, OAuthError, GoogleAPIError, log_exception_context
from ...services.oauth_service import oauth_service

router = APIRouter()
security = HTTPBearer()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class AuthService:
    """JWT Authentication Service with context tracking"""
    
    def __init__(self):
        self.settings = get_settings()
    
    def create_access_token(self, data: dict, expires_delta: Optional[timedelta] = None) -> str:
        """Create JWT access token with 'sub' field standard"""
        to_encode = data.copy()
        
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(minutes=self.settings.access_token_expire_minutes)
        
        to_encode.update({
            "exp": expire,
            "sub": data.get("sub", data.get("user_id")),  # Standard 'sub' field
            "iat": datetime.utcnow()
        })
        
        encoded_jwt = jwt.encode(to_encode, self.settings.secret_key, algorithm=self.settings.algorithm)
        return encoded_jwt
    
    def create_refresh_token(self, data: dict) -> str:
        """Create refresh token with rotation"""
        to_encode = data.copy()
        expire = datetime.utcnow() + timedelta(days=self.settings.refresh_token_expire_days)
        
        to_encode.update({
            "exp": expire,
            "type": "refresh",
            "iat": datetime.utcnow()
        })
        
        encoded_jwt = jwt.encode(to_encode, self.settings.secret_key, algorithm=self.settings.algorithm)
        return encoded_jwt
    
    def verify_token(self, token: str) -> Dict[str, Any]:
        """Verify JWT token"""
        try:
            payload = jwt.decode(token, self.settings.secret_key, algorithms=[self.settings.algorithm])
            return payload
        except JWTError:
            raise TokenExpiredError("Could not validate credentials")
    
    def hash_password(self, password: str) -> str:
        """Hash password using bcrypt"""
        return pwd_context.hash(password)
    
    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        """Verify password against hash"""
        return pwd_context.verify(plain_password, hashed_password)


# Global auth service instance
auth_service = AuthService()


@router.post("/auth/login")
async def login(credentials: Dict[str, str]) -> Dict[str, Any]:
    """Login endpoint with context tracking"""
    
    # Log login attempt
    await context_logger.log_context_status(
        context_id="auth-login-001",
        priority="CRITICAL",
        status="started",
        position="beginning",
        message="Login attempt initiated",
        phase="auth",
        task="login"
    )
    
    try:
        # Mock user validation (replace with actual database lookup)
        username = credentials.get("username")
        password = credentials.get("password")
        
        if not username or not password:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Username and password required"
            )
        
        # Mock user data (replace with actual user lookup)
        user_data = {
            "user_id": "user_123",
            "username": username,
            "email": f"{username}@example.com",
            "role": "teacher"
        }
        
        # Create tokens
        access_token = auth_service.create_access_token(data=user_data)
        refresh_token = auth_service.create_refresh_token(data=user_data)
        
        # Log successful login
        await context_logger.log_context_status(
            context_id="auth-login-001",
            priority="CRITICAL",
            status="completed",
            position="beginning",
            message="Login successful",
            phase="auth",
            task="login"
        )
        
        return {
            "access_token": access_token,
            "refresh_token": refresh_token,
            "token_type": "bearer",
            "expires_in": get_settings().access_token_expire_minutes * 60,
            "user": user_data
        }
        
    except Exception as e:
        # Log failed login
        await context_logger.log_context_status(
            context_id="auth-login-001",
            priority="CRITICAL",
            status="failed",
            position="beginning",
            message=f"Login failed: {str(e)}",
            phase="auth",
            task="login"
        )
        raise


@router.post("/auth/refresh")
async def refresh_token(refresh_data: Dict[str, str]) -> Dict[str, Any]:
    """Refresh token endpoint with rotation"""
    
    # Log refresh attempt
    await context_logger.log_context_status(
        context_id="auth-refresh-002",
        priority="HIGH",
        status="started",
        position="middle",
        message="Token refresh initiated",
        phase="auth",
        task="refresh_token"
    )
    
    try:
        refresh_token = refresh_data.get("refresh_token")
        
        if not refresh_token:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Refresh token required"
            )
        
        # Verify refresh token
        payload = auth_service.verify_token(refresh_token)
        
        if payload.get("type") != "refresh":
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid refresh token"
            )
        
        # Create new access token
        user_data = {
            "user_id": payload.get("sub"),
            "username": payload.get("username"),
            "email": payload.get("email"),
            "role": payload.get("role")
        }
        
        new_access_token = auth_service.create_access_token(data=user_data)
        
        # Log successful refresh
        await context_logger.log_context_status(
            context_id="auth-refresh-002",
            priority="HIGH",
            status="completed",
            position="middle",
            message="Token refresh successful",
            phase="auth",
            task="refresh_token"
        )
        
        return {
            "access_token": new_access_token,
            "token_type": "bearer",
            "expires_in": get_settings().access_token_expire_minutes * 60
        }
        
    except Exception as e:
        # Log failed refresh
        await context_logger.log_context_status(
            context_id="auth-refresh-002",
            priority="HIGH",
            status="failed",
            position="middle",
            message=f"Token refresh failed: {str(e)}",
            phase="auth",
            task="refresh_token"
        )
        raise


@router.get("/auth/me")
async def get_current_user(token: str = Depends(security)) -> Dict[str, Any]:
    """Get current user information"""
    
    # Log user info request
    await context_logger.log_context_status(
        context_id="auth-me-003",
        priority="MEDIUM",
        status="started",
        position="middle",
        message="User info request initiated",
        phase="auth",
        task="get_current_user"
    )
    
    try:
        # Verify token
        payload = auth_service.verify_token(token.credentials)
        
        user_data = {
            "user_id": payload.get("sub"),
            "username": payload.get("username"),
            "email": payload.get("email"),
            "role": payload.get("role")
        }
        
        # Log successful user info retrieval
        await context_logger.log_context_status(
            context_id="auth-me-003",
            priority="MEDIUM",
            status="completed",
            position="middle",
            message="User info retrieved successfully",
            phase="auth",
            task="get_current_user"
        )
        
        return user_data
        
    except Exception as e:
        # Log failed user info retrieval
        await context_logger.log_context_status(
            context_id="auth-me-003",
            priority="MEDIUM",
            status="failed",
            position="middle",
            message=f"User info retrieval failed: {str(e)}",
            phase="auth",
            task="get_current_user"
        )
        raise


@router.get("/auth/google/authorize")
async def google_authorize() -> Dict[str, Any]:
    """Get Google OAuth authorization URL"""
    
    try:
        auth_data = await oauth_service.get_authorization_url()
        
        return {
            "authorization_url": auth_data["authorization_url"],
            "state": auth_data["state"],
            "scopes": auth_data["scopes"]
        }
        
    except OAuthError as e:
        await log_exception_context(e, "oauth", "google_authorize")
        raise


@router.post("/auth/google/callback")
async def google_callback(callback_data: Dict[str, str]) -> Dict[str, Any]:
    """Handle Google OAuth callback"""
    
    # Log OAuth callback
    await context_logger.log_context_status(
        context_id="oauth-callback-005",
        priority="CRITICAL",
        status="started",
        position="beginning",
        message="Processing Google OAuth callback",
        phase="oauth",
        task="google_callback"
    )
    
    try:
        code = callback_data.get("code")
        state = callback_data.get("state")
        code_verifier = callback_data.get("code_verifier")
        
        if not all([code, state, code_verifier]):
            raise OAuthError("Missing required OAuth parameters")
        
        # Exchange code for token
        token_data = await oauth_service.exchange_code_for_token(
            code=code,
            state=state,
            code_verifier=code_verifier
        )
        
        # Get user info
        user_info = await oauth_service.get_user_info(token_data["access_token"])
        
        # Create JWT tokens for our system
        user_data = {
            "user_id": user_info.get("id"),
            "username": user_info.get("email"),
            "email": user_info.get("email"),
            "name": user_info.get("name"),
            "picture": user_info.get("picture"),
            "role": "teacher"  # Default role
        }
        
        access_token = auth_service.create_access_token(data=user_data)
        refresh_token = auth_service.create_refresh_token(data=user_data)
        
        # Log successful OAuth callback
        await context_logger.log_context_status(
            context_id="oauth-callback-005",
            priority="CRITICAL",
            status="completed",
            position="beginning",
            message="Google OAuth callback processed successfully",
            phase="oauth",
            task="google_callback"
        )
        
        return {
            "access_token": access_token,
            "refresh_token": refresh_token,
            "token_type": "bearer",
            "expires_in": get_settings().access_token_expire_minutes * 60,
            "user": user_data,
            "google_tokens": {
                "access_token": token_data.get("access_token"),
                "refresh_token": token_data.get("refresh_token"),
                "expires_in": token_data.get("expires_in")
            }
        }
        
    except Exception as e:
        # Log OAuth callback error
        await context_logger.log_context_status(
            context_id="oauth-callback-005",
            priority="CRITICAL",
            status="failed",
            position="beginning",
            message=f"Google OAuth callback failed: {str(e)}",
            phase="oauth",
            task="google_callback"
        )
        
        if isinstance(e, (OAuthError, GoogleAPIError)):
            await log_exception_context(e, "oauth", "google_callback")
            raise
        else:
            raise OAuthError(f"OAuth callback failed: {str(e)}")


@router.post("/auth/google/refresh")
async def google_refresh(refresh_data: Dict[str, str]) -> Dict[str, Any]:
    """Refresh Google access token"""
    
    try:
        google_refresh_token = refresh_data.get("google_refresh_token")
        
        if not google_refresh_token:
            raise OAuthError("Google refresh token required")
        
        # Refresh Google token
        token_data = await oauth_service.refresh_access_token(google_refresh_token)
        
        return {
            "google_tokens": {
                "access_token": token_data.get("access_token"),
                "expires_in": token_data.get("expires_in")
            }
        }
        
    except OAuthError as e:
        await log_exception_context(e, "oauth", "google_refresh")
        raise