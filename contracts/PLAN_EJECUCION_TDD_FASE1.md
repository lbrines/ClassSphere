# Plan de Ejecución TDD: Fase 1 - Fundaciones

---
**Autor**: Sistema de Planes de Ejecución TDD
**Fecha**: 2025-10-04
**Versión**: 1.0
**Fase**: Fundaciones TDD (Días 1-12)
---

## Objetivo de la Fase

Implementar el sistema básico funcionando con autenticación completa y tests TDD, garantizando la cobertura 100% en todos los componentes críticos y el cumplimiento de los estándares de arquitectura.

## Principios TDD de la Fase 1

### Ciclo TDD Estricto

1. **Red**: Escribir test que falle
2. **Green**: Implementar código mínimo para pasar
3. **Refactor**: Mejorar código manteniendo tests verdes

### Timeouts Configurados

Todos los tests de la Fase 1 tendrán timeouts específicos:

```python
# Tests unitarios: 2 segundos máximo
@pytest.mark.asyncio(timeout=2.0)
async def test_auth_service_unit():
    # Test code here
    pass

# Tests de integración: 5 segundos máximo
@pytest.mark.asyncio(timeout=5.0)
async def test_auth_integration():
    # Test code here
    pass
```

### Puerto 8000 Obligatorio

Siguiendo la definición de [Puerto 8000 - Estándar Arquitectónico] del contrato unificado, el servidor siempre se iniciará en el puerto 8000:

```python
# Servidor siempre en puerto 8000
if __name__ == "__main__":
    uvicorn.run(
        "src.app.main:app",
        host="127.0.0.1",
        port=8000,
        reload=True
    )
```

Se implementarán verificaciones automáticas para garantizar que el puerto 8000 esté disponible:

```bash
echo "🔍 Verificación TDD: puerto 8000..."
if lsof -Pi :8000 -sTCP:LISTEN -t >/dev/null ; then
    echo "⚠️  Puerto ocupado. Limpieza TDD..."
    pkill -f "port 8000"
    sleep 2
fi
```

## Plan de Implementación TDD

### Día 1-3: Configuración Base TDD

#### Día 1: Configuración del Entorno TDD

1. **Configuración del proyecto Python 3.11.4 con pyenv**
   - Test: Verificar versión de Python
   - Implementación: Configurar pyenv con Python 3.11.4
   - Refactor: Optimizar configuración

2. **Configuración FastAPI 0.104.1 + Pydantic v2**
   - Test: Verificar importación de FastAPI y Pydantic v2
   - Implementación: Instalar dependencias
   - Refactor: Organizar requirements.txt

3. **Estructura de directorios TDD**
   - Test: Verificar estructura de directorios
   - Implementación: Crear estructura según contrato
   - Refactor: Optimizar organización

#### Día 2: Configuración de Testing TDD

1. **Configuración pytest con AsyncMock**
   - Test: Verificar funcionamiento de AsyncMock
   - Implementación: Configurar pytest con soporte para AsyncMock
   - Refactor: Optimizar configuración

2. **Configuración de timeouts para tests**
   - Test: Verificar funcionamiento de timeouts
   - Implementación: Configurar pytest con timeouts
   - Refactor: Ajustar timeouts según tipo de test

3. **Configuración de cobertura 100%**
   - Test: Verificar generación de informes de cobertura
   - Implementación: Configurar pytest-cov
   - Refactor: Optimizar configuración

#### Día 3: Configuración de Infraestructura TDD

1. **Configuración de Redis para caché**
   - Test: Verificar conexión a Redis
   - Implementación: Configurar cliente Redis
   - Refactor: Optimizar configuración

2. **Configuración de puerto 8000 fijo**
   - Test: Verificar inicio en puerto 8000
   - Implementación: Configurar servidor en puerto 8000
   - Refactor: Implementar verificación automática

3. **Configuración de CI/CD para TDD**
   - Test: Verificar pipeline CI/CD
   - Implementación: Configurar GitHub Actions
   - Refactor: Optimizar pipeline

### Día 4-6: Autenticación Completa TDD

#### Día 4: JWT Authentication TDD

1. **JWT Authentication con refresh rotation**
   - Test: Verificar generación y validación de tokens JWT
   - Implementación: Implementar servicio de autenticación JWT
   - Refactor: Optimizar seguridad y rendimiento

2. **Middleware de autenticación JWT**
   - Test: Verificar funcionamiento de middleware
   - Implementación: Implementar middleware de autenticación
   - Refactor: Optimizar manejo de errores

#### Día 5: OAuth 2.0 TDD

1. **OAuth 2.0 con Google (PKCE + State validation)**
   - Test: Verificar flujo OAuth con mocks
   - Implementación: Implementar servicio OAuth
   - Refactor: Optimizar seguridad y manejo de errores

2. **Integración OAuth con sistema de usuarios**
   - Test: Verificar integración OAuth-usuarios
   - Implementación: Implementar integración
   - Refactor: Optimizar manejo de sesiones

#### Día 6: Sistema de Roles TDD

1. **Sistema de roles (admin, coordinador, teacher, estudiante)**
   - Test: Verificar funcionamiento de roles
   - Implementación: Implementar sistema de roles
   - Refactor: Optimizar validación de permisos

2. **Middleware de seguridad (Rate limiting + CORS)**
   - Test: Verificar funcionamiento de middleware
   - Implementación: Implementar middleware de seguridad
   - Refactor: Optimizar configuración

### Día 7-9: Frontend Fundacional TDD

#### Día 7: UI Base TDD

1. **Next.js 13.5.6 + TypeScript 5.2 setup**
   - Test: Verificar configuración Next.js
   - Implementación: Configurar proyecto Next.js
   - Refactor: Optimizar configuración

2. **Tailwind CSS 3.3 configuración**
   - Test: Verificar funcionamiento de Tailwind
   - Implementación: Configurar Tailwind CSS
   - Refactor: Optimizar configuración

#### Día 8: Componentes de Autenticación TDD

1. **Componentes de autenticación (LoginForm, OAuthButton)**
   - Test: Verificar renderizado de componentes
   - Implementación: Implementar componentes
   - Refactor: Optimizar UI/UX

2. **Hooks personalizados (useAuth, useOAuth, useApi)**
   - Test: Verificar funcionamiento de hooks
   - Implementación: Implementar hooks
   - Refactor: Optimizar manejo de estado

#### Día 9: Servicios de API TDD

1. **Servicios de API y manejo de errores**
   - Test: Verificar funcionamiento de servicios
   - Implementación: Implementar servicios de API
   - Refactor: Optimizar manejo de errores

2. **Integración con backend**
   - Test: Verificar comunicación frontend-backend
   - Implementación: Implementar integración
   - Refactor: Optimizar comunicación

### Día 10-12: Integración Base TDD

#### Día 10: Comunicación Frontend-Backend TDD

1. **Tests de integración frontend-backend**
   - Test: Verificar integración completa
   - Implementación: Implementar tests de integración
   - Refactor: Optimizar cobertura

2. **Comunicación API completa con envelope estándar**
   - Test: Verificar formato de respuestas
   - Implementación: Implementar envelope estándar
   - Refactor: Optimizar formato

#### Día 11: Protección de Rutas TDD

1. **Protección de rutas por rol**
   - Test: Verificar protección de rutas
   - Implementación: Implementar protección
   - Refactor: Optimizar seguridad

2. **Tests E2E básicos con Playwright**
   - Test: Verificar funcionamiento de tests E2E
   - Implementación: Implementar tests E2E
   - Refactor: Optimizar cobertura

#### Día 12: CI/CD y Documentación TDD

1. **Configuración CI/CD básica**
   - Test: Verificar pipeline completo
   - Implementación: Configurar pipeline
   - Refactor: Optimizar automatización

2. **Documentación TDD**
   - Test: Verificar generación de documentación
   - Implementación: Implementar documentación
   - Refactor: Optimizar claridad

## Criterios de Aceptación TDD Fase 1

- [ ] Servidor inicia en puerto 8000 sin errores
- [ ] Tests async usan `AsyncMock` correctamente
- [ ] Tests de CORS verifican headers básicos
- [ ] Health check responde correctamente
- [ ] Cobertura 100% en toda la Fase 1 sin warnings críticos
- [ ] Lifespan resiliente funciona sin servicios externos

## Templates TDD Estándar

### Template para Tests de Autenticación

```python
"""
Test file for auth_service.py

CRITICAL OBJECTIVES:
- Verify JWT token generation and validation
- Test OAuth flow with Google

DEPENDENCIES:
- AsyncMock for async methods
- Redis for session storage
"""

import pytest
from unittest.mock import AsyncMock
from datetime import datetime, timedelta
from jose import jwt

from src.app.services.auth_service import AuthService
from src.app.core.config import settings

# BEGINNING: Critical tests for core functionality
@pytest.mark.asyncio(timeout=2.0)
async def test_jwt_token_generation():
    # Arrange
    auth_service = AuthService()
    user_data = {"sub": "user123", "role": "teacher"}
    
    # Act
    token = await auth_service.create_access_token(user_data)
    
    # Assert
    decoded = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
    assert decoded["sub"] == "user123"
    assert decoded["role"] == "teacher"
    assert "exp" in decoded

# MIDDLE: Detailed implementation tests
@pytest.mark.asyncio(timeout=2.0)
async def test_token_refresh():
    # Arrange
    auth_service = AuthService()
    user_data = {"sub": "user123", "role": "teacher"}
    token = await auth_service.create_access_token(user_data)
    
    # Act
    new_token = await auth_service.refresh_token(token)
    
    # Assert
    decoded = jwt.decode(new_token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
    assert decoded["sub"] == "user123"
    assert decoded["role"] == "teacher"
    assert decoded["exp"] > jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])["exp"]

# END: Verification and next steps
@pytest.mark.asyncio(timeout=2.0)
async def test_token_validation_edge_cases():
    # Arrange
    auth_service = AuthService()
    
    # Act & Assert: Empty token
    with pytest.raises(Exception):
        await auth_service.validate_token("")
    
    # Act & Assert: Invalid token
    with pytest.raises(Exception):
        await auth_service.validate_token("invalid.token.here")
    
    # Act & Assert: Expired token
    expired_token = jwt.encode(
        {"sub": "user123", "exp": datetime.utcnow() - timedelta(minutes=5)},
        settings.SECRET_KEY,
        algorithm=settings.ALGORITHM
    )
    with pytest.raises(Exception):
        await auth_service.validate_token(expired_token)
```

### Template para Tests de Redis

```python
"""
Test file for redis_cache.py

CRITICAL OBJECTIVES:
- Verify Redis connection and operations
- Test cache functionality

DEPENDENCIES:
- AsyncMock for Redis client
"""

import pytest
import json
from unittest.mock import AsyncMock, patch

from src.app.core.cache import get_redis_client, get_cached_data, set_cached_data

# BEGINNING: Critical tests for core functionality
@pytest.fixture
def mock_redis_fixed():
    """Mock Redis con configuración correcta"""
    mock_redis = AsyncMock()
    mock_redis.ping = AsyncMock(return_value=True)
    mock_redis.get = AsyncMock(return_value=None)
    mock_redis.set = AsyncMock(return_value=True)
    mock_redis.delete = AsyncMock(return_value=1)
    mock_redis.exists = AsyncMock(return_value=False)
    mock_redis.close = AsyncMock()
    mock_redis.aclose = AsyncMock()  # Para Redis moderno
    return mock_redis

@pytest.mark.asyncio(timeout=2.0)
async def test_redis_connection():
    # Arrange
    with patch('src.app.core.cache.AsyncRedis') as mock_redis_class:
        mock_redis = AsyncMock()
        mock_redis_class.from_url.return_value = mock_redis
        mock_redis.ping.return_value = True
        
        # Act
        client = await get_redis_client()
        
        # Assert
        assert client is mock_redis
        mock_redis_class.from_url.assert_called_once()
        mock_redis.ping.assert_called_once()

# MIDDLE: Detailed implementation tests
@pytest.mark.asyncio(timeout=2.0)
async def test_get_cached_data():
    # Arrange
    test_data = {"name": "test", "value": 123}
    with patch('src.app.core.cache.get_redis_client') as mock_get_redis:
        mock_redis = AsyncMock()
        mock_get_redis.return_value = mock_redis
        mock_redis.get.return_value = json.dumps(test_data)
        
        # Act
        result = await get_cached_data("test_key")
        
        # Assert
        assert result == test_data
        mock_redis.get.assert_called_once_with("test_key")

@pytest.mark.asyncio(timeout=2.0)
async def test_set_cached_data():
    # Arrange
    test_data = {"name": "test", "value": 123}
    with patch('src.app.core.cache.get_redis_client') as mock_get_redis:
        mock_redis = AsyncMock()
        mock_get_redis.return_value = mock_redis
        
        # Act
        await set_cached_data("test_key", test_data, 3600)
        
        # Assert
        mock_redis.set.assert_called_once_with(
            "test_key", 
            json.dumps(test_data), 
            ex=3600
        )

# END: Verification and next steps
@pytest.mark.asyncio(timeout=2.0)
async def test_redis_connection_error():
    # Arrange
    with patch('src.app.core.cache.AsyncRedis') as mock_redis_class:
        mock_redis_class.from_url.side_effect = Exception("Redis connection failed")
        
        # Act & Assert
        with pytest.raises(Exception, match="Redis connection failed"):
            await get_redis_client()
```

### Template para Verificación de Puerto 8000

```bash
#!/bin/bash
# Script TDD para verificación de puerto 8000

echo "🔧 TDD: Iniciando verificación de puerto 8000..."

# Limpieza previa
pkill -f uvicorn || true
sleep 2

echo "🔍 TDD: Verificación de puerto 8000..."
if lsof -Pi :8000 -sTCP:LISTEN -t >/dev/null 2>&1; then
    echo "⚠️  TDD: Puerto ocupado. Limpieza automática..."
    pkill -f "port 8000" || true
    sleep 3
fi

echo "🚀 TDD: Iniciando servidor en puerto 8000..."
python3 -m uvicorn src.app.main:app --host 127.0.0.1 --port 8000 &
SERVER_PID=$!

# Esperar a que el servidor esté listo
sleep 3

# Verificar que el servidor está funcionando
if ! curl -s -o /dev/null -w "%{http_code}" http://127.0.0.1:8000/health | grep -q "200"; then
    echo "❌ TDD: Error al iniciar servidor en puerto 8000"
    kill $SERVER_PID
    exit 1
fi

echo "✅ TDD: Servidor funcionando correctamente en puerto 8000"
echo "📊 TDD: PID del servidor: $SERVER_PID"
```

## Entregables TDD Fase 1

1. **Código Backend**
   - Estructura completa del proyecto
   - Autenticación JWT + OAuth
   - Sistema de roles
   - Middleware de seguridad
   - Health check

2. **Código Frontend**
   - Estructura Next.js + TypeScript
   - Componentes de autenticación
   - Hooks personalizados
   - Servicios de API

3. **Tests**
   - Tests unitarios con AsyncMock y timeouts
   - Tests de integración frontend-backend
   - Tests E2E básicos
   - Cobertura 100% en módulos críticos

4. **Documentación**
   - Documentación de API
   - Documentación de componentes
   - Documentación de tests

## Próximos Pasos

1. Validar cumplimiento de criterios de aceptación
2. Preparar transición a Fase 2: Google Integration TDD
3. Revisar y actualizar documentación
4. Optimizar pipeline CI/CD para Fase 2
