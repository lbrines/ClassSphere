---
title: "ClassSphere - Fase 1: Fundaciones Go + Angular"
version: "3.0"
type: "development_plan"
priority: "CRITICAL"
max_tokens: 2000
duration: "12 días"
related_files:
  - "contracts/principal/05_ClassSphere_arquitectura.md"
  - "contracts/principal/09_ClassSphere_testing.md"
  - "contracts/principal/10_ClassSphere_plan_implementacion.md"
---

# Fase 1: Fundaciones - Stack Go + Angular 19

## 🎯 INICIO: Objetivos Críticos y Dependencias Bloqueantes

### Objetivo Principal
Establecer fundaciones sólidas con stack moderno Go + Angular 19, implementando autenticación completa, sistema de roles y testing con cobertura ≥80%.

### Dependencias Bloqueantes
- **Go 1.21+** instalado y configurado
- **Angular 19** con esbuild oficial
- **Docker** para containerización
- **GitHub Actions** para CI/CD
- **Redis** para caché (opcional en desarrollo)

### Stack Tecnológico Validado
**Backend (Go)**:
- Go 1.21+ (lenguaje compilado)
- Echo v4 (framework web)
- JWT + OAuth 2.0 Google
- Sistema de roles (admin > coordinator > teacher > student)
- Redis (caché compartido)
- testify + mock (testing)

**Frontend (Angular 19)**:
- Angular 19 (framework)
- esbuild (bundler oficial desde Angular 17)
- Vite (dev server integrado)
- TypeScript 5.x
- RxJS (reactive programming)
- TailwindCSS 3.x
- Jasmine + Karma (testing unit)
- Playwright (testing E2E)
- Biome (linter/formatter)

## 📅 MEDIO: Implementación Detallada Día por Día

### Día 1-2: Configuración Inicial Backend Go

**Objetivo**: Establecer estructura base del backend Go con Echo

**Pasos**:
```bash
# 1. Inicializar proyecto Go
mkdir classsphere-backend && cd classsphere-backend
go mod init github.com/classsphere/backend

# 2. Instalar dependencias
go get github.com/labstack/echo/v4
go get github.com/golang-jwt/jwt/v5
go get github.com/redis/go-redis/v9
go get github.com/stretchr/testify

# 3. Crear estructura de directorios
mkdir -p {cmd,internal/{auth,handlers,models,middleware,services},pkg,configs,tests}
```

**TDD Implementación**:
```go
// tests/auth_test.go - RED PHASE
func TestJWTAuth(t *testing.T) {
    // Test que falla inicialmente
    token, err := GenerateJWT("user@test.com", "admin")
    assert.NoError(t, err)
    assert.NotEmpty(t, token)
}

// internal/auth/jwt.go - GREEN PHASE
func GenerateJWT(email, role string) (string, error) {
    // Implementación mínima para pasar el test
    return "dummy-token", nil
}
```

**Validación**:
```bash
go test ./... -cover
# Objetivo: 80% cobertura en módulos críticos
```

### Día 3-4: Autenticación JWT + OAuth 2.0

**Objetivo**: Implementar sistema de autenticación completo

**Pasos**:
```bash
# 1. Configurar OAuth 2.0 Google
go get golang.org/x/oauth2
go get google.golang.org/api/oauth2/v2

# 2. Implementar handlers de autenticación
```

**TDD Implementación**:
```go
// tests/oauth_test.go
func TestGoogleOAuthCallback(t *testing.T) {
    mockGoogle := &MockGoogleService{}
    handler := NewAuthHandler(mockGoogle)
    
    // Test callback OAuth
    req := httptest.NewRequest("GET", "/auth/google/callback?code=test", nil)
    w := httptest.NewRecorder()
    
    err := handler.GoogleCallback(c, req)
    assert.NoError(t, err)
    assert.Equal(t, 200, w.Code)
}
```

**Patrones de Prevención Aplicados**:
- **AsyncMock**: Para métodos async de Google API
- **Server Restart**: `pkill -f classsphere-backend` → `PORT=8081 ./classsphere-backend`
- **CORS Tests**: Headers básicos verificables

### Día 5-6: Sistema de Roles y Middleware

**Objetivo**: Implementar autorización por roles

**TDD Implementación**:
```go
// tests/middleware_test.go
func TestRoleMiddleware(t *testing.T) {
    e := echo.New()
    req := httptest.NewRequest("GET", "/admin/dashboard", nil)
    req.Header.Set("Authorization", "Bearer admin-token")
    
    // Test middleware de roles
    handler := RoleMiddleware("admin")
    // Verificar que admin puede acceder
}
```

### Día 7-8: Configuración Frontend Angular 19

**Objetivo**: Establecer estructura base del frontend Angular

**Pasos**:
```bash
# 1. Crear proyecto Angular 19
npx @angular/cli@19 new classsphere-frontend --routing --style=scss
cd classsphere-frontend

# 2. Instalar dependencias adicionales
npm install @angular/material @angular/cdk
npm install tailwindcss @tailwindcss/typography
npm install @playwright/test

# 3. Configurar TailwindCSS
npx tailwindcss init
```

**TDD Implementación**:
```typescript
// src/app/services/auth.service.spec.ts
describe('AuthService', () => {
  let service: AuthService;
  
  beforeEach(() => {
    TestBed.configureTestingModule({});
    service = TestBed.inject(AuthService);
  });
  
  it('should login with valid credentials', () => {
    // Test que falla inicialmente
    expect(service.login('admin@classsphere.edu', 'secret')).toBeTruthy();
  });
});
```

**Patrones de Prevención Aplicados**:
- **Angular CLI**: `npx ng` en lugar de `ng`
- **TypeScript**: Optional chaining `?.prop?.subprop`
- **TailwindCSS**: v3.4.0 para Angular, evitar CDN

### Día 9-10: Integración Frontend-Backend

**Objetivo**: Conectar frontend Angular con backend Go

**TDD Implementación**:
```typescript
// src/app/services/api.service.spec.ts
describe('ApiService', () => {
  it('should authenticate with backend', async () => {
    const mockResponse = { token: 'jwt-token', user: { role: 'admin' } };
    
    // Mock HTTP service
    httpClientSpy.post.and.returnValue(of(mockResponse));
    
    const result = await apiService.login('admin@test.com', 'password');
    expect(result.token).toBe('jwt-token');
  });
});
```

### Día 11-12: Testing Completo y CI/CD

**Objetivo**: Alcanzar cobertura ≥80% y configurar CI/CD

**Pasos**:
```bash
# Backend testing
go test ./... -cover -coverprofile=coverage.out
go tool cover -html=coverage.out -o coverage.html

# Frontend testing
ng test --watch=false --browsers=ChromeHeadless
ng e2e --configuration=ci

# Configurar GitHub Actions
mkdir -p .github/workflows
```

**TDD Implementación**:
```yaml
# .github/workflows/ci.yml
name: CI/CD Pipeline
on: [push, pull_request]
jobs:
  backend-test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-go@v4
        with:
          go-version: '1.21'
      - run: go test ./... -cover
        env:
          COVERAGE_THRESHOLD: 80
```

## ✅ FINAL: Checklist Verificación y Próximos Pasos

### Criterios de Aceptación Fase 1
- [ ] **Backend Go**: API REST funcionando en puerto 8081
- [ ] **Autenticación**: JWT + OAuth 2.0 Google operativo
- [ ] **Sistema de Roles**: admin > coordinator > teacher > student
- [ ] **Frontend Angular**: Aplicación funcionando en puerto 4200
- [ ] **Testing**: Cobertura ≥80% backend y frontend
- [ ] **CI/CD**: Pipeline GitHub Actions funcionando
- [ ] **Docker**: Containerización básica configurada

### Comandos de Verificación
```bash
# Verificar backend
curl http://localhost:8081/health
curl http://localhost:8081/auth/google

# Verificar frontend
curl http://localhost:4200
ng test --watch=false

# Verificar cobertura
go test ./... -cover | grep "coverage:"
ng test --code-coverage --watch=false
```

### Errores Críticos Prevenidos
- **Dashboard Endpoints 404**: Server restart protocol implementado
- **TypeScript Compilation**: Optional chaining completo aplicado
- **OAuth Tests Hanging**: Timeout 10s configurado
- **Angular CLI Not Found**: `npx ng` en lugar de `ng`
- **TailwindCSS Issues**: v3.4.0 para Angular

### Próximos Pasos
1. **Iniciar Fase 2**: Google Classroom API integration
2. **Configurar mocks**: Sistema de alternancia Google/Mock
3. **Implementar dashboards**: Por rol específico
4. **Validar patrones**: Aplicar prevención de errores

### Métricas de Éxito
- **Cobertura Backend**: ≥80% con testify
- **Cobertura Frontend**: ≥80% con Jasmine + Karma
- **Performance**: <3s load time
- **Vulnerabilidades**: 0 CRITICAL
- **Errores Resueltos**: 14 errores bloqueadores previstos

**Estado**: ✅ LISTO PARA FASE 2  
**Duración**: 12 días  
**Stack**: Go 1.21+ + Angular 19 + TDD-RunFix+  
**Cobertura**: ≥80% testing garantizado
