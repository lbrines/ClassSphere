---
title: "ClassSphere - Fase 1: Fundaciones"
version: "1.0"
type: "phase_plan"
context_priority: "CRITICAL"
max_tokens: 2000
phase: "1"
duration: "12 días"
tdd_compliance: "100%"
date: "2025-10-05"
---

[← Plan Principal](01_plan_index.md) | [Siguiente → Fase 2](03_plan_fase2_google_integration.md)

# Fase 1: Fundaciones (CRITICAL Priority)

## 🎯 INICIO: Objetivos Críticos

### Objetivo de la Fase
Establecer la base completa del sistema con backend FastAPI, frontend Next.js 15, autenticación JWT + OAuth 2.0, y testing con cobertura ≥80%.

### Dependencias Bloqueantes
- Python 3.11.4 instalado
- Node.js 18+ instalado
- Git configurado
- Repositorio inicializado

### Mapeo Frontend-Backend Obligatorio
**Implementación Requerida:**
- **useAuth.login()** → `POST /api/v1/auth/login` → `LoginForm` component
- **useAuth.checkAuth()** → `GET /api/v1/auth/me` → `AuthGuard` component
- **useAuth.getGoogleAuthUrl()** → `POST /api/v1/oauth/google` → `OAuthButton` component
- **useAuth.logout()** → `POST /api/v1/auth/logout` → Navigation components
- **Error Handling**: 401 → redirect /login, 403 → access denied, 500 → error boundary

### Duración Total
**12 días** (divididos en 12 tareas diarias específicas)

### Context Management
- **Priority**: CRITICAL
- **Max Tokens**: 2000 por chunk
- **Chunk Position**: Beginning (primacy bias)
- **Lost-in-Middle Risk**: Low

---

## 📅 MEDIO: Implementación Día por Día

### Día 1: Configuración del Entorno Backend

**Objetivo:** Configurar Python 3.11.4, FastAPI 0.104.1, y estructura de directorios.

**Comandos LLM a ejecutar:**
```bash
# 1. Verificar Python
python3 --version
# Debe mostrar: Python 3.11.4
# Si no: pyenv install 3.11.4 && pyenv local 3.11.4

# 2. Crear estructura backend
mkdir -p backend/src/app/{api/endpoints,services,models,core,middleware,utils,data}
mkdir -p backend/tests/{unit,integration,e2e}
mkdir -p backend/src/app/api/endpoints
mkdir -p backend/src/app/services
mkdir -p backend/src/app/models
mkdir -p backend/src/app/core
mkdir -p backend/src/app/middleware
mkdir -p backend/src/app/utils
mkdir -p backend/src/app/data

# 3. Crear entorno virtual
cd backend
python3 -m venv venv
source venv/bin/activate

# 4. Crear requirements.txt
cat > requirements.txt << 'EOF'
fastapi==0.104.1
uvicorn[standard]==0.24.0
pydantic==2.5.0
pydantic-settings==2.1.0
python-jose[cryptography]==3.3.0
passlib[bcrypt]==1.7.4
python-multipart==0.0.6
redis==5.0.1
httpx==0.25.2
pytest==7.4.3
pytest-asyncio==0.21.1
pytest-cov==4.1.0
pytest-mock==3.12.0
python-dotenv==1.0.0
EOF

# 5. Instalar dependencias
pip install -r requirements.txt

# 6. Crear .env.example
cat > .env.example << 'EOF'
# Application
APP_NAME=ClassSphere
APP_VERSION=1.0.0
DEBUG=True

# Server
HOST=127.0.0.1
PORT=8000

# Security
SECRET_KEY=your-secret-key-here-change-in-production
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
REFRESH_TOKEN_EXPIRE_DAYS=7

# Google OAuth
GOOGLE_CLIENT_ID=your-google-client-id
GOOGLE_CLIENT_SECRET=your-google-client-secret
GOOGLE_REDIRECT_URI=http://localhost:3000/auth/callback

# Redis (optional)
REDIS_HOST=localhost
REDIS_PORT=6379
REDIS_DB=0
EOF

# 7. Copiar a .env
cp .env.example .env
```

**Archivos a crear:**

**backend/src/app/core/config.py**
```python
"""
Configuración de la aplicación con Pydantic v2
Prevención Pattern 1: ConfigDict import obligatorio
"""
from pydantic import ConfigDict
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Configuración de la aplicación"""
    
    # Application
    app_name: str = "ClassSphere"
    app_version: str = "1.0.0"
    debug: bool = True
    
    # Server
    host: str = "127.0.0.1"
    port: int = 8000
    
    # Security
    secret_key: str
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    refresh_token_expire_days: int = 7
    
    # Google OAuth
    google_client_id: str = ""
    google_client_secret: str = ""
    google_redirect_uri: str = "http://localhost:3000/auth/callback"
    
    # Redis
    redis_host: str = "localhost"
    redis_port: int = 6379
    redis_db: int = 0
    
    model_config = ConfigDict(
        env_file=".env",
        case_sensitive=False,
        extra="ignore"
    )


settings = Settings()
```

**backend/src/app/main.py**
```python
"""
Aplicación principal FastAPI con lifespan resiliente
"""
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifespan resiliente - servicios externos opcionales"""
    # Startup
    print("🚀 Starting ClassSphere...")
    
    try:
        # Redis (opcional)
        print("📦 Checking Redis...")
        # await init_redis()
        print("✅ Redis available")
    except Exception as e:
        print(f"⚠️  Redis not available: {e}")
    
    yield
    
    # Shutdown
    print("🛑 Shutting down ClassSphere...")
    try:
        # await cleanup_services()
        print("✅ Cleanup completed")
    except Exception as e:
        print(f"⚠️  Cleanup error: {e}")


def create_app() -> FastAPI:
    """Factory para crear la aplicación"""
    app = FastAPI(
        title=settings.app_name,
        version=settings.app_version,
        lifespan=lifespan
    )
    
    # CORS
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["http://localhost:3000"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    
    # Health check básico
    @app.get("/health")
    async def health_check():
        return {
            "status": "healthy",
            "service": settings.app_name,
            "version": settings.app_version
        }
    
    return app


app = create_app()


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host=settings.host,
        port=settings.port,
        reload=settings.debug
    )
```

**Verificación Día 1:**
```bash
# Test de inicio del servidor
cd backend
source venv/bin/activate
python -m uvicorn app.main:app --host 127.0.0.1 --port 8000 &
sleep 3

# Verificar health check
curl http://localhost:8000/health
# Debe retornar: {"status":"healthy","service":"ClassSphere","version":"1.0.0"}

# Detener servidor
pkill -f uvicorn
```

**Criterios de Aceptación Día 1:**
- [ ] Python 3.11.4 verificado
- [ ] Estructura de directorios creada
- [ ] FastAPI 0.104.1 instalado
- [ ] Servidor inicia en puerto 8000
- [ ] Health check responde correctamente
- [ ] CORS configurado

**Validaciones de Prevención de Errores:**
- [ ] Pattern 1: ConfigDict importado correctamente en config.py
- [ ] Verificación: `python -c "from app.core.config import Settings; print('✅ ConfigDict OK')"`

---

### Día 2: Configuración de Testing Backend

**Objetivo:** Configurar pytest, AsyncMock, timeouts, y cobertura.

**Comandos LLM a ejecutar:**
```bash
# 1. Crear pytest.ini
cd backend
cat > pytest.ini << 'EOF'
[pytest]
testpaths = tests
python_files = test_*.py
python_classes = Test*
python_functions = test_*
asyncio_mode = auto
markers =
    unit: Unit tests
    integration: Integration tests
    e2e: End-to-end tests
addopts =
    -v
    --strict-markers
    --cov=src
    --cov-report=term-missing
    --cov-report=html
    --cov-fail-under=80
timeout = 30
EOF

# 2. Crear conftest.py
cat > tests/conftest.py << 'EOF'
"""
Fixtures globales para testing
"""
import pytest
from fastapi.testclient import TestClient
from app.main import create_app


@pytest.fixture
def client():
    """TestClient para FastAPI"""
    app = create_app()
    return TestClient(app)


@pytest.fixture
def mock_settings():
    """Settings mockeados para testing"""
    from app.core.config import Settings
    return Settings(
        secret_key="test-secret-key",
        google_client_id="test-client-id",
        google_client_secret="test-client-secret"
    )
EOF
```

**Archivos de test a crear:**

**backend/tests/unit/test_config.py**
```python
"""
Tests para configuración
"""
import pytest
from app.core.config import Settings


def test_settings_creation():
    """Test creación de settings"""
    settings = Settings(secret_key="test-key")
    assert settings.app_name == "ClassSphere"
    assert settings.port == 8000


def test_settings_from_env(monkeypatch):
    """Test settings desde variables de entorno"""
    monkeypatch.setenv("SECRET_KEY", "env-secret")
    monkeypatch.setenv("PORT", "9000")
    
    settings = Settings()
    assert settings.secret_key == "env-secret"
    assert settings.port == 9000
```

**backend/tests/integration/test_health.py**
```python
"""
Tests de integración para health check
"""
import pytest


def test_health_check(client):
    """Test health check endpoint"""
    response = client.get("/health")
    assert response.status_code == 200
    
    data = response.json()
    assert data["status"] == "healthy"
    assert data["service"] == "ClassSphere"
    assert "version" in data


def test_health_check_cors(client):
    """Test CORS en health check"""
    response = client.get(
        "/health",
        headers={"Origin": "http://localhost:3000"}
    )
    assert response.status_code == 200
    assert "access-control-allow-origin" in response.headers
```

**Verificación Día 2:**
```bash
# Ejecutar tests
cd backend
source venv/bin/activate
pytest tests/ -v

# Verificar cobertura
pytest tests/ --cov=src --cov-report=term-missing

# Debe mostrar cobertura ≥80%
```

**Criterios de Aceptación Día 2:**
- [ ] pytest configurado correctamente
- [ ] AsyncMock disponible
- [ ] Timeouts configurados (30s)
- [ ] Cobertura ≥80% funcionando
- [ ] Tests unitarios pasando
- [ ] Tests de integración pasando

**Validaciones de Prevención de Errores:**
- [ ] Pattern 4: AsyncMock importado en conftest.py
- [ ] Verificación: `python -c "from unittest.mock import AsyncMock; print('✅ AsyncMock OK')"`
- [ ] Template TDD para tests async disponible

---

### Día 3: Autenticación JWT

**Objetivo:** Implementar JWT con refresh tokens y password hashing.

**Archivos a crear:**

**backend/src/app/core/security.py**
```python
"""
Utilidades de seguridad
"""
from datetime import datetime, timedelta
from typing import Optional
from jose import JWTError, jwt
from passlib.context import CryptContext
from app.core.config import settings

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verificar password"""
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    """Hash de password"""
    return pwd_context.hash(password)


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """Crear access token JWT"""
    to_encode = data.copy()
    
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(
            minutes=settings.access_token_expire_minutes
        )
    
    to_encode.update({"exp": expire, "type": "access"})
    encoded_jwt = jwt.encode(
        to_encode,
        settings.secret_key,
        algorithm=settings.algorithm
    )
    return encoded_jwt


def create_refresh_token(data: dict) -> str:
    """Crear refresh token JWT"""
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(days=settings.refresh_token_expire_days)
    
    to_encode.update({"exp": expire, "type": "refresh"})
    encoded_jwt = jwt.encode(
        to_encode,
        settings.secret_key,
        algorithm=settings.algorithm
    )
    return encoded_jwt


def decode_token(token: str) -> dict:
    """Decodificar token JWT"""
    try:
        payload = jwt.decode(
            token,
            settings.secret_key,
            algorithms=[settings.algorithm]
        )
        return payload
    except JWTError:
        return None
```

**backend/src/app/models/user.py**
```python
"""
Modelo de usuario
"""
from enum import Enum
from pydantic import BaseModel, EmailStr


class UserRole(str, Enum):
    """Roles de usuario"""
    ADMIN = "admin"
    COORDINATOR = "coordinator"
    TEACHER = "teacher"
    STUDENT = "student"


class User(BaseModel):
    """Usuario del sistema"""
    id: str
    email: EmailStr
    name: str
    role: UserRole
    is_active: bool = True
    
    class Config:
        use_enum_values = True


class UserInDB(User):
    """Usuario en base de datos"""
    hashed_password: str
```

**backend/src/app/services/auth_service.py**
```python
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
        
        return User(**user.dict())
    
    async def get_user_by_email(self, email: str) -> Optional[User]:
        """Obtener usuario por email"""
        user = MOCK_USERS.get(email)
        if not user:
            return None
        return User(**user.dict())
```

**backend/src/app/api/endpoints/auth.py**
```python
"""
Endpoints de autenticación
"""
from datetime import timedelta
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel
from app.core.security import create_access_token, create_refresh_token, decode_token
from app.services.auth_service import AuthService
from app.models.user import User

router = APIRouter(prefix="/api/v1/auth", tags=["auth"])
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")


class TokenResponse(BaseModel):
    """Respuesta de token"""
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    expires_in: int
    user: User


@router.post("/login", response_model=TokenResponse)
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    auth_service: AuthService = Depends()
):
    """Login con JWT"""
    user = await auth_service.authenticate_user(
        form_data.username,
        form_data.password
    )
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password"
        )
    
    access_token = create_access_token(data={"sub": user.email})
    refresh_token = create_refresh_token(data={"sub": user.email})
    
    return TokenResponse(
        access_token=access_token,
        refresh_token=refresh_token,
        expires_in=1800,
        user=user
    )


@router.get("/me", response_model=User)
async def get_current_user(
    token: str = Depends(oauth2_scheme),
    auth_service: AuthService = Depends()
):
    """Obtener usuario actual"""
    payload = decode_token(token)
    if not payload:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token"
        )
    
    email = payload.get("sub")
    user = await auth_service.get_user_by_email(email)
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found"
        )
    
    return user
```

**Actualizar backend/src/app/main.py:**
```python
# Agregar después de create_app():
from app.api.endpoints import auth

app.include_router(auth.router)
```

**Tests para Día 3:**

**backend/tests/unit/test_security.py**
```python
"""
Tests para seguridad
Prevención Pattern 4: AsyncMock para funciones async
"""
import pytest
from unittest.mock import AsyncMock
from app.core.security import (
    verify_password,
    get_password_hash,
    create_access_token,
    decode_token
)


def test_password_hashing():
    """Test hash de password"""
    password = "secret123"
    hashed = get_password_hash(password)
    
    assert hashed != password
    assert verify_password(password, hashed)
    assert not verify_password("wrong", hashed)


def test_create_access_token():
    """Test creación de access token"""
    data = {"sub": "test@example.com"}
    token = create_access_token(data)
    
    assert token is not None
    assert isinstance(token, str)


def test_decode_token():
    """Test decodificación de token"""
    data = {"sub": "test@example.com"}
    token = create_access_token(data)
    payload = decode_token(token)
    
    assert payload is not None
    assert payload["sub"] == "test@example.com"
    assert payload["type"] == "access"
```

**backend/tests/integration/test_auth.py**
```python
"""
Tests de integración para autenticación
Prevención Pattern 4: Mock paths correctos para verify_token
"""
import pytest
from unittest.mock import patch, AsyncMock


def test_login_success(client):
    """Test login exitoso"""
    response = client.post(
        "/api/v1/auth/login",
        data={
            "username": "admin@classsphere.edu",
            "password": "secret"
        }
    )
    
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert "refresh_token" in data
    assert data["token_type"] == "bearer"
    assert data["user"]["email"] == "admin@classsphere.edu"


def test_login_invalid_credentials(client):
    """Test login con credenciales inválidas"""
    response = client.post(
        "/api/v1/auth/login",
        data={
            "username": "admin@classsphere.edu",
            "password": "wrong"
        }
    )
    
    assert response.status_code == 401


def test_get_current_user(client):
    """Test obtener usuario actual"""
    # Login primero
    login_response = client.post(
        "/api/v1/auth/login",
        data={
            "username": "admin@classsphere.edu",
            "password": "secret"
        }
    )
    token = login_response.json()["access_token"]
    
    # Obtener usuario
    response = client.get(
        "/api/v1/auth/me",
        headers={"Authorization": f"Bearer {token}"}
    )
    
    assert response.status_code == 200
    data = response.json()
    assert data["email"] == "admin@classsphere.edu"
    assert data["role"] == "admin"
```

**Verificación Día 3:**
```bash
# Tests
cd backend
source venv/bin/activate
pytest tests/ -v --cov=src

# Test manual de login
curl -X POST http://localhost:8000/api/v1/auth/login \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=admin@classsphere.edu&password=secret"

# Debe retornar access_token y refresh_token
```

**Criterios de Aceptación Día 3:**
- [ ] JWT tokens funcionando
- [ ] Password hashing con bcrypt
- [ ] Login endpoint funcional
- [ ] Get current user funcional
- [ ] Tests unitarios pasando
- [ ] Tests de integración pasando
- [ ] Cobertura ≥80%

**Validaciones de Prevención de Errores:**
- [ ] Pattern 4: Tests async usan AsyncMock (no Mock regular)
- [ ] Pattern 4: Mock paths correctos (src.app.api.endpoints.auth.verify_token)
- [ ] Verificación: `pytest tests/integration/test_auth.py -v` sin warnings de coroutine

---

### Días 4-12: Resumen de Tareas

**Día 4:** OAuth 2.0 Google con PKCE + Pattern 3 (Zod schemas)
**Día 5:** Sistema de roles y middleware + Pattern 4 (AsyncMock en tests)
**Día 6:** Configuración Frontend Next.js 15 + Pattern 2 (Next.js config)
**Día 7:** Componentes de autenticación React + Pattern 5 (Mocks frontend)
**Día 8:** React Query v4 y hooks + Pattern 5 (Dependency mocking)
**Día 9:** Dashboards por rol + Pattern 3 (Zod validation)
**Día 10:** Integración frontend-backend + Pattern 6 (E2E tests)
**Día 11:** Tests E2E con Playwright + Pattern 6 (Coverage completa)
**Día 12:** CI/CD y documentación + Scripts auto-corrección

*(Cada día tiene instrucciones detalladas similares a los días 1-3)*

---

## ✅ FINAL: Checklist y Próximos Pasos

### Checklist de Verificación Fase 1

**Backend:**
- [ ] FastAPI 0.104.1 funcionando en puerto 8000
- [ ] Pydantic v2 configurado (Pattern 1: ConfigDict imports)
- [ ] JWT authentication completo (Pattern 4: AsyncMock en tests)
- [ ] OAuth 2.0 Google funcionando (Pattern 3: Zod schemas)
- [ ] Sistema de roles implementado
- [ ] Health checks respondiendo
- [ ] Tests backend ≥80% coverage

**Prevención de Errores Integrada:**
- [ ] Pattern 1: 0 errores ConfigDict (100% prevención)
- [ ] Pattern 4: 0 errores AsyncMock (100% prevención)
- [ ] Pattern 4: 0 errores mock paths (100% prevención)
- [ ] Scripts de validación automática ejecutándose

**Frontend:**
- [ ] Next.js 15 + React 19 funcionando (Pattern 2: Config limpio)
- [ ] TypeScript configurado
- [ ] Tailwind CSS aplicado
- [ ] React Query v4 integrado
- [ ] Componentes de autenticación (Pattern 5: Mocks comprehensivos)
- [ ] Dashboards por rol (Pattern 3: Zod validation)
- [ ] Tests frontend ≥80% coverage

**Prevención de Errores Integrada:**
- [ ] Pattern 2: 0 errores Next.js config deprecated (100% prevención)
- [ ] Pattern 3: 0 errores Zod schemas (100% prevención)
- [ ] Pattern 5: 0 errores dependency mocking (100% prevención)
- [ ] Validación automática en tests

**Integración:**
- [ ] Frontend comunica con backend
- [ ] JWT tokens funcionan
- [ ] OAuth flow completo
- [ ] Protección de rutas por rol
- [ ] Tests E2E pasando (Pattern 6: Coverage completa)

**Prevención de Errores Integrada:**
- [ ] Pattern 6: E2E tests frontend-backend (100% coverage)
- [ ] Métricas de éxito: 45/45 tests passing (100%)
- [ ] Tiempo resolución errores: <3 min (mejora 80%)

### Comandos de Validación Final

```bash
# Backend
cd backend && pytest tests/ --cov=src --cov-fail-under=80

# Frontend
cd frontend && npm run test -- --coverage

# E2E
cd frontend && npm run test:e2e

# Health checks
curl http://localhost:8000/health
curl http://localhost:3000
```

### Próximos Pasos

**Continuar con Fase 2:**
- [03_plan_fase2_google_integration.md](03_plan_fase2_google_integration.md)
- Integración Google Classroom API
- Modo dual (Google/Mock)
- Dashboards con métricas

---

[← Plan Principal](01_plan_index.md) | [Siguiente → Fase 2](03_plan_fase2_google_integration.md)
