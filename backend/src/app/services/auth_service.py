"""
Authentication service for ClassSphere.
"""
import asyncio
import json
from datetime import datetime, timedelta
from typing import Optional
from pathlib import Path

from ..core.security import (
    verify_password,
    get_password_hash,
    create_access_token,
    AuthenticationError,
)
from ..core.config import settings
from ..models.user import UserInDB, UserRole


class AuthService:
    """Authentication service with mock data support."""

    def __init__(self):
        """Initialize authentication service."""
        self.users_data = self._load_mock_users()

    def _load_mock_users(self) -> dict:
        """Load mock users from JSON file."""
        try:
            data_path = Path(__file__).parent.parent / "data" / "mock_users.json"
            with open(data_path, "r") as f:
                return json.load(f)
        except Exception:
            # Fallback data if file not found
            return {
                "users": [
                    {
                        "id": "admin-001",
                        "email": "admin@classsphere.edu",
                        "name": "System Administrator",
                        "role": "admin",
                        "hashed_password": "$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW",
                        "is_active": True,
                        "created_at": "2024-01-01T00:00:00Z",
                        "updated_at": "2024-01-01T00:00:00Z"
                    }
                ]
            }

    async def authenticate_user(
        self,
        email: str,
        password: str
    ) -> Optional[UserInDB]:
        """
        Authenticate user with email and password.

        Args:
            email: User email
            password: User password

        Returns:
            UserInDB object if authentication successful, None otherwise

        Raises:
            AuthenticationError: If authentication fails
        """
        try:
            user = await asyncio.wait_for(
                self._get_user_by_email(email),
                timeout=2.0
            )

            if not user:
                raise AuthenticationError("User not found")

            if not verify_password(password, user.hashed_password):
                raise AuthenticationError("Invalid password")

            if not user.is_active:
                raise AuthenticationError("User account is disabled")

            return user

        except asyncio.TimeoutError:
            raise AuthenticationError("Authentication timeout")

    async def _get_user_by_email(self, email: str) -> Optional[UserInDB]:
        """Get user by email from mock data."""
        for user_data in self.users_data["users"]:
            if user_data["email"] == email:
                return UserInDB(
                    id=user_data["id"],
                    email=user_data["email"],
                    name=user_data["name"],
                    role=UserRole(user_data["role"]),
                    hashed_password=user_data["hashed_password"],
                    is_active=user_data["is_active"],
                    created_at=datetime.fromisoformat(
                        user_data["created_at"].replace("Z", "+00:00")
                    ),
                    updated_at=datetime.fromisoformat(
                        user_data["updated_at"].replace("Z", "+00:00")
                    ),
                )
        return None

    async def get_user_by_id(self, user_id: str) -> Optional[UserInDB]:
        """Get user by ID from mock data."""
        try:
            return await asyncio.wait_for(
                self._get_user_by_id_internal(user_id),
                timeout=2.0
            )
        except asyncio.TimeoutError:
            return None

    async def _get_user_by_id_internal(self, user_id: str) -> Optional[UserInDB]:
        """Internal method to get user by ID."""
        for user_data in self.users_data["users"]:
            if user_data["id"] == user_id:
                return UserInDB(
                    id=user_data["id"],
                    email=user_data["email"],
                    name=user_data["name"],
                    role=UserRole(user_data["role"]),
                    hashed_password=user_data["hashed_password"],
                    is_active=user_data["is_active"],
                    created_at=datetime.fromisoformat(
                        user_data["created_at"].replace("Z", "+00:00")
                    ),
                    updated_at=datetime.fromisoformat(
                        user_data["updated_at"].replace("Z", "+00:00")
                    ),
                )
        return None

    async def create_token(self, user: UserInDB) -> str:
        """
        Create JWT token for authenticated user.

        Args:
            user: Authenticated user

        Returns:
            JWT token string
        """
        token_data = {
            "sub": user.id,
            "email": user.email,
            "role": user.role.value,
        }

        access_token_expires = timedelta(
            minutes=settings.access_token_expire_minutes
        )

        return await create_access_token(
            data=token_data,
            expires_delta=access_token_expires
        )