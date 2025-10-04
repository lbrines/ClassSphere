"""
JWT Authentication middleware for ClassSphere

CRITICAL OBJECTIVES:
- Implement JWT token validation middleware
- Handle authentication errors gracefully
- Extract user information from tokens
- Support both access and refresh tokens

DEPENDENCIES:
- FastAPI
- JWT tokens
- HTTPException
"""

from fastapi import HTTPException, status, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi import Query
from typing import Optional, Dict, Any
import logging

from src.app.services.auth_service import AuthService

logger = logging.getLogger(__name__)

# HTTP Bearer token scheme
security = HTTPBearer(auto_error=False)

class AuthMiddleware:
    """JWT Authentication middleware"""
    
    def __init__(self):
        self.auth_service = AuthService()
    
    async def get_current_user(self, credentials: Optional[HTTPAuthorizationCredentials] = Depends(security)) -> Dict[str, Any]:
        """Get current user from JWT token"""
        try:
            if not credentials:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Authentication required",
                    headers={"WWW-Authenticate": "Bearer"},
                )
            
            token = credentials.credentials
            
            # Verify access token
            payload = self.auth_service.verify_token(token, "access")
            if not payload:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Invalid or expired token",
                    headers={"WWW-Authenticate": "Bearer"},
                )
            
            # Extract user information
            user_id = payload.get("sub")
            if not user_id:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Invalid token payload",
                    headers={"WWW-Authenticate": "Bearer"},
                )
            
            user_data = {
                "id": user_id,
                "email": payload.get("email"),
                "role": payload.get("role"),
                "exp": payload.get("exp")
            }
            
            logger.info(f"User authenticated: {user_id}")
            return user_data
            
        except HTTPException:
            raise
        except Exception as e:
            logger.error(f"Authentication error: {e}")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Authentication failed",
                headers={"WWW-Authenticate": "Bearer"},
            )
    
    async def get_current_user_optional(self, credentials: Optional[HTTPAuthorizationCredentials] = Depends(security)) -> Optional[Dict[str, Any]]:
        """Get current user from JWT token (optional)"""
        try:
            if not credentials:
                return None
            
            token = credentials.credentials
            payload = self.auth_service.verify_token(token, "access")
            
            if not payload:
                return None
            
            user_id = payload.get("sub")
            if not user_id:
                return None
            
            return {
                "id": user_id,
                "email": payload.get("email"),
                "role": payload.get("role"),
                "exp": payload.get("exp")
            }
            
        except Exception as e:
            logger.warning(f"Optional authentication error: {e}")
            return None
    
    async def require_role(self, required_role: str, current_user: Dict[str, Any] = Depends(get_current_user)) -> Dict[str, Any]:
        """Require specific role for access"""
        try:
            user_role = current_user.get("role")
            if not user_role:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="User role not found"
                )
            
            # Role hierarchy: admin > coordinator > teacher > student
            role_hierarchy = {
                "admin": 4,
                "coordinator": 3,
                "teacher": 2,
                "student": 1
            }
            
            user_level = role_hierarchy.get(user_role, 0)
            required_level = role_hierarchy.get(required_role, 0)
            
            if user_level < required_level:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail=f"Insufficient permissions. Required: {required_role}, Current: {user_role}"
                )
            
            return current_user
            
        except HTTPException:
            raise
        except Exception as e:
            logger.error(f"Role verification error: {e}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Role verification failed"
            )

# Global middleware instance
auth_middleware = AuthMiddleware()

# Dependency functions
async def get_current_user(credentials: Optional[HTTPAuthorizationCredentials] = Depends(security)) -> Dict[str, Any]:
    """Dependency to get current authenticated user"""
    return await auth_middleware.get_current_user(credentials)

async def get_current_user_optional(credentials: Optional[HTTPAuthorizationCredentials] = Depends(security)) -> Optional[Dict[str, Any]]:
    """Dependency to get current user (optional)"""
    return await auth_middleware.get_current_user_optional(credentials)

async def require_admin(current_user: Dict[str, Any] = Depends(get_current_user)) -> Dict[str, Any]:
    """Require admin role"""
    return await auth_middleware.require_role("admin", current_user)

async def require_coordinator(current_user: Dict[str, Any] = Depends(get_current_user)) -> Dict[str, Any]:
    """Require coordinator role or higher"""
    return await auth_middleware.require_role("coordinator", current_user)

async def require_teacher(current_user: Dict[str, Any] = Depends(get_current_user)) -> Dict[str, Any]:
    """Require teacher role or higher"""
    return await auth_middleware.require_role("teacher", current_user)

async def require_student(current_user: Dict[str, Any] = Depends(get_current_user)) -> Dict[str, Any]:
    """Require student role or higher"""
    return await auth_middleware.require_role("student", current_user)