"""
Servicio de autenticación
"""
from typing import Optional
from app.models.user import User, UserInDB, UserRole
from app.core.security import verify_password, get_password_hash


# Mock users para desarrollo
MOCK_USERS = {
    "admin@classsphere.edu": UserInDB(
        id="user-001",
        email="admin@classsphere.edu",
        name="Admin User",
        role=UserRole.ADMIN,
        hashed_password=get_password_hash("secret")
    ),
    "teacher@classsphere.edu": UserInDB(
        id="user-002",
        email="teacher@classsphere.edu",
        name="Teacher User",
        role=UserRole.TEACHER,
        hashed_password=get_password_hash("secret")
    )
}


class AuthService:
    """Servicio de autenticación"""
    
    async def authenticate_user(
        self,
        email: str,
        password: str
    ) -> Optional[User]:
        """Autenticar usuario"""
        user = MOCK_USERS.get(email)
        if not user:
            return None
        
        if not verify_password(password, user.hashed_password):
            return None
        
        return User(**user.model_dump())
    
    async def get_user_by_email(self, email: str) -> Optional[User]:
        """Obtener usuario por email"""
        user = MOCK_USERS.get(email)
        if not user:
            return None
        return User(**user.model_dump())
