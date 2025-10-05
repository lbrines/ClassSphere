---
title: "ClassSphere - Arquitectura del Sistema Unificado"
version: "2.6"
type: "documentation"
related_files:
  - "00_ClassSphere_index.md"
  - "04_ClassSphere_objetivos.md"
  - "06_ClassSphere_funcionalidades.md"
---

[← Objetivos del Sistema](04_ClassSphere_objetivos.md) | [Índice](00_ClassSphere_index.md) | [Siguiente → Funcionalidades Consolidadas](06_ClassSphere_funcionalidades.md)

# Arquitectura del Sistema Unificado

## Stack Tecnológico Consolidado

```
# Backend
- Python 3.11.4 (pyenv)
- FastAPI 0.104.1
- Pydantic v2 (validación estricta)
- Google Classroom API (fuente de datos principal)
- WebSockets (notificaciones)
- Redis (cache y sesiones únicamente)
- pytest (testing)

# Frontend
- Next.js 15 (actualizado desde 13.5.6)
- React 19 (actualizado desde 18.2.0)
- TypeScript 5.1.6
- @tanstack/react-query 4.36.1
- ApexCharts 5.3.5
- Tailwind CSS 3.3.3
- Vitest + React Testing Library + Playwright (testing)

# DevOps
- Docker (multi-stage)
- GitHub Actions
- Trivy (security)
- pnpm 8.x+
```

## Instalación Nueva Google Classroom con Mocks

Siguiendo la definición de [Instalación Nueva Google Classroom](02_ClassSphere_glosario_tecnico.md#instalación-nueva-google-classroom) del Glosario Técnico:

**Implementación**: Proceso de instalación desde cero con sistema de mocks preconfigurados
**Componentes**: Google Classroom API service, sistema de alternancia mock/real, tests unitarios con mocks controlados
**Configuración**: Flexible para diferentes entornos (desarrollo, testing, producción)

## Arquitectura Resiliente con Prevención de Errores

### 1. Arquitectura Estándar Moderna

Siguiendo las definiciones del [Glosario Técnico](02_ClassSphere_glosario_tecnico.md#arquitectura-semántica-simplificada):

**Pydantic v2**: Implementación según [Pydantic v2 - Migración Automática](02_ClassSphere_glosario_tecnico.md#pydantic-v2---migración-automática)
**FastAPI Lifespan**: Implementación según [FastAPI Lifespan - Context Manager Estándar](02_ClassSphere_glosario_tecnico.md#fastapi-lifespan---context-manager-estándar)
**Error Prevention**: Siguiendo [Error Prevention Protocols](02_ClassSphere_glosario_tecnico.md#error-prevention-protocols)
**Work Plan Context Management**: Implementación según [Work Plan Development Rules](02_ClassSphere_glosario_tecnico.md#work-plan-development-rules-llm-2024-2025)

#### 1.1. Context-Aware Architecture Implementation

Siguiendo las [Work Plan Development Rules (LLM 2024-2025)](02_ClassSphere_glosario_tecnico.md#work-plan-development-rules-llm-2024-2025):

**Context Window Management en Servicios:**
```python
# ✅ ARQUITECTURA CONTEXT-AWARE - Chunking por prioridad
class ContextAwareService:
    """Servicio con gestión de contexto según prioridad 2024-2025"""

    def __init__(self, priority: str = "MEDIUM"):
        self.priority = priority
        self.max_tokens = self._get_max_tokens(priority)
        self.context_id = f"{priority.lower()}-{uuid4().hex[:8]}"

    def _get_max_tokens(self, priority: str) -> int:
        """Límites de tokens según prioridad (LLM 2024-2025)"""
        limits = {
            "CRITICAL": 2000,  # auth, config, main.py
            "HIGH": 1500,      # google_service, classroom_service
            "MEDIUM": 1000,    # components, charts
            "LOW": 800         # admin, a11y
        }
        return limits.get(priority, 1000)

    async def log_context_status(self, status: str, **kwargs):
        """Log estructurado según template obligatorio"""
        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "context_id": self.context_id,
            "token_count": kwargs.get("token_count", 0),
            "context_priority": self.priority,
            "status": status,
            "memory_management": {
                "chunk_position": kwargs.get("chunk_position", "middle"),
                "lost_in_middle_risk": kwargs.get("risk", "low")
            }
        }

        # Log a archivo temporal para tracking LLM
        with open("/tmp/classsphere_context_status.json", "a") as f:
            f.write(json.dumps(log_entry) + "\n")
```

**Anti Lost-in-the-Middle Service Structure:**
```python
# ✅ ARQUITECTURA ANTI LOST-IN-THE-MIDDLE
class AntiLostInMiddleService:
    """Servicio estructurado para prevenir pérdida de contexto"""

    async def execute_with_context_priority(self, task_data: dict):
        """
        Estructura Anti Lost-in-the-Middle:
        - inicio: objetivos críticos + dependencias bloqueantes
        - medio: implementación detallada + casos de uso
        - final: checklist verificación + próximos pasos
        """

        # INICIO (primacy bias): información crítica
        critical_objectives = task_data.get("critical_objectives", [])
        blocking_dependencies = task_data.get("blocking_dependencies", [])

        # Log inicio con prioridad alta
        await self.log_context_status(
            "started",
            chunk_position="beginning",
            risk="low",
            token_count=len(str(critical_objectives))
        )

        # MEDIO: implementación detallada (riesgo de pérdida)
        detailed_implementation = task_data.get("implementation", {})
        use_cases = task_data.get("use_cases", [])

        # Log medio con gestión de riesgo
        await self.log_context_status(
            "in_progress",
            chunk_position="middle",
            risk="medium",
            token_count=len(str(detailed_implementation))
        )

        # FINAL (recency bias): próximos pasos críticos
        verification_checklist = task_data.get("verification", [])
        next_steps = task_data.get("next_steps", [])

        # Log final con prioridad alta
        await self.log_context_status(
            "completed",
            chunk_position="end",
            risk="low",
            token_count=len(str(verification_checklist))
        )

        return {
            "critical_processed": critical_objectives,
            "next_actions": next_steps,
            "verification_required": verification_checklist
        }
```

### 2. Infraestructura Estándar

Siguiendo la definición de [Puerto 8000 - Estándar Arquitectónico](02_ClassSphere_glosario_tecnico.md#puerto-8000---estándar-arquitectónico):

**Puerto Fijo**: Implementación obligatoria en puerto 8000
**Limpieza Automática**: Scripts estándar para limpieza de procesos
**Verificación**: Checks automáticos de disponibilidad de puerto

### 3. Implementación Evolutiva

Siguiendo las definiciones del [Glosario Técnico](02_ClassSphere_glosario_tecnico.md#arquitectura-semántica-simplificada):

**Migración Automática**: Implementación transparente de APIs modernas
**Verificación Post-Implementación**: Checks automáticos de éxito
**Ciclo de Vida**: Integración en el desarrollo arquitectónico

## Estructura de Directorios Completa

```
/
├── docs/
│   ├── architecture/
│   │   ├── overview.md           # Visión general de la arquitectura
│   │   ├── backend.md           # Arquitectura del backend
│   │   ├── frontend.md          # Arquitectura del frontend
│   │   ├── testing.md           # Estrategia de testing (Next.js 15 + React 19)
│   │   ├── security.md          # Arquitectura de seguridad
│   │   ├── deployment.md        # Estrategia de deployment
│   │   └── monitoring.md        # Estrategia de monitoreo
│   └── api/                    # Documentación de API
├── backend/
│   ├── app/
│   │   ├── api/
│   │   │   └── endpoints/
│   │   │       ├── auth.py                    # Stage 1
│   │   │       ├── oauth.py                   # Stage 1
│   │   │       ├── health.py                  # Stage 1
│   │   │       ├── dashboard.py               # Stage 2
│   │   │       ├── courses.py                 # Stage 2
│   │   │       ├── students.py                # Stage 2
│   │   │       ├── search.py                  # Stage 3
│   │   │       ├── notifications.py           # Stage 3
│   │   │       ├── websocket.py               # Stage 3
│   │   │       ├── google_sync.py             # Stage 4
│   │   │       ├── google_admin.py            # Stage 4
│   │   │       └── webhooks.py                # Stage 4
│   │   ├── services/
│   │   │   ├── auth_service.py                # Stage 1
│   │   │   ├── oauth_service.py               # Stage 1
│   │   │   ├── mock_service.py                # Stage 1
│   │   │   ├── google_service.py              # Stage 2
│   │   │   ├── classroom_service.py           # Stage 2
│   │   │   ├── metrics_service.py             # Stage 2
│   │   │   ├── search_service.py              # Stage 3
│   │   │   ├── notification_service.py        # Stage 3
│   │   │   ├── websocket_service.py           # Stage 3
│   │   │   ├── google_sync_service.py         # Stage 4
│   │   │   ├── conflict_resolution_service.py # Stage 4
│   │   │   └── backup_service.py              # Stage 4
│   │   ├── models/
│   │   │   ├── user.py                        # Stage 1
│   │   │   ├── oauth_token.py                 # Stage 1
│   │   │   ├── course.py                      # Stage 2
│   │   │   ├── student.py                     # Stage 2
│   │   │   ├── metric.py                      # Stage 2
│   │   │   ├── notification.py                # Stage 3
│   │   │   └── sync_status.py                 # Stage 4
│   │   ├── core/
│   │   │   ├── config.py
│   │   │   ├── security.py
│   │   │   └── exceptions.py
│   │   ├── middleware/
│   │   │   ├── auth_middleware.py
│   │   │   ├── oauth_middleware.py
│   │   │   ├── google_auth_middleware.py
│   │   │   └── rate_limit_middleware.py
│   │   ├── utils/
│   │   │   ├── logger.py
│   │   │   ├── response_helper.py
│   │   │   ├── google_helper.py
│   │   │   ├── cache_helper.py
│   │   │   └── metrics_helper.py
│   │   └── data/
│   │       └── mock_users.json
│   ├── tests/
│   │   ├── unit/
│   │   ├── integration/
│   │   ├── performance/
│   │   └── conftest.py
│   ├── Dockerfile
│   ├── requirements.txt
│   ├── pytest.ini
│   └── .env.example
├── frontend/
│   ├── src/
│   │   ├── app/
│   │   │   ├── (auth)/
│   │   │   │   ├── login/page.tsx             # Stage 1
│   │   │   │   └── oauth/
│   │   │   │       ├── callback/page.tsx     # Stage 1
│   │   │   │       └── page.tsx              # Stage 1
│   │   │   ├── dashboard/
│   │   │   │   ├── page.tsx                  # Stage 1
│   │   │   │   ├── admin/page.tsx            # Stage 2
│   │   │   │   ├── coordinator/page.tsx      # Stage 2
│   │   │   │   ├── teacher/page.tsx          # Stage 2
│   │   │   │   └── student/page.tsx          # Stage 2
│   │   │   ├── courses/
│   │   │   │   ├── page.tsx                  # Stage 2
│   │   │   │   └── [id]/page.tsx             # Stage 2
│   │   │   ├── search/
│   │   │   │   ├── page.tsx                  # Stage 3
│   │   │   │   └── [id]/page.tsx             # Stage 3
│   │   │   ├── notifications/
│   │   │   │   └── page.tsx                  # Stage 3
│   │   │   ├── admin/
│   │   │   │   └── google/
│   │   │   │       ├── page.tsx              # Stage 4
│   │   │   │       ├── sync/page.tsx         # Stage 4
│   │   │   │       └── backup/page.tsx       # Stage 4
│   │   │   ├── layout.tsx
│   │   │   ├── globals.css
│   │   │   └── page.tsx
│   │   ├── components/
│   │   │   ├── ui/                           # Stage 1
│   │   │   │   ├── Button.tsx
│   │   │   │   ├── Card.tsx
│   │   │   │   ├── Input.tsx
│   │   │   │   └── Layout.tsx
│   │   │   ├── auth/                         # Stage 1
│   │   │   │   ├── LoginForm.tsx
│   │   │   │   ├── OAuthButton.tsx
│   │   │   │   └── AuthGuard.tsx
│   │   │   ├── google/                       # Stage 2
│   │   │   │   ├── GoogleConnect.tsx
│   │   │   │   ├── CourseList.tsx
│   │   │   │   ├── ModeSelector.tsx
│   │   │   │   ├── SyncPanel.tsx             # Stage 4
│   │   │   │   ├── ConflictResolver.tsx      # Stage 4
│   │   │   │   └── PermissionsManager.tsx    # Stage 4
│   │   │   ├── dashboard/                    # Stage 2
│   │   │   │   ├── MetricCard.tsx
│   │   │   │   ├── ChartWidget.tsx
│   │   │   │   ├── CourseMetrics.tsx
│   │   │   │   └── StudentProgress.tsx
│   │   │   ├── charts/                       # Stage 2 + 3
│   │   │   │   ├── BarChart.tsx
│   │   │   │   ├── LineChart.tsx
│   │   │   │   ├── PieChart.tsx
│   │   │   │   ├── AdvancedChart.tsx         # Stage 3
│   │   │   │   └── DrillDownChart.tsx        # Stage 3
│   │   │   ├── search/                       # Stage 3
│   │   │   │   ├── SearchBar.tsx
│   │   │   │   ├── SearchResults.tsx
│   │   │   │   └── StudentDetail.tsx
│   │   │   ├── notifications/                # Stage 3
│   │   │   │   ├── NotificationCenter.tsx
│   │   │   │   ├── NotificationBadge.tsx
│   │   │   │   └── AlertBanner.tsx
│   │   │   ├── widgets/                      # Stage 3
│   │   │   │   ├── MetricWidget.tsx
│   │   │   │   ├── ChartWidget.tsx
│   │   │   │   └── CustomWidget.tsx
│   │   │   ├── admin/                        # Stage 4
│   │   │   │   ├── BackupControls.tsx
│   │   │   │   └── DiagnosticsTools.tsx
│   │   │   └── a11y/                         # Stage 4
│   │   │       ├── SkipLink.tsx
│   │   │       ├── FocusTrap.tsx
│   │   │       ├── ScreenReaderText.tsx
│   │   │       └── ContrastToggle.tsx
│   │   ├── hooks/
│   │   │   ├── useAuth.ts                    # Stage 1
│   │   │   ├── useOAuth.ts                   # Stage 1
│   │   │   ├── useApi.ts                     # Stage 1
│   │   │   ├── useTranslation.ts             # Stage 1
│   │   │   ├── useDashboardData.ts           # Stage 1
│   │   │   ├── useNotifications.ts           # Stage 1
│   │   │   ├── useGoogleClassroom.ts         # Stage 2
│   │   │   ├── useMetrics.ts                 # Stage 2
│   │   │   ├── useCharts.ts                  # Stage 2 + 3
│   │   │   ├── useSearch.ts                  # Stage 3
│   │   │   ├── useNotifications.ts           # Stage 3
│   │   │   └── useA11y.ts                    # Stage 4
│   │   ├── lib/
│   │   │   ├── api.ts                        # Stage 1
│   │   │   ├── auth.ts                       # Stage 1
│   │   │   ├── oauth.ts                      # Stage 1
│   │   │   ├── utils.ts                      # Stage 1
│   │   │   ├── google.ts                     # Stage 2
│   │   │   ├── metrics.ts                    # Stage 2
│   │   │   ├── charts.ts                     # Stage 2
│   │   │   ├── search.ts                     # Stage 3
│   │   │   └── notifications.ts              # Stage 3
│   │   ├── types/
│   │   │   ├── auth.types.ts                 # Stage 1
│   │   │   ├── oauth.types.ts                # Stage 1
│   │   │   ├── api.types.ts                  # Stage 1
│   │   │   ├── dashboard.types.ts            # Stage 1
│   │   │   ├── google.types.ts               # Stage 2
│   │   │   ├── course.types.ts               # Stage 2
│   │   │   ├── metrics.types.ts              # Stage 2
│   │   │   ├── search.types.ts               # Stage 3
│   │   │   ├── notification.types.ts         # Stage 3
│   │   │   └── chart.types.ts                # Stage 3
│   │   ├── i18n/
│   │   │   ├── config.ts
│   │   │   ├── locales/
│   │   │   │   └── en.json
│   │   │   └── types.ts
│   │   ├── providers/
│   │   │   └── QueryProvider.tsx
│   │   └── styles/
│   │       └── a11y.css
│   ├── tests/
│   │   ├── e2e/
│   │   ├── performance/
│   │   └── visual/
│   ├── public/
│   │   └── favicon.ico
│   ├── Dockerfile
│   ├── package.json
│   ├── next.config.js
│   ├── tailwind.config.js
│   ├── vitest.config.ts
│   ├── playwright.config.ts
│   └── .env.local.example
├── scripts/
│   ├── check-ports.sh
│   ├── cleanup-ports.sh
│   ├── generate-favicon.py
│   └── recovery/
│       ├── api_failure.sh
│       ├── database_recovery.sh
│       ├── oauth_reset.sh
│       └── sync_recovery.sh
├── .github/
│   └── workflows/
│       ├── test.yml
│       ├── build.yml
│       ├── deploy.yml
│       ├── docker-deploy.yml
│       └── accessibility.yml
├── docker-compose.yml
├── docker-compose.test.yml
├── .gitignore
└── README.md
```

## Arquitectura de Servicios con Prevención de Errores

### 1. Servicios Resilientes con Puerto 8000

**Metodología**: Todos los servicios usan puerto 8000 como estándar arquitectónico

**Arquitectura de Servicios Backend:**
```python
# ✅ ARQUITECTURA ESTÁNDAR - Servicios con puerto fijo
from fastapi import FastAPI
from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup - servicios externos opcionales (instalación nueva)
    try:
        # Google Classroom API (verificación)
        await verify_google_api_access()
    except Exception as e:
        print(f"Warning: Google Classroom API no disponible: {e}")
    
    try:
        # Redis (opcional)
        await init_redis()
    except Exception as e:
        print(f"Warning: Redis no disponible: {e}")
    
    yield
    
    # Shutdown - limpieza automática
    try:
        await cleanup_services()
    except Exception as e:
        print(f"Warning: Error en cleanup: {e}")

def create_app() -> FastAPI:
    return FastAPI(
        title="ClassSphere",
        version="1.0.0",
        lifespan=lifespan
    )

# Servidor siempre en puerto 8000
if __name__ == "__main__":
    uvicorn.run(
        "src.app.main:app",
        host="127.0.0.1",
        port=8000,  # Puerto fijo arquitectónico
        reload=True
    )
```

## Documentación de Arquitectura

La documentación detallada de arquitectura se encuentra en el directorio `docs/architecture/` y contiene los siguientes archivos clave:

```
docs/architecture/
├── overview.md           # Visión general de la arquitectura
├── backend.md           # Arquitectura del backend
├── frontend.md          # Arquitectura del frontend
├── testing.md           # Estrategia de testing (Next.js 15 + React 19)
├── security.md          # Arquitectura de seguridad
├── deployment.md        # Estrategia de deployment
└── monitoring.md        # Estrategia de monitoreo
```

El archivo `docs/architecture/testing.md` contiene la documentación completa sobre la estrategia de testing, incluyendo:

- Stack de testing definido (Vitest + React Testing Library + Playwright)
- Justificación de la eliminación de Jest
- Ejemplos de configuración y uso
- Estrategias de migración

## Referencias a Otros Documentos

- Para detalles sobre términos técnicos, consulte el [Glosario Técnico](02_ClassSphere_glosario_tecnico.md).
- Para los objetivos del sistema, consulte [Objetivos del Sistema](04_ClassSphere_objetivos.md).
- Para las funcionalidades del sistema, consulte [Funcionalidades Consolidadas](06_ClassSphere_funcionalidades.md).
- Para la estrategia de testing completa, consulte [Estrategia de Testing](09_ClassSphere_testing.md).

---

[← Objetivos del Sistema](04_ClassSphere_objetivos.md) | [Índice](00_ClassSphere_index.md) | [Siguiente → Funcionalidades Consolidadas](06_ClassSphere_funcionalidades.md)
