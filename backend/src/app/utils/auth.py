"""
Utilidades de autenticación JWT y OAuth
"""
import hashlib
import secrets
from datetime import datetime, timedelta
from typing import Optional, Dict, Any

from jose import JWTError, jwt
import hashlib
from fastapi import HTTPException, status

from app.core.config import settings
from app.models.auth import UserRole, TokenData


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verificar contraseña usando SHA256 simple (temporal)"""
    return get_password_hash(plain_password) == hashed_password


def get_password_hash(password: str) -> str:
    """Hash de contraseña usando SHA256 simple (temporal)"""
    return hashlib.sha256((password + settings.secret_key).encode()).hexdigest()


def create_access_token(data: Dict[str, Any], expires_delta: Optional[timedelta] = None) -> str:
    """Crear token de acceso JWT"""
    to_encode = data.copy()

    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=settings.access_token_expire_minutes)

    to_encode.update({"exp": expire, "type": "access"})
    encoded_jwt = jwt.encode(to_encode, settings.secret_key, algorithm=settings.algorithm)
    return encoded_jwt


def create_refresh_token(data: Dict[str, Any]) -> str:
    """Crear token de refresh"""
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(days=settings.refresh_token_expire_days)

    to_encode.update({"exp": expire, "type": "refresh"})
    encoded_jwt = jwt.encode(to_encode, settings.secret_key, algorithm=settings.algorithm)
    return encoded_jwt


def verify_token(token: str, token_type: str = "access") -> TokenData:
    """Verificar y decodificar token JWT"""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(token, settings.secret_key, algorithms=[settings.algorithm])

        # Verificar tipo de token
        if payload.get("type") != token_type:
            raise credentials_exception

        user_id: int = payload.get("sub")
        email: str = payload.get("email")
        role: str = payload.get("role")

        if user_id is None or email is None:
            raise credentials_exception

        token_data = TokenData(
            user_id=user_id,
            email=email,
            role=UserRole(role) if role else None
        )
        return token_data

    except (JWTError, ValueError):
        raise credentials_exception


def generate_pkce_challenge() -> tuple[str, str]:
    """Generar código y challenge para PKCE"""
    # Código verificador (43-128 caracteres)
    code_verifier = secrets.token_urlsafe(96)[:128]

    # Challenge (SHA256 del código verificador, codificado en base64url)
    code_challenge = hashlib.sha256(code_verifier.encode()).digest()
    code_challenge_b64 = secrets.token_urlsafe(len(code_challenge))

    return code_verifier, code_challenge_b64


def verify_pkce_challenge(code_verifier: str, code_challenge: str) -> bool:
    """Verificar código PKCE"""
    computed_challenge = hashlib.sha256(code_verifier.encode()).digest()
    computed_challenge_b64 = secrets.token_urlsafe(len(computed_challenge))

    return computed_challenge_b64 == code_challenge


def check_role_permission(user_role: UserRole, required_role: UserRole) -> bool:
    """Verificar permisos de rol jerárquico"""
    role_hierarchy = {
        UserRole.STUDENT: 1,
        UserRole.TEACHER: 2,
        UserRole.COORDINATOR: 3,
        UserRole.ADMIN: 4
    }

    return role_hierarchy.get(user_role, 0) >= role_hierarchy.get(required_role, 0)