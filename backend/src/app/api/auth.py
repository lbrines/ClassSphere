"""
Authentication API endpoints

CRITICAL OBJECTIVES:
- JWT authentication endpoints
- OAuth 2.0 Google integration
- User management endpoints
- Token refresh and validation

DEPENDENCIES:
- FastAPI
- OAuth service
- Auth service
- JWT middleware
"""

from fastapi import APIRouter, HTTPException, status, Depends, Request
from fastapi.responses import RedirectResponse
from pydantic import BaseModel, EmailStr
from typing import Optional, Dict, Any
import logging

from src.app.services.auth_service import AuthService
from src.app.services.oauth_service import OAuthService
from src.app.middleware.auth_middleware import get_current_user, get_current_user_optional

logger = logging.getLogger(__name__)

# Create router
router = APIRouter(prefix="/auth", tags=["authentication"])

# Initialize services
auth_service = AuthService()
oauth_service = OAuthService()

# Pydantic models
class LoginRequest(BaseModel):
    email: EmailStr
    password: str

class LoginResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str
    expires_in: int
    user: Dict[str, Any]

class RefreshTokenRequest(BaseModel):
    refresh_token: str

class UserResponse(BaseModel):
    id: str
    email: str
    name: Optional[str] = None
    role: str
    picture: Optional[str] = None
    verified: bool = False

# BEGINNING: Critical endpoints for core functionality
@router.post("/login", response_model=LoginResponse)
async def login(login_data: LoginRequest):
    """Login with email and password"""
    try:
        # TODO: Implement user lookup and password verification
        # For now, we'll create a mock user for testing
        if login_data.email == "test@classsphere.com" and login_data.password == "test123":
            user_data = {
                "sub": "test_user_123",
                "email": login_data.email,
                "name": "Test User",
                "role": "teacher"
            }
            
            tokens = auth_service.create_token_pair(user_data)
            
            return LoginResponse(
                access_token=tokens["access_token"],
                refresh_token=tokens["refresh_token"],
                token_type=tokens["token_type"],
                expires_in=tokens["expires_in"],
                user=user_data
            )
        else:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid credentials"
            )
            
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Login error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Login failed"
        )

@router.post("/refresh", response_model=LoginResponse)
async def refresh_token(refresh_data: RefreshTokenRequest):
    """Refresh access token using refresh token"""
    try:
        result = auth_service.refresh_access_token(refresh_data.refresh_token)
        
        if not result:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid refresh token"
            )
        
        # Decode token to get user data
        user_data = auth_service.decode_token(result["access_token"])
        if not user_data:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token data"
            )
        
        return LoginResponse(
            access_token=result["access_token"],
            refresh_token=result["refresh_token"],
            token_type=result["token_type"],
            expires_in=auth_service.access_token_expire_minutes * 60,
            user={
                "sub": user_data.get("sub"),
                "email": user_data.get("email"),
                "name": user_data.get("name"),
                "role": user_data.get("role")
            }
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Token refresh error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Token refresh failed"
        )

@router.get("/google")
async def google_oauth():
    """Initiate Google OAuth flow"""
    try:
        result = oauth_service.get_authorization_url()
        
        return {
            "authorization_url": result["authorization_url"],
            "state": result["state"]
        }
        
    except Exception as e:
        logger.error(f"Google OAuth initiation error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="OAuth initiation failed"
        )

@router.get("/google/callback")
async def google_oauth_callback(code: str, state: str):
    """Handle Google OAuth callback"""
    try:
        result = await oauth_service.handle_oauth_callback(code, state)
        
        if not result:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="OAuth callback failed"
            )
        
        # Redirect to frontend with tokens
        # In a real app, you'd redirect to frontend with tokens in URL params or store in secure cookie
        return {
            "message": "OAuth successful",
            "user": result["user"],
            "tokens": result["tokens"]
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Google OAuth callback error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="OAuth callback failed"
        )

# MIDDLE: Detailed implementation endpoints
@router.get("/me", response_model=UserResponse)
async def get_current_user_info(current_user: Dict[str, Any] = Depends(get_current_user)):
    """Get current user information"""
    try:
        return UserResponse(
            id=current_user["id"],
            email=current_user["email"],
            name=current_user.get("name"),
            role=current_user["role"],
            picture=current_user.get("picture"),
            verified=current_user.get("verified", False)
        )
        
    except Exception as e:
        logger.error(f"Get user info error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to get user info"
        )

@router.post("/logout")
async def logout(current_user: Dict[str, Any] = Depends(get_current_user)):
    """Logout user (invalidate tokens)"""
    try:
        # In a real implementation, you'd add tokens to a blacklist
        # For now, we'll just return success
        logger.info(f"User logged out: {current_user['id']}")
        
        return {"message": "Logged out successfully"}
        
    except Exception as e:
        logger.error(f"Logout error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Logout failed"
        )

# END: Verification and next steps
@router.get("/verify")
async def verify_token(current_user: Optional[Dict[str, Any]] = Depends(get_current_user_optional)):
    """Verify if token is valid"""
    if current_user:
        return {
            "valid": True,
            "user": current_user
        }
    else:
        return {
            "valid": False,
            "user": None
        }