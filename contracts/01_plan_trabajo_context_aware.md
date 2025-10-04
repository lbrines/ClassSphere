---
llm:metadata:
  title: "Plan de Trabajo Context-Aware - Dashboard Educativo"
  version: "1.0"
  type: "context_aware_work_plan"
  stage: "implementation_roadmap"
  execution_priority: "context_management_first"
  contains:
    - work_plan_development_rules_llm_2024_2025
    - context_window_management
    - anti_lost_in_middle_structure
    - contextual_retrieval_strategies
    - tmux_integration_best_practices
    - structured_logging_templates
    - semantic_coherence_protocols
    - chunking_priority_system
    - error_prevention_context_aware
---

# Plan de Trabajo Context-Aware - Dashboard Educativo

## Información del Proyecto
- **Proyecto**: Dashboard Educativo - Sistema Completo
- **Plan**: Context-Aware Work Plan con LLM Best Practices 2024-2025
- **Autor**: Sistema de Contratos LLM
- **Fecha**: 2025-10-04 (Implementa Work Plan Development Rules LLM 2024-2025)
- **Propósito**: Plan de trabajo que implementa las mejores prácticas de gestión de contexto para LLMs basadas en papers de 2024-2025

## =====
<llm:section id="context_management_foundation" type="context_rules">
## Fundamentos de Gestión de Contexto

### Aplicación de Work Plan Development Rules (LLM 2024-2025)

Siguiendo las **[Work Plan Development Rules (LLM 2024-2025)](00_dashboard_educativo_fullstack_unified_complete.md#work-plan-development-rules-llm-2024-2025)** del contrato principal:

#### **Context Window Management por Prioridad**
```yaml
Chunking Estratégico:
  CRITICAL: máximo 2000 tokens
    - Tareas: autenticación, configuración, main.py, seguridad
    - Contexto: información bloqueante para el proyecto
    - Posición: beginning (primacy bias)

  HIGH: máximo 1500 tokens
    - Tareas: google_service, classroom_service, APIs principales
    - Contexto: funcionalidad core del sistema
    - Posición: beginning-middle

  MEDIUM: máximo 1000 tokens
    - Tareas: components, charts, UI/UX
    - Contexto: funcionalidad secundaria
    - Posición: middle

  LOW: máximo 800 tokens
    - Tareas: admin, a11y, optimizaciones
    - Contexto: mejoras y refinamiento
    - Posición: end (recency bias)
```

#### **Anti Lost-in-the-Middle Structure Obligatoria**
Cada fase del plan debe estructurarse como:

**INICIO (Primacy Bias)**:
- Objetivos críticos de la fase
- Dependencias bloqueantes
- Criterios de éxito obligatorios
- Context ID y token count

**MEDIO (Detailed Implementation)**:
- Implementación específica paso a paso
- Casos de uso detallados
- Configuraciones técnicas
- Manejo de errores

**FINAL (Recency Bias)**:
- Checklist de verificación
- Comandos de validación
- Próximos pasos críticos
- Context status update

#### **Template de Logs Estructurados Obligatorio**
```json
{
  "timestamp": "2025-10-04T10:00:00Z",
  "context_id": "phase-1-auth-critical-001",
  "token_count": 1247,
  "context_priority": "CRITICAL",
  "status": "started|in_progress|completed|failed|blocked",
  "memory_management": {
    "chunk_position": "beginning",
    "lost_in_middle_risk": "low"
  },
  "phase": "1",
  "task": "authentication_setup",
  "dependencies": ["config", "pydantic_v2"],
  "next_action": "implement_jwt_service",
  "coherence_check": {
    "glossary_references": 5,
    "terminology_consistency": "9.0/10"
  }
}
```

### Contextual Retrieval Strategies (Anthropic 2024)

#### **Descripción Contextualizada para Cada Chunk**
Cada tarea incluye:
- **Contexto previo**: Estado del sistema antes de la tarea
- **Contexto objetivo**: Estado deseado después de la tarea
- **Contexto de dependencias**: Referencias al glosario técnico
- **Contexto de continuación**: Enlaces a próximas tareas

#### **RAG para Conocimiento Externo**
- Referencias automáticas al **[Glosario Técnico Unificado](00_dashboard_educativo_fullstack_unified_complete.md#glosario-técnico-unificado)**
- Enlaces a **[Error Prevention Protocols](00_dashboard_educativo_fullstack_unified_complete.md#error-prevention-protocols)**
- Conexiones con **[Template Method Pattern](00_dashboard_educativo_fullstack_unified_complete.md#template-method-pattern)**

#### **Strategic Truncation**
- Preservar información **CRITICAL** en cada chunk
- Comprimir detalles de implementación en contexto **MEDIUM**
- Eliminar información redundante en contexto **LOW**

</llm:section>

## =====
<llm:section id="tmux_integration_strategy" type="tmux_management">
## Estrategia de Integración Tmux Context-Aware

### Tmux Session Management con Context Tracking

Basado en las mejores prácticas de 2024 para CI/CD frontend y las **[Work Plan Development Rules](00_dashboard_educativo_fullstack_unified_complete.md#work-plan-development-rules-llm-2024-2025)**:

#### **Context-Aware Tmux Sessions**
```bash
#!/bin/bash
# Context-Aware Tmux Session Management
# Implementa Work Plan Development Rules (LLM 2024-2025)
set -e

# Context Management Functions
init_context_logging() {
    mkdir -p /tmp/dashboard_context
    touch /tmp/dashboard_context_status.json
    touch /tmp/dashboard_tmux_context.log

    # Initial context log (CRITICAL priority)
    cat > /tmp/dashboard_context_status.json << EOF
{
  "timestamp": "$(date -Iseconds)",
  "context_id": "tmux-init-$(date +%s)",
  "token_count": 0,
  "context_priority": "CRITICAL",
  "status": "started",
  "memory_management": {
    "chunk_position": "beginning",
    "lost_in_middle_risk": "low"
  },
  "tmux_phase": "initialization"
}
EOF
}

# Context-Aware Session Creation
create_context_aware_sessions() {
    local PHASE=$1
    local CONTEXT_PRIORITY=$2

    echo "🚀 [CONTEXT-INIT] Creando sesiones tmux para Fase $PHASE (Prioridad: $CONTEXT_PRIORITY)"

    # Backend Session (CRITICAL priority)
    tmux new-session -d -s "edu-dashboard-backend-p$PHASE"
    tmux send-keys -t "edu-dashboard-backend-p$PHASE" "cd backend" Enter
    tmux send-keys -t "edu-dashboard-backend-p$PHASE" "echo '🔧 [BACKEND-$CONTEXT_PRIORITY] Fase $PHASE iniciada'" Enter

    # Frontend Session (HIGH/MEDIUM priority based on phase)
    tmux new-session -d -s "edu-dashboard-frontend-p$PHASE"
    tmux send-keys -t "edu-dashboard-frontend-p$PHASE" "cd frontend" Enter
    tmux send-keys -t "edu-dashboard-frontend-p$PHASE" "echo '⚡ [FRONTEND-$CONTEXT_PRIORITY] Fase $PHASE iniciada'" Enter

    # Context Monitoring Session (LOW priority)
    tmux new-session -d -s "edu-dashboard-context-p$PHASE"
    tmux send-keys -t "edu-dashboard-context-p$PHASE" "echo '📊 [CONTEXT-MONITOR] Fase $PHASE - Monitoring activo'" Enter
    tmux send-keys -t "edu-dashboard-context-p$PHASE" "tail -f /tmp/dashboard_context_status.json" Enter

    # Log context creation
    log_context_status "tmux-sessions-p$PHASE" "$CONTEXT_PRIORITY" "completed" "beginning" "Tmux sessions created for phase $PHASE"
}

# Context Status Logging Function
log_context_status() {
    local context_id=$1
    local priority=$2
    local status=$3
    local position=$4
    local message=$5

    cat >> /tmp/dashboard_context_status.json << EOF
{
  "timestamp": "$(date -Iseconds)",
  "context_id": "$context_id",
  "token_count": ${#message},
  "context_priority": "$priority",
  "status": "$status",
  "memory_management": {
    "chunk_position": "$position",
    "lost_in_middle_risk": "low"
  },
  "component": "tmux_management",
  "message": "$message"
}
EOF
}

# Initialize context logging
init_context_logging
```

#### **Fase-Specific Tmux Commands**

**Fase 1 (CRITICAL Context - Fundaciones)**:
```bash
# Crear sesiones para fundaciones (máximo 2000 tokens por chunk)
create_context_aware_sessions "1" "CRITICAL"

# Backend Session Commands (CRITICAL priority)
tmux send-keys -t "edu-dashboard-backend-p1" "python3 -m uvicorn src.app.main:app --host 127.0.0.1 --port 8000" Enter

# Context Monitoring (chunk position: beginning)
tmux send-keys -t "edu-dashboard-context-p1" "echo 'Context Phase 1: Fundaciones - Token limit 2000'" Enter
```

**Fase 2 (HIGH Context - Google Integration)**:
```bash
# Crear sesiones para Google integration (máximo 1500 tokens por chunk)
create_context_aware_sessions "2" "HIGH"

# Context Monitoring (chunk position: beginning-middle)
tmux send-keys -t "edu-dashboard-context-p2" "echo 'Context Phase 2: Google Integration - Token limit 1500'" Enter
```

### Context Recovery and Health Checks

#### **Context-Aware Health Verification**
```bash
# Context-Aware Health Check
verify_context_health() {
    local phase=$1
    local expected_priority=$2

    echo "🔍 [CONTEXT-HEALTH] Verificando salud contextual Fase $phase"

    # Verify tmux sessions exist
    if tmux has-session -t "edu-dashboard-backend-p$phase" 2>/dev/null; then
        echo "✅ [CONTEXT-OK] Backend session Fase $phase activa"
    else
        echo "❌ [CONTEXT-FAIL] Backend session Fase $phase no encontrada"
        log_context_status "health-check-p$phase" "CRITICAL" "failed" "middle" "Backend session missing for phase $phase"
        return 1
    fi

    # Verify context log integrity
    if jq empty /tmp/dashboard_context_status.json 2>/dev/null; then
        echo "✅ [CONTEXT-OK] Context log válido"
    else
        echo "❌ [CONTEXT-FAIL] Context log corrupto"
        log_context_status "health-check-p$phase" "CRITICAL" "failed" "middle" "Context log corrupted"
        return 1
    fi

    # Verify server health for backend phases
    if [ "$phase" -ge 1 ]; then
        if curl -f http://127.0.0.1:8000/health &>/dev/null; then
            echo "✅ [CONTEXT-OK] Backend health check exitoso"
            log_context_status "health-check-p$phase" "$expected_priority" "completed" "middle" "Health check successful for phase $phase"
        else
            echo "❌ [CONTEXT-FAIL] Backend health check falló"
            log_context_status "health-check-p$phase" "CRITICAL" "failed" "middle" "Backend health check failed"
            return 1
        fi
    fi

    return 0
}
```

</llm:section>

## =====
<llm:section id="phase_implementation_context_aware" type="implementation_phases">
## Fases de Implementación Context-Aware

### **INICIO (Primacy Bias) - Objetivos Críticos**

**Objetivo Principal**: Implementar Dashboard Educativo completo siguiendo **[Work Plan Development Rules (LLM 2024-2025)](00_dashboard_educativo_fullstack_unified_complete.md#work-plan-development-rules-llm-2024-2025)** con gestión de contexto óptima.

**Dependencias Bloqueantes**:
- Coherencia semántica con **[Glosario Técnico Unificado](00_dashboard_educativo_fullstack_unified_complete.md#glosario-técnico-unificado)**
- Implementación de **[Error Prevention Protocols](00_dashboard_educativo_fullstack_unified_complete.md#error-prevention-protocols)**
- Sistema de logs estructurados en `/tmp/dashboard_context_status.json`

**Criterios de Éxito Obligatorios**:
- Cada fase debe mantener coherencia semántica ≥ 9.0/10
- Context logs deben actualizarse automáticamente
- Tmux sessions deben persistir entre fases
- Token count debe respetarse por prioridad

---

### **MEDIO (Detailed Implementation) - Fases Específicas**

## Fase 1: Fundaciones Context-Aware (Días 1-10)

**Context Priority**: CRITICAL (máximo 2000 tokens por chunk)
**Chunk Position**: beginning
**Lost-in-Middle Risk**: low

### Día 1-2: Backend Fundacional con Context Management

**Context ID**: `phase-1-backend-critical-001`

**TDD Approach con Context Awareness**:
```bash
# INICIO (primacy bias): Verificación de contexto obligatoria
verify_context_before_task() {
    echo "🔍 [CONTEXT-VERIFY] Verificando contexto antes de Día 1-2"

    # Verificar coherencia semántica
    local glossary_refs=$(jq '.coherence_check.glossary_references' /tmp/dashboard_context_status.json 2>/dev/null || echo 0)
    if [ "$glossary_refs" -lt 3 ]; then
        echo "⚠️ [CONTEXT-WARNING] Referencias al glosario insuficientes"
        exit 1
    fi

    # Inicializar context logging para esta tarea
    log_context_status "phase-1-backend-critical-001" "CRITICAL" "started" "beginning" "Backend foundational setup started"
}

# Ejecutar verificación obligatoria
verify_context_before_task
```

**Implementación Detallada**:

1. **Estructura Backend** (Token count: ~500):
   - Crear `backend/` siguiendo **[Arquitectura Resiliente](00_dashboard_educativo_fullstack_unified_complete.md#arquitectura-resiliente-con-prevención-de-errores)**
   - Configurar `requirements.txt` con FastAPI 0.104.1, Pydantic v2
   - Implementar **[Puerto 8000 - Estándar Arquitectónico](00_dashboard_educativo_fullstack_unified_complete.md#puerto-8000---estándar-arquitectónico)**

2. **Configuración Pydantic v2** (Token count: ~400):
   - Seguir **[Pydantic v2 - Migración Automática](00_dashboard_educativo_fullstack_unified_complete.md#pydantic-v2---migración-automática)**
   - Implementar `ConfigDict` moderno
   - Configurar `BaseSettings` con validación estricta

3. **FastAPI con Lifespan** (Token count: ~600):
   - Implementar **[FastAPI Lifespan - Context Manager Estándar](00_dashboard_educativo_fullstack_unified_complete.md#fastapi-lifespan---context-manager-estándar)**
   - Context manager resiliente para startup/shutdown
   - Health check endpoint en `/health`

4. **Context Logging Integration** (Token count: ~300):
   ```python
   # Integración de context logging en la aplicación
   from datetime import datetime
   import json

   async def log_application_context(phase: str, task: str, status: str):
       context_entry = {
           "timestamp": datetime.now().isoformat(),
           "context_id": f"app-{phase}-{task}",
           "context_priority": "CRITICAL",
           "status": status,
           "memory_management": {
               "chunk_position": "beginning",
               "lost_in_middle_risk": "low"
           }
       }

       with open("/tmp/dashboard_context_status.json", "a") as f:
           f.write(json.dumps(context_entry) + "\n")
   ```

**Tmux Integration para Día 1-2**:
```bash
# INICIO (primacy): Crear sesiones context-aware
create_context_aware_sessions "1" "CRITICAL"

# MEDIO: Ejecutar tareas en sesiones tmux
tmux send-keys -t "edu-dashboard-backend-p1" "cd backend && python3 -m uvicorn src.app.main:app --host 127.0.0.1 --port 8000 --reload" Enter

# Context monitoring
tmux send-keys -t "edu-dashboard-context-p1" "echo '[CONTEXT-TRACK] Día 1-2: Backend fundacional en progreso'" Enter

# FINAL (recency): Verificar estado
sleep 5
verify_context_health "1" "CRITICAL"
```

### Día 3-4: Autenticación Dual con Context Tracking

**Context ID**: `phase-1-auth-critical-002`
**Token Count Estimate**: 1800 tokens (dentro del límite CRITICAL de 2000)

**Context-Aware Implementation**:

1. **JWT Service** (Token count: ~600):
   - Implementar `AuthService` con tokens seguros
   - Campo 'sub' estándar en payload
   - Refresh token rotation
   - Context logging para cada operación de auth

2. **OAuth 2.0 Google** (Token count: ~700):
   - Seguir **[Instalación Nueva Google Classroom](00_dashboard_educativo_fullstack_unified_complete.md#instalación-nueva-google-classroom)**
   - PKCE + State validation
   - Scopes limitados para seguridad
   - Modo dual desde instalación inicial

3. **Template Method Pattern** (Token count: ~500):
   - Implementar **[Template Method Pattern](00_dashboard_educativo_fullstack_unified_complete.md#template-method-pattern)** para excepciones de auth
   - `BaseAPIException` con `_build_message()`
   - `AuthenticationError`, `TokenExpiredError`, `OAuthError`

**Context Status Update**:
```bash
# FINAL (recency bias): Actualizar contexto al completar autenticación
log_context_status "phase-1-auth-critical-002" "CRITICAL" "completed" "beginning" "Dual authentication implemented with context tracking"
```

### Día 5-7: Frontend Fundacional Context-Aware

**Context Priority**: HIGH (máximo 1500 tokens por chunk)
**Context ID**: `phase-1-frontend-high-003`

**Context-Aware Frontend Setup**:

1. **Next.js 13.5.6 Setup** (Token count: ~500):
   - Configurar estructura siguiendo **[Stack Tecnológico Consolidado](00_dashboard_educativo_fullstack_unified_complete.md#stack-tecnológico-consolidado)**
   - TypeScript 5.1.6 + Tailwind CSS 3.3.3
   - React Query v4 para estado global

2. **Context-Aware Components** (Token count: ~600):
   ```typescript
   // Context-aware component template
   interface ContextAwareComponentProps {
     contextId: string;
     priority: 'CRITICAL' | 'HIGH' | 'MEDIUM' | 'LOW';
   }

   export const ContextAwareComponent: React.FC<ContextAwareComponentProps> = ({
     contextId,
     priority,
     children
   }) => {
     useEffect(() => {
       // Log component context
       logComponentContext(contextId, priority, 'mounted');
     }, [contextId, priority]);

     return <div data-context-id={contextId}>{children}</div>;
   };
   ```

3. **Auth Components** (Token count: ~400):
   - `LoginForm` con validación integrada
   - `AuthGuard` para rutas protegidas
   - `useAuth` hook con React Query
   - Context logging para auth flows

**Tmux Frontend Integration**:
```bash
# Frontend development con context tracking
tmux send-keys -t "edu-dashboard-frontend-p1" "npm run dev" Enter
tmux send-keys -t "edu-dashboard-context-p1" "echo '[CONTEXT-TRACK] Frontend con Context-Aware components activo'" Enter
```

### Día 8-10: Integración y Testing Context-Aware

**Context Priority**: MEDIUM (máximo 1000 tokens por chunk)
**Context ID**: `phase-1-integration-medium-004`

**Context-Aware Integration**:

1. **API Communication** (Token count: ~400):
   - `useApi` hook con React Query
   - Interceptors para auth tokens
   - Error handling centralizado
   - Context logging para requests

2. **Testing Context-Aware** (Token count: ~400):
   ```typescript
   // Context-aware testing template
   describe('Context-Aware Component Tests', () => {
     beforeEach(() => {
       // Initialize context for testing
       initTestContext('test-component-001', 'MEDIUM');
     });

     it('should track context correctly', () => {
       // Test with context awareness
       render(<ComponentWithContext contextId="test-001" priority="MEDIUM" />);
       expect(getContextLog()).toContain('test-001');
     });
   });
   ```

3. **E2E Testing** (Token count: ~200):
   - Playwright configuration
   - Context tracking en tests E2E
   - Health checks automatizados

---

## Fase 2: Google Integration Context-Aware (Días 11-20)

**Context Priority**: HIGH (máximo 1500 tokens por chunk)
**Chunk Position**: beginning-middle
**Lost-in-Middle Risk**: medium

### Día 11-13: Google Classroom API con Context Management

**Context ID**: `phase-2-google-high-005`

**Context-Aware Google Implementation**:

1. **Google Service** (Token count: ~600):
   - Implementar siguiendo **[Instalación Nueva Google Classroom](00_dashboard_educativo_fullstack_unified_complete.md#instalación-nueva-google-classroom)**
   - Mocks preconfigurados desde inicio
   - Rate limiting + fallback automático
   - Context logging para API calls

2. **Modo Dual Context-Aware** (Token count: ~500):
   - Service factory con context tracking
   - Switching Google/Mock con logs
   - Environment-based configuration
   - Context recovery en caso de fallo

3. **Cache Integration** (Token count: ~400):
   - Redis para datos Google API
   - Context-aware cache invalidation
   - Background refresh con logging

**Context Recovery Implementation**:
```python
# Context-aware recovery for Google API
async def recover_google_context(context_id: str, phase: str):
    """Recuperar contexto de Google API en caso de fallo"""
    try:
        # Log recovery attempt
        await log_application_context(phase, "google_recovery", "started")

        # Attempt to restore Google service
        service = await get_google_service_with_fallback()

        # Update context status
        await log_application_context(phase, "google_recovery", "completed")

        return service
    except Exception as e:
        await log_application_context(phase, "google_recovery", "failed")
        # Fallback to mock service
        return await get_mock_service()
```

### Día 14-16: Dashboards Context-Aware

**Context Priority**: MEDIUM (máximo 1000 tokens por chunk)
**Context ID**: `phase-2-dashboards-medium-006`

**Context-Aware Dashboard Implementation**:

1. **Role-based Dashboards** (Token count: ~400):
   - Admin, Coordinator, Teacher, Student views
   - Context tracking por rol
   - Métricas específicas con logs

2. **ApexCharts Integration** (Token count: ~400):
   - Charts v5.3.5 con context awareness
   - Interactive features con logging
   - Export functionality

3. **Responsive Design** (Token count: ~200):
   - Mobile-first approach
   - Context-aware breakpoints
   - Performance optimization

### Día 17-20: Métricas y Cache Context-Aware

**Context Priority**: MEDIUM (máximo 1000 tokens por chunk)
**Context ID**: `phase-2-metrics-medium-007`

**Context-Aware Metrics**:

1. **KPIs Educativos** (Token count: ~350):
   - Engagement, Risk, Performance scores
   - Context logging para cálculos
   - Trend analysis básico

2. **Cache Strategy** (Token count: ~350):
   - Redis con context awareness
   - Invalidación inteligente
   - Background jobs con logging

3. **Performance Optimization** (Token count: ~300):
   - <2s dashboard load time
   - Context tracking para performance
   - Memory usage optimization

---

## Fase 3: Visualización Avanzada Context-Aware (Días 21-30)

**Context Priority**: MEDIUM (máximo 1000 tokens por chunk)
**Chunk Position**: middle
**Lost-in-Middle Risk**: medium

### Día 21-23: Sistema de Búsqueda Context-Aware

**Context ID**: `phase-3-search-medium-008`

**Context-Aware Search Implementation**:

1. **SearchService** (Token count: ~400):
   - Multi-entity search con context
   - Filtros avanzados con logging
   - Resultados contextuales

2. **Search UI** (Token count: ~400):
   - SearchBar con context tracking
   - Real-time results
   - Export functionality

3. **Saved Searches** (Token count: ~200):
   - User preferences con context
   - Shared searches
   - History tracking

### Día 24-26: Notificaciones WebSocket Context-Aware

**Context ID**: `phase-3-notifications-medium-009`

**Context-Aware Notifications**:

1. **WebSocket Service** (Token count: ~400):
   - Real-time connections con context
   - Connection recovery
   - Fallback polling

2. **Multi-channel Delivery** (Token count: ~350):
   - WebSocket + Email + Telegram (mock)
   - Smart alerts con context
   - User preferences

3. **Notification Center** (Token count: ~250):
   - UI components context-aware
   - Badge updates
   - Push notifications

### Día 27-30: Visualizaciones D3.js Context-Aware

**Context ID**: `phase-3-d3-medium-010`

**Context-Aware Visualizations**:

1. **D3.js Integration** (Token count: ~350):
   - Custom visualizations con context
   - Animations fluidas
   - Interactive features

2. **Advanced Charts** (Token count: ~350):
   - Network graphs, heatmaps
   - Drill-down functionality
   - Export avanzado

3. **Widgets Personalizables** (Token count: ~300):
   - Drag & drop con context
   - Dashboard customization
   - Sharing functionality

---

## Fase 4: Production Ready Context-Aware (Días 31-40)

**Context Priority**: LOW (máximo 800 tokens por chunk)
**Chunk Position**: end
**Lost-in-Middle Risk**: low

### Día 31-33: Sincronización Avanzada Context-Aware

**Context ID**: `phase-4-sync-low-011`

**Context-Aware Sync Implementation**:

1. **Google Sync Service** (Token count: ~300):
   - Bidirectional sync con context
   - Conflict resolution
   - Incremental updates

2. **Backup System** (Token count: ~300):
   - Automated backups con logging
   - Point-in-time recovery
   - Data integrity checks

3. **Admin Panel** (Token count: ~200):
   - Sync controls context-aware
   - Diagnostics tools
   - Monitoring dashboard

### Día 34-36: Accesibilidad WCAG 2.2 Context-Aware

**Context ID**: `phase-4-a11y-low-012`

**Context-Aware Accessibility**:

1. **WCAG 2.2 AA Implementation** (Token count: ~300):
   - Keyboard navigation con context
   - Screen reader support
   - High contrast mode

2. **Accessibility Testing** (Token count: ~250):
   - Automated testing con axe-core
   - Manual validation
   - Context logging para a11y

3. **A11y Components** (Token count: ~250):
   - SkipLink, FocusTrap
   - ScreenReaderText
   - ContrastToggle

### Día 37-40: Production Deployment Context-Aware

**Context ID**: `phase-4-production-low-013`

**Context-Aware Production Setup**:

1. **CI/CD Pipeline** (Token count: ~300):
   - GitHub Actions con context
   - Quality gates automated
   - Context validation

2. **Docker Deployment** (Token count: ~250):
   - Multi-stage builds
   - Context environment variables
   - Health checks

3. **Monitoring & Alerts** (Token count: ~250):
   - Application monitoring
   - Context log aggregation
   - Alert system

---

### **FINAL (Recency Bias) - Verificación y Próximos Pasos**

## Checklist de Verificación Context-Aware

### **Verificación de Contexto por Fase**
```bash
#!/bin/bash
# Verificación final de contexto
verify_final_context() {
    echo "🔍 [FINAL-VERIFY] Verificación final de contexto"

    # Verificar logs de contexto
    if [ -f "/tmp/dashboard_context_status.json" ]; then
        echo "✅ [CONTEXT-OK] Logs de contexto presentes"

        # Verificar coherencia semántica
        local coherence=$(jq '.coherence_check.terminology_consistency' /tmp/dashboard_context_status.json 2>/dev/null || echo "0/10")
        if [[ "$coherence" > "8.0/10" ]]; then
            echo "✅ [COHERENCE-OK] Coherencia semántica: $coherence"
        else
            echo "❌ [COHERENCE-FAIL] Coherencia semántica insuficiente: $coherence"
            return 1
        fi
    else
        echo "❌ [CONTEXT-FAIL] Logs de contexto no encontrados"
        return 1
    fi

    # Verificar sesiones tmux de todas las fases
    for phase in {1..4}; do
        if tmux has-session -t "edu-dashboard-backend-p$phase" 2>/dev/null; then
            echo "✅ [TMUX-OK] Sesión backend Fase $phase activa"
        else
            echo "⚠️ [TMUX-WARNING] Sesión backend Fase $phase no activa"
        fi
    done

    # Verificar aplicación final
    if curl -f http://127.0.0.1:8000/health &>/dev/null; then
        echo "✅ [APP-OK] Aplicación respondiendo correctamente"
    else
        echo "❌ [APP-FAIL] Aplicación no responde"
        return 1
    fi

    echo "🎉 [FINAL-SUCCESS] Verificación context-aware completada"
    return 0
}

# Ejecutar verificación final
verify_final_context
```

### **Comandos de Validación Context-Aware**
```bash
# Validar coherencia semántica final
jq '.coherence_check' /tmp/dashboard_context_status.json

# Verificar todas las sesiones tmux
tmux list-sessions | grep "edu-dashboard"

# Health check completo
curl -f http://127.0.0.1:8000/health

# Verificar frontend
curl -f http://localhost:3000

# Generar reporte final de contexto
generate_context_report() {
    echo "📊 Reporte Final Context-Aware - $(date)" > /tmp/dashboard_final_context_report.log
    echo "Total chunks procesados: $(wc -l < /tmp/dashboard_context_status.json)" >> /tmp/dashboard_final_context_report.log
    echo "Coherencia semántica promedio: $(jq -r '.coherence_check.terminology_consistency' /tmp/dashboard_context_status.json | head -1)" >> /tmp/dashboard_final_context_report.log
    echo "Fases completadas: 4/4" >> /tmp/dashboard_final_context_report.log
}
```

### **Próximos Pasos Críticos**
1. **Monitoreo Continuo**: Configurar alertas para context logs
2. **Optimización**: Revisar token usage y optimizar chunks
3. **Escalabilidad**: Preparar para nuevas fases con context management
4. **Mantenimiento**: Configurar limpieza automática de logs antiguos

### **Context Recovery Procedures**
Si el contexto se pierde durante la implementación:

```bash
# Procedimiento de recovery context-aware
recover_lost_context() {
    echo "🔄 [CONTEXT-RECOVERY] Iniciando recuperación de contexto"

    # Recrear logs de contexto
    init_context_logging

    # Recrear sesiones tmux si es necesario
    for phase in {1..4}; do
        if ! tmux has-session -t "edu-dashboard-backend-p$phase" 2>/dev/null; then
            create_context_aware_sessions "$phase" "CRITICAL"
        fi
    done

    # Verificar coherencia semántica
    verify_context_health "current" "CRITICAL"

    echo "✅ [CONTEXT-RECOVERY] Recuperación completada"
}
```

</llm:section>

## =====
<llm:section id="quality_gates_context_aware" type="quality_assurance">
## Quality Gates Context-Aware

### Criterios de Aceptación por Fase con Context Management

#### **Fase 1 - Quality Gate Context-Aware**
- [ ] **Context Management**: Logs estructurados funcionando
- [ ] **Token Limits**: Respetados límites CRITICAL (2000 tokens)
- [ ] **Semantic Coherence**: ≥ 9.0/10 puntuación
- [ ] **Tmux Integration**: Sesiones persistentes funcionando
- [ ] **Backend Foundation**: FastAPI + Pydantic v2 + Puerto 8000
- [ ] **Frontend Foundation**: Next.js + React Query + Auth
- [ ] **Testing**: ≥ 90% cobertura con context tracking
- [ ] **Health Checks**: Endpoint `/health` respondiendo
- [ ] **Context Recovery**: Procedimientos de recovery funcionando

#### **Fase 2 - Quality Gate Context-Aware**
- [ ] **Google Integration**: API + Mocks funcionando con context
- [ ] **Token Limits**: Respetados límites HIGH (1500 tokens)
- [ ] **Dashboard Performance**: <2s load time con tracking
- [ ] **Cache Integration**: Redis con context-aware invalidation
- [ ] **ApexCharts**: Visualizaciones funcionando
- [ ] **Tmux Stability**: Sesiones Fase 2 estables
- [ ] **Context Continuity**: Enlaces entre Fase 1 y 2 manteni dos

#### **Fase 3 - Quality Gate Context-Aware**
- [ ] **Search System**: Funcionando con context tracking
- [ ] **WebSocket Notifications**: Real-time con recovery
- [ ] **Token Limits**: Respetados límites MEDIUM (1000 tokens)
- [ ] **D3.js Visualizations**: Interactive charts funcionando
- [ ] **Performance**: <1.5s load time
- [ ] **Context Monitoring**: Logs de contexto actualizándose
- [ ] **Lost-in-Middle Prevention**: Estructura mantenida

#### **Fase 4 - Quality Gate Context-Aware**
- [ ] **Production Ready**: Aplicación desplegable
- [ ] **Token Limits**: Respetados límites LOW (800 tokens)
- [ ] **WCAG 2.2 AA**: Accesibilidad completa con context
- [ ] **Performance**: <1s load time
- [ ] **CI/CD**: Pipeline con context validation
- [ ] **Context Reporting**: Reportes finales generados
- [ ] **Recovery Procedures**: Documentados y probados

### Context Validation Commands

```bash
# Validación completa context-aware
validate_context_implementation() {
    echo "🔍 Validación Context-Aware Completa"

    # 1. Verificar estructura de logs
    test -f "/tmp/dashboard_context_status.json" || exit 1

    # 2. Verificar coherencia semántica
    local coherence=$(jq -r '.coherence_check.terminology_consistency' /tmp/dashboard_context_status.json | head -1)
    [[ "$coherence" > "8.0/10" ]] || exit 1

    # 3. Verificar límites de tokens por fase
    local phase1_tokens=$(jq '.token_count' /tmp/dashboard_context_status.json | head -1)
    [ "$phase1_tokens" -le 2000 ] || exit 1

    # 4. Verificar tmux sessions
    tmux list-sessions | grep -q "edu-dashboard" || exit 1

    # 5. Verificar aplicación
    curl -f http://127.0.0.1:8000/health || exit 1

    echo "✅ Validación Context-Aware exitosa"
}
```

</llm:section>

---

**Referencias al Contrato Principal**:
- **[Glosario Técnico Unificado](00_dashboard_educativo_fullstack_unified_complete.md#glosario-técnico-unificado)**
- **[Work Plan Development Rules (LLM 2024-2025)](00_dashboard_educativo_fullstack_unified_complete.md#work-plan-development-rules-llm-2024-2025)**
- **[Error Prevention Protocols](00_dashboard_educativo_fullstack_unified_complete.md#error-prevention-protocols)**
- **[Template Method Pattern](00_dashboard_educativo_fullstack_unified_complete.md#template-method-pattern)**
- **[Arquitectura Resiliente](00_dashboard_educativo_fullstack_unified_complete.md#arquitectura-resiliente-con-prevención-de-errores)**

**Context Management Status**: ✅ Implementado con token limits, anti lost-in-the-middle structure, contextual retrieval strategies y tmux integration best practices.