---
title: "ClassSphere - Estrategia de Testing Unificada"
version: "3.0"
type: "development_plan"
related_files:
  - "contracts/principal/09_ClassSphere_testing.md"
  - "contracts/principal/10_ClassSphere_plan_implementacion.md"
---

# Estrategia de Testing Unificada - TDD-RunFix+

## Stack de Testing Consolidado

### Backend (Go)
- **Unit Testing**: testify/assert + testify/mock
- **HTTP Testing**: httptest (Go standard library)
- **Mocking**: testify/mock + mockery
- **Coverage**: go test -cover

### Frontend (Angular 19)
- **Unit Testing**: Jasmine + Karma (estándar Angular)
- **Component Testing**: Angular Testing Library
- **E2E Testing**: Playwright
- **Coverage**: karma-coverage

### Ventajas del Stack
| Aspecto | Beneficio |
|---------|----------|
| Estándar oficial | Jasmine es el framework oficial de Angular |
| Zero-config | Angular CLI configura automáticamente |
| Maduro y estable | testify es el estándar de facto en Go |
| Documentación completa | Ambos tienen documentación oficial extensa |

## Metodología TDD-RunFix+ Consolidada

El sistema completo sigue Test-Driven Development (TDD) estricto con prevención de errores integrada:

1. **Red**: Escribir test que falle
2. **Green**: Implementar código mínimo para pasar
3. **Refactor**: Mejorar código manteniendo tests verdes
4. **Validate Patterns**: Aplicar validación automática de patterns críticos
5. **Document**: Documentar decisiones basadas en tests
6. **Integrate**: Integrar con sistema existente
7. **Validate**: Validar cumplimiento de criterios de aceptación

## Cobertura de Testing Requerida

### Cobertura Global
- **Global**: ≥80% líneas, ≥65% ramas
- **Módulos Críticos**: ≥90% líneas, ≥80% ramas
- **Componentes de Seguridad**: ≥95% líneas, ≥85% ramas
- **API Endpoints**: 100% casos de éxito y error
- **Backend Go**: ≥80% líneas con testify
- **Frontend Angular**: ≥80% líneas con Jasmine + Karma
- **E2E**: Cobertura de flujos críticos con Playwright

### Criterios de Aceptación Medibles

#### Funcional
- [ ] Login funciona con credenciales demo (admin@classsphere.edu / secret)
- [ ] OAuth Google redirige a Google y retorna exitosamente
- [ ] Dashboard muestra contenido específico por rol
- [ ] Navegación funciona entre todas las páginas
- [ ] Logout limpia sesión y redirige a login

#### Técnico
- [ ] Backend coverage ≥ 80% (medido por `go test -cover`)
- [ ] Frontend coverage ≥ 80% (medido por `ng test --code-coverage`)
- [ ] Todos los tests pasan 100% (medido por CI/CD pipeline)
- [ ] Sin errores de consola en navegador (medido manualmente)
- [ ] Tiempo de carga página < 2 segundos (medido por Lighthouse)

#### Integración
- [ ] Frontend se comunica con backend exitosamente
- [ ] JWT tokens se almacenan y envían correctamente
- [ ] Flujo OAuth completa sin errores
- [ ] Manejo de errores muestra mensajes apropiados
- [ ] Diseño responsivo funciona en móvil/tablet

## Principios TDD con Prevención Integral

### Patrones de Prevención Aplicados

#### 1. Testing Async como Estándar TDD (Pattern 4)

**Metodología**: Tests async son parte integral del ciclo Red-Green-Refactor

```go
// ✅ TDD ESTÁNDAR - AsyncMock como parte del flujo (Pattern 4)
mock_instance := AsyncMock()
mock_instance.admin.command.return_value = {"ok": 1}

// ❌ INCORRECTO - Mock no funciona con async
mock_instance := Mock()
mock_instance.admin.command.return_value = {"ok": 1}
```

**Prevención Automática Pattern 4**:
```go
// Validación automática en tests
if strings.Contains(testFile, "async def") && strings.Contains(testFile, "@patch") {
    assert.Contains(t, testFile, "AsyncMock", "Pattern 4: Use AsyncMock for async functions")
    assert.Contains(t, testFile, "new_callable=AsyncMock", "Pattern 4: Add new_callable parameter")
}
```

**Integración TDD**:
- `AsyncMock` como estándar para métodos async (Pattern 4)
- Template TDD para tests de base de datos
- Verificación automática en CI como parte del flujo
- Mock paths correctos: `src.app.api.endpoints.auth.verify_token` (Pattern 4)

#### 2. Headers HTTP como Verificación TDD

**Metodología**: Tests de CORS como parte del flujo TDD estándar

```go
// ✅ TDD ESTÁNDAR - Headers básicos verificables
assert.Contains(t, response.Headers, "Access-Control-Allow-Origin")
assert.Contains(t, response.Headers, "Access-Control-Allow-Credentials")

// ❌ INCORRECTO - Headers específicos pueden variar
assert.Contains(t, response.Headers, "Access-Control-Allow-Methods")
```

#### 3. Validación Go Structs (Pattern 1)

**Metodología**: Go structs con tags obligatorios para validación

```go
// ✅ CORRECTO - Pattern 1
type User struct {
    Email string `json:"email" validate:"required,email"`
    Role  string `json:"role" validate:"required,oneof=admin coordinator teacher student"`
}

// ❌ INCORRECTO - Missing validation tags
type User struct {
    Email string `json:"email"`
    Role  string `json:"role"`
}
```

**Prevención Automática Pattern 1**:
```bash
# Script de validación pre-commit
grep -r "type.*struct" --include="*.go" | while read line; do
    file=$(echo $line | cut -d: -f1)
    if ! grep -q "validate:" "$file"; then
        echo "❌ Pattern 1 Error: $file missing validation tags"
        exit 1
    fi
done
```

#### 4. Angular Configuration Validation (Pattern 2)

**Metodología**: Evitar configuraciones deprecated en angular.json

```json
// ✅ CORRECTO - Pattern 2
{
  "projects": {
    "classsphere-frontend": {
      "architect": {
        "build": {
          "builder": "@angular-devkit/build-angular:application",
          "options": {
            "outputPath": "dist/classsphere-frontend"
          }
        }
      }
    }
  }
}

// ❌ INCORRECTO - Deprecated builder
{
  "builder": "@angular-devkit/build-angular:browser"
}
```

#### 5. TypeScript Validation (Pattern 3)

**Metodología**: TypeScript estricto y error handling apropiado

```typescript
// ✅ CORRECTO - Pattern 3
interface Course {
  id: string;
  name: string;
  description?: string;
}

const processCourse = (course: Course): string => {
  return course.name ?? 'Unnamed Course';
};

// ❌ INCORRECTO
const processCourse = (course: any): string => {
  return course.name; // Potential runtime error
};
```

#### 6. Frontend Dependency Mocking (Pattern 5)

**Metodología**: Mocking comprehensivo de dependencias frontend

```typescript
// ✅ CORRECTO - Pattern 5
describe('CourseService', () => {
  let service: CourseService;
  let httpClientSpy: jasmine.SpyObj<HttpClient>;

  beforeEach(() => {
    const spy = jasmine.createSpyObj('HttpClient', ['get', 'post']);
    TestBed.configureTestingModule({
      providers: [
        CourseService,
        { provide: HttpClient, useValue: spy }
      ]
    });
    service = TestBed.inject(CourseService);
    httpClientSpy = TestBed.inject(HttpClient) as jasmine.SpyObj<HttpClient>;
  });

  it('should fetch courses', () => {
    const mockCourses = [{ id: '1', name: 'Math 101' }];
    httpClientSpy.get.and.returnValue(of(mockCourses));

    service.getCourses().subscribe(courses => {
      expect(courses).toEqual(mockCourses);
    });
  });
});
```

#### 7. E2E Test Coverage (Pattern 6)

**Metodología**: Cobertura E2E completa para integración frontend-backend

```typescript
// ✅ CORRECTO - Pattern 6
import { test, expect } from '@playwright/test';

test.describe('Authentication Flow', () => {
  test('complete login flow works', async ({ page }) => {
    await page.goto('/login');
    
    // Test login
    await page.fill('[data-testid="email"]', 'admin@classsphere.edu');
    await page.fill('[data-testid="password"]', 'secret');
    await page.click('[data-testid="login-button"]');
    
    // Verify redirect to dashboard
    await expect(page).toHaveURL('/admin/dashboard');
    
    // Test logout
    await page.click('[data-testid="logout-button"]');
    await expect(page).toHaveURL('/login');
  });
});
```

## Templates de Tests

### Backend Go Template

```go
// tests/services/example_service_test.go
package services

import (
    "testing"
    "github.com/stretchr/testify/assert"
    "github.com/stretchr/testify/mock"
)

type MockExampleService struct {
    mock.Mock
}

func (m *MockExampleService) GetData(id string) (string, error) {
    args := m.Called(id)
    return args.String(0), args.Error(1)
}

func TestExampleService(t *testing.T) {
    mockService := new(MockExampleService)
    mockService.On("GetData", "test-id").Return("test-data", nil)
    
    service := NewExampleService(mockService)
    
    result, err := service.ProcessData("test-id")
    
    assert.NoError(t, err)
    assert.Equal(t, "processed-test-data", result)
    mockService.AssertExpectations(t)
}
```

### Frontend Angular Template

```typescript
// src/app/services/example.service.spec.ts
import { TestBed } from '@angular/core/testing';
import { HttpClientTestingModule } from '@angular/common/http/testing';
import { ExampleService } from './example.service';

describe('ExampleService', () => {
  let service: ExampleService;
  let httpMock: HttpTestingController;

  beforeEach(() => {
    TestBed.configureTestingModule({
      imports: [HttpClientTestingModule],
      providers: [ExampleService]
    });
    service = TestBed.inject(ExampleService);
    httpMock = TestBed.inject(HttpTestingController);
  });

  afterEach(() => {
    httpMock.verify();
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });

  it('should fetch data', () => {
    const mockData = { id: '1', name: 'Test' };
    
    service.getData('1').subscribe(data => {
      expect(data).toEqual(mockData);
    });
    
    const req = httpMock.expectOne('/api/data/1');
    expect(req.request.method).toBe('GET');
    req.flush(mockData);
  });
});
```

### E2E Playwright Template

```typescript
// e2e/example.e2e-spec.ts
import { test, expect } from '@playwright/test';

test.describe('Example Feature', () => {
  test.beforeEach(async ({ page }) => {
    await page.goto('/');
  });

  test('should display correct content', async ({ page }) => {
    await expect(page.locator('h1')).toHaveText('Welcome to ClassSphere');
  });

  test('should handle user interaction', async ({ page }) => {
    await page.click('[data-testid="example-button"]');
    await expect(page.locator('[data-testid="result"]')).toBeVisible();
  });
});
```

## Comandos de Verificación

### Backend Testing
```bash
# Run all tests
go test ./...

# Run with coverage
go test ./... -cover -coverprofile=coverage.out

# Generate coverage report
go tool cover -html=coverage.out -o coverage.html

# Run specific package
go test ./internal/services/

# Run with verbose output
go test ./... -v

# Run with race detection
go test ./... -race
```

### Frontend Testing
```bash
# Run unit tests
ng test

# Run with coverage
ng test --code-coverage --watch=false

# Run E2E tests
ng e2e

# Run E2E in CI mode
ng e2e --configuration=ci

# Run specific test file
ng test --include='**/auth.service.spec.ts'
```

### Accessibility Testing
```bash
# Install axe-core CLI
npm install -g @axe-core/cli

# Run accessibility tests
axe http://localhost:4200 --exit

# Run with specific rules
axe http://localhost:4200 --rules wcag2a,wcag2aa --exit
```

### Performance Testing
```bash
# Install Lighthouse CI
npm install -g @lhci/cli

# Run Lighthouse tests
lhci autorun

# Run specific test
lighthouse http://localhost:4200 --output html --output-path ./lighthouse-report.html
```

## CI/CD Integration

### GitHub Actions Workflow
```yaml
name: Testing Pipeline

on: [push, pull_request]

jobs:
  backend-test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-go@v4
        with:
          go-version: '1.21'
      
      - name: Run tests
        run: go test ./... -cover -coverprofile=coverage.out
      
      - name: Upload coverage
        uses: codecov/codecov-action@v3
        with:
          file: ./coverage.out

  frontend-test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: '18'
      
      - name: Install dependencies
        run: npm ci
      
      - name: Run unit tests
        run: npm run test:ci
      
      - name: Run E2E tests
        run: npm run e2e:ci
      
      - name: Run accessibility tests
        run: axe http://localhost:4200 --exit
```

## Métricas de Éxito

### Cobertura de Código
- **Backend Go**: ≥80% líneas con testify
- **Frontend Angular**: ≥80% líneas con Jasmine + Karma
- **E2E**: 100% flujos críticos con Playwright
- **Accessibility**: 100% WCAG 2.2 AA compliance

### Performance
- **Unit Tests**: <5s ejecución total
- **E2E Tests**: <30s por test suite
- **Coverage Report**: <10s generación
- **CI Pipeline**: <10min ejecución completa

### Calidad
- **0 errores** en tests unitarios
- **0 errores** en tests E2E
- **0 vulnerabilidades** CRITICAL
- **100% compliance** WCAG 2.2 AA

**Estado**: ✅ ESTRATEGIA DE TESTING COMPLETA  
**Stack**: testify + Jasmine + Playwright  
**Metodología**: TDD-RunFix+ con prevención de errores  
**Cobertura**: ≥80% garantizada con quality gates
