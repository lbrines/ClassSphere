---
title: "ClassSphere - Fase 1: Fundaciones TDD"
version: "1.0"
type: "documentation"
date: "2025-10-04"
author: "Sistema de Contratos LLM"
related_files:
  - "01_plam_index.md"
  - "03_plan_fase2_google_integration.md"
---

[← Índice](01_plam_index.md) | [Siguiente → Fase 2: Integración Google](03_plan_fase2_google_integration.md)

# Fase 1: Fundaciones TDD

## Objetivos de la Fase

Esta fase establece las bases fundamentales del sistema ClassSphere siguiendo una metodología TDD estricta:

1. **Backend Fundacional**: FastAPI + JWT + OAuth + Redis
2. **Frontend Fundacional**: Next.js 15 + React 19 + TypeScript
3. **Integración Básica**: Comunicación frontend-backend
4. **Testing Completo**: 100% cobertura en todos los componentes

## Duración Estimada: 10-12 días

### Distribución de Tareas

**Días 1-3: Backend Fundacional**
- Tests para FastAPI + JWT + OAuth + MockService
- Implementación de autenticación completa
- API REST con envelope estándar
- Health checks básicos

**Días 4-6: Frontend Fundacional**
- Tests para Next.js + Auth + Layout + i18n
- Implementación de UI base
- React Query v4 + Tailwind CSS
- Páginas principales (login, dashboard)

**Días 7-9: Integración Base**
- Tests de integración frontend-backend
- Comunicación API completa
- Manejo de errores y estados
- Protección de rutas

**Días 10-12: Testing y Refinamiento**
- Tests E2E básicos
- Documentación inicial
- Configuración CI/CD básica
- Validación Stage 1 completo

## Estructura de Tests Backend

### Requisitos Técnicos Obligatorios

1. **Puerto 8000 Fijo**
   ```python
   # test_server_port.py
   def test_server_runs_on_port_8000():
       """Verificar que el servidor inicie en puerto 8000"""
       # Implementar verificación de puerto
       assert port == 8000
   ```

2. **Timeouts en Tests Async**
   ```python
   # test_async_timeout.py
   @pytest.mark.asyncio
   async def test_async_function_with_timeout():
       """Test con timeout explícito"""
       result = await asyncio.wait_for(
           async_function(), 
           timeout=2.0  # Timeout obligatorio
       )
       assert result is not None
   ```

3. **Redis para Caché**
   ```python
   # test_redis_cache.py
   def test_redis_cache_with_fallback():
       """Test caché con degradación elegante"""
       # Test con Redis disponible
       assert cache.get("key") == "value"
       
       # Test con Redis no disponible (fallback)
       with patch("redis.Redis.get", side_effect=Exception("Redis error")):
           assert cache.get("key") == "fallback_value"
   ```

### Estructura de Directorios de Tests

```
backend/
└── tests/
    ├── unit/
    │   ├── services/
    │   │   ├── test_auth_service.py
    │   │   ├── test_oauth_service.py
    │   │   └── test_mock_service.py
    │   ├── api/
    │   │   ├── test_auth_endpoints.py
    │   │   └── test_health_endpoints.py
    │   └── core/
    │       ├── test_config.py
    │       └── test_security.py
    ├── integration/
    │   ├── test_auth_flow.py
    │   └── test_oauth_flow.py
    └── conftest.py
```

### Tests Unitarios Críticos

```python
# test_auth_service.py
@pytest.mark.asyncio
async def test_authenticate_user_with_valid_credentials():
    """Test autenticación con credenciales válidas"""
    auth_service = AuthService()
    result = await asyncio.wait_for(
        auth_service.authenticate_user("user@example.com", "password"),
        timeout=2.0  # Timeout obligatorio
    )
    assert result is not None
    assert result.email == "user@example.com"

@pytest.mark.asyncio
async def test_authenticate_user_with_invalid_password():
    """Test autenticación con password inválido"""
    auth_service = AuthService()
    with pytest.raises(AuthenticationError):
        await asyncio.wait_for(
            auth_service.authenticate_user("user@example.com", "wrong"),
            timeout=2.0  # Timeout obligatorio
        )
```

### Tests de Integración

```python
# test_auth_flow.py
def test_login_endpoint_with_valid_credentials():
    """Test endpoint de login con credenciales válidas"""
    client = TestClient(app)
    response = client.post(
        "/api/v1/auth/login",
        json={"email": "user@example.com", "password": "password"}
    )
    assert response.status_code == 200
    data = response.json()
    assert "data" in data
    assert "token" in data["data"]
    assert "user" in data["data"]
```

## Estructura de Tests Frontend

### Requisitos Técnicos Obligatorios

1. **Puerto 3000 Fijo**
   ```typescript
   // test_server_port.ts
   test('server runs on port 3000', async () => {
     // Verificar puerto del servidor
     expect(port).toBe(3000);
   });
   ```

2. **Timeouts en Tests Async**
   ```typescript
   // test_async_timeout.ts
   test('async operation completes within timeout', async () => {
     const result = await Promise.race([
       asyncOperation(),
       new Promise((_, reject) => 
         setTimeout(() => reject(new Error('Timeout')), 2000)
       )
     ]);
     expect(result).toBeDefined();
   });
   ```

### Estructura de Directorios de Tests

```
frontend/
└── src/
    ├── components/
    │   ├── auth/
    │   │   ├── LoginForm.tsx
    │   │   └── LoginForm.test.tsx
    │   └── layout/
    │       ├── Header.tsx
    │       └── Header.test.tsx
    ├── hooks/
    │   ├── useAuth.ts
    │   └── useAuth.test.ts
    └── test/
        └── setup.ts
```

### Tests de Componentes

```typescript
// LoginForm.test.tsx
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import { describe, it, expect, vi } from 'vitest';
import LoginForm from './LoginForm';

describe('LoginForm', () => {
  it('renders login form correctly', () => {
    render(<LoginForm />);
    expect(screen.getByLabelText(/email/i)).toBeInTheDocument();
    expect(screen.getByLabelText(/password/i)).toBeInTheDocument();
    expect(screen.getByRole('button', { name: /login/i })).toBeInTheDocument();
  });

  it('validates form fields', async () => {
    render(<LoginForm />);
    
    // Submit sin datos
    fireEvent.click(screen.getByRole('button', { name: /login/i }));
    
    // Esperar validación con timeout
    await waitFor(() => {
      expect(screen.getByText(/email is required/i)).toBeInTheDocument();
    }, { timeout: 1000 });
  });

  it('submits form with valid data', async () => {
    const onSubmit = vi.fn();
    render(<LoginForm onSubmit={onSubmit} />);
    
    // Llenar formulario
    fireEvent.change(screen.getByLabelText(/email/i), {
      target: { value: 'user@example.com' }
    });
    fireEvent.change(screen.getByLabelText(/password/i), {
      target: { value: 'password' }
    });
    
    // Submit
    fireEvent.click(screen.getByRole('button', { name: /login/i }));
    
    // Verificar submit con timeout
    await waitFor(() => {
      expect(onSubmit).toHaveBeenCalledWith({
        email: 'user@example.com',
        password: 'password'
      });
    }, { timeout: 1000 });
  });
});
```

### Tests de Hooks

```typescript
// useAuth.test.ts
import { renderHook, act, waitFor } from '@testing-library/react';
import { describe, it, expect, vi } from 'vitest';
import { useAuth } from './useAuth';

describe('useAuth', () => {
  it('initializes with unauthenticated state', () => {
    const { result } = renderHook(() => useAuth());
    expect(result.current.isAuthenticated).toBe(false);
    expect(result.current.user).toBeNull();
  });

  it('authenticates user with valid credentials', async () => {
    const { result } = renderHook(() => useAuth());
    
    await act(async () => {
      await result.current.login('user@example.com', 'password');
    });
    
    await waitFor(() => {
      expect(result.current.isAuthenticated).toBe(true);
      expect(result.current.user).not.toBeNull();
      expect(result.current.user?.email).toBe('user@example.com');
    }, { timeout: 2000 });
  });
});
```

## Scripts de Verificación

### Script de Verificación de Puerto 8000

```bash
#!/bin/bash
# scripts/verify_port_8000.sh
set -e

echo "🔍 Verificando puerto 8000..."
if lsof -Pi :8000 -sTCP:LISTEN -t >/dev/null; then
  echo "✅ Puerto 8000 está en uso por la aplicación"
  exit 0
else
  echo "❌ Puerto 8000 no está en uso"
  exit 1
fi
```

### Script de Verificación de Puerto 3000

```bash
#!/bin/bash
# scripts/verify_port_3000.sh
set -e

echo "🔍 Verificando puerto 3000..."
if lsof -Pi :3000 -sTCP:LISTEN -t >/dev/null; then
  echo "✅ Puerto 3000 está en uso por la aplicación"
  exit 0
else
  echo "❌ Puerto 3000 no está en uso"
  exit 1
fi
```

## Comandos de Testing

### Backend Tests

```bash
# Tests unitarios con cobertura
pytest tests/unit/ --cov=src --cov-report=term-missing

# Tests de integración
pytest tests/integration/ --cov=src --cov-report=term-missing

# Tests completos con 100% cobertura
pytest tests/ --cov=src --cov-fail-under=100 --cov-report=term-missing
```

### Frontend Tests

```bash
# Tests unitarios
npm run test

# Tests unitarios en modo watch
npm run test:watch

# Tests de integración
npm run test:integration

# Tests E2E
npm run test:e2e
```

## Criterios de Aceptación

### Backend

- [ ] FastAPI + JWT + OAuth funcionando en puerto 8000
- [ ] Autenticación completa con JWT y OAuth 2.0 Google
- [ ] Sistema de roles (admin > coordinator > teacher > student)
- [ ] Redis caché con degradación elegante
- [ ] Tests unitarios con cobertura 100%
- [ ] CI/CD pipeline básico

### Frontend

- [ ] Next.js 15 + React 19 funcionando en puerto 3000
- [ ] UI base con Tailwind CSS
- [ ] Componentes de autenticación (LoginForm, OAuthButton)
- [ ] Servicios API y manejo de errores
- [ ] Tests de componentes con cobertura 100%

### Integración

- [ ] Comunicación frontend-backend completa
- [ ] Manejo de errores y estados
- [ ] Protección de rutas por rol
- [ ] Tests E2E básicos

## Referencias

Para más detalles sobre la implementación TDD, consultar:
- [Estrategia de Testing Unificada](principal/09_ClassSphere_testing.md)
- [Plan de Implementación Unificado](principal/10_ClassSphere_plan_implementacion.md)
- [TDD Best Practices](extra/TDD_BEST_PRACTICES.md)

---

[← Índice](01_plam_index.md) | [Siguiente → Fase 2: Integración Google](03_plan_fase2_google_integration.md)
