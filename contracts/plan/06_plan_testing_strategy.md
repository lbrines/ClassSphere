---
title: "ClassSphere - Estrategia de Testing Completa"
version: "1.0"
type: "strategy_document"
context_priority: "HIGH"
date: "2025-10-05"
---

[← Plan Principal](01_plan_index.md)

# Estrategia de Testing Completa

## Stack de Testing Definido

### Backend
- **pytest** + **pytest-asyncio** + **pytest-cov**
- **AsyncMock** para servicios async
- **TestClient** para endpoints FastAPI
- **Timeouts**: 30s unit, 60s integration

### Frontend
- **Vitest** + **React Testing Library** (unit/integration)
- **Playwright** (E2E)
- 🚫 **NO usar Jest** (incompatible con ESM y React 19)

## Cobertura Requerida

| Tipo de Módulo | Líneas | Ramas |
|----------------|--------|-------|
| Global | ≥80% | ≥65% |
| Módulos Críticos | ≥90% | ≥80% |
| Seguridad | ≥95% | ≥85% |
| API Endpoints | 100% | 100% |

## Criterios de Aceptación Medibles

### Funcional
- [ ] Login funciona con credenciales demo (admin@classsphere.edu / secret)
- [ ] OAuth Google redirige a Google y retorna exitosamente
- [ ] Dashboard muestra contenido específico por rol
- [ ] API responde en <2 segundos
- [ ] Tests pasan 100% sin fallos

### Técnico
- [ ] Cobertura backend ≥80%
- [ ] Cobertura frontend ≥80%
- [ ] Módulos críticos ≥90%
- [ ] Seguridad ≥95%
- [ ] 0 vulnerabilidades CRITICAL

### Comandos de Verificación Automática
```bash
# Backend coverage
cd backend && python -m pytest --cov=src --cov-report=term-missing --cov-fail-under=80

# Frontend coverage  
cd frontend && npm run test:coverage

# Security scan
docker run --rm -v "$(pwd):/app" aquasec/trivy:latest fs /app

# Performance test
curl -w "@curl-format.txt" -o /dev/null -s http://localhost:8000/health
```

## Metodología TDD Estricta

### Ciclo Red-Green-Refactor

1. **Red**: Escribir test que falle
2. **Green**: Implementar código mínimo para pasar
3. **Refactor**: Mejorar código manteniendo tests verdes
4. **Repeat**: Para cada nueva funcionalidad

### Template de Test Backend

```python
import pytest
from unittest.mock import AsyncMock, patch
from fastapi.testclient import TestClient


@pytest.mark.asyncio
async def test_async_service():
    """Test servicio async con AsyncMock"""
    with patch('app.services.ExternalService') as mock_service:
        mock_instance = AsyncMock()
        mock_service.return_value = mock_instance
        mock_instance.method.return_value = {"result": "success"}
        
        result = await service_function()
        
        assert result is not None
        mock_instance.method.assert_called_once()


def test_endpoint(client: TestClient):
    """Test endpoint con TestClient"""
    response = client.get("/api/v1/endpoint")
    
    assert response.status_code == 200
    assert response.json()["status"] == "success"
```

### Template de Test Frontend

```typescript
import { render, screen, fireEvent } from '@testing-library/react';
import { describe, it, expect, vi } from 'vitest';
import Component from './Component';

describe('Component', () => {
  it('renders correctly', () => {
    render(<Component />);
    expect(screen.getByText('Expected Text')).toBeInTheDocument();
  });

  it('handles user interaction', () => {
    const handleClick = vi.fn();
    render(<Component onClick={handleClick} />);
    
    fireEvent.click(screen.getByRole('button'));
    expect(handleClick).toHaveBeenCalledTimes(1);
  });
});
```

### Template E2E con Playwright

```typescript
import { test, expect } from '@playwright/test';

test('user can complete flow', async ({ page }) => {
  await page.goto('/');
  
  await page.fill('input[name="email"]', 'user@example.com');
  await page.fill('input[name="password"]', 'password');
  await page.click('button[type="submit"]');
  
  await expect(page).toHaveURL('/dashboard');
  await expect(page.locator('h1')).toContainText('Dashboard');
});
```

## Comandos de Verificación

### Backend
```bash
# Tests unitarios
pytest tests/unit/ -v

# Tests de integración
pytest tests/integration/ -v

# Cobertura completa
pytest tests/ --cov=src --cov-report=term-missing --cov-fail-under=80

# Reporte HTML
pytest tests/ --cov=src --cov-report=html
open htmlcov/index.html
```

### Frontend
```bash
# Tests unitarios
npm run test

# Tests en modo watch
npm run test:watch

# Cobertura
npm run test -- --coverage

# E2E
npm run test:e2e

# E2E con UI
npm run test:e2e -- --ui
```

## Fixtures y Mocks

### Backend (conftest.py)
```python
import pytest
from fastapi.testclient import TestClient
from app.main import create_app


@pytest.fixture
def client():
    """TestClient para FastAPI"""
    app = create_app()
    return TestClient(app)


@pytest.fixture
def mock_google_service():
    """Mock de Google Classroom Service"""
    from app.services.google_service import GoogleClassroomService
    service = GoogleClassroomService(use_mock=True)
    return service


@pytest.fixture
def test_users():
    """Usuarios de prueba"""
    return {
        "admin": {
            "email": "admin@classsphere.edu",
            "password": "secret",
            "role": "admin"
        },
        "teacher": {
            "email": "teacher@classsphere.edu",
            "password": "secret",
            "role": "teacher"
        }
    }
```

### Frontend (setup.ts)
```typescript
import { expect, afterEach } from 'vitest';
import { cleanup } from '@testing-library/react';
import matchers from '@testing-library/jest-dom/matchers';

expect.extend(matchers);

afterEach(() => {
  cleanup();
});

// Mock Next.js router
vi.mock('next/navigation', () => ({
  useRouter: () => ({
    push: vi.fn(),
    replace: vi.fn(),
    back: vi.fn(),
  }),
  usePathname: () => '/',
  useSearchParams: () => new URLSearchParams(),
}));
```

## Quality Gates

### Pre-commit
- Linting (flake8, eslint)
- Type checking (mypy, TypeScript)
- Unit tests pasando

### Pre-push
- Tests completos pasando
- Cobertura ≥80%
- Security scan sin errores críticos

### CI/CD
- Todos los tests pasando
- Cobertura ≥80%
- Security scan completo
- E2E tests pasando
- Performance tests pasando

## Timeouts de Testing

```yaml
Unit Tests: 30 segundos máximo
Integration Tests: 60 segundos máximo
E2E Tests: 120 segundos máximo
API Tests: 45 segundos máximo
```

## Configuración pytest.ini

```ini
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
```

## Configuración vitest.config.ts

```typescript
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
      lines: 80,
      branches: 65,
      functions: 80,
      statements: 80,
    },
  },
  resolve: {
    alias: {
      '@': resolve(__dirname, './src'),
    },
  },
});
```

---

[← Plan Principal](01_plan_index.md)
