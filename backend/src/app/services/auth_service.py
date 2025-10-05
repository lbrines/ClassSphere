"""
Servicio de autenticación
"""
from datetime import datetime, timedelta
from typing import Optional, Dict, List
from fastapi import HTTPException, status

from app.models.auth import (
    User, UserCreate, UserLogin, UserRole, Token,
    GoogleUserInfo, AuthResponse
)
from app.utils.auth import (
    verify_password, get_password_hash,
    create_access_token, create_refresh_token, verify_token
)
from app.core.config import settings


class AuthService:
    """Servicio de autenticación con mock de base de datos"""

    def __init__(self):
        # Mock database - En producción usar PostgreSQL
        self._users: Dict[int, Dict] = {}
        self._next_id = 1
        self._initialize_demo_users()

    def _initialize_demo_users(self):
        """Inicializar usuarios demo"""
        demo_users = [
            {
                "email": "admin@classsphere.com",
                "password": "admin123",
                "first_name": "Admin",
                "last_name": "User",
                "role": UserRole.ADMIN
            },
            {
                "email": "coordinator@classsphere.com",
                "password": "coord123",
                "first_name": "Coordinator",
                "last_name": "User",
                "role": UserRole.COORDINATOR
            },
            {
                "email": "teacher@classsphere.com",
                "password": "teacher123",
                "first_name": "Teacher",
                "last_name": "User",
                "role": UserRole.TEACHER
            },
            {
                "email": "student@classsphere.com",
                "password": "student123",
                "first_name": "Student",
                "last_name": "User",
                "role": UserRole.STUDENT
            }
        ]

        for demo_user in demo_users:
            user_data = {
                "id": self._next_id,
                "email": demo_user["email"],
                "password_hash": get_password_hash(demo_user["password"]),
                "first_name": demo_user["first_name"],
                "last_name": demo_user["last_name"],
                "role": demo_user["role"],
                "is_active": True,
                "google_id": None,
                "avatar_url": None,
                "created_at": datetime.utcnow(),
                "last_login": None
            }
            self._users[self._next_id] = user_data
            self._next_id += 1

    def get_user_by_email(self, email: str) -> Optional[User]:
        """Obtener usuario por email"""
        for user_data in self._users.values():
            if user_data["email"] == email:
                return User(**user_data)
        return None

    def get_user_by_id(self, user_id: int) -> Optional[User]:
        """Obtener usuario por ID"""
        user_data = self._users.get(user_id)
        if user_data:
            return User(**user_data)
        return None

    def get_user_by_google_id(self, google_id: str) -> Optional[User]:
        """Obtener usuario por Google ID"""
        for user_data in self._users.values():
            if user_data.get("google_id") == google_id:
                return User(**user_data)
        return None

    def create_user(self, user_create: UserCreate) -> User:
        """Crear nuevo usuario"""
        # Verificar que no existe el email
        if self.get_user_by_email(user_create.email):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered"
            )

        user_data = {
            "id": self._next_id,
            "email": user_create.email,
            "password_hash": get_password_hash(user_create.password),
            "first_name": user_create.first_name,
            "last_name": user_create.last_name,
            "role": user_create.role,
            "is_active": True,
            "google_id": None,
            "avatar_url": None,
            "created_at": datetime.utcnow(),
            "last_login": None
        }

        self._users[self._next_id] = user_data
        self._next_id += 1

        return User(**user_data)

    def authenticate_user(self, email: str, password: str) -> Optional[User]:
        """Autenticar usuario con email y contraseña"""
        user_data = None
        for data in self._users.values():
            if data["email"] == email:
                user_data = data
                break

        if not user_data:
            return None

        if not verify_password(password, user_data["password_hash"]):
            return None

        # Actualizar último login
        user_data["last_login"] = datetime.utcnow()

        return User(**user_data)

    def create_tokens(self, user: User) -> Token:
        """Crear tokens JWT para usuario"""
        token_data = {
            "sub": str(user.id),
            "email": user.email,
            "role": user.role.value
        }

        access_token = create_access_token(token_data)
        refresh_token = create_refresh_token(token_data)

        return Token(
            access_token=access_token,
            refresh_token=refresh_token,
            token_type="bearer",
            expires_in=settings.access_token_expire_minutes * 60
        )

    def login(self, user_login: UserLogin) -> AuthResponse:
        """Login de usuario"""
        user = self.authenticate_user(user_login.email, user_login.password)

        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect email or password"
            )

        if not user.is_active:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Inactive user"
            )

        token = self.create_tokens(user)

        return AuthResponse(user=user, token=token)

    def refresh_token(self, refresh_token: str) -> Token:
        """Renovar token de acceso"""
        token_data = verify_token(refresh_token, token_type="refresh")

        user = self.get_user_by_id(token_data.user_id)
        if not user or not user.is_active:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid refresh token"
            )

        return self.create_tokens(user)

    def create_or_update_google_user(self, google_user: GoogleUserInfo) -> User:
        """Crear o actualizar usuario de Google"""
        # Buscar usuario existente por Google ID
        existing_user = self.get_user_by_google_id(google_user.google_id)

        if existing_user:
            # Actualizar información
            user_data = self._users[existing_user.id]
            user_data["first_name"] = google_user.first_name
            user_data["last_name"] = google_user.last_name
            user_data["avatar_url"] = google_user.avatar_url
            user_data["last_login"] = datetime.utcnow()
            return User(**user_data)

        # Buscar por email
        existing_user = self.get_user_by_email(google_user.email)

        if existing_user:
            # Vincular cuenta de Google
            user_data = self._users[existing_user.id]
            user_data["google_id"] = google_user.google_id
            user_data["avatar_url"] = google_user.avatar_url
            user_data["last_login"] = datetime.utcnow()
            return User(**user_data)

        # Crear nuevo usuario
        user_data = {
            "id": self._next_id,
            "email": google_user.email,
            "password_hash": "",  # No password for Google users
            "first_name": google_user.first_name,
            "last_name": google_user.last_name,
            "role": UserRole.STUDENT,  # Default role
            "is_active": True,
            "google_id": google_user.google_id,
            "avatar_url": google_user.avatar_url,
            "created_at": datetime.utcnow(),
            "last_login": datetime.utcnow()
        }

        self._users[self._next_id] = user_data
        self._next_id += 1

        return User(**user_data)

    def get_all_users(self) -> List[User]:
        """Obtener todos los usuarios (solo para admin)"""
        return [User(**user_data) for user_data in self._users.values()]