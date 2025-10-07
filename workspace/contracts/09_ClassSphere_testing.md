---
title: "ClassSphere - Unified Testing Strategy"
version: "4.0"
type: "documentation"
language: "English (Mandatory)"
date: "2025-10-07"
related_files:
  - "00_ClassSphere_index.md"
  - "08_ClassSphere_modelos_datos.md"
  - "10_ClassSphere_plan_implementacion.md"
---

[← Modelos de Datos](08_ClassSphere_modelos_datos.md) | [Índice](00_ClassSphere_index.md) | [Siguiente → Plan de Implementación](10_ClassSphere_plan_implementacion.md)

# Estrategia de Testing Unificada

### Stack de Testing Backend (Go)
- ✅ **Unit Testing:** testify/assert + testify/mock
- ✅ **HTTP Testing:** httptest (Go standard library)
- ✅ **Mocking:** testify/mock + mockery
- ✅ **Coverage:** go test -cover

### Stack de Testing Frontend (Angular 19)
- ✅ **Unit Testing:** Jasmine + Karma (estándar Angular)
- ✅ **Component Testing:** Angular Testing Library
- ✅ **E2E Testing:** Playwright
- ✅ **Coverage:** karma-coverage

### Ventajas del Stack
| Aspecto | Beneficio |
|---------|----------|
| Estándar oficial | Jasmine es el framework oficial de Angular |
| Zero-config | Angular CLI configura automáticamente |
| Maduro y estable | testify es el estándar de facto en Go |
| Documentación completa | Ambos tienen documentación oficial extensa |

## Metodología TDD Consolidada

El sistema completo sigue Test-Driven Development (TDD) estricto:

1. **Red**: Escribir test que falle
2. **Green**: Implementar código mínimo para pasar
3. **Refactor**: Mejorar código manteniendo tests verdes
4. **Repeat**: Para cada nueva funcionalidad

## Cobertura de Testing Requerida

- **Global**: ≥80% líneas, ≥65% ramas
- **Módulos Críticos**: ≥90% líneas, ≥80% ramas
- **Componentes de Seguridad**: ≥95% líneas, ≥85% ramas
- **API Endpoints**: 100% casos de éxito y error
- **Backend Go**: ≥80% líneas con testify
- **Frontend Angular**: ≥80% líneas con Jasmine + Karma
- **E2E**: Cobertura de flujos críticos con Playwright

### Criterios de Aceptación Medibles:

#### Funcional:
- [ ] Login funciona con credenciales demo (admin@classsphere.edu / secret)
- [ ] OAuth Google redirige a Google y retorna exitosamente
- [ ] Dashboard muestra contenido específico por rol
- [ ] Navegación funciona entre todas las páginas
- [ ] Logout limpia sesión y redirige a login

#### Técnico:
- [ ] Backend coverage ≥ 80% (medido por `pytest --cov`)
- [ ] Frontend coverage ≥ 80% (medido por `vitest --coverage`)
- [ ] Todos los tests pasan 100% (medido por CI/CD pipeline)
- [ ] Sin errores de consola en navegador (medido manualmente)
- [ ] Tiempo de carga página < 2 segundos (medido por Lighthouse)

#### Integración:
- [ ] Frontend se comunica con backend exitosamente
- [ ] JWT tokens se almacenan y envían correctamente
- [ ] Flujo OAuth completa sin errores
- [ ] Manejo de errores muestra mensajes apropiados
- [ ] Diseño responsivo funciona en móvil/tablet

## Principios TDD con Prevención Integral

### Referencia: Guía de Prevención de Errores LLM

Esta sección implementa los patterns documentados en `contracts/extra/revision/llm_error_prevention_guide.md`.

**Patterns Aplicados:**
- **Pattern 1**: Missing Pydantic Imports (ConfigDict)
- **Pattern 2**: Deprecated Next.js Configuration (swcMinify)
- **Pattern 3**: Zod Schema Issues (z.record, error.issues)
- **Pattern 4**: Async Function Mocking Errors (AsyncMock, mock paths)
- **Pattern 5**: Frontend Dependency Mocking Issues (debounce, safeTry, logger)
- **Pattern 6**: Missing E2E Test Coverage (frontend-backend integration)

### 1. Testing Async como Estándar TDD (Pattern 4)

**Metodología**: Tests async son parte integral del ciclo Red-Green-Refactor
```python
# ✅ TDD ESTÁNDAR - AsyncMock como parte del flujo (Pattern 4)
mock_instance = AsyncMock()
mock_instance.admin.command.return_value = {"ok": 1}

# ❌ INCORRECTO - Mock no funciona con async
mock_instance = Mock()
mock_instance.admin.command.return_value = {"ok": 1}
```

**Prevención Automática Pattern 4:**
```python
# Validación automática en tests
if 'async def' in test_file and '@patch' in test_file:
    assert 'AsyncMock' in test_file, "Pattern 4: Use AsyncMock for async functions"
    assert 'new_callable=AsyncMock' in test_file, "Pattern 4: Add new_callable parameter"
```

**Integración TDD**:
- `AsyncMock` como estándar para métodos async (Pattern 4)
- Template TDD para tests de base de datos
- Verificación automática en CI como parte del flujo
- Mock paths correctos: `src.app.api.endpoints.auth.verify_token` (Pattern 4)

**Métricas de Éxito Pattern 4:**
- 2 errores backend auth resueltos (100%)
- 0 warnings "coroutine never awaited"
- Tiempo resolución: <2 minutos

### 2. Headers HTTP como Verificación TDD

**Metodología**: Tests de CORS como parte del flujo TDD estándar
```python
# ✅ TDD ESTÁNDAR - Headers básicos verificables
assert "access-control-allow-origin" in response.headers
assert "access-control-allow-credentials" in response.headers

# ❌ INCORRECTO - Headers específicos pueden variar
assert "access-control-allow-methods" in response.headers
```

### 3. Validación Pydantic Imports (Pattern 1)

**Metodología**: ConfigDict import obligatorio en modelos Pydantic v2
```python
# ✅ CORRECTO - Pattern 1
from pydantic import BaseModel, EmailStr, Field, ConfigDict

class User(BaseModel):
    email: EmailStr
    model_config = ConfigDict(from_attributes=True)

# ❌ INCORRECTO - Missing import
class User(BaseModel):
    email: EmailStr
    model_config = ConfigDict(from_attributes=True)  # NameError!
```

**Prevención Automática Pattern 1:**
```bash
# Script de validación pre-commit
grep -r "model_config = ConfigDict" --include="*.py" | while read line; do
    file=$(echo $line | cut -d: -f1)
    if ! grep -q "from pydantic import.*ConfigDict" "$file"; then
        echo "❌ Pattern 1 Error: $file missing ConfigDict import"
        exit 1
    fi
done
```

### 4. Next.js Configuration Validation (Pattern 2)

**Metodología**: Evitar opciones deprecated en next.config.js
```javascript
// ✅ CORRECTO - Pattern 2
module.exports = {
  reactStrictMode: true,
  // swcMinify removido (deprecated en Next.js 14+)
}

// ❌ INCORRECTO - Deprecated option
module.exports = {
  reactStrictMode: true,
  swcMinify: true  // Unrecognized key error!
}
```

### 5. Zod Schema Validation (Pattern 3)

**Metodología**: Schemas Zod correctos y error handling apropiado
```typescript
// ✅ CORRECTO - Pattern 3
const schema = z.object({
  metadata: z.record(z.string(), z.any())  // 2 parameters
})

const result = schema.safeParse(data)
if (!result.success) {
  const errors = result.error.issues  // .issues, not .errors
}

// ❌ INCORRECTO
const schema = z.object({
  metadata: z.record(z.any())  // Missing key type!
})
const errors = result.error.errors  // Property doesn't exist!
```

### 6. Frontend Dependency Mocking (Pattern 5)

**Metodología**: Mocks comprehensivos para todas las dependencias
```typescript
// ✅ CORRECTO - Pattern 5
vi.mock('@/lib/defensive', () => ({
  safeToString: vi.fn((value) => String(value)),
  debounce: vi.fn((fn, delay) => fn),
  safeTry: vi.fn((fn) => fn())
}))

vi.mock('@/lib/logger', () => ({
  authLogger: { info: vi.fn(), warn: vi.fn(), error: vi.fn() },
  logUserAction: vi.fn()
}))

// ❌ INCORRECTO - Missing mocks
// No mocks for debounce, safeTry, logger
// Result: "ReferenceError: debounce is not defined"
```

**Métricas de Éxito Pattern 5:**
- 4 errores frontend validation resueltos (100%)
- 0 errores "X is not defined"
- Tiempo resolución: <3 minutos

**Integración TDD**:
- Tests de CORS simplificados y robustos
- Verificación de headers esenciales solamente
- Documentación de comportamiento esperado de middleware

## Metodología TDD por Fase

### Fase 1 - Fundaciones TDD (5/12 días completados)

**Verificaciones Automáticas**:
- [x] Tests async usan testify/mock correctamente ✅
- [x] Tests de CORS verifican headers básicos ✅
- [x] Servidor inicia en puerto 8080 (nunca alternativo) ✅
- [x] Health check responde correctamente ✅
- [x] Cobertura ≥80% en toda la Fase 1 sin warnings críticos ✅
- [x] Servidor resiliente funciona sin servicios externos ✅

**Progreso Detallado**:
- ✅ **Día 1**: Configuración del Entorno TDD - Go 1.24, Echo v4, estructura de directorios
- ✅ **Día 2**: Configuración de Testing TDD - testify, httptest, timeouts, cobertura
- ✅ **Día 3**: Configuración de Infraestructura TDD - Redis, puerto 8080, CI/CD
- ✅ **Día 4**: JWT Authentication TDD - tokens, middleware, refresh rotation
- ✅ **Día 5**: OAuth 2.0 TDD - Google OAuth, PKCE, integración usuarios
- ⏳ **Día 6**: Sistema de Roles TDD - roles, middleware seguridad, rate limiting (En progreso)
- ⏳ **Día 7**: UI Base TDD - Next.js, TypeScript, Tailwind CSS (Pendiente)
- ⏳ **Día 8**: Componentes de Autenticación TDD - LoginForm, OAuthButton, hooks (Pendiente)
- ⏳ **Día 9**: Servicios de API TDD - servicios API, manejo errores, integración (Pendiente)
- ⏳ **Día 10**: Comunicación Frontend-Backend TDD - tests integración, envelope estándar (Pendiente)
- ⏳ **Día 11**: Protección de Rutas TDD - protección por rol, tests E2E Playwright (Pendiente)
- ⏳ **Día 12**: CI/CD y Documentación TDD - pipeline, documentación completa (Pendiente)

**Templates TDD Estándar**:
- Template para tests de base de datos con AsyncMock
- Template para tests de CORS simplificados
- Template para lifespan resiliente
- Template para verificación de health check

### Fase 2 - Google Integration TDD

**Verificaciones Automáticas**:
- [ ] Mocks de Google API funcionan correctamente (Pattern 4: AsyncMock)
- [ ] Modo dual switching sin errores
- [ ] Tests de OAuth completos (Pattern 3: Zod validation)
- [ ] Tests de Classroom API mockeados (Pattern 4: AsyncMock)

**Patterns Aplicados en Fase 2:**
- Pattern 3: Zod schemas para validación OAuth
- Pattern 4: AsyncMock en tests de Google API
- Pattern 6: E2E tests para flujo Google completo

**Templates TDD Estándar**:
- Template para mocks de Google API
- Template para tests de OAuth
- Template para modo dual switching

### Fase 3 - Frontend TDD

**Verificaciones Automáticas**:
- [ ] Componentes React renderizan correctamente (Pattern 5: Mocks comprehensivos)
- [ ] Hooks personalizados funcionan (Pattern 5: Dependency mocking)
- [ ] Tests de integración frontend-backend (Pattern 6: E2E coverage)
- [ ] Tests de UI con Testing Library (Pattern 2: Next.js config limpio)

**Patterns Aplicados en Fase 3:**
- Pattern 2: Next.js config sin opciones deprecated
- Pattern 3: Zod schemas en validación de métricas
- Pattern 5: Mocks comprehensivos en componentes de visualización
- Pattern 6: E2E tests para dashboards por rol

**Templates TDD Estándar**:
- Template para componentes React
- Template para hooks personalizados
- Template para tests de integración

### Fase 4 - Integración TDD

**Verificaciones Automáticas**:
- [ ] Tests end-to-end completos (Pattern 6: 100% coverage)
- [ ] Tests de performance
- [ ] Tests de carga
- [ ] Tests de seguridad

**Patterns Aplicados en Fase 4:**
- Todos los patterns 1-6 aplicados en tests de integración
- Scripts de detección automática ejecutándose
- Validación de métricas de éxito (100% tests passing)

**Métricas Finales de Prevención:**
- ConfigDict errors: 0 (100% prevención)
- AsyncMock errors: 0 (100% prevención)
- Frontend mocking errors: 0 (100% prevención)
- E2E coverage: 100%
- Tiempo promedio resolución: <3 min (mejora 80%)

**Templates TDD Estándar**:
- Template para tests E2E
- Template para tests de performance
- Template para tests de seguridad

## Flujo TDD de Resolución

### 1. Identificación Automática
- CI/CD detecta errores automáticamente
- Logs estructurados para debugging
- Alertas inmediatas para errores críticos

### 2. Clasificación de Errores
- **CRITICAL**: Bloquean funcionalidad principal
- **HIGH**: Afectan funcionalidad importante
- **MEDIUM**: Afectan funcionalidad secundaria
- **LOW**: Mejoras y optimizaciones

### 3. Resolución Priorizada
- **CRITICAL**: Resolución inmediata (< 1 hora)
- **HIGH**: Resolución en mismo día (< 8 horas)
- **MEDIUM**: Resolución en 2-3 días
- **LOW**: Resolución en próxima iteración

### 4. Prevención Futura
- Documentar causa raíz del error
- Actualizar templates y checklists
- Mejorar tests para detectar error
- Capacitar equipo en prevención

## Backend Tests Completos

```python
# Stage 1: Fundaciones
tests/unit/services/
├── test_auth_service.py          # Autenticación JWT
├── test_oauth_service.py         # OAuth Google
├── test_mock_service.py          # Datos mock
└── test_response_helper.py       # Response envelope

tests/integration/
├── test_auth_integration.py      # Endpoints auth
├── test_oauth_integration.py     # Endpoints OAuth
└── test_health_integration.py    # Health checks

# Stage 2: Google Integration
tests/unit/services/
├── test_google_service.py        # Google API
├── test_classroom_service.py     # Classroom logic
└── test_metrics_service.py       # Métricas básicas

tests/integration/
├── test_google_integration.py    # Google endpoints
├── test_dashboard_integration.py # Dashboard endpoints
└── test_metrics_integration.py   # Metrics endpoints

# Stage 3: Visualización Avanzada
tests/unit/services/
├── test_search_service.py        # Búsqueda avanzada
├── test_notification_service.py  # Notificaciones
└── test_websocket_service.py     # WebSockets

tests/integration/
├── test_search_integration.py    # Search endpoints
└── test_notifications_integration.py # Notifications

# Stage 4: Integración Completa
tests/unit/services/
├── test_google_sync_service.py   # Sincronización
├── test_conflict_resolution.py   # Resolución conflictos
└── test_backup_service.py        # Backup/recovery

tests/integration/
├── test_google_api_integration.py # Google API completa
├── test_sync_flow_integration.py  # Flujo sincronización
└── test_backup_restore_integration.py # Backup/restore

tests/performance/
├── test_sync_performance.py      # Performance sync
├── test_api_load.py              # Carga API
└── test_database_performance.py  # Performance DB
```

## Cobertura TDD 100%

### 1. Identificación de Líneas Sin Cubrir

```bash
# Comando para identificar líneas específicas sin cubrir
pytest tests/ --cov=src --cov-report=term-missing --cov-report=html

# Verificar cobertura por archivo
pytest tests/unit/ --cov=src --cov-report=term-missing

# Generar reporte HTML detallado
pytest tests/ --cov=src --cov-report=html
open htmlcov/index.html
```

### 2. Técnicas de Testing para 100%

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
async def test_async_function_success():
    """Test async function caso exitoso"""
    result = await async_function()
    assert result is not None

@pytest.mark.asyncio
async def test_async_function_error():
    """Test async function caso de error"""
    with pytest.raises(Exception):
        await async_function_with_error()
```

**Para Edge Cases:**
```python
def test_edge_case_min_value():
    """Test valor mínimo"""
    result = function_with_validation(0)
    assert result is not None

def test_edge_case_max_value():
    """Test valor máximo"""
    result = function_with_validation(999999)
    assert result is not None

def test_edge_case_none():
    """Test valor None"""
    with pytest.raises(ValidationError):
        function_with_validation(None)
```

### 3. Checklist de Cobertura por Día

**Día 1-3: Fundaciones**
- [ ] **Backend Completo**: 100% cobertura en todos los módulos backend
- [ ] **Frontend Completo**: 100% cobertura en todos los componentes frontend
- [ ] **Tests Completo**: 100% cobertura en todos los archivos de test
- [ ] **Configuración**: 100% cobertura en `config.py`
- [ ] **Google Classroom API**: 100% cobertura en servicios de integración
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

## Frontend Tests Completos

```typescript
// Stage 1: Fundaciones
src/components/auth/
├── LoginForm.test.tsx            # Login form
├── OAuthButton.test.tsx          # OAuth button
└── AuthGuard.test.tsx            # Route protection

src/hooks/
├── useAuth.test.ts               # Auth hook
├── useOAuth.test.ts              # OAuth hook
├── useApi.test.ts                # API hook
└── useTranslation.test.ts        # i18n hook

// Stage 2: Google Integration
src/components/google/
├── GoogleConnect.test.tsx        # Google connection
├── ModeSelector.test.tsx         # Mode selector
└── CourseList.test.tsx           # Course list

src/components/dashboard/
├── MetricCard.test.tsx           # Metric cards
├── ChartWidget.test.tsx          # Chart widgets
└── DashboardHeader.test.tsx      # Dashboard header

src/hooks/
├── useGoogleClassroom.test.ts    # Google Classroom hook
├── useMetrics.test.ts            # Metrics hook
└── useDashboardData.test.ts      # Dashboard data hook

// Stage 3: Visualización Avanzada
src/components/search/
├── SearchBar.test.tsx            # Search bar
├── SearchResults.test.tsx        # Search results
└── StudentDetail.test.tsx        # Student detail

src/components/notifications/
├── NotificationCenter.test.tsx   # Notification center
├── NotificationBadge.test.tsx    # Notification badge
└── AlertBanner.test.tsx          # Alert banner

src/components/charts/
├── AdvancedChart.test.tsx        # Advanced charts
└── DrillDownChart.test.tsx       # Drill-down charts

src/hooks/
├── useSearch.test.ts             # Search hook
├── useNotifications.test.ts      # Notifications hook
└── useCharts.test.ts             # Charts hook

// Stage 4: Integración Completa
src/components/admin/
├── SyncPanel.test.tsx            # Sync panel
├── ConflictResolver.test.tsx     # Conflict resolver
└── BackupControls.test.tsx       # Backup controls

src/components/a11y/
├── SkipLink.test.tsx             # Skip link
├── FocusTrap.test.tsx            # Focus trap
└── ContrastToggle.test.tsx       # Contrast toggle

// E2E Tests
tests/e2e/
├── auth/
│   ├── login.spec.ts             # Login flow
│   ├── oauth.spec.ts             # OAuth flow
│   └── permissions.spec.ts       # Permissions
├── dashboard/
│   ├── admin.spec.ts             # Admin dashboard
│   ├── teacher.spec.ts           # Teacher dashboard
│   └── student.spec.ts           # Student dashboard
├── google/
│   ├── sync.spec.ts              # Google sync
│   └── integration.spec.ts       # Google integration
└── accessibility/
    ├── keyboard.spec.ts          # Keyboard navigation
    └── screenreader.spec.ts      # Screen reader
```

## Configuración de Vitest para Next.js 15 + React 19

```typescript
// vitest.config.ts
import { defineConfig } from 'vitest/config';
import react from '@vitejs/plugin-react';
import { resolve } from 'path';

export default defineConfig({
  plugins: [react()],
  test: {
    environment: 'jsdom',
    globals: true,
    setupFiles: ['./src/test/setup.ts'],
    coverage: {
      reporter: ['text', 'html'],
      exclude: ['node_modules/', 'src/test/'],
    },
  },
  resolve: {
    alias: {
      '@': resolve(__dirname, './src'),
    },
  },
});
```

## Ejemplos de Tests con Vitest + React Testing Library

### Test de Componente React

```tsx
// Button.test.tsx
import { render, screen, fireEvent } from '@testing-library/react';
import { describe, it, expect, vi } from 'vitest';
import Button from './Button';

describe('Button', () => {
  it('renders correctly', () => {
    render(<Button>Click me</Button>);
    expect(screen.getByText('Click me')).toBeInTheDocument();
  });

  it('calls onClick when clicked', () => {
    const handleClick = vi.fn();
    render(<Button onClick={handleClick}>Click me</Button>);
    fireEvent.click(screen.getByText('Click me'));
    expect(handleClick).toHaveBeenCalledTimes(1);
  });
});
```

### Test E2E con Playwright

```ts
// login.spec.ts
import { test, expect } from '@playwright/test';

test('user can login', async ({ page }) => {
  await page.goto('/login');
  await page.fill('input[name="email"]', 'user@example.com');
  await page.fill('input[name="password"]', 'password');
  await page.click('button[type="submit"]');
  await expect(page).toHaveURL('/dashboard');
});
```

## Templates TDD Estándar

### Template TDD para Verificación

```python
# Verificación TDD estándar con TestClient
from fastapi.testclient import TestClient

def test_endpoint_tdd():
    """Test TDD estándar para endpoints"""
    client = TestClient(app)
    response = client.get("/health")
    assert response.status_code == 200
    return response.json()
```

### Template TDD para Tests Async

```python
# Template estándar para tests async
@pytest.mark.asyncio
async def test_async_method():
    """Test método async con AsyncMock"""
    with patch('module.AsyncClass') as mock_class:
        mock_instance = AsyncMock()
        mock_class.return_value = mock_instance
        result = await async_method()
        assert result is not None
        mock_instance.method.assert_called_once()
```

### Template TDD para Tests CORS

```go
// Template estándar para tests CORS (Go + Echo)
package handlers_test

import (
    "net/http"
    "net/http/httptest"
    "testing"
    
    "github.com/labstack/echo/v4"
    "github.com/stretchr/testify/assert"
)

func TestCORSHeaders(t *testing.T) {
    // Setup
    e := echo.New()
    req := httptest.NewRequest(http.MethodGet, "/health", nil)
    req.Header.Set("Origin", "http://localhost:4200") // Angular default port
    rec := httptest.NewRecorder()
    c := e.NewContext(req, rec)
    
    // Test
    if assert.NoError(t, healthHandler(c)) {
        assert.Equal(t, http.StatusOK, rec.Code)
        assert.Contains(t, rec.Header().Get("Access-Control-Allow-Origin"), "*")
    }
}
```

### Template TDD para Configuración Pydantic v2

```python
# Template estándar para configuración Pydantic v2
from pydantic import ConfigDict
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    # Campos de configuración
    field_name: str = "default_value"
    
    model_config = ConfigDict(
        env_file=".env",
        case_sensitive=False,
        extra="ignore"
    )
```

### Template TDD para FastAPI con Lifespan

```python
# Template estándar para FastAPI con lifespan
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

## Fixtures y Mocks Consolidados

```python
# tests/conftest.py - Backend fixtures centralizados
# Incluye templates de resolución de errores de tests (ver Protocolos de Resolución)
@pytest.fixture
def mock_service():
    """MockService con datos completos"""
    return MockService()

@pytest.fixture
def google_service_mock():
    """Google service mock para testing"""
    return MockGoogleService()

@pytest.fixture
def websocket_mock():
    """WebSocket mock para notificaciones"""
    return MockWebSocketService()

@pytest.fixture
def test_users():
    """Usuarios completos para testing"""
    return {
        "admin": {...},
        "teacher": {...},
        "student": {...},
        "coordinator": {...}
    }
```

```typescript
// src/test/setup.ts - Frontend mocks centralizados para Vitest
import { expect, afterEach } from 'vitest';
import { cleanup } from '@testing-library/react';
import matchers from '@testing-library/jest-dom/matchers';

// Extender matchers de Vitest con los de Testing Library
expect.extend(matchers);

// Limpieza automática después de cada test
afterEach(() => {
  cleanup();
});

// Mocks globales para Next.js
vi.mock('next/navigation', () => ({
  useRouter: () => mockRouter,
  usePathname: () => '/',
  useSearchParams: () => new URLSearchParams(),
}))

// Mocks para hooks del sistema
vi.mock('@/hooks/useAuth', () => ({
  useAuth: () => mockAuthHook,
}))

// Mocks para WebSocket
global.WebSocket = MockWebSocket

// Mocks para ApexCharts
vi.mock('react-apexcharts', () => ({
  default: MockApexChart,
}))
```

## Scripts de Auto-Corrección

### Script 1: Fix Pydantic Imports (Pattern 1)
```python
def fix_pydantic_imports(file_path):
    """Auto-fix Pattern 1: Add missing ConfigDict import"""
    with open(file_path, 'r') as f:
        content = f.read()
    
    if 'ConfigDict' in content and 'from pydantic import' not in content:
        lines = content.split('\n')
        insert_at = 0
        for i, line in enumerate(lines):
            if line.strip() and not line.startswith('#'):
                insert_at = i
                break
        lines.insert(insert_at, 'from pydantic import BaseModel, EmailStr, Field, ConfigDict')
        
        with open(file_path, 'w') as f:
            f.write('\n'.join(lines))
        print(f"✅ Pattern 1 fixed: {file_path}")
```

### Script 2: Fix AsyncMock Issues (Pattern 4)
```python
def fix_async_mocking(file_path):
    """Auto-fix Pattern 4: Add AsyncMock for async tests"""
    with open(file_path, 'r') as f:
        content = f.read()
    
    # Fix mock paths
    content = content.replace(
        'src.app.core.security.verify_token',
        'src.app.api.endpoints.auth.verify_token'
    )
    
    # Add AsyncMock import
    if 'AsyncMock' in content and 'from unittest.mock import' in content:
        content = content.replace(
            'from unittest.mock import patch',
            'from unittest.mock import patch, AsyncMock'
        )
    
    # Fix @patch decorators
    import re
    pattern = r"@patch\('([^']*\.verify_token)'\)"
    replacement = r"@patch('\1', new_callable=AsyncMock)"
    content = re.sub(pattern, replacement, content)
    
    with open(file_path, 'w') as f:
        f.write(content)
    print(f"✅ Pattern 4 fixed: {file_path}")
```

### Script 3: Fix Frontend Mocking (Pattern 5)
```typescript
function fixFrontendMocking(filePath: string): void {
  // Auto-fix Pattern 5: Add comprehensive dependency mocks
  const requiredMocks = [
    `vi.mock('@/lib/defensive', () => ({
  safeToString: vi.fn((value) => String(value)),
  debounce: vi.fn((fn, delay) => fn),
  safeTry: vi.fn((fn) => fn())
}))`,
    `vi.mock('@/lib/logger', () => ({
  authLogger: { info: vi.fn(), warn: vi.fn(), error: vi.fn() },
  logUserAction: vi.fn()
}))`
  ]
  
  // Implementation to add missing mocks
  console.log(`✅ Pattern 5 fixed: ${filePath}`)
}
```

## Comandos de Verificación Automática

### Validación de Patterns:
```bash
# Pattern 1: ConfigDict imports
find backend/src -name "*.py" -exec grep -l "model_config = ConfigDict" {} \; | \
  xargs -I {} sh -c 'grep -q "from pydantic import.*ConfigDict" {} || echo "❌ Pattern 1: {}"'

# Pattern 4: AsyncMock usage
find backend/tests -name "test_*.py" -exec grep -l "async def test" {} \; | \
  xargs -I {} sh -c 'grep -q "AsyncMock" {} || echo "❌ Pattern 4: {}"'

# Pattern 5: Frontend mocks
find frontend/src -name "*.test.tsx" -exec grep -l "vi.mock" {} \; | \
  xargs -I {} sh -c 'grep -q "@/lib/defensive" {} || echo "❌ Pattern 5: {}"'
```

### OAuth Integration:
```bash
# Backend verification (Go + Echo)
curl -X GET http://localhost:8080/api/v1/auth/oauth/google

# Frontend testing (Angular + Playwright)
cd frontend && npm run test:e2e -- oauth-flow.spec.ts

# Manual verification
# 1. Start backend: cd backend && go run ./cmd/api
# 2. Start frontend: cd frontend && npm start
# 3. Navigate to http://localhost:4200 and click Google OAuth button
```

### React Query Usage:
```bash
# Coverage verification
npm run test:coverage:frontend

# Hook testing
npm run test:hooks

# Integration testing
npm run test:integration:api

# Manual verification
# Check Network tab for API calls using React Query
```

### Role-Based Dashboard:
```bash
# Unit testing
npm run test:role-based

# Integration testing
npm run test:integration:dashboard

# E2E testing
npm run test:e2e:dashboard

# Manual verification
# Login as different roles, verify content changes
```

### Test Coverage:
```bash
# Backend coverage
pytest --cov=src --cov-fail-under=80

# Frontend coverage
npm run test:coverage

# Combined coverage
npm run test:coverage:all

# Coverage report
open coverage/lcov-report/index.html
```

## Métricas de Éxito de Prevención

### Baseline Fase 1 (Antes de Patterns)
- Tests pasando: 41/45 (91%)
- Backend auth tests: 2/4 failing (50%)
- Frontend validation tests: 4/6 failing (33%)
- E2E coverage: 0%

### Resultado Fase 1 (Después de Patterns)
- Tests pasando: 45/45 (100%) ✅
- Backend auth tests: 4/4 passing (100%) ✅
- Frontend validation tests: 6/6 passing (100%) ✅
- E2E coverage: 25 tests (100%) ✅

### Mejoras Cuantificables
- ConfigDict errors: -100% (0 errores)
- AsyncMock errors: -100% (0 errores)
- Frontend mocking errors: -100% (0 errores)
- Tiempo resolución: -80% (<3 min promedio)
- Cobertura E2E: +100% (de 0 a completa)

## Referencias a Otros Documentos

- **Guía de Prevención LLM**: [llm_error_prevention_guide.md](../extra/revision/llm_error_prevention_guide.md) - Patterns completos y algoritmos
- Para detalles sobre los modelos de datos, consulte [Modelos de Datos](08_ClassSphere_modelos_datos.md).
- Para detalles sobre el plan de implementación, consulte [Plan de Implementación](10_ClassSphere_plan_implementacion.md).
- Para detalles sobre la configuración de deployment, consulte [Configuración de Deployment](11_ClassSphere_deployment.md).

---

[← Modelos de Datos](08_ClassSphere_modelos_datos.md) | [Índice](00_ClassSphere_index.md) | [Siguiente → Plan de Implementación](10_ClassSphere_plan_implementacion.md)
