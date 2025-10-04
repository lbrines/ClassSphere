"""
User repository for MongoDB operations.
"""
from typing import Any, Dict, List, Optional
from datetime import datetime
from motor.motor_asyncio import AsyncIOMotorCollection

from .base import BaseRepository
from src.app.models.user import UserRole, UserStatus
from src.app.exceptions.base import NotFoundError, ConflictError


class UserRepository(BaseRepository):
    """User repository for MongoDB operations."""
    
    def __init__(self):
        super().__init__("users")
    
    async def create_user(self, user_data: Dict[str, Any]) -> str:
        """Create a new user."""
        # Check if email already exists
        if await self.exists({'email': user_data['email']}):
            raise ConflictError(f"User with email {user_data['email']} already exists")
        
        return await self.create(user_data)
    
    async def get_user_by_email(self, email: str) -> Optional[Dict[str, Any]]:
        """Get user by email."""
        return await self.get_by_field('email', email.lower())
    
    async def get_user_by_google_id(self, google_id: str) -> Optional[Dict[str, Any]]:
        """Get user by Google ID."""
        return await self.get_by_field('google_id', google_id)
    
    async def get_users_by_role(self, role: UserRole, skip: int = 0, limit: int = 100) -> List[Dict[str, Any]]:
        """Get users by role."""
        return await self.get_many(
            filter_dict={'role': role.value},
            skip=skip,
            limit=limit,
            sort=[('created_at', -1)]
        )
    
    async def get_users_by_status(self, status: UserStatus, skip: int = 0, limit: int = 100) -> List[Dict[str, Any]]:
        """Get users by status."""
        return await self.get_many(
            filter_dict={'status': status.value},
            skip=skip,
            limit=limit,
            sort=[('created_at', -1)]
        )
    
    async def search_users(self, query: str, skip: int = 0, limit: int = 100) -> List[Dict[str, Any]]:
        """Search users by name or email."""
        filter_dict = {
            '$or': [
                {'name': {'$regex': query, '$options': 'i'}},
                {'email': {'$regex': query, '$options': 'i'}}
            ]
        }
        
        return await self.get_many(
            filter_dict=filter_dict,
            skip=skip,
            limit=limit,
            sort=[('name', 1)]
        )
    
    async def update_user_status(self, user_id: str, status: UserStatus) -> bool:
        """Update user status."""
        return await self.update_by_id(user_id, {'status': status.value})
    
    async def update_user_role(self, user_id: str, role: UserRole) -> bool:
        """Update user role."""
        return await self.update_by_id(user_id, {'role': role.value})
    
    async def update_last_login(self, user_id: str) -> bool:
        """Update user last login timestamp."""
        return await self.update_by_id(user_id, {'last_login': datetime.utcnow()})
    
    async def get_user_stats(self, user_id: str) -> Dict[str, Any]:
        """Get user statistics."""
        pipeline = [
            {'$match': {'_id': self._convert_to_object_id(user_id)}},
            {'$lookup': {
                'from': 'enrollments',
                'localField': '_id',
                'foreignField': 'user_id',
                'as': 'enrollments'
            }},
            {'$lookup': {
                'from': 'submissions',
                'localField': '_id',
                'foreignField': 'student_id',
                'as': 'submissions'
            }},
            {'$project': {
                'user_id': '$_id',
                'total_logins': 1,
                'last_login': 1,
                'courses_enrolled': {'$size': '$enrollments'},
                'assignments_completed': {'$size': '$submissions'},
                'average_grade': {
                    '$avg': '$submissions.grade'
                }
            }}
        ]
        
        results = await self.aggregate(pipeline)
        return results[0] if results else {}
    
    async def get_active_users_count(self) -> int:
        """Get count of active users."""
        return await self.count({'status': UserStatus.ACTIVE.value})
    
    async def get_users_by_department(self, department: str, skip: int = 0, limit: int = 100) -> List[Dict[str, Any]]:
        """Get users by department."""
        return await self.get_many(
            filter_dict={'department': department},
            skip=skip,
            limit=limit,
            sort=[('name', 1)]
        )
    
    async def bulk_update_status(self, user_ids: List[str], status: UserStatus) -> int:
        """Bulk update user status."""
        return await self.bulk_update(
            {'_id': {'$in': [self._convert_to_object_id(uid) for uid in user_ids]}},
            {'status': status.value}
        )
    
    async def create_user_indexes(self) -> None:
        """Create user-specific indexes."""
        indexes = [
            [('email', 1)],  # Unique index for email
            [('google_id', 1)],  # Index for Google ID
            [('role', 1)],  # Index for role
            [('status', 1)],  # Index for status
            [('department', 1)],  # Index for department
            [('created_at', -1)],  # Index for creation date
            [('name', 'text'), ('email', 'text')]  # Text index for search
        ]
        
        await self.create_indexes(indexes)