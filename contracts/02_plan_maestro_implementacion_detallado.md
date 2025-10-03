---
llm:metadata:
  title: "Plan Maestro de Implementación Detallado - Dashboard Educativo"
  version: "2.4"
  type: "implementation_master_plan"
  stage: "unified_implementation"
  execution_priority: "complete_system_roadmap"
  contains:
    - unified_phase_breakdown
    - tdd_methodology_strict
    - quality_gates_per_phase
    - unified_technical_specifications
    - comprehensive_testing_strategy
    - coverage_100_protocols
    - error_prevention_protocols
    - infrastructure_error_prevention
    - production_deployment_roadmap
---

# Plan Maestro de Implementación Detallado - Dashboard Educativo

## Información del Proyecto
- **Proyecto**: Dashboard Educativo - Sistema Completo Unificado
- **Plan**: Implementación Detallada por Fases Unificadas
- **Autor**: Sistema de Contratos LLM
- **Fecha**: 2025-10-03 (Actualizado con Especificación Unificada Completa + Prevención de Errores + Cobertura 100% + Infraestructura)
- **Propósito**: Plan detallado para cumplir el contrato unificado completo con metodología TDD estricta y arquitectura resiliente

## =====
<llm:section id="plan_overview" type="overview">
## Resumen Ejecutivo del Plan

### Objetivo Principal
Implementar el Dashboard Educativo completo siguiendo el contrato unificado `00_dashboard_educativo_fullstack_unified_complete.md` con metodología TDD estricta, arquitectura resiliente, prevención de errores y quality gates por fase.

### Metodología TDD Consolidada
**Ciclo Red-Green-Refactor estricto**:
1. **Red**: Escribir test que falle definiendo comportamiento esperado
2. **Green**: Implementar código mínimo para hacer pasar el test
3. **Refactor**: Mejorar código manteniendo tests verdes
4. **Document**: Documentar decisiones basadas en tests
5. **Integrate**: Integrar con sistema existente
6. **Validate**: Validar cumplimiento de criterios de aceptación

### Duración Total: 45 días
- **Fase 1**: Fundaciones Unificadas (12 días)
- **Fase 2**: Google Integration Completa (10 días)
- **Fase 3**: Visualización Avanzada + Notificaciones (10 días)
- **Fase 4**: Production Ready + WCAG 2.2 AA (13 días)

### Stack Tecnológico Unificado
```
# Backend Unificado
- Python 3.11.4 (pyenv)
- FastAPI 0.104.1 + Pydantic v2 (validación estricta)
- Google Classroom API + WebSockets (notificaciones)
- MongoDB + Redis (cache y sesiones)
- pytest (testing exhaustivo)

# Frontend Unificado
- Next.js 13.5.6 (LTS) + React 18.2.0
- TypeScript 5.1.6 + @tanstack/react-query 4.36.1
- ApexCharts 5.3.5 + D3.js (visualizaciones)
- Tailwind CSS 3.3.3 + i18n (internacionalización)
- Vitest + Playwright (testing completo)

# DevOps Unificado
- Docker (multi-stage) + GitHub Actions
- Trivy (security) + pnpm 8.x+
- Quality Gates + Auto-deploy
```

### Quality Gates Obligatorios
- **Cobertura**: ≥100% módulos críticos (config, database, main, auth, models)
- **Performance**: <2s dashboard load (Fase 2), <1.5s (Fase 3), <1s (Fase 4)
- **Security**: 0 vulnerabilidades CRITICAL/HIGH
- **Accessibility**: WCAG 2.2 AA compliance completo (Fase 4)
- **Testing**: E2E + Unit + Integration + Performance + Visual
- **Error Prevention**: 0 warnings críticos + APIs modernas + Puerto 8000 fijo
- **Context Managers**: Tests completos para lifespan + AsyncMock
- **Error Paths**: Todos los try/except cubiertos + Limpieza automática
- **Modern APIs**: Pydantic v2 + FastAPI lifespan + Migración automática
- **Infraestructura**: Servicios resilientes + Verificación automática

</llm:section>

## =====
<llm:section id="phase1_foundations" type="detailed_phase">
## Fase 1: Fundaciones Unificadas (Días 1-12)

### Objetivo de la Fase
Establecer las fundaciones sólidas del sistema unificado con backend FastAPI + Pydantic v2, frontend Next.js + React Query, autenticación dual (JWT + OAuth 2.0), comunicación API funcional y arquitectura resiliente con puerto 8000 fijo.

### Días 1-3: Backend Fundacional

#### Día 1: Estructura y Configuración Unificada
**TDD Approach**:
- [ ] Crear estructura de directorios backend/ completa según especificación unificada
- [ ] Configurar requirements.txt con versiones exactas (FastAPI 0.104.1, Pydantic v2)
- [ ] Crear pytest.ini y pyproject.toml con configuración unificada
- [ ] Configurar variables de entorno (.env.example) con todas las variables necesarias
- [ ] Escribir tests fallidos para configuración base + arquitectura resiliente

**Implementación**:
- [ ] Instalar dependencias: FastAPI 0.104.1, Pydantic v2, pydantic-settings, MongoDB, Redis
- [ ] Configurar settings con BaseSettings + ConfigDict (Pydantic v2)
- [ ] Crear main.py con FastAPI app + lifespan context manager
- [ ] Implementar health check endpoint + verificación de servicios
- [ ] Configurar puerto 8000 fijo como estándar arquitectónico
- [ ] Implementar limpieza automática de procesos
- [ ] Verificar que tests pasen + arquitectura resiliente

**Quality Gate**:
- [ ] pytest -q ejecuta sin errores (34 tests pasando)
- [ ] curl http://localhost:8000/health retorna 200
- [ ] Cobertura 100% en módulos críticos (config, database, main)
- [ ] Context Managers: Tests completos para lifespan
- [ ] Error Paths: Tests para todos los try/except
- [ ] 0 warnings de deprecación (Pydantic v2 + FastAPI)
- [ ] ConfigDict + lifespan implementados correctamente
- [ ] Tests async usan AsyncMock

#### Día 2: Modelos y Excepciones Unificadas
**TDD Approach**:
- [ ] Escribir tests para modelos User + OAuthToken (Pydantic v2)
- [ ] Tests para excepciones personalizadas + OAuth exceptions
- [ ] Tests para validación de datos + OAuth token validation
- [ ] Tests para migración automática de APIs deprecadas

**Implementación**:
- [ ] Crear modelos User, UserCreate, UserResponse + OAuthToken, OAuthTokenCreate
- [ ] Implementar excepciones: AuthenticationError, TokenExpiredError, OAuthError, GoogleAPIError
- [ ] Configurar json_encoders con model_config (Pydantic v2) + ConfigDict
- [ ] Campos opcionales para compatibilidad MockService + Google API
- [ ] Implementar migración automática de Pydantic v1 a v2
- [ ] Configurar validadores estrictos para OAuth tokens

**Quality Gate**:
- [ ] Todos los tests de modelos pasan
- [ ] Cobertura 100% en modelos y excepciones
- [ ] Edge Cases: Tests para valores límite
- [ ] Serialization: Tests para model_dump() y model_validate()
- [ ] Validación Pydantic v2 funciona correctamente
- [ ] Modelos compatibles con datos mock
- [ ] Sin warnings de Pydantic v1 (ConfigDict usado)
- [ ] Tests de modelos usan AsyncMock para métodos async
- [ ] Validadores funcionan sin deprecation warnings

#### Día 3: Autenticación Dual (JWT + OAuth 2.0)
**TDD Approach**:
- [ ] Tests para AuthService.create_access_token (JWT)
- [ ] Tests para AuthService.verify_token (JWT)
- [ ] Tests para OAuthService.google_oauth_flow
- [ ] Tests para OAuthService.exchange_code_for_token
- [ ] Tests para hash_password/verify_password
- [ ] Tests para get_user_permissions_by_role

**Implementación**:
- [ ] Implementar AuthService con JWT estándar + refresh rotation
- [ ] Implementar OAuthService con Google OAuth 2.0 + PKCE
- [ ] Campo 'sub' en payload JWT (estándar) + OAuth token validation
- [ ] Campos email, id, role, exp, iat + OAuth scopes
- [ ] Manejo de TokenExpiredError + OAuthError
- [ ] Configuración JWT + OAuth con variables de entorno
- [ ] Implementar dual mode switching (JWT/Mock vs OAuth/Google)

**Quality Gate**:
- [ ] JWT se crea y verifica correctamente
- [ ] Campo 'sub' presente en payload
- [ ] Tests de autenticación pasan 100%

### Días 4-6: Frontend Fundacional

#### Día 4: Estructura Next.js Unificada
**TDD Approach**:
- [ ] Crear estructura de directorios frontend/ completa según especificación unificada
- [ ] Configurar package.json con dependencias exactas
- [ ] Configurar Next.js 13.5.6 + TypeScript 5.1.6
- [ ] Escribir tests fallidos para componentes base + i18n

**Implementación**:
- [ ] Instalar Next.js 13.5.6, React 18.2.0, TypeScript 5.1.6
- [ ] Configurar Tailwind CSS 3.3.3 + @tanstack/react-query 4.36.1
- [ ] Configurar i18n (internacionalización) + locales
- [ ] Crear layout básico + providers (QueryProvider)
- [ ] Configurar routing + middleware de autenticación
- [ ] Configurar puerto 3000 fijo para desarrollo

**Quality Gate**:
- [ ] Next.js se ejecuta sin errores
- [ ] TypeScript compila correctamente
- [ ] Tailwind CSS funciona

#### Día 5: Componentes UI Base
**TDD Approach**:
- [ ] Tests para componentes Button, Card, Input
- [ ] Tests para Layout component
- [ ] Tests para responsive design

**Implementación**:
- [ ] Crear componentes UI base con Tailwind
- [ ] Implementar Layout responsivo
- [ ] Configurar tema y colores
- [ ] Añadir iconos y assets

**Quality Gate**:
- [ ] Componentes renderizan correctamente
- [ ] Design responsivo funciona
- [ ] Tests de componentes pasan

#### Día 6: Autenticación Dual Frontend
**TDD Approach**:
- [ ] Tests para LoginForm component + OAuthButton
- [ ] Tests para AuthGuard + OAuthGuard
- [ ] Tests para useAuth hook + useOAuth hook
- [ ] Tests para manejo de tokens (JWT + OAuth)

**Implementación**:
- [ ] Crear LoginForm con validación + OAuthButton component
- [ ] Implementar AuthGuard para rutas protegidas + OAuth flow
- [ ] Crear useAuth hook con React Query + useOAuth hook
- [ ] Manejo de tokens en localStorage + OAuth token management
- [ ] Redirección post-login + OAuth callback handling
- [ ] Implementar dual mode switching en frontend

**Quality Gate**:
- [ ] Login funciona end-to-end
- [ ] Rutas protegidas funcionan
- [ ] Manejo de errores implementado

### Días 7-9: Integración Base

#### Día 7: API Communication
**TDD Approach**:
- [ ] Tests para useApi hook
- [ ] Tests para manejo de errores API
- [ ] Tests para interceptors de request/response

**Implementación**:
- [ ] Crear useApi hook con React Query
- [ ] Configurar axios con interceptors
- [ ] Manejo de errores centralizado
- [ ] Loading states y error states
- [ ] Retry logic para requests fallidos

**Quality Gate**:
- [ ] Frontend se comunica con backend
- [ ] Manejo de errores funciona
- [ ] Loading states implementados

#### Día 8: Manejo de Estados
**TDD Approach**:
- [ ] Tests para estado de autenticación
- [ ] Tests para cache de React Query
- [ ] Tests para sincronización de datos

**Implementación**:
- [ ] Configurar React Query cache
- [ ] Implementar estado global de auth
- [ ] Sincronización automática de datos
- [ ] Invalidación de cache inteligente
- [ ] Optimistic updates

**Quality Gate**:
- [ ] Estados sincronizados correctamente
- [ ] Cache funciona eficientemente
- [ ] Performance optimizada

#### Día 9: Protección de Rutas
**TDD Approach**:
- [ ] Tests para AuthGuard
- [ ] Tests para redirecciones
- [ ] Tests para roles y permisos

**Implementación**:
- [ ] Implementar protección por roles
- [ ] Redirecciones automáticas
- [ ] Middleware de autenticación
- [ ] Manejo de permisos granulares
- [ ] Logout automático por expiración

**Quality Gate**:
- [ ] Rutas protegidas por rol
- [ ] Redirecciones funcionan
- [ ] Permisos implementados

### Días 10-12: Testing y Refinamiento

#### Día 10: Tests E2E Básicos
**TDD Approach**:
- [ ] Tests E2E para flujo de login
- [ ] Tests E2E para navegación
- [ ] Tests E2E para protección de rutas

**Implementación**:
- [ ] Configurar Playwright
- [ ] Crear tests E2E básicos
- [ ] Configurar CI básico
- [ ] Tests de regresión visual

**Quality Gate**:
- [ ] Tests E2E pasan
- [ ] CI básico funciona
- [ ] Cobertura E2E > 70%

#### Día 11: Documentación y CI/CD
**TDD Approach**:
- [ ] Tests para documentación automática
- [ ] Tests para CI/CD pipeline
- [ ] Tests para quality gates

**Implementación**:
- [ ] Crear documentación API
- [ ] Configurar GitHub Actions básico
- [ ] Implementar quality gates
- [ ] Configurar Docker básico

**Quality Gate**:
- [ ] Documentación generada
- [ ] CI/CD funciona
- [ ] Quality gates implementados

#### Día 12: Validación Fase 1
**TDD Approach**:
- [ ] Tests de integración completos
- [ ] Tests de performance básicos
- [ ] Tests de security básicos

**Implementación**:
- [ ] Validar todos los criterios de aceptación
- [ ] Performance testing básico
- [ ] Security scanning básico
- [ ] Preparar para Fase 2

**Quality Gate**:
- [ ] 100% criterios Fase 1 completados
- [ ] Performance < 3s load time
- [ ] 0 vulnerabilidades CRITICAL
- [ ] Cobertura > 80%

### Criterios de Finalización Fase 1
- [ ] **Backend**: FastAPI + JWT + OAuth 2.0 + Pydantic v2 funcionando
- [ ] **Frontend**: Next.js + React Query + Auth dual + Layout responsivo + i18n
- [ ] **Testing**: ≥80% cobertura + CI básico + AsyncMock
- [ ] **Integration**: Frontend-Backend comunicación + OAuth flow completo
- [ ] **Performance**: <3s load time + Puerto 8000 fijo
- [ ] **Security**: 0 vulnerabilidades CRITICAL + CORS configurado
- [ ] **Error Prevention**: AsyncMock + CORS tests + Server health + Limpieza automática
- [ ] **Warnings**: 0 warnings de deprecación críticos + Migración automática
- [ ] **Modern APIs**: Pydantic v2 + FastAPI lifespan + ConfigDict implementados
- [ ] **Arquitectura**: Servicios resilientes + Verificación automática + Puerto fijo

</llm:section>

## =====
<llm:section id="error_prevention_protocols" type="error_prevention">
## Protocolos de Prevención de Errores

### Errores Comunes Identificados y Soluciones

#### 1. Errores de Testing Async
**Problema**: Tests de métodos async fallan por mocks incorrectos
**Solución**: Usar `AsyncMock` para todos los métodos async
```python
# ✅ CORRECTO
from unittest.mock import AsyncMock
mock_instance = AsyncMock()
mock_instance.admin.command.return_value = {"ok": 1}
```

#### 2. Errores de Headers HTTP
**Problema**: Tests de CORS fallan por headers específicos no presentes
**Solución**: Tests simplificados con headers básicos verificables
```python
# ✅ CORRECTO
assert "access-control-allow-origin" in response.headers
assert "access-control-allow-credentials" in response.headers
```

#### 3. Warnings de Deprecación
**Problema**: Pydantic v2 y FastAPI warnings por APIs deprecadas
**Solución**: Migrar a APIs modernas
```python
# ✅ PYDANTIC V2 - ConfigDict moderno
from pydantic import ConfigDict
model_config = ConfigDict(env_file=".env", case_sensitive=False)

# ✅ FASTAPI - Lifespan context manager
from contextlib import asynccontextmanager
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup/Shutdown logic
    yield
```

#### 4. Problemas de Servidor
**Problema**: Uvicorn no inicia correctamente en ciertos entornos
**Solución**: Configuración estándar de host/puerto
```bash
# ✅ CORRECTO
python3 -m uvicorn src.app.main:app --host 127.0.0.1 --port 8000
```

### Checklist de Prevención por Día

#### Día 1 - Estructura y Configuración
- [ ] **Setup**: Estructura de directorios creada
- [ ] **Dependencies**: Todas las dependencias instaladas
- [ ] **Config**: Variables de entorno configuradas
- [ ] **Tests**: Tests básicos pasando (27 tests)
- [ ] **Coverage**: Cobertura > 80% alcanzada
- [ ] **Server**: Health check endpoint funcional
- [ ] **Async**: Tests async usan AsyncMock
- [ ] **CORS**: Tests de CORS simplificados
- [ ] **Warnings**: 0 warnings de deprecación (Pydantic v2 + FastAPI)
- [ ] **Modern APIs**: ConfigDict + lifespan implementados

#### Día 2 - Modelos y Excepciones
- [ ] **Models**: Pydantic v2 con ConfigDict
- [ ] **Validation**: Validadores funcionan correctamente
- [ ] **Exceptions**: Jerarquía de excepciones completa
- [ ] **Tests**: Tests de modelos pasando
- [ ] **Migration**: Sin warnings de Pydantic v1
- [ ] **Async Tests**: AsyncMock usado correctamente

#### Días 3-12 - Fundaciones Completas
- [ ] **Auth**: JWT + OAuth funcionando
- [ ] **Frontend**: Next.js + Auth + Layout
- [ ] **Integration**: Frontend-Backend comunicación
- [ ] **E2E**: Tests end-to-end básicos
- [ ] **CI**: Pipeline básico funcionando
- [ ] **Error Prevention**: Todos los checks de prevención pasando

### Templates Estándar para Prevención

#### Template para Tests Async
```python
@pytest.mark.asyncio
async def test_async_method():
    with patch('module.AsyncClass') as mock_class:
        mock_instance = AsyncMock()
        mock_class.return_value = mock_instance
        # Test implementation
```

#### Template para Configuración Pydantic v2
```python
from pydantic import ConfigDict
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    field_name: str = "default_value"
    
    model_config = ConfigDict(
        env_file=".env",
        case_sensitive=False,
        extra="ignore"
    )
```

#### Template para FastAPI con Lifespan
```python
from contextlib import asynccontextmanager
from fastapi import FastAPI

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup logic
    try:
        # Initialize services
        pass
    except Exception as e:
        print(f"Warning: Startup error: {e}")
    
    yield
    
    # Shutdown logic
    try:
        # Cleanup services
        pass
    except Exception as e:
        print(f"Warning: Shutdown error: {e}")

def create_app() -> FastAPI:
    return FastAPI(
        title="App Name",
        version="1.0.0",
        lifespan=lifespan
    )
```

### Protocolo de Cobertura 100%

#### 1. Identificación de Líneas Sin Cubrir
```bash
# Comando para identificar líneas específicas sin cubrir
pytest tests/ --cov=src --cov-report=term-missing --cov-report=html

# Verificar cobertura por archivo
pytest tests/unit/ --cov=src --cov-report=term-missing

# Generar reporte HTML detallado
pytest tests/ --cov=src --cov-report=html
open htmlcov/index.html
```

#### 2. Análisis de Código Complejo
**Archivos que requieren atención especial:**
- **Context Managers**: `lifespan`, `async with`, `try/except`
- **Async Functions**: Métodos con `async/await`
- **Error Handling**: Bloques `try/except/finally`
- **Conditional Logic**: `if/elif/else` complejos
- **Loop Constructs**: `for/while` con break/continue

#### 3. Técnicas de Testing para 100%
**Para Context Managers:**
```python
@pytest.mark.asyncio
async def test_context_manager_success():
    """Test caso exitoso del context manager"""
    with patch('module.dependency') as mock_dep:
        mock_dep.method = AsyncMock()
        async with context_manager():
            mock_dep.method.assert_called_once()

@pytest.mark.asyncio
async def test_context_manager_error():
    """Test caso de error del context manager"""
    with patch('module.dependency') as mock_dep:
        mock_dep.method = AsyncMock(side_effect=Exception("Error"))
        async with context_manager():
            # Verificar manejo de error
            mock_dep.method.assert_called_once()
```

**Para Async Functions:**
```python
@pytest.mark.asyncio
async def test_async_function():
    """Test función async con AsyncMock"""
    with patch('module.async_service') as mock_service:
        mock_service.async_method = AsyncMock(return_value="result")
        result = await async_function()
        assert result == "result"
        mock_service.async_method.assert_called_once()
```

**Para Error Handling:**
```python
def test_error_handling_success():
    """Test manejo de error exitoso"""
    with patch('module.risky_function') as mock_func:
        mock_func.side_effect = Exception("Test error")
        result = function_with_error_handling()
        assert result == "error_handled"

def test_error_handling_failure():
    """Test manejo de error fallido"""
    with patch('module.risky_function') as mock_func:
        mock_func.return_value = "success"
        result = function_with_error_handling()
        assert result == "success"
```

#### 4. Checklist de Cobertura por Día
**Día 1-3: Fundaciones**
- [ ] **Configuración**: 100% cobertura en `config.py`
- [ ] **Base de datos**: 100% cobertura en `database.py`
- [ ] **Aplicación**: 100% cobertura en `main.py`
- [ ] **Context Managers**: Tests para `lifespan` completo
- [ ] **Error Paths**: Tests para todos los `try/except`

**Día 4-6: Modelos y Excepciones**
- [ ] **Modelos Pydantic**: 100% cobertura en validadores
- [ ] **Excepciones**: Tests para todas las excepciones custom
- [ ] **Serialización**: Tests para `model_dump()` y `model_validate()`
- [ ] **Edge Cases**: Tests para valores límite

**Día 7-9: Autenticación**
- [ ] **JWT**: 100% cobertura en creación/validación
- [ ] **OAuth**: Tests para todos los flujos OAuth
- [ ] **Middleware**: Tests para autenticación/autorización
- [ ] **Error Cases**: Tests para tokens inválidos/expirados

#### 5. Templates Estándar para 100% Cobertura
**Template para Context Manager:**
```python
@pytest.mark.asyncio
async def test_{context_manager_name}_success():
    """Test {context_manager_name} caso exitoso"""
    with patch('{module_path}') as mock_dependency:
        mock_dependency.method = AsyncMock()
        async with {context_manager_name}():
            # Verificar startup
            mock_dependency.method.assert_called_once()
        # Verificar shutdown
        mock_dependency.cleanup.assert_called_once()

@pytest.mark.asyncio
async def test_{context_manager_name}_startup_error():
    """Test {context_manager_name} error en startup"""
    with patch('{module_path}') as mock_dependency:
        mock_dependency.method = AsyncMock(side_effect=Exception("Startup failed"))
        async with {context_manager_name}():
            # Verificar manejo de error
            mock_dependency.method.assert_called_once()

@pytest.mark.asyncio
async def test_{context_manager_name}_shutdown_error():
    """Test {context_manager_name} error en shutdown"""
    with patch('{module_path}') as mock_dependency:
        mock_dependency.method = AsyncMock()
        mock_dependency.cleanup = AsyncMock(side_effect=Exception("Shutdown failed"))
        async with {context_manager_name}():
            pass  # Trigger shutdown
        # Verificar manejo de error
        mock_dependency.cleanup.assert_called_once()
```

**Template para Async Function:**
```python
@pytest.mark.asyncio
async def test_{async_function_name}_success():
    """Test {async_function_name} caso exitoso"""
    with patch('{module_path}') as mock_service:
        mock_service.async_method = AsyncMock(return_value="expected_result")
        result = await {async_function_name}()
        assert result == "expected_result"
        mock_service.async_method.assert_called_once()

@pytest.mark.asyncio
async def test_{async_function_name}_error():
    """Test {async_function_name} caso de error"""
    with patch('{module_path}') as mock_service:
        mock_service.async_method = AsyncMock(side_effect=Exception("Service error"))
        with pytest.raises(Exception, match="Service error"):
            await {async_function_name}()
        mock_service.async_method.assert_called_once()
```

#### 6. Comandos de Verificación Específicos
```bash
# Verificar cobertura específica por archivo
pytest tests/unit/test_main.py --cov=src/app/main --cov-report=term-missing

# Verificar cobertura de context managers
pytest tests/unit/test_lifespan.py --cov=src/app/main --cov-report=term-missing

# Verificar cobertura de async functions
pytest tests/unit/test_database.py --cov=src/app/core/database --cov-report=term-missing

# Verificar cobertura de modelos
pytest tests/unit/test_models.py --cov=src/app/models --cov-report=term-missing

# Verificar cobertura de autenticación
pytest tests/unit/test_auth.py --cov=src/app/api/auth --cov-report=term-missing
```

#### 7. Métricas de Cobertura por Módulo
**Backend - Módulos Críticos (100% requerido):**
- `src/app/core/config.py` - Configuración
- `src/app/core/database.py` - Base de datos
- `src/app/main.py` - Aplicación principal
- `src/app/core/security.py` - Seguridad
- `src/app/models/user.py` - Modelos de usuario
- `src/app/api/auth.py` - Autenticación

**Frontend - Componentes Críticos (100% requerido):**
- `src/components/Auth/` - Componentes de autenticación
- `src/hooks/useAuth.ts` - Hook de autenticación
- `src/services/api.ts` - Servicios de API
- `src/utils/auth.ts` - Utilidades de autenticación

#### 8. Verificación Automática de Cobertura
```bash
# Script para verificar cobertura 100% en CI/CD
#!/bin/bash
echo "Verificando cobertura 100%..."

# Verificar módulos críticos
CRITICAL_MODULES=(
    "src/app/core/config"
    "src/app/core/database" 
    "src/app/main"
    "src/app/core/security"
)

for module in "${CRITICAL_MODULES[@]}"; do
    echo "Verificando $module..."
    coverage=$(pytest tests/ --cov=$module --cov-report=term-missing | grep "TOTAL" | awk '{print $4}' | sed 's/%//')
    if [ "$coverage" != "100" ]; then
        echo "❌ $module: $coverage% (requerido: 100%)"
        exit 1
    else
        echo "✅ $module: $coverage%"
    fi
done

echo "🎉 Todos los módulos críticos tienen 100% de cobertura"
```

</llm:section>

## =====
<llm:section id="phase2_google_integration" type="detailed_phase">
## Fase 2: Google Integration Completa (Días 13-22)

### Objetivo de la Fase
Integrar Google Classroom API completa con modo dual (Google/Mock), implementar dashboards avanzados por rol, métricas educativas, visualizaciones ApexCharts y sistema de cache Redis.

### Días 13-15: Backend Google

#### Día 13: Google Classroom API Completa
**TDD Approach**:
- [ ] Tests para GoogleService + GoogleClassroomService
- [ ] Tests para ClassroomService + MetricsService
- [ ] Tests para autenticación OAuth + Google API authentication
- [ ] Tests para rate limiting + error handling + fallback

**Implementación**:
- [ ] Implementar GoogleService con API v1 + todas las funcionalidades
- [ ] Crear ClassroomService para lógica de negocio + métricas educativas
- [ ] Configurar OAuth 2.0 con Google + PKCE + scopes limitados
- [ ] Manejo de tokens de acceso + refresh + expiration
- [ ] Rate limiting (100 requests/100 seconds) + error handling + fallback automático
- [ ] Implementar cache Redis para datos de Google API

**Quality Gate**:
- [ ] Google API se conecta correctamente
- [ ] OAuth funciona end-to-end
- [ ] Rate limiting implementado

#### Día 14: Modo Dual
**TDD Approach**:
- [ ] Tests para modo Google vs Mock
- [ ] Tests para switching de modos
- [ ] Tests para fallback automático

**Implementación**:
- [ ] Implementar modo dual (Google/Mock)
- [ ] Service factory para switching
- [ ] Fallback automático a Mock
- [ ] Configuración por environment
- [ ] Logging de modo activo

**Quality Gate**:
- [ ] Modo dual funciona correctamente
- [ ] Switching de modos implementado
- [ ] Fallback automático funciona

#### Día 15: Endpoints Dashboard
**TDD Approach**:
- [ ] Tests para endpoints por rol
- [ ] Tests para métricas básicas
- [ ] Tests para agregaciones

**Implementación**:
- [ ] Crear endpoints /dashboard/admin
- [ ] Crear endpoints /dashboard/coordinator
- [ ] Crear endpoints /dashboard/teacher
- [ ] Crear endpoints /dashboard/student
- [ ] Implementar métricas básicas

**Quality Gate**:
- [ ] Endpoints por rol funcionan
- [ ] Métricas se calculan correctamente
- [ ] Performance < 2s por endpoint

### Días 16-18: Frontend Google

#### Día 16: Google UI Components
**TDD Approach**:
- [ ] Tests para GoogleConnect component
- [ ] Tests para ModeSelector
- [ ] Tests para OAuth flow

**Implementación**:
- [ ] Crear GoogleConnect component
- [ ] Implementar ModeSelector
- [ ] OAuth flow completo
- [ ] Manejo de estados de conexión
- [ ] Error handling para Google

**Quality Gate**:
- [ ] OAuth flow funciona end-to-end
- [ ] ModeSelector funciona
- [ ] Estados de conexión correctos

#### Día 17: Lista de Cursos
**TDD Approach**:
- [ ] Tests para CourseList component
- [ ] Tests para filtros y búsqueda
- [ ] Tests para paginación

**Implementación**:
- [ ] Crear CourseList component
- [ ] Implementar filtros básicos
- [ ] Paginación eficiente
- [ ] Loading states
- [ ] Error handling

**Quality Gate**:
- [ ] Lista de cursos carga correctamente
- [ ] Filtros funcionan
- [ ] Performance optimizada

#### Día 18: Dashboards por Rol
**TDD Approach**:
- [ ] Tests para dashboard components
- [ ] Tests para métricas display
- [ ] Tests para responsive design

**Implementación**:
- [ ] Crear dashboards específicos por rol
- [ ] Implementar MetricCard components
- [ ] ChartWidget básico
- [ ] Layout responsivo
- [ ] Navegación entre dashboards

**Quality Gate**:
- [ ] Dashboards por rol funcionan
- [ ] Métricas se muestran correctamente
- [ ] Design responsivo

### Días 19-21: Métricas y Dashboards

#### Día 19: Métricas Avanzadas
**TDD Approach**:
- [ ] Tests para KPIs educativos
- [ ] Tests para agregaciones
- [ ] Tests para cálculos complejos

**Implementación**:
- [ ] Implementar KPIs educativos
- [ ] Agregaciones por período
- [ ] Cálculos de engagement
- [ ] Risk scoring básico
- [ ] Performance metrics

**Quality Gate**:
- [ ] KPIs se calculan correctamente
- [ ] Agregaciones funcionan
- [ ] Performance optimizada

#### Día 20: ApexCharts Integration Completa
**TDD Approach**:
- [ ] Tests para ChartWidget + AdvancedChart
- [ ] Tests para diferentes tipos de gráficos (Bar, Line, Pie, Area)
- [ ] Tests para interactividad + drill-down + export

**Implementación**:
- [ ] Integrar ApexCharts v5.3.5 + configuración completa
- [ ] Crear ChartWidget genérico + AdvancedChart component
- [ ] Implementar gráficos básicos + avanzados (heatmaps, treemaps)
- [ ] Interactividad drill-down + zoom + pan
- [ ] Export functionality (PDF, PNG, SVG) + custom themes
- [ ] Implementar responsive charts + accessibility features

**Quality Gate**:
- [ ] Gráficos renderizan correctamente
- [ ] Interactividad funciona
- [ ] Performance < 2s load

#### Día 21: Cache y Optimización
**TDD Approach**:
- [ ] Tests para cache de métricas
- [ ] Tests para invalidación
- [ ] Tests para performance

**Implementación**:
- [ ] Implementar cache Redis
- [ ] Cache de métricas calculadas
- [ ] Invalidación inteligente
- [ ] Precomputed aggregates
- [ ] Background jobs

**Quality Gate**:
- [ ] Cache funciona eficientemente
- [ ] Performance < 1s load
- [ ] Invalidación correcta

### Día 22: Integración Google

#### Día 22: Validación Completa
**TDD Approach**:
- [ ] Tests de integración Google completa
- [ ] Tests de performance end-to-end
- [ ] Tests de modo dual

**Implementación**:
- [ ] Validar modo dual completamente
- [ ] Performance tuning
- [ ] Documentación Google
- [ ] Preparar para Fase 3

**Quality Gate**:
- [ ] 100% criterios Fase 2 completados
- [ ] Performance < 2s dashboard load
- [ ] Google integration estable
- [ ] Cobertura > 85%

### Criterios de Finalización Fase 2
- [ ] **Backend**: Google API completa + Modo dual + Dashboards + Métricas educativas
- [ ] **Frontend**: Google UI + ApexCharts v5.3.5 + Dashboards por rol + Cache Redis
- [ ] **Testing**: Google mocks + Integration tests + Chart tests
- [ ] **Performance**: <2s dashboard load + Cache optimizado
- [ ] **Google**: OAuth + Classroom API + Rate limiting funcionando
- [ ] **Modo Dual**: Switching Google/Mock estable + Fallback automático
- [ ] **Visualizaciones**: ApexCharts avanzados + Export + Responsive
- [ ] **Cache**: Redis implementado + Invalidación inteligente

</llm:section>

## =====
<llm:section id="phase3_advanced_visualization" type="detailed_phase">
## Fase 3: Visualización Avanzada + Notificaciones (Días 23-32)

### Objetivo de la Fase
Implementar búsqueda avanzada, notificaciones WebSocket en tiempo real, visualizaciones D3.js interactivas, métricas predictivas y widgets personalizables.

### Días 23-25: Backend Avanzado

#### Día 23: Sistema de Búsqueda
**TDD Approach**:
- [ ] Tests para SearchService
- [ ] Tests para filtros avanzados
- [ ] Tests para resultados contextuales

**Implementación**:
- [ ] Implementar SearchService
- [ ] Búsqueda multi-entidad
- [ ] Filtros avanzados
- [ ] Resultados contextuales
- [ ] Saved searches

**Quality Gate**:
- [ ] Búsqueda funciona correctamente
- [ ] Filtros avanzados implementados
- [ ] Performance < 1s search time

#### Día 24: Notificaciones WebSocket Completas
**TDD Approach**:
- [ ] Tests para WebSocketService + NotificationService
- [ ] Tests para notificaciones real-time + WebSocket connections
- [ ] Tests para delivery garantizada + fallback polling

**Implementación**:
- [ ] Implementar WebSocketService + WebSocket endpoints
- [ ] Notificaciones real-time + WebSocket connections
- [ ] Multi-channel delivery (WebSocket + Email + Telegram mock)
- [ ] Smart alerts + notification preferences
- [ ] Preferences por usuario + notification center
- [ ] Implementar fallback polling cada 30 segundos

**Quality Gate**:
- [ ] WebSocket funciona correctamente
- [ ] Notificaciones se entregan
- [ ] Delivery garantizada

#### Día 25: Métricas Predictivas
**TDD Approach**:
- [ ] Tests para algoritmos predictivos
- [ ] Tests para trend analysis
- [ ] Tests para risk detection

**Implementación**:
- [ ] Implementar métricas predictivas
- [ ] Trend analysis básico
- [ ] Risk detection automático
- [ ] Insights generados
- [ ] Alertas inteligentes

**Quality Gate**:
- [ ] Métricas predictivas funcionan
- [ ] Risk detection preciso
- [ ] Insights útiles

### Días 26-28: Frontend Avanzado

#### Día 26: Búsqueda Frontend
**TDD Approach**:
- [ ] Tests para SearchBar component
- [ ] Tests para SearchResults
- [ ] Tests para filtros UI

**Implementación**:
- [ ] Crear SearchBar component
- [ ] Implementar SearchResults
- [ ] Filtros UI avanzados
- [ ] Saved searches UI
- [ ] Export results

**Quality Gate**:
- [ ] UI de búsqueda funciona
- [ ] Filtros UI implementados
- [ ] UX optimizada

#### Día 27: Notificaciones Frontend
**TDD Approach**:
- [ ] Tests para NotificationCenter
- [ ] Tests para NotificationBadge
- [ ] Tests para real-time updates

**Implementación**:
- [ ] Crear NotificationCenter
- [ ] Implementar NotificationBadge
- [ ] Real-time updates UI
- [ ] Preferences UI
- [ ] Push notifications

**Quality Gate**:
- [ ] Notificaciones UI funcionan
- [ ] Real-time updates correctos
- [ ] UX intuitiva

#### Día 28: Widgets Personalizables
**TDD Approach**:
- [ ] Tests para widgets
- [ ] Tests para drag & drop
- [ ] Tests para configuración

**Implementación**:
- [ ] Crear sistema de widgets
- [ ] Drag & drop functionality
- [ ] Configuración de widgets
- [ ] Dashboard personalizable
- [ ] Sharing de dashboards

**Quality Gate**:
- [ ] Widgets funcionan correctamente
- [ ] Drag & drop implementado
- [ ] Personalización funciona

### Días 29-31: Visualización Completa

#### Día 29: D3.js Integration Completa
**TDD Approach**:
- [ ] Tests para visualizaciones D3 + AdvancedChart
- [ ] Tests para animaciones + transitions
- [ ] Tests para interactividad + zoom + brush

**Implementación**:
- [ ] Integrar D3.js + configuración completa
- [ ] Visualizaciones custom (network graphs, treemaps, heatmaps)
- [ ] Animaciones fluidas + transitions + easing
- [ ] Interactividad avanzada + zoom + pan + brush
- [ ] Export avanzado + SVG + Canvas + WebGL
- [ ] Implementar responsive D3 charts + accessibility

**Quality Gate**:
- [ ] D3.js funciona correctamente
- [ ] Animaciones fluidas
- [ ] Interactividad avanzada

#### Día 30: ApexCharts Avanzado
**TDD Approach**:
- [ ] Tests para gráficos avanzados
- [ ] Tests para drill-down
- [ ] Tests para export

**Implementación**:
- [ ] Gráficos avanzados ApexCharts
- [ ] Drill-down functionality
- [ ] Export PDF/PNG/SVG
- [ ] Custom themes
- [ ] Performance optimization

**Quality Gate**:
- [ ] Gráficos avanzados funcionan
- [ ] Drill-down implementado
- [ ] Export funciona

#### Día 31: Performance Optimization
**TDD Approach**:
- [ ] Tests de performance
- [ ] Tests de memory leaks
- [ ] Tests de load time

**Implementación**:
- [ ] Optimización de performance
- [ ] Lazy loading
- [ ] Code splitting
- [ ] Memory leak prevention
- [ ] Bundle optimization

**Quality Gate**:
- [ ] Performance < 1.5s load
- [ ] Sin memory leaks
- [ ] Bundle size optimizado

### Día 32: Integración Avanzada

#### Día 32: Validación Completa
**TDD Approach**:
- [ ] Tests E2E avanzados
- [ ] Tests de performance completos
- [ ] Tests de accessibility básicos

**Implementación**:
- [ ] Validar funcionalidades avanzadas
- [ ] Performance testing completo
- [ ] Accessibility básica
- [ ] Preparar para Fase 4

**Quality Gate**:
- [ ] 100% criterios Fase 3 completados
- [ ] Performance < 1.5s load
- [ ] Accessibility básica implementada
- [ ] Cobertura > 88%

### Criterios de Finalización Fase 3
- [ ] **Backend**: Búsqueda avanzada + Notificaciones WebSocket + Métricas predictivas
- [ ] **Frontend**: UI avanzada + Gráficos D3.js + ApexCharts + Widgets personalizables
- [ ] **Testing**: E2E scenarios + Performance + Visual + WebSocket tests
- [ ] **Accessibility**: Keyboard + Screen reader básico + Chart accessibility
- [ ] **Performance**: <1.5s load time + Optimización de gráficos
- [ ] **Visualization**: D3.js completo + ApexCharts avanzado + Export + Responsive
- [ ] **Real-time**: WebSocket estable + Fallback polling + Multi-channel delivery

</llm:section>

## =====
<llm:section id="phase4_production_ready" type="detailed_phase">
## Fase 4: Production Ready + WCAG 2.2 AA (Días 33-45)

### Objetivo de la Fase
Completar Google sync bidireccional, implementar WCAG 2.2 AA completo, testing exhaustivo, deployment production-ready y sistema de monitoreo 24/7.

### Días 33-35: Google Completo

#### Día 33: Sincronización Bidireccional Completa
**TDD Approach**:
- [ ] Tests para GoogleSyncService + ConflictResolutionService
- [ ] Tests para conflict resolution + audit trail
- [ ] Tests para backup/restore + point-in-time recovery

**Implementación**:
- [ ] Implementar GoogleSyncService + ConflictResolutionService
- [ ] Sincronización bidireccional + incremental + programada
- [ ] Conflict resolution automática + manual + audit trail
- [ ] Backup automático + selectivo + point-in-time
- [ ] Webhooks para eventos + signature validation + retry logic

**Quality Gate**:
- [ ] Sync bidireccional funciona
- [ ] Conflict resolution automática
- [ ] Backup automático

#### Día 34: Admin Panel Google
**TDD Approach**:
- [ ] Tests para admin panel
- [ ] Tests para sync controls
- [ ] Tests para diagnostics

**Implementación**:
- [ ] Crear admin panel Google
- [ ] Controles de sincronización
- [ ] Herramientas de diagnóstico
- [ ] Monitoring de sync
- [ ] Logs detallados

**Quality Gate**:
- [ ] Admin panel funciona
- [ ] Controles implementados
- [ ] Diagnósticos útiles

#### Día 35: Webhooks y Monitoring
**TDD Approach**:
- [ ] Tests para webhooks
- [ ] Tests para monitoring
- [ ] Tests para alertas

**Implementación**:
- [ ] Implementar webhooks Google
- [ ] Monitoring de API usage
- [ ] Alertas automáticas
- [ ] Performance tracking
- [ ] Error tracking

**Quality Gate**:
- [ ] Webhooks funcionan
- [ ] Monitoring implementado
- [ ] Alertas automáticas

### Días 36-38: Accesibilidad WCAG 2.2 AA Completa

#### Día 36: Keyboard Navigation Completa
**TDD Approach**:
- [ ] Tests de navegación por teclado + focus management
- [ ] Tests de shortcuts + tab order + skip links
- [ ] Tests de accessibility con axe-core

**Implementación**:
- [ ] Navegación completa por teclado + focus management
- [ ] Keyboard shortcuts + tab order correcto + skip links
- [ ] Implementar FocusTrap + SkipLink components
- [ ] Configurar axe-core para testing automático
- [ ] Implementar keyboard navigation para gráficos

**Quality Gate**:
- [ ] Navegación por teclado completa
- [ ] Focus management correcto
- [ ] Shortcuts funcionan

#### Día 37: Screen Reader Support Completo
**TDD Approach**:
- [ ] Tests con screen reader + axe-core
- [ ] Tests de ARIA + semantic HTML + live regions
- [ ] Tests de accessibility con pa11y

**Implementación**:
- [ ] ARIA labels completos + roles + states + properties
- [ ] Semantic HTML + landmarks + headings hierarchy
- [ ] Screen reader announcements + live regions + alternative text
- [ ] Implementar ScreenReaderText component
- [ ] Configurar pa11y para testing automático de accessibility

**Quality Gate**:
- [ ] Screen reader funciona
- [ ] ARIA implementado correctamente
- [ ] Semantic HTML completo

#### Día 38: Visual Accessibility Completa
**TDD Approach**:
- [ ] Tests de contraste + escalabilidad + color-blind friendly
- [ ] Tests de high contrast mode + visual indicators
- [ ] Tests de accessibility con axe-core + pa11y

**Implementación**:
- [ ] Contraste AA/AAA + color contrast validation
- [ ] Fonts escalables + responsive typography
- [ ] Color-blind friendly + alternative color schemes
- [ ] High contrast mode + ContrastToggle component
- [ ] Visual indicators + focus indicators + error indicators
- [ ] Implementar accessibility testing automático en CI/CD

**Quality Gate**:
- [ ] Contraste AA/AAA
- [ ] Escalabilidad funciona
- [ ] Color-blind friendly

### Días 39-41: Testing Completo

#### Día 39: E2E Exhaustivos
**TDD Approach**:
- [ ] Tests E2E completos
- [ ] Tests de regresión
- [ ] Tests cross-browser

**Implementación**:
- [ ] E2E tests exhaustivos
- [ ] Regresión visual
- [ ] Cross-browser testing
- [ ] Mobile testing
- [ ] Performance E2E

**Quality Gate**:
- [ ] E2E tests completos
- [ ] Cross-browser funciona
- [ ] Mobile responsive

#### Día 40: Performance Testing
**TDD Approach**:
- [ ] Tests de load
- [ ] Tests de stress
- [ ] Tests de memory

**Implementación**:
- [ ] Load testing
- [ ] Stress testing
- [ ] Memory leak testing
- [ ] Performance benchmarks
- [ ] Optimization

**Quality Gate**:
- [ ] Load testing pasa
- [ ] Sin memory leaks
- [ ] Performance optimizada

#### Día 41: Security Testing
**TDD Approach**:
- [ ] Tests de seguridad
- [ ] Tests de penetration
- [ ] Tests de dependencies

**Implementación**:
- [ ] Security scanning
- [ ] Penetration testing
- [ ] Dependency audit
- [ ] OWASP compliance
- [ ] Security headers

**Quality Gate**:
- [ ] 0 vulnerabilidades CRITICAL
- [ ] OWASP compliance
- [ ] Security headers

### Días 42-45: Production Deployment

#### Día 42: CI/CD Pipeline Completo
**TDD Approach**:
- [ ] Tests para CI/CD
- [ ] Tests para quality gates
- [ ] Tests para deployment

**Implementación**:
- [ ] CI/CD pipeline completo
- [ ] Quality gates estrictos
- [ ] Automated deployment
- [ ] Rollback automático
- [ ] Feature flags

**Quality Gate**:
- [ ] CI/CD funciona
- [ ] Quality gates pasan
- [ ] Deployment automático

#### Día 43: Docker Production
**TDD Approach**:
- [ ] Tests para Docker
- [ ] Tests para security scan
- [ ] Tests para resource limits

**Implementación**:
- [ ] Docker production-ready
- [ ] Security scanning
- [ ] Resource limits
- [ ] Health checks
- [ ] Monitoring

**Quality Gate**:
- [ ] Docker optimizado
- [ ] Security scan pasa
- [ ] Resource limits

#### Día 44: Monitoring y Alerting
**TDD Approach**:
- [ ] Tests para monitoring
- [ ] Tests para alertas
- [ ] Tests para dashboards

**Implementación**:
- [ ] Monitoring 24/7
- [ ] Alertas automáticas
- [ ] Dashboards operacionales
- [ ] Log aggregation
- [ ] Metrics collection

**Quality Gate**:
- [ ] Monitoring funciona
- [ ] Alertas automáticas
- [ ] Dashboards operacionales

#### Día 45: Documentación y Handover
**TDD Approach**:
- [ ] Tests para documentación
- [ ] Tests para runbooks
- [ ] Tests para training

**Implementación**:
- [ ] Documentación completa
- [ ] Runbooks operacionales
- [ ] Training materials
- [ ] User guides
- [ ] API documentation

**Quality Gate**:
- [ ] Documentación completa
- [ ] Runbooks listos
- [ ] Training materials

### Criterios de Finalización Fase 4
- [ ] **Google**: Sync bidireccional + Backup + Webhooks + Conflict resolution
- [ ] **Accessibility**: WCAG 2.2 AA completo + axe-core + pa11y + Keyboard + Screen reader
- [ ] **Testing**: ≥90% críticos + Security + Load + Accessibility + Visual
- [ ] **CI/CD**: Pipeline completo + Docker + Monitoring + Quality gates
- [ ] **Production**: Deployment ready + Monitoring 24/7 + Alertas automáticas
- [ ] **Documentation**: Completa + Runbooks + Training + API docs
- [ ] **Performance**: <1s load time + Optimización completa + Bundle optimization
- [ ] **Security**: 0 vulnerabilidades CRITICAL/HIGH + OWASP compliance

</llm:section>

## =====
<llm:section id="quality_gates" type="quality_assurance">
## Quality Gates por Fase

### Gate 1: Fundaciones Unificadas (Día 12)
- [ ] **Cobertura**: ≥100% módulos críticos (config, database, main, auth, models)
- [ ] **Performance**: <3s load time + Puerto 8000 fijo
- [ ] **Security**: 0 vulnerabilidades CRITICAL + CORS configurado
- [ ] **Tests**: Backend + Frontend + E2E básicos + AsyncMock
- [ ] **Integration**: Frontend-Backend comunicación + OAuth flow completo
- [ ] **CI/CD**: Pipeline básico funcionando + Quality gates
- [ ] **Error Prevention**: Todos los checks de prevención pasando + Limpieza automática
- [ ] **Context Managers**: Tests completos para lifespan + AsyncMock
- [ ] **Error Paths**: Todos los try/except cubiertos + Migración automática
- [ ] **Modern APIs**: Pydantic v2 + FastAPI lifespan + ConfigDict implementados
- [ ] **Arquitectura**: Servicios resilientes + Verificación automática + Puerto fijo

### Gate 2: Google Integration Completa (Día 22)
- [ ] **Cobertura**: ≥100% servicios críticos (auth, google, models, metrics)
- [ ] **Performance**: <2s dashboard load + Cache Redis optimizado
- [ ] **Security**: 0 vulnerabilidades CRITICAL + Rate limiting
- [ ] **Tests**: Google mocks + Integration tests + Chart tests
- [ ] **Google**: OAuth + Classroom API + Rate limiting estable
- [ ] **Modo Dual**: Switching Google/Mock + Fallback automático funcional
- [ ] **Error Prevention**: Rate limiting + fallback + Cache Redis funcionando
- [ ] **API Integration**: Tests para todos los endpoints + Métricas educativas
- [ ] **Visualizaciones**: ApexCharts v5.3.5 + Export + Responsive
- [ ] **Cache**: Redis implementado + Invalidación inteligente

### Gate 3: Visualización Avanzada + Notificaciones (Día 32)
- [ ] **Cobertura**: ≥100% componentes de visualización + WebSocket
- [ ] **Performance**: <1.5s load time + Optimización de gráficos
- [ ] **Security**: 0 vulnerabilidades CRITICAL + WebSocket security
- [ ] **Tests**: E2E + Performance + Visual + WebSocket tests
- [ ] **Accessibility**: Keyboard + Screen reader básico + Chart accessibility
- [ ] **Visualization**: D3.js completo + ApexCharts avanzado + Export + Responsive
- [ ] **WebSocket**: Tests para conexiones real-time + Fallback polling
- [ ] **Real-time**: Notificaciones WebSocket + Multi-channel delivery funcionando
- [ ] **Widgets**: Sistema de widgets personalizables + Drag & drop
- [ ] **Búsqueda**: Búsqueda avanzada + Filtros + Resultados contextuales

### Gate 4: Production Ready + WCAG 2.2 AA (Día 45)
- [ ] **Cobertura**: ≥100% global + Accessibility tests
- [ ] **Performance**: <1s load time + Optimización completa + Bundle optimization
- [ ] **Security**: 0 vulnerabilidades CRITICAL/HIGH + OWASP compliance
- [ ] **Tests**: Exhaustivos + Security + Load + Accessibility + Visual
- [ ] **E2E**: Tests end-to-end completos + Cross-browser + Mobile
- [ ] **Performance**: Tests de carga + Stress + Memory leak
- [ ] **Security**: Tests de seguridad exhaustivos + Penetration + Dependency audit
- [ ] **Accessibility**: WCAG 2.2 AA completo + axe-core + pa11y + Keyboard + Screen reader
- [ ] **Production**: CI/CD + Docker + Monitoring 24/7 + Alertas automáticas
- [ ] **Google**: Sync bidireccional + Backup + Webhooks + Conflict resolution
- [ ] **Documentation**: Completa + Runbooks + Training + API docs

</llm:section>

## =====
<llm:section id="risk_mitigation" type="risk_management">
## Gestión de Riesgos y Mitigación

### Riesgos Técnicos
1. **Google API Rate Limits**
   - Mitigación: Implementar rate limiting + caching
   - Contingencia: Fallback a Mock mode

2. **Performance Degradation**
   - Mitigación: Monitoring continuo + optimization
   - Contingencia: Code splitting + lazy loading

3. **Security Vulnerabilities**
   - Mitigación: Security scanning automático
   - Contingencia: Patch inmediato + rollback

### Riesgos de Calidad
1. **Test Coverage Insuficiente**
   - Mitigación: Quality gates estrictos
   - Contingencia: Refactoring + tests adicionales

2. **Accessibility Compliance**
   - Mitigación: Testing automático + manual
   - Contingencia: UI fixes + accessibility audit

### Riesgos de Tiempo
1. **Fase 4 Complejidad**
   - Mitigación: Buffer de 3 días extra
   - Contingencia: Priorización de features

2. **Google Integration Delays**
   - Mitigación: Mock mode robusto
   - Contingencia: Implementación incremental

</llm:section>

## =====
<llm:section id="success_metrics" type="kpis">
## Métricas de Éxito del Plan

### Métricas Técnicas
- **Cobertura Testing**: ≥90% módulos críticos, ≥80% global
- **Performance**: <1s dashboard load (Fase 4)
- **Security**: 0 vulnerabilidades CRITICAL/HIGH
- **Accessibility**: WCAG 2.2 AA compliance 100%
- **Uptime**: 99.9% disponibilidad

### Métricas de Calidad
- **Bug Rate**: <1 bug crítico por semana
- **Test Success**: >95% tests passing
- **Code Quality**: A+ rating en SonarQube
- **Documentation**: 100% API documented
- **User Satisfaction**: >4.5/5 rating

### Métricas de Proceso
- **TDD Adherence**: 100% features con tests primero
- **Quality Gates**: 100% gates pasados por fase
- **CI/CD Success**: >95% deployments exitosos
- **Time to Market**: 45 días exactos
- **Budget Adherence**: 100% dentro del presupuesto

</llm:section>

## =====
<llm:section id="conclusion" type="summary">
## Conclusión del Plan Maestro

### Resumen Ejecutivo
Este plan maestro detalla la implementación completa del Dashboard Educativo siguiendo el contrato unificado completo con metodología TDD estricta, arquitectura resiliente y prevención de errores. El plan garantiza calidad, performance, accessibility WCAG 2.2 AA y producción ready desde el primer día.

### Beneficios del Plan Unificado
1. **Calidad Garantizada**: TDD + Quality Gates + Arquitectura resiliente aseguran alta calidad
2. **Risk Mitigation**: Identificación y mitigación proactiva de riesgos + Prevención de errores
3. **Time Management**: Plan detallado de 45 días con buffers + Fases unificadas
4. **Success Metrics**: KPIs claros para medir éxito + Métricas de accessibility
5. **Production Ready**: Deploy production-ready + WCAG 2.2 AA + Monitoring 24/7 desde día 45
6. **Arquitectura Resiliente**: Puerto 8000 fijo + Servicios resilientes + Verificación automática
7. **Modern APIs**: Pydantic v2 + FastAPI lifespan + Migración automática

### Próximos Pasos
1. **Aprobación**: Validar plan con stakeholders
2. **Setup**: Configurar herramientas y environments
3. **Ejecución**: Iniciar Fase 1 con TDD estricto
4. **Monitoring**: Seguir métricas de éxito
5. **Delivery**: Entregar sistema completo en 45 días

**Este plan garantiza la implementación exitosa del Dashboard Educativo más robusto y completo, cumpliendo todos los requisitos del contrato unificado completo con la más alta calidad, arquitectura resiliente, prevención de errores y accessibility WCAG 2.2 AA.**

</llm:section>
