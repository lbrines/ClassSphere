---
title: "ClassSphere - Plan de Desarrollo con Mejores Prácticas LLM"
version: "1.0"
type: "development_plan"
context_management: "chunked_by_priority"
security_level: "zero_trust"
tdd_methodology: "strict"
audience: "LLM_executor"
date: "2025-10-05"
author: "Sistema de Planificación LLM"
---

# Plan de Desarrollo ClassSphere

## 🎯 INICIO: Objetivos Críticos y Dependencias Bloqueantes

### Objetivo Principal
Implementar ClassSphere desde cero siguiendo TDD estricto, con gestión de contexto optimizada para LLMs y principios de seguridad de cero confianza.

### Dependencias Bloqueantes Críticas
1. **Python 3.11.4** - Requerido para FastAPI 0.104.1 y Pydantic v2
2. **Node.js 18+** - Requerido para Next.js 15 y React 19
3. **Redis** - Opcional pero recomendado para caché
4. **Git** - Control de versiones obligatorio
5. **Docker** - Para deployment y CI/CD

### Context Window Management Aplicado

**Chunking por Prioridad Implementado:**
```yaml
CRITICAL (2000 tokens max):
  - Autenticación JWT y OAuth 2.0
  - Configuración base (config.py, main.py)
  - Health checks y endpoints críticos

HIGH (1500 tokens max):
  - Servicios Google Classroom
  - Integraciones principales
  - Middleware de seguridad

MEDIUM (1000 tokens max):
  - Componentes UI
  - Visualizaciones con ApexCharts
  - Dashboards por rol

LOW (800 tokens max):
  - Panel de administración
  - Accesibilidad WCAG 2.2 AA
  - Documentación complementaria
```

**Estructura Anti Lost-in-the-Middle:**
- **INICIO** (este documento): Objetivos críticos + dependencias bloqueantes
- **MEDIO**: Implementación detallada en archivos de fase (02-05)
- **FINAL**: Checklist de verificación + próximos pasos

### Logs Estructurados Obligatorios

Todos los servicios deben implementar logging estructurado:

```json
{
  "timestamp": "2025-10-05T07:03:25-03:00",
  "context_id": "critical-a1b2c3d4",
  "token_count": 1850,
  "context_priority": "CRITICAL",
  "status": "in_progress",
  "memory_management": {
    "chunk_position": "beginning",
    "lost_in_middle_risk": "low"
  }
}
```

**Ubicación de Logs:**
- `/tmp/classsphere_status.json` - Estado general del proyecto
- `/tmp/classsphere_context_status.json` - Gestión de contexto
- `/tmp/classsphere_tmux_status.log` - Logs de sesiones tmux

---

## 📋 MEDIO: Fases de Desarrollo (TDD Estricto)

### Fase 1: Fundaciones (CRITICAL priority) - 12 días
**Archivo detallado:** [02_plan_fase1_fundaciones.md](02_plan_fase1_fundaciones.md)

**Objetivos:**
- Backend FastAPI 0.104.1 + Pydantic v2 funcionando en puerto 8000
- Autenticación JWT + OAuth 2.0 Google con PKCE
- Sistema de roles (admin > coordinator > teacher > student)
- Frontend Next.js 15 + React 19 + TypeScript
- Cobertura de testing ≥80% (backend y frontend)

**Comandos de Verificación:**
```bash
# Backend health check
curl http://localhost:8000/health

# Tests backend
pytest tests/ --cov=src --cov-fail-under=80

# Tests frontend
npm run test -- --coverage --coverageThreshold='{"global":{"lines":80}}'

# E2E tests
npm run test:e2e
```

**Criterios de Aceptación Medibles:**
- [ ] Login funciona con credenciales demo
- [ ] OAuth Google redirige correctamente
- [ ] Dashboard muestra contenido por rol
- [ ] Backend coverage ≥ 80%
- [ ] Frontend coverage ≥ 80%
- [ ] Todos los tests pasan 100%

---

### Fase 2: Integración Google (HIGH priority) - 10 días
**Archivo detallado:** [03_plan_fase2_google_integration.md](03_plan_fase2_google_integration.md)

**Objetivos:**
- Google Classroom API con mocks completos
- Modo dual (Google real / Mock)
- Dashboards por rol con métricas
- ApexCharts 5.3.5 para visualizaciones
- Cobertura de testing ≥85%

**Comandos de Verificación:**
```bash
# Verificar Google API mocks
pytest tests/unit/services/test_google_service.py -v

# Verificar modo dual
curl http://localhost:8000/api/v1/google/mode

# Tests de integración
pytest tests/integration/test_google_integration.py -v
```

**Criterios de Aceptación Medibles:**
- [ ] Mocks de Google API funcionan correctamente
- [ ] Modo dual switching sin errores
- [ ] Dashboards cargan en < 2 segundos
- [ ] ApexCharts renderizan correctamente
- [ ] Coverage ≥ 85% en módulos Google

---

### Fase 3: Visualización Avanzada (MEDIUM priority) - 10 días
**Archivo detallado:** [04_plan_fase3_visualizacion.md](04_plan_fase3_visualizacion.md)

**Objetivos:**
- Sistema de búsqueda avanzada
- Notificaciones en tiempo real (WebSocket)
- Gráficos interactivos con drill-down
- Widgets personalizables
- Cobertura de testing ≥85%

**Comandos de Verificación:**
```bash
# Tests de búsqueda
pytest tests/unit/services/test_search_service.py -v

# Tests de WebSocket
pytest tests/integration/test_websocket_integration.py -v

# Tests E2E de notificaciones
npm run test:e2e -- notifications.spec.ts
```

**Criterios de Aceptación Medibles:**
- [ ] Búsqueda responde en < 500ms
- [ ] WebSocket conecta sin errores
- [ ] Notificaciones llegan en tiempo real
- [ ] Gráficos interactivos funcionan
- [ ] Coverage ≥ 85% en módulos avanzados

---

### Fase 4: Integración Completa (LOW priority) - 13 días
**Archivo detallado:** [05_plan_fase4_integracion.md](05_plan_fase4_integracion.md)

**Objetivos:**
- Sincronización bidireccional Google Classroom
- Sistema de backup y recuperación
- Accesibilidad WCAG 2.2 AA completa
- CI/CD pipeline completo
- Cobertura de testing ≥90% en módulos críticos

**Comandos de Verificación:**
```bash
# Tests de sincronización
pytest tests/integration/test_google_sync_integration.py -v

# Tests de accesibilidad
npm run test:a11y

# Verificar CI/CD
gh workflow run test.yml

# Security scan
trivy image classsphere:latest
```

**Criterios de Aceptación Medibles:**
- [ ] Sincronización bidireccional funciona
- [ ] Backup/restore sin pérdida de datos
- [ ] WCAG 2.2 AA validado automáticamente
- [ ] Pipeline CI/CD pasa 100%
- [ ] Coverage ≥ 90% en módulos críticos

---

## 🔒 Seguridad y Verificación (Cero Confianza)

**Archivo detallado:** [07_plan_security_protocols.md](07_plan_security_protocols.md)

### Principio de Cero Confianza Aplicado

**Regla fundamental:** Tratar todo código generado por IA como input de desarrollador junior.

**Verificaciones Obligatorias:**
1. **SAST (Static Application Security Testing)**
   ```bash
   bandit -r backend/src/ -ll
   ```

2. **SCA (Software Composition Analysis)**
   ```bash
   safety check
   pip-audit
   ```

3. **Detección de Secretos**
   ```bash
   trufflehog filesystem backend/ --json
   ```

4. **Escaneo Contextual**
   ```bash
   semgrep --config=auto backend/src/
   ```

### Prompt Engineering de Seguridad

**Template obligatorio para generación de código:**
```
"Genera [componente] con:
- Validación de entrada estricta
- Limitación de tasa (rate limiting)
- Hash de contraseñas con bcrypt
- Soporte para autenticación resistente al phishing
- Manejo de errores sin exponer información sensible
- Logging de eventos de seguridad"
```

### Escaneo Automático en CI/CD

**Pipeline obligatorio:**
```yaml
security_scan:
  - SAST: bandit, semgrep
  - SCA: safety, pip-audit
  - Secrets: trufflehog
  - Container: trivy
  - DAST: OWASP ZAP (opcional)
```

---

## 🧪 Estrategia de Testing Completa

**Archivo detallado:** [06_plan_testing_strategy.md](06_plan_testing_strategy.md)

### Stack de Testing Definido

**Backend:**
- pytest + pytest-asyncio + pytest-cov
- AsyncMock para servicios async
- TestClient para endpoints FastAPI

**Frontend:**
- Vitest + React Testing Library (unit/integration)
- Playwright (E2E)
- 🚫 **NO usar Jest** (incompatible con ESM y React 19)

### Cobertura Requerida

| Tipo de Módulo | Líneas | Ramas |
|----------------|--------|-------|
| Global | ≥80% | ≥65% |
| Módulos Críticos | ≥90% | ≥80% |
| Seguridad | ≥95% | ≥85% |
| API Endpoints | 100% | 100% |

### Timeouts de Testing

```yaml
Unit Tests: 30 segundos máximo
Integration Tests: 60 segundos máximo
E2E Tests: 120 segundos máximo
API Tests: 45 segundos máximo
```

### Metodología TDD Estricta

**Ciclo Red-Green-Refactor:**
1. **Red**: Escribir test que falle
2. **Green**: Implementar código mínimo para pasar
3. **Refactor**: Mejorar código manteniendo tests verdes
4. **Repeat**: Para cada nueva funcionalidad

**Comandos de verificación:**
```bash
# Backend TDD
pytest tests/ --cov=src --cov-report=term-missing

# Frontend TDD
npm run test -- --coverage

# E2E TDD
npm run test:e2e -- --reporter=html
```

---

## 📊 Gestión de Contexto para LLMs

**Archivo detallado:** [08_plan_context_management.md](08_plan_context_management.md)

### Arquitectura Context-Aware

**Implementación en servicios:**
```python
class ContextAwareService:
    """Servicio con gestión de contexto según prioridad"""
    
    def __init__(self, priority: str = "MEDIUM"):
        self.priority = priority
        self.max_tokens = self._get_max_tokens(priority)
        self.context_id = f"{priority.lower()}-{uuid4().hex[:8]}"
    
    def _get_max_tokens(self, priority: str) -> int:
        limits = {
            "CRITICAL": 2000,
            "HIGH": 1500,
            "MEDIUM": 1000,
            "LOW": 800
        }
        return limits.get(priority, 1000)
```

### Anti Lost-in-the-Middle Pattern

**Estructura obligatoria para documentos:**
```
INICIO (primacy bias):
  - Objetivos críticos
  - Dependencias bloqueantes
  - Comandos de verificación inmediata

MEDIO (detalle):
  - Implementación paso a paso
  - Casos de uso específicos
  - Ejemplos de código

FINAL (recency bias):
  - Checklist de verificación
  - Próximos pasos
  - Comandos de validación
```

### Logs Estructurados

**Template obligatorio:**
```json
{
  "timestamp": "ISO 8601",
  "context_id": "unique-identifier",
  "token_count": "número",
  "context_priority": "CRITICAL|HIGH|MEDIUM|LOW",
  "status": "started|in_progress|completed|failed",
  "memory_management": {
    "chunk_position": "beginning|middle|end",
    "lost_in_middle_risk": "low|medium|high"
  }
}
```

---

## 📈 Métricas de Evaluación

**Archivo detallado:** [09_plan_evaluation_metrics.md](09_plan_evaluation_metrics.md)

### Métricas de Calidad del Plan

| Métrica | Objetivo | Medición |
|---------|----------|----------|
| Precisión | ≥95% | Especificaciones cumplidas vs. totales |
| Completitud | 100% | Fases documentadas vs. fases requeridas |
| Coherencia Semántica | ≥85% | Consistencia terminológica cross-document |
| Seguridad | 100% | Protocolos de cero confianza implementados |

### Métricas de Calidad Técnica

| Métrica | Objetivo | Comando de Verificación |
|---------|----------|-------------------------|
| Test Coverage Backend | ≥80% | `pytest --cov=src --cov-fail-under=80` |
| Test Coverage Frontend | ≥80% | `npm run test -- --coverage` |
| Security Score | 100% | `bandit -r backend/src/ -ll` |
| Performance | <2s | `lighthouse http://localhost:3000` |

### Métricas de TDD Compliance

| Fase | TDD Compliance | Verificación |
|------|----------------|--------------|
| Fase 1 | 100% | Tests escritos antes de implementación |
| Fase 2 | 100% | Mocks antes de integración real |
| Fase 3 | 100% | Tests E2E antes de features |
| Fase 4 | 100% | Tests de seguridad antes de deploy |

### Métricas de Context Management

| Aspecto | Objetivo | Medición |
|---------|----------|----------|
| Token Count por Chunk | <2000 | Análisis automático de documentos |
| Lost-in-Middle Risk | Low | Estructura beginning-middle-end validada |
| Context Recovery | <5 min | Tiempo para recuperar contexto completo |
| Chunking Effectiveness | ≥90% | Información crítica en posiciones óptimas |

---

## ✅ FINAL: Checklist de Verificación y Próximos Pasos

### Checklist de Preparación del Entorno

**Antes de comenzar:**
- [ ] Python 3.11.4 instalado y verificado (`python3 --version`)
- [ ] Node.js 18+ instalado y verificado (`node --version`)
- [ ] Git configurado (`git config --list`)
- [ ] Docker instalado (`docker --version`)
- [ ] Redis instalado (opcional) (`redis-server --version`)
- [ ] Repositorio inicializado (`git init`)
- [ ] Estructura de directorios creada

**Comandos de verificación:**
```bash
# Verificar herramientas
python3 --version  # Debe ser 3.11.4
node --version     # Debe ser 18+
git --version
docker --version
redis-server --version

# Crear estructura base
mkdir -p backend/src/app/{api,services,models,core,middleware,utils,data}
mkdir -p backend/tests/{unit,integration,e2e}
mkdir -p frontend/src/{app,components,hooks,lib,types,providers}
mkdir -p frontend/tests/{unit,integration,e2e}
mkdir -p docs/architecture
mkdir -p scripts
```

### Checklist de Fase 1 (Fundaciones)

**Backend:**
- [ ] FastAPI 0.104.1 instalado y funcionando
- [ ] Pydantic v2 configurado correctamente
- [ ] JWT authentication implementado
- [ ] OAuth 2.0 Google con PKCE funcionando
- [ ] Sistema de roles completo
- [ ] Health checks respondiendo
- [ ] Tests backend ≥80% coverage

**Frontend:**
- [ ] Next.js 15 + React 19 funcionando
- [ ] TypeScript configurado
- [ ] Tailwind CSS aplicado
- [ ] React Query v4 integrado
- [ ] Componentes de autenticación
- [ ] Dashboards por rol
- [ ] Tests frontend ≥80% coverage

**Integración:**
- [ ] Frontend se comunica con backend
- [ ] JWT tokens funcionan correctamente
- [ ] OAuth flow completo
- [ ] Protección de rutas por rol
- [ ] Tests E2E pasando

### Checklist de Seguridad (Todas las Fases)

**Escaneo Automático:**
- [ ] SAST ejecutado sin errores críticos
- [ ] SCA sin vulnerabilidades conocidas
- [ ] Detección de secretos sin hallazgos
- [ ] Container scan sin vulnerabilidades HIGH/CRITICAL

**Verificación Manual:**
- [ ] Código revisado y comprendido
- [ ] Validación de entrada implementada
- [ ] Rate limiting configurado
- [ ] Logging de seguridad activo

### Checklist de Context Management

**Documentación:**
- [ ] Chunking por prioridad aplicado
- [ ] Estructura anti lost-in-the-middle validada
- [ ] Logs estructurados implementados
- [ ] Context recovery testeado

**Archivos de Log:**
- [ ] `/tmp/classsphere_status.json` actualizado
- [ ] `/tmp/classsphere_context_status.json` monitoreado
- [ ] `/tmp/classsphere_tmux_status.log` funcionando

### Próximos Pasos Inmediatos

**Paso 1: Configurar Entorno (Día 1)**
```bash
# 1. Clonar o inicializar repositorio
git init
git remote add origin <repository-url>

# 2. Crear estructura de directorios
bash scripts/setup-structure.sh

# 3. Configurar Python
pyenv install 3.11.4
pyenv local 3.11.4
python3 -m venv venv
source venv/bin/activate

# 4. Instalar dependencias backend
cd backend
pip install -r requirements.txt

# 5. Configurar Node.js
cd ../frontend
npm install

# 6. Verificar instalación
cd ../backend && pytest tests/ --version
cd ../frontend && npm run test -- --version
```

**Paso 2: Implementar Fase 1 (Días 2-13)**
- Seguir instrucciones detalladas en [02_plan_fase1_fundaciones.md](02_plan_fase1_fundaciones.md)
- Ejecutar comandos de verificación después de cada día
- Mantener logs estructurados actualizados
- Validar cobertura de testing diariamente

**Paso 3: Validar Fase 1 (Día 13)**
```bash
# Verificación completa Fase 1
bash scripts/validate-phase1.sh

# Debe incluir:
# - Tests backend ≥80%
# - Tests frontend ≥80%
# - Security scan sin errores críticos
# - E2E tests pasando
# - Performance < 2s
```

**Paso 4: Continuar con Fases 2-4**
- Fase 2: [03_plan_fase2_google_integration.md](03_plan_fase2_google_integration.md)
- Fase 3: [04_plan_fase3_visualizacion.md](04_plan_fase3_visualizacion.md)
- Fase 4: [05_plan_fase4_integracion.md](05_plan_fase4_integracion.md)

### Comandos de Validación Final

**Validación Completa del Proyecto:**
```bash
# 1. Tests completos
pytest backend/tests/ --cov=backend/src --cov-fail-under=80
npm --prefix frontend run test -- --coverage

# 2. Security scan
bandit -r backend/src/ -ll
npm audit --prefix frontend

# 3. E2E tests
npm --prefix frontend run test:e2e

# 4. Performance
lighthouse http://localhost:3000 --output=html

# 5. Accessibility
npm --prefix frontend run test:a11y

# 6. Build verification
docker-compose build
docker-compose up -d
curl http://localhost:8000/health
curl http://localhost:3000
```

---

## 📚 Archivos Relacionados del Plan

### Archivos de Fase (Implementación Detallada)
- [02_plan_fase1_fundaciones.md](02_plan_fase1_fundaciones.md) - CRITICAL priority
- [03_plan_fase2_google_integration.md](03_plan_fase2_google_integration.md) - HIGH priority
- [04_plan_fase3_visualizacion.md](04_plan_fase3_visualizacion.md) - MEDIUM priority
- [05_plan_fase4_integracion.md](05_plan_fase4_integracion.md) - LOW priority

### Archivos de Estrategia (Protocolos y Mejores Prácticas)
- [06_plan_testing_strategy.md](06_plan_testing_strategy.md) - Estrategia completa de testing
- [07_plan_security_protocols.md](07_plan_security_protocols.md) - Protocolos de seguridad
- [08_plan_context_management.md](08_plan_context_management.md) - Gestión de contexto LLM
- [09_plan_evaluation_metrics.md](09_plan_evaluation_metrics.md) - Métricas de evaluación

### Documentación de Referencia
- [../principal/00_ClassSphere_index.md](../principal/00_ClassSphere_index.md) - Especificaciones completas
- [../extra/SOFTWARE_PROJECT_BEST_PRACTICES.md](../extra/SOFTWARE_PROJECT_BEST_PRACTICES.md) - Mejores prácticas LLM

---

## 🎯 Resumen Ejecutivo

### Características Clave del Plan

**✅ Completamente ejecutable desde repositorio vacío**
- Instrucciones paso a paso sin ambigüedades
- Comandos específicos verificables
- Dependencias claramente identificadas

**✅ Optimizado para LLMs**
- Chunking por prioridad implementado
- Estructura anti lost-in-the-middle
- Logs estructurados para tracking

**✅ Seguridad de cero confianza**
- Escaneo automático obligatorio
- Verificación manual requerida
- Prompt engineering de seguridad

**✅ TDD estricto desde el inicio**
- Tests antes de implementación
- Cobertura medible y verificable
- Metodología Red-Green-Refactor

**✅ Métricas objetivas de éxito**
- Precisión ≥95%
- Completitud 100%
- Coherencia semántica ≥85%
- Calidad técnica ≥90%

### Duración Total Estimada

- **Fase 1 (Fundaciones)**: 12 días
- **Fase 2 (Google Integration)**: 10 días
- **Fase 3 (Visualización)**: 10 días
- **Fase 4 (Integración Completa)**: 13 días
- **Total**: 45 días

### Recursos Necesarios

**Humanos:**
- 1 LLM executor (puede ser asistente IA)
- 1 revisor técnico (validación manual)
- 1 security reviewer (opcional pero recomendado)

**Técnicos:**
- Servidor de desarrollo (local o cloud)
- Cuenta Google Cloud (para OAuth)
- Repositorio Git
- CI/CD pipeline (GitHub Actions)

---

**Última actualización:** 2025-10-05
**Versión del plan:** 1.0
**Estado:** Listo para ejecución
