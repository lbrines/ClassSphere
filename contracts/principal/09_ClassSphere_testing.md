---
title: "ClassSphere - Estrategia de Testing Unificada"
version: "2.6"
type: "documentation"
related_files:
  - "00_ClassSphere_index.md"
  - "08_ClassSphere_modelos_datos.md"
  - "10_ClassSphere_plan_implementacion.md"
---

[← Modelos de Datos](08_ClassSphere_modelos_datos.md) | [Índice](00_ClassSphere_index.md) | [Siguiente → Plan de Implementación](10_ClassSphere_plan_implementacion.md)

# Estrategia de Testing Unificada

## Estrategia de Testing Frontend (Next.js 15 + React 19)

### Stack de Testing Definido
- ✅ **Unit / Integration:** Vitest + React Testing Library  
- ✅ **E2E:** Playwright  
- 🚫 **No usar Jest** (incompatible con ESM y React 19, soporte experimental)

> **Nota:** No agregar Jest ni dependencias relacionadas (`jest`, `babel-jest`, `ts-jest`, `jest-environment-jsdom`).  
> Si se requiere compatibilidad con tests antiguos, migrarlos a Vitest gradualmente.

### Motivación del Cambio
| Motivo | Beneficio |
|--------|----------|
| Claridad técnica | Todos saben qué stack usar |
| Prevención | Evita roturas en builds/tests |
| Estándar oficial Next 15 | 100% compatible |
| Automatización CI | Garantiza cumplimiento |

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
- **Fase 1 Completa**: ≥100% cobertura en toda la Fase 1 (backend + frontend + tests)

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

### 1. Testing Async como Estándar TDD

**Metodología**: Tests async son parte integral del ciclo Red-Green-Refactor
```python
# ✅ TDD ESTÁNDAR - AsyncMock como parte del flujo
mock_instance = AsyncMock()
mock_instance.admin.command.return_value = {"ok": 1}

# ❌ INCORRECTO - Mock no funciona con async
mock_instance = Mock()
mock_instance.admin.command.return_value = {"ok": 1}
```

**Integración TDD**:
- `AsyncMock` como estándar para métodos async
- Template TDD para tests de base de datos
- Verificación automática en CI como parte del flujo

### 2. Headers HTTP como Verificación TDD

**Metodología**: Tests de CORS como parte del flujo TDD estándar
```python
# ✅ TDD ESTÁNDAR - Headers básicos verificables
assert "access-control-allow-origin" in response.headers
assert "access-control-allow-credentials" in response.headers

# ❌ INCORRECTO - Headers específicos pueden variar
assert "access-control-allow-methods" in response.headers
```

**Integración TDD**:
- Tests de CORS simplificados y robustos
- Verificación de headers esenciales solamente
- Documentación de comportamiento esperado de middleware

## Metodología TDD por Fase

### Fase 1 - Fundaciones TDD (5/12 días completados)

**Verificaciones Automáticas**:
- [x] Tests async usan `AsyncMock` correctamente ✅
- [x] Tests de CORS verifican headers básicos ✅
- [x] Servidor inicia en puerto 8000 (nunca alternativo) ✅
- [x] Health check responde correctamente ✅
- [x] Cobertura 100% en toda la Fase 1 sin warnings críticos ✅
- [x] Lifespan resiliente funciona sin servicios externos ✅

**Progreso Detallado**:
- ✅ **Día 1**: Configuración del Entorno TDD - Python 3.11.4, FastAPI, estructura de directorios
- ✅ **Día 2**: Configuración de Testing TDD - pytest, AsyncMock, timeouts, cobertura
- ✅ **Día 3**: Configuración de Infraestructura TDD - Redis, puerto 8000, CI/CD
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
- [ ] Mocks de Google API funcionan correctamente
- [ ] Modo dual switching sin errores
- [ ] Tests de OAuth completos
- [ ] Tests de Classroom API mockeados

**Templates TDD Estándar**:
- Template para mocks de Google API
- Template para tests de OAuth
- Template para modo dual switching

### Fase 3 - Frontend TDD

**Verificaciones Automáticas**:
- [ ] Componentes React renderizan correctamente
- [ ] Hooks personalizados funcionan
- [ ] Tests de integración frontend-backend
- [ ] Tests de UI con Testing Library

**Templates TDD Estándar**:
- Template para componentes React
- Template para hooks personalizados
- Template para tests de integración

### Fase 4 - Integración TDD

**Verificaciones Automáticas**:
- [ ] Tests end-to-end completos
- [ ] Tests de performance
- [ ] Tests de carga
- [ ] Tests de seguridad

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

```python
# Template estándar para tests CORS
def test_cors_headers():
    """Test CORS con headers básicos"""
    client = TestClient(app)
    response = client.get("/health", headers={"Origin": "http://localhost:3000"})
    assert response.status_code == 200
    assert "access-control-allow-origin" in response.headers
    assert "access-control-allow-credentials" in response.headers
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

## Comandos de Verificación Automática

### OAuth Integration:
```bash
# Backend verification
curl -X GET http://localhost:8000/api/v1/oauth/google

# Frontend testing
npm run test:oauth
npm run test:e2e:oauth

# Manual verification
# Click OAuthButton, verify Google redirect works
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

## Referencias a Otros Documentos

- Para detalles sobre los modelos de datos, consulte [Modelos de Datos](08_ClassSphere_modelos_datos.md).
- Para detalles sobre el plan de implementación, consulte [Plan de Implementación](10_ClassSphere_plan_implementacion.md).
- Para detalles sobre la configuración de deployment, consulte [Configuración de Deployment](11_ClassSphere_deployment.md).

---

[← Modelos de Datos](08_ClassSphere_modelos_datos.md) | [Índice](00_ClassSphere_index.md) | [Siguiente → Plan de Implementación](10_ClassSphere_plan_implementacion.md)
