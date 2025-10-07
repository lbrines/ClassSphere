# 📋 CHECKLIST DE TAREAS PENDIENTES - FASE 1

**Proyecto**: ClassSphere  
**Fase**: 1 - Fundaciones (Backend Go + Frontend Angular)  
**Duración Total**: 12 días  
**Progreso Actual**: ~70% (6/12 días completados)  
**Fecha**: 2025-10-07

---

## 🎯 RESUMEN EJECUTIVO

### Estado General
- ✅ **Completado**: Backend Go + Frontend Angular básicos funcionando
- ✅ **Completado**: go.mod corregido, tests backend ejecutándose
- ⚠️ **En Progreso**: Mejorando cobertura de tests
- 🔴 **Crítico**: Redis no operacional, E2E tests faltantes

### Métricas Actuales (ACTUALIZADO 2025-10-07)
- **Backend**: Puerto 8080 ✅ | Tests ✅ (todos pasan) | **Coverage 89.9%** ✅✅
  - cmd/api: 71.9% ⚠️ (necesita +8.1%)
  - adapters/cache: 100.0% ✅✅✅
  - adapters/http: 98.5% ✅✅✅ (objetivo 90% SUPERADO)
  - adapters/oauth: 92.1% ✅✅✅ (objetivo 90% SUPERADO)
  - adapters/repo: 95.0% ✅✅
  - app: 92.1% ✅✅✅ (objetivo 90% SUPERADO)
  - domain: 100.0% ✅✅✅
  - shared: 78.9% ⚠️ (necesita +1.1%)
  - **TOTAL GLOBAL**: 89.9% ✅✅ (objetivo ≥80% SUPERADO)
  - **MÓDULOS CRÍTICOS**: TODOS ≥90% ✅✅✅
- **Frontend**: Puerto 4200 ✅ | Tests ❓ | Coverage ❓
- **Integración**: Login ✅ | OAuth ⚠️ (placeholders) | E2E ❌

---

## 🔴 PRIORIDAD CRÍTICA (Bloqueantes)

### 1. ✅ Corregir go.mod (Backend) - COMPLETADO

**Problema**: Versión de Go incorrecta impide ejecutar tests (RESUELTO)
```go
// Archivo: backend/go.mod línea 3
// ERROR ACTUAL:
go 1.24.0    // ❌ Formato inválido
toolchain    // ❌ Directiva desconocida

// DEBE SER:
go 1.24      // ✅ Sin patch version
```

**Comandos de Corrección**:
```bash
cd /home/lbrines/projects/AI/ClassSphere/backend
# Editar go.mod manualmente o usar sed:
sed -i 's/go 1\.24\.0/go 1.24/' go.mod
# Eliminar línea toolchain si existe
sed -i '/^toolchain/d' go.mod
# Verificar
go mod verify
go mod tidy
```

**Criterio de Aceptación**:
- [x] `go mod verify` sin errores ✅
- [x] `go test ./...` ejecutable ✅
- [x] Sin warnings de versión ✅

**Resultado**: COMPLETADO (2025-10-07)
- go.mod corregido: `go 1.24.0` → `go 1.24`
- Toolchain eliminada
- Usando Go 1.24.7 de `/workspace/tools/go1.24.7`
- Todos los tests ejecutándose correctamente

---

### 2. ✅ Verificar y Completar Test Coverage Backend - CASI COMPLETADO

**Requisito del Plan**: ≥80% global, ≥90% módulos críticos

**Estado Actual**: **89.9% global** ✅✅ | **Módulos críticos TODOS ≥90%** ✅✅✅

**Comandos de Verificación**:
```bash
cd /home/lbrines/projects/AI/ClassSphere/backend

# Ejecutar todos los tests
go test ./... -v

# Verificar cobertura
go test ./... -cover

# Generar reporte detallado
go test ./... -coverprofile=coverage.out
go tool cover -html=coverage.out -o coverage.html

# Verificar módulos críticos (debe ser ≥90%)
go test ./internal/app/... -cover        # AuthService, UserService
go test ./internal/adapters/http/... -cover  # Handlers, Middleware
go test ./internal/adapters/oauth/... -cover # OAuth Google
```

**Archivos Verificados**:
- [x] `internal/domain/` - Coverage 100.0% ✅ EXCELENTE
- [x] `internal/adapters/cache/` - Coverage 100.0% ✅ EXCELENTE
- [x] `internal/adapters/repo/` - Coverage 95.0% ✅ EXCELENTE
- [x] `internal/adapters/http/` - Coverage 83.1% ✅
- [x] `internal/adapters/oauth/` - Coverage 81.6% ✅
- [ ] `cmd/api/` - Coverage 71.9% ❌ (necesita +8.1%)
- [ ] `internal/app/` - Coverage 75.0% ❌ (necesita +5%)
- [ ] `internal/shared/` - Coverage 78.9% ❌ (necesita +1.1%)

**Criterio de Aceptación**:
- [x] Todos los tests pasan (100%) ✅
- [x] Reporte HTML generado ✅ (`coverage.html`)
- [ ] Coverage global ≥80% ⚠️ (actual: 85.7% promedio, pero 3 módulos bajo 80%)
- [ ] Coverage módulos críticos ≥90% ⚠️ (adapters críticos: OK, app: 75%)
- [ ] 0 race conditions ⚠️ (1 test falla con -race: TestMainFunction timeout)

**Próximo Paso**: Mejorar cobertura en cmd/api, internal/app, internal/shared

**Estimación Restante**: 1-2 horas  
**Bloqueado por**: ~~Tarea #1 (go.mod)~~ DESBLOQUEADO ✅  
**Prioridad**: ALTA (bajó de CRÍTICA)

---

### 3. ✅ Verificar y Completar Test Coverage Frontend - COMPLETADO

**Requisito del Plan**: ≥80% líneas, Jasmine + Karma

**Estado Final**: **93.45% statements, 93.81% lines** ✅✅✅

**Comandos de Verificación**:
```bash
cd /home/lbrines/projects/AI/ClassSphere/frontend

# Ejecutar todos los tests
npm test

# Generar reporte de cobertura
npm run test -- --code-coverage --watch=false

# Verificar archivo de configuración
cat karma.conf.js
cat src/test.ts
```

**Archivos Verificados**:
- [x] `core/services/auth.service.spec.ts` - Coverage 100% ✅✅✅
- [x] `core/guards/auth.guard.spec.ts` - Coverage 100% ✅✅✅
- [x] `core/guards/role.guard.spec.ts` - Coverage 100% ✅✅✅
- [x] `core/interceptors/auth.interceptor.spec.ts` - Coverage 100% ✅✅✅
- [x] `shared/components/login-form/*.spec.ts` - Coverage 100% ✅✅✅
- [x] `features/dashboard/**/*.spec.ts` - Coverage 100% ✅✅✅ (agregados)
- [x] `features/auth/pages/login/*.spec.ts` - Coverage 100% ✅✅✅ (agregado)

**Tests Creados Nuevos** (20 tests):
- ✅ admin-dashboard.component.spec.ts
- ✅ coordinator-dashboard.component.spec.ts
- ✅ teacher-dashboard.component.spec.ts
- ✅ student-dashboard.component.spec.ts
- ✅ dashboard-layout.component.spec.ts
- ✅ login.page.spec.ts

**Criterio de Aceptación**:
- [x] Todos los tests pasan (100%) ✅ (38/38)
- [x] Coverage global ≥80% ✅ (93.45%)
- [x] Coverage servicios core ≥90% ✅ (90%)
- [x] Reporte en `coverage/frontend/index.html` ✅
- [x] Sin errores de consola ✅

**Resultado**: COMPLETADO (2025-10-07)
- 38 tests implementados (18 originales + 20 nuevos)
- Coverage: 93.45% statements, 93.81% lines
- Tiempo ejecución: 0.5 segundos
- Framework: Jasmine + Karma + Chrome

---

### 4. ❌ Instalar y Configurar Redis

**Requisito del Plan**: Redis para cache y sesiones (Días 4-6)

**Comandos de Instalación**:
```bash
# Instalar Redis
sudo apt-get update
sudo apt-get install -y redis-server

# Configurar Redis
sudo systemctl enable redis-server
sudo systemctl start redis-server

# Verificar instalación
redis-cli ping
# Debe responder: PONG

# Verificar puerto
lsof -i :6379
```

**Configuración Backend**:
```bash
# Archivo: backend/.env (crear si no existe)
REDIS_ADDR=localhost:6379
REDIS_PASSWORD=
REDIS_DB=0
```

**Tests de Verificación**:
```bash
cd /home/lbrines/projects/AI/ClassSphere/backend

# Test específico de Redis
go test ./internal/adapters/cache/... -v

# Verificar conexión desde Go
go run -exec 'echo "Testing Redis..."' cmd/api/main.go
```

**Criterio de Aceptación**:
- [ ] Redis server corriendo
- [ ] `redis-cli ping` responde PONG
- [ ] Backend conecta a Redis sin errores
- [ ] Tests de `redis_cache_test.go` pasan
- [ ] Cache funcional para sesiones JWT

**Estimación**: 30 minutos  
**Bloqueado por**: Ninguno  
**Prioridad**: CRÍTICA

---

## 🟠 PRIORIDAD ALTA (Completar Fase 1)

### 5. ❌ Implementar E2E Tests con Playwright

**Requisito del Plan**: Día 12 - Tests E2E flujos críticos

**Instalación Playwright**:
```bash
cd /home/lbrines/projects/AI/ClassSphere/frontend

# Instalar Playwright
npm install -D @playwright/test@^1.48.2

# Inicializar configuración
npx playwright install
npx playwright install-deps

# Crear estructura
mkdir -p e2e
```

**Tests a Crear**:

#### `e2e/auth-flow.spec.ts`
```typescript
import { test, expect } from '@playwright/test';

test.describe('Authentication Flow', () => {
  test('should login with valid credentials', async ({ page }) => {
    await page.goto('http://localhost:4200/auth/login');
    await page.fill('#email', 'admin@classsphere.edu');
    await page.fill('#password', 'admin123');
    await page.click('button[type="submit"]');
    await expect(page).toHaveURL(/\/dashboard/);
  });

  test('should show error with invalid credentials', async ({ page }) => {
    await page.goto('http://localhost:4200/auth/login');
    await page.fill('#email', 'invalid@test.com');
    await page.fill('#password', 'wrong');
    await page.click('button[type="submit"]');
    await expect(page.locator('.text-red-300')).toBeVisible();
  });
});
```

#### `e2e/oauth-flow.spec.ts`
```typescript
test.describe('OAuth Google Flow', () => {
  test('should redirect to Google OAuth', async ({ page }) => {
    await page.goto('http://localhost:4200/auth/login');
    await page.click('button:has-text("Continue with Google")');
    await page.waitForURL(/accounts\.google\.com/);
    expect(page.url()).toContain('accounts.google.com');
  });
});
```

#### `e2e/role-based-routing.spec.ts`
```typescript
test.describe('Role-Based Dashboards', () => {
  test('admin should see admin dashboard', async ({ page }) => {
    // Login as admin
    await page.goto('http://localhost:4200/auth/login');
    await page.fill('#email', 'admin@classsphere.edu');
    await page.fill('#password', 'admin123');
    await page.click('button[type="submit"]');
    
    // Verify admin dashboard
    await expect(page.locator('h2:has-text("Administrator Overview")')).toBeVisible();
  });

  test('coordinator should see coordinator dashboard', async ({ page }) => {
    await page.goto('http://localhost:4200/auth/login');
    await page.fill('#email', 'coordinator@classsphere.edu');
    await page.fill('#password', 'coord123');
    await page.click('button[type="submit"]');
    await expect(page.locator('h2:has-text("Coordinator Console")')).toBeVisible();
  });
});
```

**Configuración**:
```typescript
// playwright.config.ts
import { defineConfig } from '@playwright/test';

export default defineConfig({
  testDir: './e2e',
  use: {
    baseURL: 'http://localhost:4200',
    screenshot: 'only-on-failure',
  },
  webServer: {
    command: 'npm start',
    port: 4200,
    reuseExistingServer: true,
  },
});
```

**Criterio de Aceptación**:
- [ ] Playwright instalado y configurado
- [ ] Test login flow end-to-end ✅
- [ ] Test OAuth redirect ✅
- [ ] Test role-based routing ✅
- [ ] Test protected routes ✅
- [ ] Screenshots on failure
- [ ] Todos los tests E2E pasan

**Estimación**: 3-4 horas  
**Bloqueado por**: Ninguno  
**Prioridad**: ALTA

---

### 6. ❌ Crear .env.example

**Requisito del Plan**: Día 1 - Documentar variables de entorno

**Archivos a Crear**:

#### `backend/.env.example`
```bash
# JWT Configuration
JWT_SECRET=your-secret-key-min-32-chars-change-in-production-xxxxxxxxxxxx

# Google OAuth 2.0
GOOGLE_CLIENT_ID=your-client-id.apps.googleusercontent.com
GOOGLE_CLIENT_SECRET=GOCSPX-your-client-secret
GOOGLE_REDIRECT_URL=http://localhost:4200/auth/callback

# Server Configuration
APP_ENV=development
SERVER_PORT=8080
LOG_LEVEL=debug

# Redis Configuration
REDIS_ADDR=localhost:6379
REDIS_PASSWORD=
REDIS_DB=0

# CORS Configuration
CORS_ALLOWED_ORIGINS=http://localhost:4200,http://localhost:4200/
```

#### `frontend/.env.example`
```bash
# API Configuration
API_URL=http://localhost:8080/api/v1

# Environment
NODE_ENV=development

# Feature Flags
ENABLE_OAUTH=true
ENABLE_ANALYTICS=false
```

**Documentación**:

#### `backend/README.md` (actualizar)
```markdown
## Environment Variables

Copy `.env.example` to `.env` and configure:

```bash
cp .env.example .env
# Edit .env with your values
```

### Required Variables
- `JWT_SECRET`: Min 32 chars, change in production
- `GOOGLE_CLIENT_ID`: Get from Google Cloud Console
- `GOOGLE_CLIENT_SECRET`: Get from Google Cloud Console

### Optional Variables
- `REDIS_ADDR`: Default localhost:6379
- `LOG_LEVEL`: debug|info|warn|error
```

**Criterio de Aceptación**:
- [ ] `backend/.env.example` creado
- [ ] `frontend/.env.example` creado
- [ ] Documentación en READMEs
- [ ] Instrucciones de configuración claras
- [ ] Valores ejemplo seguros (no secretos reales)

**Estimación**: 30 minutos  
**Bloqueado por**: Ninguno  
**Prioridad**: ALTA

---

### 7. ⚠️ Configurar Google OAuth Real

**Requisito del Plan**: Día 3 - OAuth 2.0 Google completo

**Estado Actual**: Placeholders de desarrollo
```bash
GOOGLE_CLIENT_ID=dev-client-id.apps.googleusercontent.com  # ❌ Placeholder
GOOGLE_CLIENT_SECRET=dev-client-secret-GOCSPX-xxxxx       # ❌ Placeholder
```

**Pasos para Configuración Real**:

#### 1. Google Cloud Console
```bash
1. Ir a: https://console.cloud.google.com
2. Crear nuevo proyecto: "ClassSphere"
3. Habilitar APIs:
   - Google+ API
   - Google Classroom API
   - People API
4. Configurar OAuth Consent Screen:
   - User Type: External
   - App name: ClassSphere
   - User support email: tu-email@gmail.com
   - Authorized domains: localhost (para desarrollo)
   - Scopes:
     * .../auth/userinfo.email
     * .../auth/userinfo.profile
     * .../auth/classroom.courses.readonly
```

#### 2. Crear OAuth 2.0 Credentials
```bash
1. Credentials → Create Credentials → OAuth 2.0 Client ID
2. Application type: Web application
3. Name: ClassSphere Backend
4. Authorized JavaScript origins:
   - http://localhost:4200
   - http://localhost:8080
5. Authorized redirect URIs:
   - http://localhost:4200/auth/callback
   - http://localhost:8080/api/v1/auth/oauth/callback
6. Copiar Client ID y Client Secret
```

#### 3. Actualizar Backend
```bash
cd /home/lbrines/projects/AI/ClassSphere/backend
# Editar .env con credenciales reales
export GOOGLE_CLIENT_ID="tu-client-id.apps.googleusercontent.com"
export GOOGLE_CLIENT_SECRET="GOCSPX-tu-client-secret-real"
export GOOGLE_REDIRECT_URL="http://localhost:4200/auth/callback"
```

#### 4. Probar OAuth Flow
```bash
# Terminal 1: Backend
cd backend
go run cmd/api/main.go

# Terminal 2: Frontend
cd frontend
npm start

# Terminal 3: Test
curl http://localhost:8080/api/v1/auth/oauth/google
# Copiar URL y abrir en navegador
# Completar flujo OAuth
```

**Criterio de Aceptación**:
- [ ] Proyecto Google Cloud creado
- [ ] OAuth Consent Screen configurado
- [ ] Client ID y Secret obtenidos
- [ ] Backend actualizado con credenciales reales
- [ ] OAuth flow funciona end-to-end
- [ ] Usuario puede hacer login con Google
- [ ] Token JWT generado tras OAuth exitoso

**Estimación**: 1-2 horas  
**Bloqueado por**: Ninguno  
**Prioridad**: ALTA (pero puede ser opcional para desarrollo)

---

### 8. ❌ Verificar Middleware Completo (Días 4-6)

**Requisito del Plan**: Role-based middleware, rate limiting, logging

**Archivos a Verificar**:

#### `internal/adapters/http/middleware.go`
```go
// Debe contener:
- JWTMiddleware() - Verificación de tokens ✅
- RoleMiddleware(roles ...Role) - Control de acceso por rol
- RateLimitMiddleware() - Límite de requests
- LoggingMiddleware() - Logging estructurado
- CORSMiddleware() - Configuración CORS ✅
- RecoverMiddleware() - Panic recovery ✅
```

**Tests a Verificar**:

#### `internal/adapters/http/middleware_test.go`
```bash
# Debe existir y cubrir:
- TestJWTMiddleware_ValidToken
- TestJWTMiddleware_InvalidToken
- TestJWTMiddleware_MissingToken
- TestRoleMiddleware_Authorized
- TestRoleMiddleware_Unauthorized
- TestRateLimitMiddleware_UnderLimit
- TestRateLimitMiddleware_ExceedsLimit
- TestLoggingMiddleware
- TestCORSMiddleware
```

**Comandos de Verificación**:
```bash
cd /home/lbrines/projects/AI/ClassSphere/backend

# Verificar middleware implementado
grep -r "func.*Middleware" internal/adapters/http/

# Ejecutar tests de middleware
go test ./internal/adapters/http/... -v -cover

# Verificar rate limiting funcional
for i in {1..100}; do 
  curl -s http://localhost:8080/api/v1/auth/login > /dev/null
done
# Debe recibir 429 Too Many Requests
```

**Criterio de Aceptación**:
- [ ] JWT middleware funcionando
- [ ] Role middleware implementado y testeado
- [ ] Rate limiting configurado (100 req/min por IP)
- [ ] Logging estructurado (JSON format)
- [ ] CORS configurado correctamente
- [ ] Tests middleware ≥90% coverage
- [ ] Documentación de uso

**Estimación**: 2-3 horas  
**Bloqueado por**: Tarea #4 (Redis para rate limiting)  
**Prioridad**: ALTA

---

### 9. ❌ Scripts de Verificación Automatizada

**Requisito del Plan**: Día 12 - Scripts de validación completa

**Scripts a Crear**:

#### `scripts/verify-phase1.sh`
```bash
#!/bin/bash
set -e

echo "🔍 Verificando Fase 1 - ClassSphere"
echo "===================================="

# 1. Backend Health
echo -n "Backend (8080)... "
if curl -sf http://localhost:8080/health > /dev/null; then
    echo "✅"
else
    echo "❌ FAILED"
    exit 1
fi

# 2. Frontend Health
echo -n "Frontend (4200)... "
if curl -sf http://localhost:4200 > /dev/null; then
    echo "✅"
else
    echo "❌ FAILED"
    exit 1
fi

# 3. Redis Connection
echo -n "Redis (6379)... "
if redis-cli ping > /dev/null 2>&1; then
    echo "✅"
else
    echo "⚠️  WARNING: Redis not available"
fi

# 4. Backend Tests
echo -n "Backend Tests... "
cd backend
if go test ./... -cover > /tmp/backend-tests.log 2>&1; then
    COVERAGE=$(go test ./... -cover 2>&1 | grep "coverage:" | awk '{sum+=$3; n++} END {print sum/n}')
    echo "✅ Coverage: ${COVERAGE}%"
else
    echo "❌ FAILED"
    cat /tmp/backend-tests.log
    exit 1
fi
cd ..

# 5. Frontend Tests
echo -n "Frontend Tests... "
cd frontend
if npm test -- --watch=false --code-coverage > /tmp/frontend-tests.log 2>&1; then
    echo "✅"
else
    echo "❌ FAILED"
    cat /tmp/frontend-tests.log
    exit 1
fi
cd ..

# 6. E2E Tests
echo -n "E2E Tests... "
cd frontend
if npm run test:e2e > /tmp/e2e-tests.log 2>&1; then
    echo "✅"
else
    echo "⚠️  WARNING: E2E tests failed or not configured"
fi
cd ..

echo ""
echo "✅ Fase 1 Verification Complete!"
```

#### `scripts/health-check.sh`
```bash
#!/bin/bash

echo "🏥 Health Check - ClassSphere"
echo "============================="

# Backend
if curl -sf http://localhost:8080/health; then
    echo "✅ Backend: Healthy"
else
    echo "❌ Backend: Unhealthy"
fi

# Frontend
if curl -sf http://localhost:4200; then
    echo "✅ Frontend: Healthy"
else
    echo "❌ Frontend: Unhealthy"
fi

# Redis
if redis-cli ping > /dev/null 2>&1; then
    echo "✅ Redis: Connected"
else
    echo "⚠️  Redis: Disconnected"
fi

# Ports
echo ""
echo "Ports:"
lsof -i :8080 -i :4200 -i :6379 | grep LISTEN
```

#### `scripts/run-all-tests.sh`
```bash
#!/bin/bash
set -e

echo "🧪 Running All Tests - ClassSphere"
echo "=================================="

# Backend
echo "📦 Backend Tests..."
cd backend
go test ./... -v -cover -race
cd ..

# Frontend Unit
echo "📦 Frontend Unit Tests..."
cd frontend
npm test -- --watch=false --code-coverage
cd ..

# E2E
echo "📦 E2E Tests..."
cd frontend
npm run test:e2e
cd ..

echo ""
echo "✅ All Tests Passed!"
```

**Hacer scripts ejecutables**:
```bash
chmod +x scripts/*.sh
```

**Criterio de Aceptación**:
- [ ] `verify-phase1.sh` creado y ejecutable
- [ ] `health-check.sh` creado y ejecutable
- [ ] `run-all-tests.sh` creado y ejecutable
- [ ] Scripts verifican todos los servicios
- [ ] Scripts reportan coverage
- [ ] Scripts tienen exit codes correctos
- [ ] Documentación en README

**Estimación**: 1 hora  
**Bloqueado por**: Tareas #1, #2, #3, #5  
**Prioridad**: ALTA

---

## 🟡 PRIORIDAD MEDIA (Mejoras)

### 10. ❌ CI/CD Pipeline Básico

**Requisito del Plan**: GitHub Actions para testing automático

**Archivos a Crear**:

#### `.github/workflows/backend-tests.yml`
```yaml
name: Backend Tests

on:
  push:
    branches: [main, develop]
    paths:
      - 'backend/**'
  pull_request:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest
    
    services:
      redis:
        image: redis:7-alpine
        ports:
          - 6379:6379
    
    steps:
      - uses: actions/checkout@v3
      
      - name: Setup Go
        uses: actions/setup-go@v4
        with:
          go-version: '1.24'
      
      - name: Install dependencies
        working-directory: ./backend
        run: go mod download
      
      - name: Run tests
        working-directory: ./backend
        run: go test ./... -v -cover -race
      
      - name: Check coverage
        working-directory: ./backend
        run: |
          go test ./... -coverprofile=coverage.out
          go tool cover -func=coverage.out
          COVERAGE=$(go tool cover -func=coverage.out | grep total | awk '{print $3}' | sed 's/%//')
          if (( $(echo "$COVERAGE < 80" | bc -l) )); then
            echo "Coverage $COVERAGE% is below 80%"
            exit 1
          fi
```

#### `.github/workflows/frontend-tests.yml`
```yaml
name: Frontend Tests

on:
  push:
    branches: [main, develop]
    paths:
      - 'frontend/**'
  pull_request:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest
    
    steps:
      - uses: actions/checkout@v3
      
      - name: Setup Node.js
        uses: actions/setup-node@v3
        with:
          node-version: '18'
          cache: 'npm'
          cache-dependency-path: './frontend/package-lock.json'
      
      - name: Install dependencies
        working-directory: ./frontend
        run: npm ci
      
      - name: Run tests
        working-directory: ./frontend
        run: npm test -- --watch=false --code-coverage
      
      - name: Check coverage
        working-directory: ./frontend
        run: |
          COVERAGE=$(cat coverage/frontend/coverage-summary.json | jq '.total.lines.pct')
          if (( $(echo "$COVERAGE < 80" | bc -l) )); then
            echo "Coverage $COVERAGE% is below 80%"
            exit 1
          fi
```

#### `.github/workflows/e2e-tests.yml`
```yaml
name: E2E Tests

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest
    
    steps:
      - uses: actions/checkout@v3
      
      - name: Setup Node.js
        uses: actions/setup-node@v3
        with:
          node-version: '18'
      
      - name: Setup Go
        uses: actions/setup-go@v4
        with:
          go-version: '1.24'
      
      - name: Install Playwright
        working-directory: ./frontend
        run: |
          npm ci
          npx playwright install --with-deps
      
      - name: Start Backend
        working-directory: ./backend
        run: |
          go run cmd/api/main.go &
          sleep 5
      
      - name: Run E2E Tests
        working-directory: ./frontend
        run: npm run test:e2e
      
      - name: Upload test results
        if: failure()
        uses: actions/upload-artifact@v3
        with:
          name: playwright-report
          path: frontend/playwright-report/
```

**Criterio de Aceptación**:
- [ ] Workflows creados en `.github/workflows/`
- [ ] Backend tests ejecutan en CI
- [ ] Frontend tests ejecutan en CI
- [ ] E2E tests ejecutan en CI
- [ ] Coverage verificado en CI (≥80%)
- [ ] Redis disponible en CI para tests
- [ ] Badges en README.md

**Estimación**: 2 horas  
**Bloqueado por**: Tareas #1, #2, #3, #5  
**Prioridad**: MEDIA

---

### 11. ❌ Documentación de Deployment

**Requisito**: Documentar proceso de despliegue

**Archivos a Crear/Actualizar**:

#### `backend/README.md`
```markdown
# ClassSphere Backend

## Quick Start

### Development
```bash
# Install dependencies
go mod download

# Run server
go run cmd/api/main.go

# Run tests
go test ./... -v -cover
```

### Environment Variables
See `.env.example` for required configuration.

### Deployment
See `docs/DEPLOYMENT.md`

## Architecture
- **Framework**: Echo v4
- **Language**: Go 1.24
- **Auth**: JWT + OAuth 2.0 Google
- **Cache**: Redis
- **Port**: 8080 (mandatory)
```

#### `frontend/README.md`
```markdown
# ClassSphere Frontend

## Quick Start

### Development
```bash
# Install dependencies
npm install

# Run dev server
npm start

# Run tests
npm test

# Build production
npm run build
```

### Environment Variables
See `.env.example`

## Architecture
- **Framework**: Angular 19
- **Bundler**: esbuild
- **Styling**: TailwindCSS 3
- **Testing**: Jasmine + Karma + Playwright
```

#### `docs/DEPLOYMENT.md`
```markdown
# Deployment Guide

## Prerequisites
- Go 1.24+
- Node.js 18+
- Redis 7+
- Docker (optional)

## Production Deployment

### Backend
```bash
cd backend
go build -o classsphere-backend cmd/api/main.go
./classsphere-backend
```

### Frontend
```bash
cd frontend
npm run build
# Serve dist/frontend/browser/
```

## Docker Deployment
Coming in Phase 5
```

**Criterio de Aceptación**:
- [ ] READMEs actualizados
- [ ] Guía de deployment creada
- [ ] Instrucciones claras y probadas
- [ ] Troubleshooting incluido

**Estimación**: 1 hora  
**Prioridad**: MEDIA

---

### 12. ⚠️ Health Checks Avanzados

**Mejora**: Health checks más detallados

#### `backend/internal/adapters/http/health_handler.go`
```go
func (h *Handler) HealthDetailed(c echo.Context) error {
    health := map[string]interface{}{
        "status": "ok",
        "timestamp": time.Now(),
        "services": map[string]bool{
            "database": h.checkDatabase(),
            "redis":    h.checkRedis(),
            "google":   true, // Always true in dev
        },
        "version": "1.0.0",
        "uptime":  time.Since(startTime).Seconds(),
    }
    
    allHealthy := true
    for _, status := range health["services"].(map[string]bool) {
        if !status {
            allHealthy = false
            break
        }
    }
    
    if !allHealthy {
        return c.JSON(http.StatusServiceUnavailable, health)
    }
    
    return c.JSON(http.StatusOK, health)
}
```

**Endpoints**:
- `GET /health` - Simple check
- `GET /health/detailed` - Detailed status
- `GET /metrics` - Prometheus metrics (futuro)

**Criterio de Aceptación**:
- [ ] Health checks detallados implementados
- [ ] Status de servicios externos verificado
- [ ] Uptime tracking
- [ ] Version info en respuesta

**Estimación**: 1 hora  
**Prioridad**: MEDIA

---

## 📊 MÉTRICAS DE ACEPTACIÓN FASE 1

### Backend ✅/❌
- [ ] Server corriendo en puerto 8080
- [ ] Health endpoint responde
- [ ] Login endpoint funcional
- [ ] OAuth Google flow completo
- [ ] JWT tokens generados y verificados
- [ ] Role system implementado
- [ ] Redis conectado y funcional
- [ ] Tests pasando: `go test ./... -v`
- [ ] Coverage ≥80% global
- [ ] Coverage ≥90% módulos críticos
- [ ] 0 race conditions
- [ ] go.mod válido

### Frontend ✅/❌
- [ ] App corriendo en puerto 4200
- [ ] LoginForm component renderiza
- [ ] OAuth button redirige a Google
- [ ] AuthGuard protege rutas
- [ ] RoleGuard implementado
- [ ] JWT token en localStorage
- [ ] Role-based routing funcional
- [ ] Tests pasando: `ng test`
- [ ] Coverage ≥80% global
- [ ] Coverage ≥90% services
- [ ] UI responsive
- [ ] Sin errores de consola

### Integración ✅/❌
- [ ] Frontend llama backend API
- [ ] Login flow end-to-end funciona
- [ ] OAuth flow end-to-end funciona
- [ ] Rutas protegidas requieren auth
- [ ] Role-based access funciona
- [ ] Error handling user-friendly
- [ ] CORS configurado correctamente
- [ ] E2E tests pasan

### Infrastructure ✅/❌
- [ ] Redis instalado y corriendo
- [ ] Scripts de verificación funcionan
- [ ] .env.example documentado
- [ ] READMEs actualizados
- [ ] CI/CD básico configurado

---

## 🚀 COMANDOS DE VALIDACIÓN FINAL

```bash
# 1. Verificación Completa
./scripts/verify-phase1.sh

# 2. Health Check
./scripts/health-check.sh

# 3. Run All Tests
./scripts/run-all-tests.sh

# 4. Backend Manual
cd backend
go test ./... -v -cover -race
go run cmd/api/main.go

# 5. Frontend Manual
cd frontend
npm test -- --watch=false --code-coverage
npm run test:e2e
npm start

# 6. Integration Test
curl -X POST http://localhost:8080/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"admin@classsphere.edu","password":"admin123"}'

# 7. OAuth Test
curl http://localhost:8080/api/v1/auth/oauth/google
```

---

## 📅 ESTIMACIÓN TEMPORAL

### Por Prioridad
- **CRÍTICA** (Tareas 1-4): 6-8 horas
- **ALTA** (Tareas 5-9): 10-13 horas
- **MEDIA** (Tareas 10-12): 4-5 horas

### Total Estimado
**20-26 horas** (~3-4 días de trabajo)

### Desglose por Día
- **Día 7**: Tareas 1-3 (Corregir go.mod, tests backend/frontend)
- **Día 8**: Tareas 4-5 (Redis, E2E tests)
- **Día 9**: Tareas 6-8 (.env, OAuth real, middleware)
- **Día 10**: Tarea 9 + validación (Scripts, verificación)
- **Día 11-12**: Tareas 10-12 (CI/CD, docs) + buffer

---

## 🎯 PRÓXIMOS PASOS INMEDIATOS

### Acción Inmediata
1. **Corregir go.mod** (15 min)
2. **Verificar tests backend** (1 hora)
3. **Instalar Redis** (30 min)
4. **Verificar tests frontend** (1 hora)

### Orden Sugerido
```bash
# 1. Fix go.mod
cd backend
sed -i 's/go 1\.24\.0/go 1.24/' go.mod
sed -i '/^toolchain/d' go.mod
go mod tidy

# 2. Run backend tests
go test ./... -v -cover

# 3. Install Redis
sudo apt-get install -y redis-server
sudo systemctl start redis-server

# 4. Run frontend tests
cd ../frontend
npm test -- --watch=false --code-coverage

# 5. Continue with E2E tests...
```

---

## 📝 NOTAS FINALES

- **Estado Actual**: ~70% Fase 1 completado
- **Bloqueador Principal**: go.mod inválido
- **Días Restantes**: 6-7 de 12 total
- **Prioridad**: Desbloquear tests → Verificar coverage → E2E tests

**Última Actualización**: 2025-10-07  
**Revisado por**: AI Assistant  
**Basado en**: Plan Fase 1 (workspace/plan/02_plan_fase1_fundaciones.md)

---

## 🔗 REFERENCIAS

- Plan Fase 1: `workspace/plan/02_plan_fase1_fundaciones.md`
- Estado Servicios: `workspace/SERVICES_STATUS.md`
- Solución Auth: `workspace/SOLUCION_AUTH_FRONTEND.md`
- Contratos: `workspace/contracts/`
- Plan General: `workspace/plan/01_plan_index.md`

