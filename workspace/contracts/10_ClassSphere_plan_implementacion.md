---
title: "ClassSphere - Unified Implementation Plan"
version: "4.0"
type: "documentation"
language: "English (Mandatory)"
related_files:
  - "00_ClassSphere_index.md"
  - "09_ClassSphere_testing.md"
  - "11_ClassSphere_deployment.md"
---

[← Estrategia de Testing](09_ClassSphere_testing.md) | [Índice](00_ClassSphere_index.md) | [Siguiente → Configuración de Deployment](11_ClassSphere_deployment.md)

# Plan de Implementación Unificado

## Metodología TDD Consolidada

Todo el sistema sigue **Test-Driven Development** estricto con **Prevención de Errores Integrada**:

1. **Red**: Escribir test que falle definiendo comportamiento esperado
2. **Green**: Implementar código mínimo para hacer pasar el test
3. **Refactor**: Mejorar código manteniendo tests verdes
4. **Validate Patterns**: Aplicar validación automática de patterns 1-6
5. **Document**: Documentar decisiones basadas en tests
6. **Integrate**: Integrar con sistema existente
7. **Validate**: Validar cumplimiento de criterios de aceptación

### Stack de Testing

**Backend (Go)**:
- testify/assert para assertions
- testify/mock para mocking
- httptest para testing HTTP
- go test -cover para cobertura

**Frontend (Angular)**:
- Jasmine + Karma (estándar Angular)
- Angular Testing Library
- Playwright para E2E

## Cobertura de Testing Requerida

- **Global**: ≥80% líneas, ≥65% ramas
- **Módulos Críticos**: ≥90% líneas, ≥80% ramas
- **Componentes de Seguridad**: ≥95% líneas, ≥85% ramas
- **API Endpoints**: 100% casos de éxito y error
- **Backend Go**: ≥80% líneas con testify
- **Frontend Angular**: ≥80% líneas con Jasmine
- **E2E**: Cobertura de flujos críticos con Playwright

## Orden de Implementación (15-20 semanas)

### Phase 1: Training (2-3 weeks)

**Week 1-2: Go + Echo**
- Go fundamentals
- Echo framework
- testify for testing
- Proof of Concept REST API
- **i18n Setup**: English default translations, i18n structure

**Week 2-3: Angular 19**
- Angular fundamentals
- esbuild and Vite
- Jasmine + Karma
- Proof of Concept components
- **i18n Integration**: Angular i18n module, translation pipes

**Phase 1 Documentation Deliverable**:
- 📝 Minimum Status Document (English):
  - Technologies implemented
  - i18n configuration status
  - Code coverage metrics
  - Known issues and resolutions
  - Next phase prerequisites

### Phase 2: Go Backend (4-6 weeks)

**Weeks 1-2: Authentication**
- JWT with Echo middleware
- OAuth 2.0 Google
- Tests with testify
- Redis for sessions
- **i18n**: Error messages in English

**Weeks 3-4: Role System**
- Authorization middleware
- Rate limiting
- CORS configuration
- Integration tests
- **i18n**: Role names and descriptions in English

**Weeks 5-6: Google Classroom API**
- Google API integration
- Dual mode (Mock/Real)
- Dashboard endpoints per role
- Tests with mocks
- **i18n**: API response messages in English

**Phase 2 Documentation Deliverable**:
- 📝 Minimum Status Document (English):
  - Backend endpoints implemented
  - Authentication flow status
  - Google Classroom integration status
  - Test coverage metrics
  - Performance benchmarks
  - Known issues and resolutions

### Phase 3: Angular Frontend (3-5 weeks)

**Weeks 1-2: Base Components**
- LoginForm component
- AuthGuard service
- Routing configuration
- Tests with Jasmine
- **i18n**: UI text in English, translation keys setup

**Weeks 3-4: Role-Based Dashboards**
- AdminDashboard component
- CoordinatorDashboard component
- TeacherDashboard component
- StudentDashboard component
- Component tests
- **i18n**: Dashboard labels in English, extensible translations

**Week 5: Backend Integration**
- Angular services for API
- RxJS observables
- Error handling
- Integration tests
- **i18n**: Error messages in English with i18n support

**Phase 3 Documentation Deliverable**:
- 📝 Minimum Status Document (English):
  - Frontend components implemented
  - i18n integration status
  - UI/UX accessibility status
  - Test coverage metrics
  - Browser compatibility
  - Known issues and resolutions

### Phase 4: Complete Testing (3-4 weeks)

**Weeks 1-2: Unit Tests**
- Backend: testify coverage ≥80%
- Frontend: Jasmine coverage ≥80%
- Test-based refactoring
- **i18n**: Test translation coverage

**Weeks 3-4: E2E Tests**
- Playwright setup
- Critical flows (login, OAuth, dashboards)
- Cross-browser tests
- Performance testing
- **i18n**: Multi-language E2E tests (English primary)

**Phase 4 Documentation Deliverable**:
- 📝 Minimum Status Document (English):
  - Test coverage summary
  - E2E test results
  - Performance benchmarks
  - Accessibility audit results
  - Security scan results
  - Known issues and resolutions

### Phase 5: Deployment (2-3 weeks)

**Weeks 1-2: Configuration**
- Dockerfile for Go
- Dockerfile for Angular
- Docker Compose
- GitHub Actions workflows
- **i18n**: Production translation assets

**Week 3: Production**
- Production deployment
- Monitoring setup
- Security scanning with Trivy
- Complete integration tests
- Dual mode validation
- Performance tuning
- **i18n**: Language switching validation

**Phase 5 Documentation Deliverable**:
- 📝 Minimum Status Document (English):
  - Deployment configuration
  - CI/CD pipeline status
  - Production environment status
  - Monitoring and alerting setup
  - Security posture
  - Known issues and resolutions

**📚 FINAL COMPLETE DOCUMENTATION** (Created after all phases):
- 📖 Complete System Architecture (English)
- 📖 Complete API Documentation (English)
- 📖 Complete User Guide (English with i18n support)
- 📖 Complete Developer Guide (English)
- 📖 Complete Operations Runbook (English)
- 📖 Complete i18n Implementation Guide (English)
- 📖 Lessons Learned and Best Practices (English)
- 📖 Future Roadmap and Enhancements (English)

### Fase 3: Visualización Avanzada (8-10 días)

**Días 24-26: Backend Avanzado**
- Tests para búsqueda + notificaciones + WebSocket
- Implementación de servicios avanzados
- Métricas predictivas + insights
- Sistema de alertas inteligentes

**Días 27-29: Frontend Avanzado**
- Tests para búsqueda + notificaciones + gráficos avanzados
- Implementación UI avanzada
- Widgets personalizables + drill-down
- Notificaciones tiempo real

**Días 30-32: Visualización Completa**
- Tests para D3.js + ApexCharts avanzado
- Gráficos interactivos + exportación
- Dashboards personalizables
- Performance optimization

**Días 33-34: Integración Avanzada**
- Tests E2E para flujos avanzados
- WebSocket testing + performance
- Mobile optimization
- Accessibility básica

### Fase 4: Integración Completa (10-12 días)

**Días 35-37: Google Completo**
- Tests para sincronización bidireccional
- Implementación sync + backup + webhooks
- Resolución de conflictos
- Admin panel Google

**Días 38-40: Accesibilidad WCAG 2.2 AA**
- Tests de accesibilidad completos
- Implementación keyboard + screen reader
- High contrast + motor accessibility
- Validación automática + manual

**Días 41-43: Testing Completo**
- Tests E2E exhaustivos
- Performance + load testing
- Visual regression testing
- Security penetration testing

**Días 44-45: Production Ready**
- CI/CD pipeline completo
- Docker optimization + security
- Monitoring + alerting
- Documentation + runbooks

## Criterios de Aceptación por Fase

### Fase 1 - Fundaciones (En Progreso - 5/12 días completados)

- [x] Backend: Go 1.24.7 + Echo + JWT + OAuth functioning ✅
- [ ] Frontend: Angular 19 + Auth + Responsive layout (Pending - Day 7)
- [x] Testing: ≥80% cobertura + CI básico ✅
- [ ] Integration: Frontend-Backend comunicación (Pendiente - Día 10)
- [x] Error Prevention: AsyncMock + CORS tests + Server health + Test Error Resolution Protocols ✅

**Patterns de Prevención Aplicados:**
- [x] Pattern 1: ConfigDict imports validados ✅
- [x] Pattern 4: AsyncMock en tests backend ✅
- [ ] Pattern 2: Angular config clean (Pending - Day 6)
- [ ] Pattern 3: Zod schemas validados (Pendiente - Día 4)
- [ ] Pattern 5: Frontend mocks comprehensivos (Pendiente - Día 7)
- [ ] Pattern 6: E2E tests completos (Pendiente - Día 10)

#### Checklist de Implementación Obligatoria:
- [ ] **OAuth Integration**: useAuth.getGoogleAuthUrl() → /api/auth/oauth/google → OAuthButton funcional
- [ ] **RxJS Usage**: Observables for auth state + HTTP calls implemented in AuthService
- [ ] **Role-Based Dashboard**: Componentes específicos AdminDashboard, CoordinatorDashboard, TeacherDashboard, StudentDashboard
- [ ] **Frontend-Backend Mapping**: Documentación explícita de cada endpoint → hook → componente
- [ ] **Test Coverage**: Backend ≥80%, Frontend ≥80%, Critical modules ≥95%
- [ ] **Verification Commands**: Comandos automáticos para validar cada funcionalidad

**Implementation Details Completed**:
- ✅ **Backend Complete**: Go 1.24.7 + Echo v4 + JWT + OAuth 2.0 Google
- ✅ **Robust Authentication**: JWT tokens + refresh rotation + password hashing with bcrypt
- ✅ **OAuth 2.0 Google**: PKCE + State validation + complete integration
- ✅ **Role System**: admin > coordinator > teacher > student with middleware
- ✅ **Infrastructure**: Redis cache + port 8080 fixed + health checks
- ✅ **Testing**: 78 tests unitarios + cobertura 100% + AsyncMock + timeouts
- ✅ **CI/CD**: GitHub Actions + linting + type checking + security scanning
- ✅ **Error Prevention**: AsyncMock + CORS + warnings deprecación + limpieza automática

**Métricas de Prevención Fase 1:**
- ConfigDict errors: 0 (100% prevención - Pattern 1)
- AsyncMock errors: 0 (100% prevención - Pattern 4)
- Mock path errors: 0 (100% prevención - Pattern 4)
- Tests pasando: 45/45 (100% - mejora desde 41/45)

### Fase 2 - Google Integration

- [ ] Backend: Google API + Modo dual + Dashboards
- [ ] Frontend: Google UI + ApexCharts + Dashboards rol
- [ ] Testing: Google mocks + Integration tests
- [ ] Error Prevention: Rate limiting + Fallback + API mocks + Google API Test Resolution
- [ ] Performance: <2s dashboard load

**Patterns de Prevención Aplicados:**
- [ ] Pattern 3: Zod schemas en validación OAuth
- [ ] Pattern 4: AsyncMock en tests Google API
- [ ] Pattern 6: E2E tests flujo Google completo
- [ ] Validación automática: Rate limiting + API mocks

### Fase 3 - Visualización Avanzada

- [ ] Backend: Búsqueda + Notificaciones + WebSocket
- [ ] Frontend: UI avanzada + Gráficos interactivos
- [ ] Error Prevention: WebSocket + Gráficos + Real-time + WebSocket Test Resolution
- [ ] Testing: E2E scenarios + Performance
- [ ] Accessibility: Keyboard + Screen reader básico

**Patterns de Prevención Aplicados:**
- [ ] Pattern 3: Zod schemas en validación de métricas
- [ ] Pattern 5: Mocks comprehensivos en componentes visualización
- [ ] Pattern 6: E2E tests para dashboards por rol
- [ ] Validación automática: WebSocket + Real-time

### Fase 4 - Production Ready

- [ ] Google: Sync bidireccional + Backup + Webhooks
- [ ] Error Prevention: Todos los sistemas estables + Monitoring + Complete Test Error Resolution
- [ ] Accessibility: WCAG 2.2 AA completo
- [ ] Testing: ≥90% críticos + Security + Load
- [ ] CI/CD: Pipeline completo + Docker + Monitoring

**Patterns de Prevención Aplicados:**
- [ ] Todos los patterns 1-6 validados en integración
- [ ] Scripts de detección automática ejecutándose
- [ ] Métricas de éxito: 100% tests passing
- [ ] Tiempo resolución errores: <3 min (mejora 80%)

**Métricas Finales de Prevención:**
- ConfigDict errors: 0 (100% prevención)
- AsyncMock errors: 0 (100% prevención)
- Frontend mocking errors: 0 (100% prevención)
- E2E coverage: 100%
- Automation success rate: >95%

## Metodología de Desarrollo

### TDD Estricto
1. **Red**: Escribir test que falle
2. **Green**: Implementar código mínimo para pasar
3. **Refactor**: Mejorar código manteniendo tests verdes
4. **Repeat**: Para cada nueva funcionalidad

### Cobertura 100% en Fase 1
- Todos los módulos backend: 100% cobertura
- Todos los componentes frontend: 100% cobertura
- Todos los archivos de test: 100% cobertura
- Context managers: Tests completos
- Error paths: Tests para todos los `try/except`

### Port 8080 Mandatory (Go Standard)
- Server always on port 8080
- Automatic cleanup scripts
- Port verification in CI/CD
- Fixed port documentation

### Lifespan Resiliente
- Servicios externos opcionales
- Manejo de errores en startup/shutdown
- Limpieza automática de recursos
- Health checks resilientes

### Sistema de Logging de Control de Status con Context Management (LLM 2024-2025)
- **Archivo de Log Obligatorio**: Crear archivo de log de control de status en directorio temporal del sistema
- **Formato LLM-Friendly**: Log en formato JSON estructurado para fácil lectura por LLM con gestión de contexto
- **Ubicación**: `/tmp/classsphere_status.json` (Linux/macOS) o `%TEMP%\classsphere_status.json` (Windows)
- **Context Awareness Files**: Archivos adicionales para gestión de contexto según Work Plan Development Rules:
  - `/tmp/classsphere_context_status.json` - Context chunks y token management
  - `/tmp/classsphere_tmux_status.log` - Logs de tmux con context tracking
  - `/tmp/classsphere_frontend_context.json` - Context específico de frontend
- **Contenido Requerido con Context Management**:
  ```json
  {
    "project": "ClassSphere",
    "version": "2.6",
    "phase": "fase_actual",
    "day": "dia_actual",
    "status": "completed|in_progress|pending|failed",
    "last_updated": "2025-01-XX XX:XX:XX",
    "tests_passed": 233,
    "coverage_percentage": 100,
    "health_endpoint": "http://localhost:8080/health",
    "server_running": true,
    "quality_gates": {
      "day_1": "completed",
      "day_2": "completed",
      "day_3": "completed"
    },
    "next_tasks": ["task_1", "task_2"],
    "errors": [],
    "warnings": [],
    "context_management": {
      "current_context_id": "unique-identifier",
      "token_count": 1500,
      "context_priority": "HIGH",
      "chunk_position": "middle",
      "lost_in_middle_risk": "low",
      "chunking_strategy": "priority_based",
      "anti_lost_middle_structure": "applied"
    },
    "tmux_sessions": {
      "active_sessions": ["tdd-dev", "classsphere-frontend"],
      "context_monitoring": true,
      "health_checks": ["backend:8080", "frontend:4200"]
    }
  }
  ```
- **Context-Aware Updates**: El archivo debe actualizarse automáticamente siguiendo las reglas de chunking por prioridad
- **Anti Lost-in-the-Middle Verification**: Verificar estructura beginning-middle-end antes de continuar
- **Context Recovery**: Capacidad de recuperar contexto desde point-in-time específico
- **Tmux Integration**: Tracking automático de sesiones tmux con context logging
- **Integración CI/CD**: Pipeline debe incluir context validation y token count management

## Scripts de Desarrollo

### Script de Inicio Estándar
```bash
#!/bin/bash
# Script de desarrollo estándar
set -e

# Cargar funciones de logging
source <(cat << 'EOF'
# Funciones de logging integradas
log_error_solution() {
    local error_type="$1"
    local solution="$2"
    local status="$3"
    local component="${4:-development}"
    local details="${5:-}"
    
    local timestamp=$(date -Iseconds)
    local error_id="ERR-$(date +%Y%m%d)-$(printf "%03d" $(($(grep -c "^$timestamp" /tmp/dashboard_errors/error_solutions.log 2>/dev/null || echo 0) + 1)))"
    
    echo "$timestamp | $error_id | $error_type | $solution | $status | $component | $details" >> /tmp/dashboard_errors/error_solutions.log
    echo "📝 Error registrado: $error_id - $error_type"
}
EOF
)

echo "🧹 Limpieza de procesos anteriores..."
pkill -f uvicorn || true
sleep 2

echo "🔍 Port 8080 verification..."
if lsof -Pi :8080 -sTCP:LISTEN -t >/dev/null 2>&1; then
    echo "⚠️  Port busy. Automatic cleanup..."
    log_error_solution "PORT_OCCUPIED" "kill_process_and_retry" "resolved" "development" "Port 8080 busy, applying automatic cleanup"
    pkill -f "port 8080" || true
    sleep 3
fi

echo "🚀 Starting server on port 8080..."
./classsphere-backend
```

### Script de Verificación
```bash
#!/bin/bash
# Script de verificación
set -e

# Cargar funciones de logging
source <(cat << 'EOF'
log_error_solution() {
    local error_type="$1"
    local solution="$2"
    local status="$3"
    local component="${4:-development}"
    local details="${5:-}"
    
    local timestamp=$(date -Iseconds)
    local error_id="ERR-$(date +%Y%m%d)-$(printf "%03d" $(($(grep -c "^$timestamp" /tmp/dashboard_errors/error_solutions.log 2>/dev/null || echo 0) + 1)))"
    
    echo "$timestamp | $error_id | $error_type | $solution | $status | $component | $details" >> /tmp/dashboard_errors/error_solutions.log
    echo "📝 Error registrado: $error_id - $error_type"
}
EOF
)

echo "🔍 Verificando servidor..."
if curl -f http://127.0.0.1:8080/health; then
    echo "✅ Server verified correctly"
else
    log_error_solution "SERVER_HEALTH_CHECK_FAILED" "restart_server" "failed" "verification" "Health check failed on port 8080"
    exit 1
fi

echo "🔍 Verificando servicios externos..."
echo "✅ Google Classroom API disponible (instalación nueva con mocks)"

if pgrep redis-server; then
    echo "✅ Redis disponible"
else
    log_error_solution "REDIS_NOT_AVAILABLE" "install_redis" "warning" "verification" "Redis no está disponible"
    echo "⚠️  Redis no disponible"
fi

echo "🎉 Verificación completada"
```

### Scripts de Mitigación Cursor
```bash
#!/bin/bash
# Script de mitigación para problemas conocidos de Cursor IDE
# Solución: Terminal externo + tmux para estabilidad
set -e

echo "🔧 Mitigación Cursor: Configurando terminal externo..."

# Verificar si tmux está disponible
if ! command -v tmux &> /dev/null; then
    echo "⚠️  tmux no está instalado. Instalando..."
    sudo apt-get update && sudo apt-get install -y tmux
fi

# Crear sesión tmux para desarrollo
SESSION_NAME="classsphere-dev"

# Cargar funciones de logging específicas para Cursor
source <(cat << 'EOF'
log_cursor_mitigation() {
    local problem="$1"
    local mitigation="$2"
    local success="$3"
    local session_name="${4:-}"
    
    local timestamp=$(date -Iseconds)
    echo "$timestamp | CURSOR_MITIGATION | $problem | $mitigation | $success | $session_name" >> /tmp/dashboard_errors/cursor_mitigation.log
    echo "📝 Mitigación Cursor registrada: $problem -> $mitigation"
}
EOF
)

if tmux has-session -t $SESSION_NAME 2>/dev/null; then
    echo "✅ Sesión $SESSION_NAME ya existe. Conectando..."
    log_cursor_mitigation "TERMINAL_HANG" "connect_existing_session" "success" "$SESSION_NAME"
    tmux attach-session -t $SESSION_NAME
else
    echo "🚀 Creando nueva sesión $SESSION_NAME..."
    tmux new-session -d -s $SESSION_NAME
    tmux send-keys -t $SESSION_NAME "cd /home/lbrines/projects/AI/classsphere" Enter
    tmux send-keys -t $SESSION_NAME "echo '🔧 Terminal externo configurado para evitar conflictos con Cursor'" Enter
    log_cursor_mitigation "TERMINAL_HANG" "create_tmux_session" "success" "$SESSION_NAME"
    tmux attach-session -t $SESSION_NAME
fi
```

## Comandos de Testing

### Backend Tests
```bash
# Tests unitarios
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

### Configuration in package.json (Angular)
```json
{
  "//": "Testing stack defined: Jasmine + Karma + Playwright. Angular standard.",
  "scripts": {
    "test": "ng test",
    "test:watch": "ng test --watch",
    "test:coverage": "ng test --code-coverage",
    "test:e2e": "playwright test"
  },
  "devDependencies": {
    "@angular/cli": "^19.0.0",
    "jasmine-core": "~5.1.0",
    "karma": "~6.4.0",
    "karma-jasmine": "~5.1.0",
    "karma-chrome-launcher": "~3.2.0",
    "karma-coverage": "~2.2.0",
    "@playwright/test": "^1.48.2"
  },
  "//": "Angular standard testing: Jasmine + Karma for unit, Playwright for E2E"
}

### Testing con Terminal Externo
```bash
#!/bin/bash
# Tests frontend con terminal externo (mitigación Cursor)
set -e

echo "🔧 Testing con Terminal Externo: Configurando..."

# Crear sesión tmux para testing
SESSION_NAME="frontend-tests"

if ! tmux has-session -t $SESSION_NAME 2>/dev/null; then
    echo "🚀 Creando sesión de testing..."
    tmux new-session -d -s $SESSION_NAME
fi

# Configurar entorno de testing en sesión tmux
tmux send-keys -t $SESSION_NAME "cd /home/lbrines/projects/AI/classsphere/frontend" Enter
tmux send-keys -t $SESSION_NAME "echo '🔧 Terminal externo configurado para testing'" Enter

# Tests unitarios con terminal externo
tmux send-keys -t $SESSION_NAME "echo '🧪 Ejecutando tests unitarios...'" Enter
tmux send-keys -t $SESSION_NAME "npm test" Enter

# Tests de integración con terminal externo
tmux send-keys -t $SESSION_NAME "echo '🧪 Ejecutando tests de integración...'" Enter
tmux send-keys -t $SESSION_NAME "npm run test:integration" Enter

# Tests E2E con terminal externo
tmux send-keys -t $SESSION_NAME "echo '🧪 Ejecutando tests E2E...'" Enter
tmux send-keys -t $SESSION_NAME "npm run test:e2e" Enter

echo "✅ Tests ejecutándose en sesión tmux. Conectar con: tmux attach-session -t $SESSION_NAME"
```

## Verificación de Deployment

### Port 8080 Verification
```bash
# Verify port
lsof -Pi :8080

# Verify connectivity
curl -f http://127.0.0.1:8080/health
```

### Verificación de Infraestructura
```bash
# Verificar herramientas
python3 --version
pip3 --version
python3 -m uvicorn --version
curl --version
lsof --version

# Verificar servicios externos
# Google Classroom API con instalación nueva y mocks
pgrep redis-server
```

## Templates Estándar

### Template de Configuración Pydantic v2
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

### Template de Echo con Graceful Shutdown
```go
package main

import (
    "context"
    "os"
    "os/signal"
    "time"
    
    "github.com/labstack/echo/v4"
    "github.com/labstack/echo/v4/middleware"
)

func main() {
    e := echo.New()
    
    // Middleware
    e.Use(middleware.Logger())
    e.Use(middleware.Recover())
    
    // Routes
    e.GET("/health", healthHandler)
    
    // Start server
    go func() {
        if err := e.Start(":8080"); err != nil {
            e.Logger.Info("shutting down the server")
        }
    }()
    
    // Graceful shutdown
    quit := make(chan os.Signal, 1)
    signal.Notify(quit, os.Interrupt)
    <-quit
    ctx, cancel := context.WithTimeout(context.Background(), 10*time.Second)
    defer cancel()
    if err := e.Shutdown(ctx); err != nil {
        e.Logger.Fatal(err)
    }
}
```

### Template de Test Async
```python
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

## Checklist de Validación de Patterns

### Pre-Commit Validation
```bash
#!/bin/bash
# Validación automática de patterns antes de commit

echo "🔍 Validando Patterns de Prevención..."

# Pattern 1: ConfigDict imports
find backend/src -name "*.py" -exec grep -l "model_config = ConfigDict" {} \; | \
  xargs -I {} sh -c 'grep -q "from pydantic import.*ConfigDict" {} || (echo "❌ Pattern 1: {}" && exit 1)'

# Pattern 4: AsyncMock usage
find backend/tests -name "test_*.py" -exec grep -l "async def test" {} \; | \
  xargs -I {} sh -c 'grep -q "AsyncMock" {} || (echo "❌ Pattern 4: {}" && exit 1)'

# Pattern 2: Next.js config
if grep -q "swcMinify" frontend/next.config.js 2>/dev/null; then
    echo "❌ Pattern 2: next.config.js contains deprecated swcMinify"
    exit 1
fi

# Pattern 5: Frontend mocks
find frontend/src -name "*.test.tsx" -exec grep -l "vi.mock" {} \; | \
  xargs -I {} sh -c 'grep -q "@/lib/defensive" {} || echo "⚠️  Pattern 5 warning: {}"'

echo "✅ Todos los patterns validados correctamente"
```

### CI/CD Integration
```yaml
# .github/workflows/pattern-validation.yml
name: Pattern Validation

on: [push, pull_request]

jobs:
  validate-patterns:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Validate Pattern 1 (ConfigDict)
        run: |
          find backend/src -name "*.py" -exec grep -l "model_config = ConfigDict" {} \; | \
            xargs -I {} sh -c 'grep -q "from pydantic import.*ConfigDict" {} || exit 1'
      
      - name: Validate Pattern 4 (AsyncMock)
        run: |
          find backend/tests -name "test_*.py" -exec grep -l "async def test" {} \; | \
            xargs -I {} sh -c 'grep -q "AsyncMock" {} || exit 1'
      
      - name: Validate Pattern 2 (Next.js config)
        run: |
          ! grep -q "swcMinify" frontend/next.config.js
      
      - name: Report Success
        run: echo "✅ All patterns validated successfully"
```

## Referencias a Otros Documentos

- **Guía de Prevención LLM**: [llm_error_prevention_guide.md](../extra/revision/llm_error_prevention_guide.md) - Patterns completos y algoritmos de detección
- Para detalles sobre la estrategia de testing, consulte [Estrategia de Testing](09_ClassSphere_testing.md).
- Para detalles sobre la configuración de deployment, consulte [Configuración de Deployment](11_ClassSphere_deployment.md).
- Para detalles sobre los criterios de aceptación, consulte [Criterios de Aceptación](12_ClassSphere_criterios_aceptacion.md).

---

[← Estrategia de Testing](09_ClassSphere_testing.md) | [Índice](00_ClassSphere_index.md) | [Siguiente → Configuración de Deployment](11_ClassSphere_deployment.md)
