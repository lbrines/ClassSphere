---
llm:metadata:
  title: "Contrato Unificado Completo: Dashboard Educativo Full-Stack"
  version: "2.3"
  type: "unified_implementation_contract"
  stage: "unified"
  execution_priority: "complete_system"
  contains:
    - complete_backend_foundation
    - complete_frontend_application
    - google_classroom_integration
    - advanced_visualizations
    - real_time_notifications
    - accessibility_wcag_2_2
    - comprehensive_testing
    - error_prevention_protocols
    - coverage_100_protocols
    - ci_cd_pipeline
    - production_deployment
---

# Contrato Unificado Completo: Dashboard Educativo Full-Stack

## Información del Proyecto
- **Proyecto**: Dashboard Educativo - Sistema Completo
- **Fase**: Implementación Unificada - Todas las Funcionalidades
- **Autor**: Sistema de Contratos LLM
- **Fecha**: 2025-10-03 (Actualizado con Prevención de Errores + Corrección de Warnings + Cobertura 100%)
- **Propósito**: Implementar sistema completo de dashboard educativo con todas las funcionalidades consolidadas

## =====
<llm:section id="unified_objectives" type="requirements">
## Objetivos del Sistema Unificado

### Backend - Sistema Completo
- **Fundaciones (Stage 1)**: FastAPI + JWT + OAuth 2.0 + MockService
- **Google Integration (Stage 2)**: Google Classroom API + Modo Dual + Métricas Básicas
- **Visualización Avanzada (Stage 3)**: Insights + Búsqueda + Notificaciones WebSocket
- **Integración Completa (Stage 4)**: Sincronización Bidireccional + Backup + Testing

### Frontend - Aplicación Completa
- **Fundaciones (Stage 1)**: Next.js 13.5.6 + React Query v4 + Tailwind CSS + i18n
- **Google UI (Stage 2)**: Selector de Modo + Lista de Cursos + Dashboards por Rol
- **Visualización Avanzada (Stage 3)**: Gráficos Interactivos + Búsqueda + Notificaciones
- **Gestión Completa (Stage 4)**: Panel Admin + Accesibilidad WCAG 2.2 + PWA

### Características Integradas
- **Autenticación Dual**: JWT + OAuth 2.0 con Google
- **Modo Dual**: Google Classroom (producción) + Mock (desarrollo)
- **Dashboards por Rol**: Admin, Coordinador, Teacher, Estudiante
- **Visualizaciones**: ApexCharts v5.3.5 + D3.js + Gráficos Interactivos
- **Notificaciones**: WebSocket + Email + Telegram (mock)
- **Búsqueda**: Avanzada + Filtros + Resultados Contextuales
- **Accesibilidad**: WCAG 2.2 AA + Navegación por Teclado + Screen Reader
- **Testing**: ≥90% críticos, ≥80% global + E2E + Performance + Visual
- **CI/CD**: GitHub Actions + Docker + Quality Gates + Auto-deploy

</llm:section>

## =====
<llm:section id="unified_architecture" type="project_structure">
## Arquitectura del Sistema Unificado

### Stack Tecnológico Consolidado
```
# Backend
- Python 3.11.4 (pyenv)
- FastAPI 0.104.1
- Pydantic v2 (validación estricta)
- Google Classroom API
- WebSockets (notificaciones)
- MongoDB + Redis
- pytest (testing)

# Frontend
- Next.js 13.5.6 (LTS)
- React 18.2.0
- TypeScript 5.1.6
- @tanstack/react-query 4.36.1
- ApexCharts 5.3.5
- Tailwind CSS 3.3.3
- Vitest + Playwright (testing)

# DevOps
- Docker (multi-stage)
- GitHub Actions
- Trivy (security)
- pnpm 8.x+
```

### Estructura de Directorios Completa
```
/
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

</llm:section>

## =====
<llm:section id="unified_features" type="features">
## Funcionalidades Consolidadas del Sistema

### 1. Autenticación y Autorización Completa (Stage 1 Base)
- **JWT Authentication**: Tokens seguros con refresh rotation
- **OAuth 2.0 with Google**: PKCE + State validation + Scopes limitados
- **Roles Sistema**: admin, coordinador, teacher, estudiante
- **Middleware Seguridad**: Rate limiting + CORS + Validation
- **Matriz Permisos**: Por rol y recurso
- **Session Management**: Persistencia + Auto-logout + Multi-device

### 2. Google Classroom Integration Completa (Stage 2 + 4)
- **Modo Dual**: Google (producción) + Mock (desarrollo)
- **API Integration**: Courses + Students + Assignments + Grades
- **Sincronización**: Bidireccional + Incremental + Programada
- **Conflict Resolution**: Automática + Manual + Audit trail
- **Webhooks**: Eventos en tiempo real + Signature validation
- **Backup & Recovery**: Automático + Selectivo + Point-in-time
- **Admin Panel**: Control total + Diagnósticos + Monitoreo

### 3. Dashboards Avanzados por Rol (Stage 2 + 3)
**Dashboard Administrador**:
- Vista general del sistema + KPIs institucionales
- Gestión de usuarios + permisos + configuración
- Análisis de tendencias + comparativas entre programas
- Métricas de uso del sistema + performance
- Panel de administración Google + sincronización
- Herramientas de backup + diagnóstico

**Dashboard Coordinador**:
- Métricas de programas asignados + análisis comparativo
- Seguimiento de teachers + evaluación de rendimiento
- Análisis de cohortes + predicción de resultados
- Reportes automáticos + exportación
- Gestión de cursos por programa

**Dashboard Teacher**:
- Análisis detallado de cursos propios
- Identificación automática de estudiantes en riesgo
- Herramientas de seguimiento + intervención
- Gestión de tareas + calificaciones sincronizadas
- Analytics de participación + engagement

**Dashboard Estudiante**:
- Progreso personalizado + metas individuales
- Calendario integrado + recordatorios
- Comparativas anónimas + gamificación
- Recomendaciones de estudio + recursos
- Notificaciones personalizadas

### 4. Visualizaciones Avanzadas (Stage 3)
- **ApexCharts v5.3.5**: Gráficos interactivos + drill-down
- **D3.js Integration**: Visualizaciones custom + animaciones
- **Real-time Updates**: WebSocket + React Query sync
- **Export Features**: PDF + PNG + SVG + Data export
- **Responsive Charts**: Mobile-first + adaptive layouts
- **Accessibility**: Screen reader + keyboard navigation
- **Custom Widgets**: Drag & drop + configurable + shareable

### 5. Sistema de Búsqueda Avanzada (Stage 3)
- **Multi-entity Search**: Students + Courses + Assignments
- **Contextual Filters**: Por rol + permisos + curso
- **Real-time Results**: Debounced + cached + highlighted
- **Advanced Filters**: Date ranges + status + performance
- **Saved Searches**: Favoritos + recent + shared
- **Export Results**: Multiple formats + bulk actions

### 6. Notificaciones en Tiempo Real (Stage 3)
- **WebSocket Real-time**: Instant delivery + connection recovery
- **Multi-channel**: In-app + Email + Telegram (mock)
- **Smart Alerts**: Risk detection + deadline reminders
- **Preferences**: Per user + per type + quiet hours
- **Push Notifications**: PWA + browser + mobile
- **Digest Options**: Daily + Weekly + Custom schedules

### 7. Métricas y Analytics Avanzados (Stage 3)
- **KPIs Educativos**: Engagement + Risk + Performance scores
- **Predictive Analytics**: Básico + trend analysis
- **Real-time Metrics**: 5min intervals + live dashboards
- **Comparative Analysis**: Temporal + cross-cohort + benchmarking
- **Custom Metrics**: User-defined + calculated fields
- **Automated Reports**: Scheduled + triggered + personalized

### 8. Accesibilidad WCAG 2.2 AA (Stage 4)
- **Keyboard Navigation**: Tab order + focus management
- **Screen Reader**: ARIA + semantic HTML + announcements
- **Visual**: High contrast + scalable fonts + color-blind friendly
- **Motor**: Large targets + sticky focus + voice control
- **Cognitive**: Clear navigation + consistent patterns + help text
- **Automated Testing**: axe-core + lighthouse + manual validation

### 9. Testing Completo (Stage 4)
- **Unit Tests**: ≥90% critical modules, ≥80% global
- **Integration Tests**: API + Database + External services
- **E2E Tests**: Playwright + cross-browser + mobile
- **Performance Tests**: Load + stress + memory leaks
- **Visual Tests**: Regression + responsive + accessibility
- **Security Tests**: OWASP + dependency scanning

### 10. CI/CD Pipeline (Stage 4)
- **GitHub Actions**: Multi-stage + parallel execution
- **Quality Gates**: Coverage + security + performance
- **Docker**: Multi-stage builds + vulnerability scanning
- **Environments**: Development + Staging + Production
- **Feature Flags**: Gradual rollout + A/B testing
- **Monitoring**: Health checks + alerts + rollback

</llm:section>

## =====
<llm:section id="unified_endpoints" type="api_reference">
## API Endpoints Consolidados

### Autenticación (Stage 1)
```
POST /api/v1/auth/login                # JWT login
POST /api/v1/auth/refresh              # Token refresh
POST /api/v1/auth/logout               # Logout
GET  /api/v1/auth/profile              # User profile
```

### OAuth (Stage 1)
```
GET  /api/v1/oauth/google/url          # OAuth URL
GET  /api/v1/oauth/google/callback     # OAuth callback
POST /api/v1/oauth/google/revoke       # Revoke tokens
GET  /api/v1/oauth/status              # OAuth status
```

### Health Checks (Stage 1-4)
```
GET /api/v1/health                     # Basic health
GET /api/v1/health/system              # System health
GET /api/v1/health/dependencies        # Dependencies health
GET /api/v1/health/google              # Google integration health
GET /api/v1/health/websocket           # WebSocket health
GET /api/v1/health/notifications       # Notifications health
GET /api/v1/health/accessibility       # Accessibility tools health
GET /api/v1/health/testing             # Testing tools health
```

### Google Classroom (Stage 2)
```
GET  /api/v1/google/status             # Connection status
GET  /api/v1/google/courses            # List courses
GET  /api/v1/google/courses/:id        # Course details
GET  /api/v1/google/courses/:id/students # Course students
POST /api/v1/google/sync/courses       # Sync courses
```

### Dashboards (Stage 2)
```
GET /api/v1/dashboard/admin            # Admin dashboard
GET /api/v1/dashboard/coordinator      # Coordinator dashboard
GET /api/v1/dashboard/teacher          # Teacher dashboard
GET /api/v1/dashboard/student          # Student dashboard
```

### Métricas (Stage 2-3)
```
GET /api/v1/metrics/overview           # General metrics
GET /api/v1/metrics/courses/:id        # Course metrics
GET /api/v1/metrics/students/:id       # Student metrics
GET /api/v1/insights/metrics           # Advanced metrics
GET /api/v1/insights/trends            # Trends analysis
GET /api/v1/insights/predictions       # Basic predictions
```

### Búsqueda (Stage 3)
```
GET  /api/v1/search/:entity            # Search by entity
GET  /api/v1/entity/:type/:id          # Entity details
GET  /api/v1/search/filters            # Available filters
POST /api/v1/search/save               # Save search
```

### Notificaciones (Stage 3)
```
GET  /api/v1/notifications             # Get notifications
PUT  /api/v1/notifications/:id/read    # Mark as read
GET  /api/v1/notifications/preferences # Get preferences
PUT  /api/v1/notifications/preferences # Update preferences
WS   /api/v1/ws/notifications          # WebSocket notifications
```

### Google Sync Avanzado (Stage 4)
```
GET  /api/v1/google/students           # Advanced student management
POST /api/v1/google/students/import    # Import students
PUT  /api/v1/google/students/:id/sync  # Sync student
DELETE /api/v1/google/students/:id     # Delete student
GET  /api/v1/google/assignments        # Advanced assignment management
POST /api/v1/google/assignments/create # Create assignment
PUT  /api/v1/google/assignments/:id    # Update assignment
DELETE /api/v1/google/assignments/:id  # Delete assignment
```

### Sincronización y Backup (Stage 4)
```
GET  /api/v1/sync/status               # Sync status
POST /api/v1/sync/start                # Start sync
POST /api/v1/sync/stop                 # Stop sync
GET  /api/v1/sync/logs                 # Sync logs
GET  /api/v1/sync/conflicts            # List conflicts
POST /api/v1/sync/conflicts/:id/resolve # Resolve conflict
GET  /api/v1/backup                    # List backups
POST /api/v1/backup/create             # Create backup
POST /api/v1/backup/:id/restore        # Restore backup
```

### Webhooks (Stage 4)
```
POST /api/v1/webhooks/google/course    # Course webhook
POST /api/v1/webhooks/google/student   # Student webhook
POST /api/v1/webhooks/google/assignment # Assignment webhook
GET  /api/v1/webhooks/status           # Webhooks status
```

### Diagnóstico (Stage 4)
```
GET /api/v1/diagnostics/google         # Google connection diagnostics
GET /api/v1/diagnostics/permissions    # Permissions diagnostics
GET /api/v1/monitoring/api-usage       # API usage monitoring
GET /api/v1/monitoring/performance     # Performance metrics
```

</llm:section>

## =====
<llm:section id="unified_data_models" type="data_models">
## Modelos de Datos Consolidados

### Usuario (Stage 1)
```json
{
  "id": "user-001",
  "email": "user@educational.dashboard",
  "role": "admin|coordinator|teacher|student",
  "name": "Full Name",
  "active": true,
  "lastLogin": "2025-10-03T10:00:00Z",
  "preferences": {
    "language": "en",
    "timezone": "UTC",
    "notifications": {
      "email": true,
      "push": true,
      "digest": "daily"
    },
    "accessibility": {
      "highContrast": false,
      "fontSize": "medium",
      "screenReader": false
    }
  },
  "oauth": {
    "google": {
      "connected": true,
      "scopes": ["classroom.courses", "classroom.rosters"],
      "lastSync": "2025-10-03T09:00:00Z"
    }
  }
}
```

### Curso Completo (Stage 2 + 4)
```json
{
  "id": "course-001",
  "googleId": "123456789",
  "name": "eCommerce Specialist",
  "section": "Section A",
  "description": "Complete eCommerce course",
  "ownerId": "teacher-001",
  "status": "active|inactive|archived",
  "enrollmentCode": "abc123",
  "students": ["student-001", "student-002"],
  "metrics": {
    "totalStudents": 150,
    "activeStudents": 142,
    "completionRate": 78.5,
    "averageGrade": 8.2,
    "engagementScore": 85.3
  },
  "syncStatus": {
    "lastSync": "2025-10-03T09:00:00Z",
    "status": "synced|pending|error",
    "conflicts": []
  },
  "createdAt": "2025-08-15T10:00:00Z",
  "updatedAt": "2025-10-03T09:00:00Z"
}
```

### Métrica Avanzada (Stage 3)
```json
{
  "id": "metric-001",
  "type": "engagement|risk|performance",
  "entityType": "student|course|program",
  "entityId": "student-001",
  "value": 85.3,
  "formula": {
    "type": "weighted_average",
    "components": [
      {"name": "participation", "weight": 0.4, "value": 90},
      {"name": "submission", "weight": 0.3, "value": 85},
      {"name": "resource_access", "weight": 0.3, "value": 80}
    ]
  },
  "thresholds": {
    "excellent": 90,
    "good": 70,
    "warning": 50,
    "critical": 30
  },
  "trends": {
    "direction": "improving|declining|stable",
    "change": 5.2,
    "period": "weekly"
  },
  "calculatedAt": "2025-10-03T10:00:00Z",
  "validUntil": "2025-10-03T16:00:00Z"
}
```

### Notificación (Stage 3)
```json
{
  "id": "notif-001",
  "userId": "teacher-001",
  "type": "alert|info|warning|success",
  "priority": "high|medium|low",
  "channel": "websocket|email|push",
  "title": "Student at Risk",
  "message": "John Smith needs attention",
  "data": {
    "studentId": "student-001",
    "courseId": "course-001",
    "riskScore": 0.75,
    "recommendation": "Contact student within 24 hours"
  },
  "actions": [
    {
      "label": "View Student",
      "type": "navigate",
      "url": "/students/student-001"
    },
    {
      "label": "Send Message",
      "type": "action",
      "action": "sendMessage"
    }
  ],
  "read": false,
  "delivered": true,
  "createdAt": "2025-10-03T10:00:00Z",
  "expiresAt": "2025-10-10T10:00:00Z"
}
```

### Estado de Sincronización (Stage 4)
```json
{
  "id": "sync-001",
  "status": "idle|running|completed|error",
  "type": "manual|scheduled|webhook",
  "startedAt": "2025-10-03T09:00:00Z",
  "completedAt": "2025-10-03T09:15:00Z",
  "progress": {
    "total": 150,
    "processed": 150,
    "succeeded": 145,
    "failed": 5,
    "percentComplete": 100
  },
  "entities": {
    "courses": {"total": 10, "synced": 10, "failed": 0},
    "students": {"total": 120, "synced": 118, "failed": 2},
    "assignments": {"total": 20, "synced": 17, "failed": 3}
  },
  "conflicts": [
    {
      "entityType": "assignment",
      "entityId": "assignment-123",
      "field": "dueDate",
      "sourceValue": "2025-10-15T23:59:59Z",
      "targetValue": "2025-10-20T23:59:59Z",
      "status": "pending|resolved"
    }
  ],
  "errors": [
    {
      "entity": "student",
      "id": "student-045",
      "error": "API_RATE_LIMIT_EXCEEDED",
      "message": "Rate limit exceeded, retrying in 60 seconds",
      "timestamp": "2025-10-03T09:10:00Z"
    }
  ]
}
```

</llm:section>

## =====
<llm:section id="unified_testing" type="testing_strategy">
## Estrategia de Testing Unificada

### Metodología TDD Consolidada
El sistema completo sigue Test-Driven Development (TDD) estricto:

1. **Red**: Escribir test que falle
2. **Green**: Implementar código mínimo para pasar
3. **Refactor**: Mejorar código manteniendo tests verdes
4. **Repeat**: Para cada nueva funcionalidad

### Cobertura de Testing Requerida
- **Global**: ≥80% líneas, ≥65% ramas
- **Módulos Críticos**: ≥90% líneas, ≥80% ramas
- **Componentes de Seguridad**: ≥95% líneas, ≥85% ramas
- **API Endpoints**: 100% casos de éxito y error

### Backend Tests Completos
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

### Frontend Tests Completos
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

### Fixtures y Mocks Consolidados
```python
# tests/conftest.py - Backend fixtures centralizados
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
// src/test/setup.ts - Frontend mocks centralizados
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

</llm:section>

## =====
<llm:section id="unified_error_prevention" type="error_prevention">
## Prevención de Errores Comunes en TDD

### Errores Identificados en Ejecuciones Anteriores

#### 1. Errores de Testing Async
**Problema**: Tests de métodos async fallan por mocks incorrectos
```python
# ❌ INCORRECTO
mock_instance = Mock()
mock_instance.admin.command.return_value = {"ok": 1}

# ✅ CORRECTO  
mock_instance = AsyncMock()
mock_instance.admin.command.return_value = {"ok": 1}
```

**Prevención**:
- Usar `AsyncMock` para todos los métodos async
- Template estándar para tests de base de datos
- Verificación automática de tipos async en CI

#### 2. Errores de Headers HTTP
**Problema**: Tests de CORS fallan por headers específicos no presentes
```python
# ❌ INCORRECTO - Headers específicos pueden variar
assert "access-control-allow-methods" in response.headers

# ✅ CORRECTO - Headers básicos verificables
assert "access-control-allow-origin" in response.headers
assert "access-control-allow-credentials" in response.headers
```

**Prevención**:
- Tests de CORS simplificados y robustos
- Verificación de headers esenciales solamente
- Documentación de comportamiento esperado de middleware

#### 3. Warnings de Deprecación
**Problema**: Warnings de Pydantic v2 y FastAPI por APIs deprecadas
```python
# ⚠️ WARNING - No crítico pero identificado
DeprecationWarning: on_event is deprecated, use lifespan event handlers
PydanticDeprecatedSince20: Support for class-based config is deprecated
```

**Solución Implementada**:
```python
# ✅ PYDANTIC V2 - ConfigDict moderno
from pydantic import ConfigDict

class Settings(BaseSettings):
    # ... campos ...
    
    model_config = ConfigDict(
        env_file=".env",
        case_sensitive=False
    )

# ✅ FASTAPI - Lifespan context manager
from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    try:
        await database.connect_to_mongodb()
        database.connect_to_redis()
    except Exception as e:
        print(f"Warning: Could not connect to databases: {e}")
    
    yield
    
    # Shutdown
    await database.close_mongodb_connection()
    database.close_redis_connection()

def create_app() -> FastAPI:
    return FastAPI(
        title=settings.app_name,
        version=settings.app_version,
        lifespan=lifespan  # Usar lifespan en lugar de on_event
    )
```

**Prevención**:
- Checklist de versiones compatibles en cada fase
- Migración gradual de APIs deprecadas
- Warnings como no-blocking en CI
- Templates modernos para Pydantic v2 y FastAPI

#### 4. Problemas de Servidor
**Problema**: Uvicorn no inicia correctamente en ciertos entornos
```bash
# ❌ PROBLEMA
curl: (7) Failed to connect to localhost port 8000

# ✅ SOLUCIÓN
python3 -m uvicorn src.app.main:app --host 127.0.0.1 --port 8000
```

**Prevención**:
- Scripts de verificación automática de servidor
- Configuración estándar de host/puerto
- Health checks automáticos en startup

### Protocolo de Prevención de Errores por Fase

#### Fase 1 - Fundaciones
**Verificaciones Automáticas**:
- [ ] Tests async usan `AsyncMock` correctamente
- [ ] Tests de CORS verifican headers básicos
- [ ] Servidor inicia en puerto configurado
- [ ] Health check responde correctamente
- [ ] Cobertura > 80% sin warnings críticos

**Templates Estándar**:
```python
# Template para tests async
@pytest.mark.asyncio
async def test_async_method():
    with patch('module.AsyncClass') as mock_class:
        mock_instance = AsyncMock()
        mock_class.return_value = mock_instance
        # Test implementation

# Template para configuración Pydantic v2
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

# Template para FastAPI con lifespan
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

#### Fase 2 - Google Integration
**Verificaciones Automáticas**:
- [ ] Mocks de Google API funcionan correctamente
- [ ] Modo dual switching sin errores
- [ ] Rate limiting implementado
- [ ] Fallback a Mock funciona

#### Fase 3 - Visualización Avanzada
**Verificaciones Automáticas**:
- [ ] WebSocket connections estables
- [ ] Gráficos renderizan sin errores
- [ ] Búsqueda funciona en tiempo real
- [ ] Notificaciones se entregan correctamente

#### Fase 4 - Production Ready
**Verificaciones Automáticas**:
- [ ] CI/CD pipeline sin errores
- [ ] Docker builds exitosos
- [ ] Security scans pasan
- [ ] Performance tests cumplen SLA

### Checklist de Prevención por Día

#### Día 1 - Estructura y Configuración
- [ ] **Setup**: Estructura de directorios creada
- [ ] **Dependencies**: Todas las dependencias instaladas
- [ ] **Config**: Variables de entorno configuradas
- [ ] **Tests**: Tests básicos pasando (34 tests)
- [ ] **Coverage**: 100% cobertura en módulos críticos (config, database, main)
- [ ] **Context Managers**: Tests completos para lifespan
- [ ] **Error Paths**: Tests para todos los try/except
- [ ] **Server**: Health check endpoint funcional
- [ ] **Async**: Tests async usan AsyncMock
- [ ] **CORS**: Tests de CORS simplificados
- [ ] **Warnings**: 0 warnings de deprecación (Pydantic v2 + FastAPI)
- [ ] **Modern APIs**: ConfigDict + lifespan implementados

#### Día 2 - Modelos y Excepciones
- [ ] **Models**: Pydantic v2 con ConfigDict
- [ ] **Validation**: Validadores funcionan correctamente
- [ ] **Exceptions**: Jerarquía de excepciones completa
- [ ] **Tests**: Tests de modelos pasando
- [ ] **Coverage**: 100% cobertura en modelos y excepciones
- [ ] **Edge Cases**: Tests para valores límite
- [ ] **Serialization**: Tests para model_dump() y model_validate()
- [ ] **Migration**: Sin warnings de Pydantic v1

#### Días 3-12 - Fundaciones Completas
- [ ] **Auth**: JWT + OAuth funcionando
- [ ] **Frontend**: Next.js + Auth + Layout
- [ ] **Integration**: Frontend-Backend comunicación
- [ ] **E2E**: Tests end-to-end básicos
- [ ] **CI**: Pipeline básico funcionando

### Quality Gates Mejorados

#### Gate 1: Fundaciones (Día 12)
- [ ] **Cobertura**: ≥100% módulos críticos (config, database, main)
- [ ] **Performance**: <3s load time
- [ ] **Security**: 0 vulnerabilidades CRITICAL
- [ ] **Tests**: Backend + Frontend + E2E básicos
- [ ] **Integration**: Frontend-Backend comunicación
- [ ] **CI/CD**: Pipeline básico funcionando
- [ ] **Error Prevention**: Todos los checks de prevención pasando
- [ ] **Context Managers**: Tests completos para lifespan
- [ ] **Async Tests**: AsyncMock usado correctamente
- [ ] **Error Paths**: Todos los try/except cubiertos
- [ ] **CORS Tests**: Headers básicos verificados
- [ ] **Server Health**: Health check funcional
- [ ] **Warnings**: 0 warnings de deprecación críticos
- [ ] **Modern APIs**: Pydantic v2 + FastAPI lifespan implementados

#### Gate 2: Google Integration (Día 22)
- [ ] **Cobertura**: ≥100% servicios críticos (auth, google, models)
- [ ] **Performance**: <2s dashboard load
- [ ] **Security**: 0 vulnerabilidades CRITICAL
- [ ] **Tests**: Google mocks + Integration tests
- [ ] **Google**: OAuth + Classroom API estable
- [ ] **Modo Dual**: Switching Google/Mock funcional
- [ ] **Error Prevention**: Rate limiting + fallback funcionando
- [ ] **API Integration**: Tests para todos los endpoints
- [ ] **Error Recovery**: Tests para fallos de conexión
- [ ] **Data Validation**: Tests para datos de Google
- [ ] **API Mocks**: Google API mocks estables

#### Gate 3: Visualización Avanzada (Día 32)
- [ ] **Cobertura**: ≥100% componentes de visualización
- [ ] **Performance**: <1.5s load time
- [ ] **Security**: 0 vulnerabilidades CRITICAL
- [ ] **Tests**: E2E + Performance + Visual
- [ ] **Accessibility**: Keyboard + Screen reader básico
- [ ] **Visualization**: D3.js + ApexCharts avanzado
- [ ] **WebSocket**: Tests para conexiones real-time
- [ ] **Charts**: Tests para renderizado de gráficos
- [ ] **Interactions**: Tests para interacciones de usuario
- [ ] **Error Prevention**: WebSocket + gráficos estables
- [ ] **Real-time**: Notificaciones funcionando

#### Gate 4: Production Ready (Día 45)
- [ ] **Cobertura**: ≥100% global
- [ ] **Performance**: <1s load time
- [ ] **Security**: 0 vulnerabilidades CRITICAL/HIGH
- [ ] **Tests**: Exhaustivos + Security + Load
- [ ] **E2E**: Tests end-to-end completos
- [ ] **Performance**: Tests de carga
- [ ] **Security**: Tests de seguridad exhaustivos
- [ ] **Accessibility**: WCAG 2.2 AA completo
- [ ] **Production**: CI/CD + Docker + Monitoring
- [ ] **Error Prevention**: Todos los sistemas estables
- [ ] **Monitoring**: Alertas automáticas funcionando

### Protocolo de Resolución de Errores

#### 1. Identificación Automática
- CI/CD detecta errores automáticamente
- Logs estructurados para debugging
- Alertas inmediatas para errores críticos

#### 2. Clasificación de Errores
- **CRITICAL**: Bloquean funcionalidad principal
- **HIGH**: Afectan funcionalidad importante
- **MEDIUM**: Afectan funcionalidad secundaria
- **LOW**: Warnings o mejoras menores

#### 3. Resolución Priorizada
- **CRITICAL**: Resolución inmediata (< 1 hora)
- **HIGH**: Resolución en mismo día (< 8 horas)
- **MEDIUM**: Resolución en 2-3 días
- **LOW**: Resolución en próxima iteración

#### 4. Prevención Futura
- Documentar causa raíz del error
- Actualizar templates y checklists
- Mejorar tests para detectar error
- Capacitar equipo en prevención

### Protocolo de Migración de APIs Deprecadas

#### 1. Identificación de Warnings
```bash
# Verificar warnings en tests
pytest tests/ -W error::DeprecationWarning

# Verificar warnings en aplicación
python -W error::DeprecationWarning -c "from src.app.main import app"
```

#### 2. Migración Pydantic v2
**Antes (Deprecado)**:
```python
class Settings(BaseSettings):
    field: str = "value"
    
    class Config:
        env_file = ".env"
        case_sensitive = False
```

**Después (Moderno)**:
```python
from pydantic import ConfigDict

class Settings(BaseSettings):
    field: str = "value"
    
    model_config = ConfigDict(
        env_file=".env",
        case_sensitive=False
    )
```

#### 3. Migración FastAPI Lifespan
**Antes (Deprecado)**:
```python
@app.on_event("startup")
async def startup():
    pass

@app.on_event("shutdown")
async def shutdown():
    pass
```

**Después (Moderno)**:
```python
from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    try:
        # Initialize
        pass
    except Exception as e:
        print(f"Warning: {e}")
    
    yield
    
    # Shutdown
    try:
        # Cleanup
        pass
    except Exception as e:
        print(f"Warning: {e}")

app = FastAPI(lifespan=lifespan)
```

#### 4. Verificación Post-Migración
- [ ] Tests pasan sin warnings
- [ ] Aplicación inicia sin warnings
- [ ] Funcionalidad preservada
- [ ] Performance mantenida
- [ ] Documentación actualizada

### Protocolo de Cobertura 100%

#### 1. Identificación de Líneas Sin Cubrir
```bash
# Comando para identificar líneas específicas sin cubrir
pytest tests/ --cov=src --cov-report=term-missing --cov-report=html

# Verificar cobertura por archivo
pytest tests/unit/ --cov=src --cov-report=term-missing

# Generar reporte HTML detallado
pytest tests/ --cov=src --cov-report=html
open htmlcov/index.html
```

#### 2. Análisis de Código Complejo
**Archivos que requieren atención especial:**
- **Context Managers**: `lifespan`, `async with`, `try/except`
- **Async Functions**: Métodos con `async/await`
- **Error Handling**: Bloques `try/except/finally`
- **Conditional Logic**: `if/elif/else` complejos
- **Loop Constructs**: `for/while` con break/continue

#### 3. Técnicas de Testing para 100%
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
async def test_async_function():
    """Test función async con AsyncMock"""
    with patch('module.async_service') as mock_service:
        mock_service.async_method = AsyncMock(return_value="result")
        result = await async_function()
        assert result == "result"
        mock_service.async_method.assert_called_once()
```

**Para Error Handling:**
```python
def test_error_handling_success():
    """Test manejo de error exitoso"""
    with patch('module.risky_function') as mock_func:
        mock_func.side_effect = Exception("Test error")
        result = function_with_error_handling()
        assert result == "error_handled"

def test_error_handling_failure():
    """Test manejo de error fallido"""
    with patch('module.risky_function') as mock_func:
        mock_func.return_value = "success"
        result = function_with_error_handling()
        assert result == "success"
```

#### 4. Checklist de Cobertura por Día
**Día 1-3: Fundaciones**
- [ ] **Configuración**: 100% cobertura en `config.py`
- [ ] **Base de datos**: 100% cobertura en `database.py`
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
- [ ] **Error Cases**: Tests para tokens inválidos/expirados

#### 5. Templates Estándar para 100% Cobertura
**Template para Context Manager:**
```python
@pytest.mark.asyncio
async def test_{context_manager_name}_success():
    """Test {context_manager_name} caso exitoso"""
    with patch('{module_path}') as mock_dependency:
        mock_dependency.method = AsyncMock()
        async with {context_manager_name}():
            # Verificar startup
            mock_dependency.method.assert_called_once()
        # Verificar shutdown
        mock_dependency.cleanup.assert_called_once()

@pytest.mark.asyncio
async def test_{context_manager_name}_startup_error():
    """Test {context_manager_name} error en startup"""
    with patch('{module_path}') as mock_dependency:
        mock_dependency.method = AsyncMock(side_effect=Exception("Startup failed"))
        async with {context_manager_name}():
            # Verificar manejo de error
            mock_dependency.method.assert_called_once()

@pytest.mark.asyncio
async def test_{context_manager_name}_shutdown_error():
    """Test {context_manager_name} error en shutdown"""
    with patch('{module_path}') as mock_dependency:
        mock_dependency.method = AsyncMock()
        mock_dependency.cleanup = AsyncMock(side_effect=Exception("Shutdown failed"))
        async with {context_manager_name}():
            pass  # Trigger shutdown
        # Verificar manejo de error
        mock_dependency.cleanup.assert_called_once()
```

**Template para Async Function:**
```python
@pytest.mark.asyncio
async def test_{async_function_name}_success():
    """Test {async_function_name} caso exitoso"""
    with patch('{module_path}') as mock_service:
        mock_service.async_method = AsyncMock(return_value="expected_result")
        result = await {async_function_name}()
        assert result == "expected_result"
        mock_service.async_method.assert_called_once()

@pytest.mark.asyncio
async def test_{async_function_name}_error():
    """Test {async_function_name} caso de error"""
    with patch('{module_path}') as mock_service:
        mock_service.async_method = AsyncMock(side_effect=Exception("Service error"))
        with pytest.raises(Exception, match="Service error"):
            await {async_function_name}()
        mock_service.async_method.assert_called_once()
```

#### 6. Comandos de Verificación Específicos
```bash
# Verificar cobertura específica por archivo
pytest tests/unit/test_main.py --cov=src/app/main --cov-report=term-missing

# Verificar cobertura de context managers
pytest tests/unit/test_lifespan.py --cov=src/app/main --cov-report=term-missing

# Verificar cobertura de async functions
pytest tests/unit/test_database.py --cov=src/app/core/database --cov-report=term-missing

# Verificar cobertura de modelos
pytest tests/unit/test_models.py --cov=src/app/models --cov-report=term-missing

# Verificar cobertura de autenticación
pytest tests/unit/test_auth.py --cov=src/app/api/auth --cov-report=term-missing
```

#### 7. Métricas de Cobertura por Módulo
**Backend - Módulos Críticos (100% requerido):**
- `src/app/core/config.py` - Configuración
- `src/app/core/database.py` - Base de datos
- `src/app/main.py` - Aplicación principal
- `src/app/core/security.py` - Seguridad
- `src/app/models/user.py` - Modelos de usuario
- `src/app/api/auth.py` - Autenticación

**Frontend - Componentes Críticos (100% requerido):**
- `src/components/Auth/` - Componentes de autenticación
- `src/hooks/useAuth.ts` - Hook de autenticación
- `src/services/api.ts` - Servicios de API
- `src/utils/auth.ts` - Utilidades de autenticación

#### 8. Verificación Automática de Cobertura
```bash
# Script para verificar cobertura 100% en CI/CD
#!/bin/bash
echo "Verificando cobertura 100%..."

# Verificar módulos críticos
CRITICAL_MODULES=(
    "src/app/core/config"
    "src/app/core/database" 
    "src/app/main"
    "src/app/core/security"
)

for module in "${CRITICAL_MODULES[@]}"; do
    echo "Verificando $module..."
    coverage=$(pytest tests/ --cov=$module --cov-report=term-missing | grep "TOTAL" | awk '{print $4}' | sed 's/%//')
    if [ "$coverage" != "100" ]; then
        echo "❌ $module: $coverage% (requerido: 100%)"
        exit 1
    else
        echo "✅ $module: $coverage%"
    fi
done

echo "🎉 Todos los módulos críticos tienen 100% de cobertura"
```

</llm:section>

## =====
<llm:section id="unified_deployment" type="configuration">
## Configuración de Deployment Unificada

### Variables de Entorno Consolidadas

#### Backend (.env)
```env
# Ambiente
ENVIRONMENT=production
PORT=8000

# Database
MONGODB_URL=mongodb://mongo:27017/dashboard_educativo
REDIS_URL=redis://redis:6379/0

# JWT & OAuth
JWT_SECRET=production-secret-change-this
JWT_EXPIRES_IN=1h
OAUTH_PKCE_ENABLED=true
OAUTH_REFRESH_TOKEN_ROTATION_ENABLED=true
OAUTH_ENFORCE_HTTPS=true

# Google Integration
GOOGLE_API_KEY=your-google-api-key
GOOGLE_CLIENT_ID=your-google-client-id
GOOGLE_CLIENT_SECRET=your-google-client-secret
GOOGLE_API_SCOPES=https://www.googleapis.com/auth/classroom.courses,https://www.googleapis.com/auth/classroom.rosters
DEFAULT_MODE=MOCK

# Sync & Backup
SYNC_SCHEDULE="0 3 * * *"
BACKUP_SCHEDULE="0 1 * * *"
BACKUP_RETENTION_DAYS=30

# Notifications
WEBSOCKET_PORT=8001
EMAIL_MOCK=true
TELEGRAM_MOCK=true
NOTIFICATION_RETENTION_DAYS=30

# Testing & Quality
TEST_COVERAGE_THRESHOLD_CRITICAL=90
TEST_COVERAGE_THRESHOLD_GLOBAL=80

# Security
ERROR_SANITIZE_SENSITIVE_DATA=true
ERROR_FRIENDLY_MESSAGES=true
CORS_ORIGINS=https://your-domain.com
```

#### Frontend (.env.local)
```env
# API Configuration
NEXT_PUBLIC_API_URL=https://api.your-domain.com/api/v1
NEXT_PUBLIC_WS_URL=wss://api.your-domain.com/api/v1/ws

# Google
NEXT_PUBLIC_GOOGLE_CLIENT_ID=your-google-client-id
NEXT_PUBLIC_DEFAULT_MODE=MOCK

# Features
NEXT_PUBLIC_FEATURE_FLAGS_ENDPOINT=/api/v1/features
NEXT_PUBLIC_ACCESSIBILITY_FEATURES=true
NEXT_PUBLIC_HIGH_CONTRAST=true

# Performance
NEXT_PUBLIC_SEARCH_DEBOUNCE_MS=300
NEXT_PUBLIC_NOTIFICATION_POLL_INTERVAL=30000
```

### Docker Configuration Completa

#### Backend Dockerfile
```dockerfile
# Multi-stage build para optimizar tamaño
FROM python:3.11.6-slim AS builder

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir --user -r requirements.txt

FROM python:3.11.6-slim AS production

# Usuario no-root para seguridad
RUN useradd -m -u 1000 appuser

WORKDIR /app
COPY --from=builder /root/.local /home/appuser/.local
COPY . .

# Cambiar ownership y cambiar a usuario no-root
RUN chown -R appuser:appuser /app
USER appuser

# Healthcheck
HEALTHCHECK --interval=30s --timeout=10s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8000/health')"

EXPOSE 8000
CMD ["python", "-m", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

#### Frontend Dockerfile
```dockerfile
# Multi-stage build
FROM node:18.17.1-alpine AS builder

WORKDIR /app
COPY package*.json ./
COPY pnpm-lock.yaml ./

# Instalar pnpm y dependencias
RUN npm install -g pnpm@8
RUN pnpm install --frozen-lockfile

COPY . .
RUN pnpm run build

FROM node:18.17.1-alpine AS production

# Usuario no-root
RUN adduser -D -s /bin/sh -u 1000 appuser

WORKDIR /app
COPY --from=builder --chown=appuser:appuser /app/.next ./.next
COPY --from=builder --chown=appuser:appuser /app/public ./public
COPY --from=builder --chown=appuser:appuser /app/package.json ./package.json
COPY --from=builder --chown=appuser:appuser /app/node_modules ./node_modules

USER appuser

EXPOSE 3000
CMD ["npm", "start"]
```

#### docker-compose.yml
```yaml
version: '3.8'

services:
  backend:
    build: ./backend
    ports:
      - "8000:8000"
    environment:
      - MONGODB_URL=mongodb://mongo:27017/dashboard_educativo
      - REDIS_URL=redis://redis:6379/0
    depends_on:
      mongo:
        condition: service_healthy
      redis:
        condition: service_healthy
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8000/health"]
      interval: 30s
      timeout: 10s
      retries: 3
    deploy:
      resources:
        limits:
          cpus: '2.0'
          memory: 2G
        reservations:
          cpus: '1.0'
          memory: 1G

  frontend:
    build: ./frontend
    ports:
      - "3000:3000"
    environment:
      - NEXT_PUBLIC_API_URL=http://backend:8000/api/v1
    depends_on:
      backend:
        condition: service_healthy
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:3000"]
      interval: 30s
      timeout: 10s
      retries: 3

  mongo:
    image: mongo:6.0.13
    environment:
      MONGO_INITDB_ROOT_USERNAME: root
      MONGO_INITDB_ROOT_PASSWORD_FILE: /run/secrets/db_password
    volumes:
      - mongo_data:/data/db
    secrets:
      - db_password
    healthcheck:
      test: ["CMD", "mongosh", "--eval", "db.adminCommand('ping')"]
      interval: 30s
      timeout: 10s
      retries: 3

  redis:
    image: redis:7.2.3-alpine
    volumes:
      - redis_data:/data
    healthcheck:
      test: ["CMD", "redis-cli", "ping"]
      interval: 30s
      timeout: 10s
      retries: 3

volumes:
  mongo_data:
  redis_data:

secrets:
  db_password:
    external: true
```

### CI/CD Pipeline Unificado

#### .github/workflows/deploy.yml
```yaml
name: Unified Deploy Pipeline

on:
  push:
    branches: [main, staging, develop]
  pull_request:
    branches: [main]

jobs:
  # Stage 1: Tests paralelos
  test-backend:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Set up Python with pyenv
        uses: gabrielfalcao/pyenv-action@v14
        with:
          default: 3.11.4
      - name: Install dependencies
        run: |
          cd backend
          pip install -r requirements.txt
      - name: Run backend tests
        run: |
          cd backend
          pytest --cov=app --cov-report=xml --cov-fail-under=80

  test-frontend:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Setup Node.js
        uses: actions/setup-node@v3
        with:
          node-version: '18'
      - name: Setup PNPM
        uses: pnpm/action-setup@v2
        with:
          version: 8
      - name: Install dependencies
        run: |
          cd frontend
          pnpm install --frozen-lockfile
      - name: Run frontend tests
        run: |
          cd frontend
          pnpm test --coverage

  # Stage 2: E2E Tests
  test-e2e:
    needs: [test-backend, test-frontend]
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Setup Node.js
        uses: actions/setup-node@v3
        with:
          node-version: '18'
      - name: Setup PNPM
        uses: pnpm/action-setup@v2
        with:
          version: 8
      - name: Install Playwright
        run: |
          cd frontend
          pnpm install --frozen-lockfile
          npx playwright install
      - name: Start services
        run: |
          docker-compose up -d
          sleep 30
      - name: Run E2E tests
        run: |
          cd frontend
          npx playwright test
      - name: Stop services
        if: always()
        run: docker-compose down

  # Stage 3: Security Scan
  security-scan:
    needs: [test-backend, test-frontend]
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Build images
        run: |
          docker build -t backend:test ./backend
          docker build -t frontend:test ./frontend
      - name: Run Trivy scanner
        uses: aquasecurity/trivy-action@master
        with:
          image-ref: 'backend:test'
          format: 'sarif'
          output: 'trivy-results.sarif'
          severity: 'CRITICAL,HIGH'
          exit-code: '1'

  # Stage 4: Deploy
  deploy:
    needs: [test-e2e, security-scan]
    runs-on: ubuntu-latest
    if: github.ref == 'refs/heads/main'
    steps:
      - uses: actions/checkout@v3
      - name: Deploy to production
        run: |
          echo "Deploying to production..."
          # Add deployment commands here
```

</llm:section>

## =====
<llm:section id="unified_acceptance_criteria" type="acceptance_criteria">
## Criterios de Aceptación Unificados (DoD)

### Backend Completo ✅
- [ ] **Stage 1**: FastAPI + JWT + OAuth + MockService funcionando
- [ ] **Stage 2**: Google Classroom API + Modo Dual + Dashboard endpoints
- [ ] **Stage 3**: WebSocket + Notificaciones + Búsqueda avanzada + Métricas
- [ ] **Stage 4**: Sincronización bidireccional + Backup + Webhooks
- [ ] **Testing**: ≥90% críticos, ≥80% global + Integration + Performance
- [ ] **Security**: Validación estricta + Sanitización + Error handling
- [ ] **Health Checks**: Todos los servicios monitoreados
- [ ] **Auto-cleanup**: Procesos + datos corruptos + sesiones expiradas

### Frontend Completo ✅
- [ ] **Stage 1**: Next.js 13.5.6 + Auth + Layout + i18n funcionando
- [ ] **Stage 2**: Google UI + Dashboards por rol + ApexCharts v5.3.5
- [ ] **Stage 3**: Búsqueda + Notificaciones + Visualizaciones avanzadas
- [ ] **Stage 4**: Admin panel + Accesibilidad WCAG 2.2 AA + PWA
- [ ] **Testing**: Componentes + E2E + Visual + Accessibility
- [ ] **Performance**: Core Web Vitals + Mobile + Responsive
- [ ] **Accessibility**: Keyboard + Screen reader + High contrast
- [ ] **PWA**: Service worker + Offline + Push notifications

### Integración Google Completa ✅
- [ ] **Conexión**: OAuth 2.0 + PKCE + Scope limitado funcionando
- [ ] **Modo Dual**: Google (prod) + Mock (dev) independientes
- [ ] **Sincronización**: Bidireccional + Incremental + Programada
- [ ] **Gestión**: Courses + Students + Assignments + Grades completa
- [ ] **Conflictos**: Detección + Resolución automática + Manual
- [ ] **Webhooks**: Eventos tiempo real + Signature validation
- [ ] **Backup**: Automático + Selectivo + Point-in-time recovery
- [ ] **Monitoreo**: Usage + Performance + Error tracking

### Dashboards y Visualización ✅
- [ ] **Por Rol**: Admin + Coordinator + Teacher + Student personalizados
- [ ] **Métricas**: KPIs + Trends + Predictions + Comparatives
- [ ] **Gráficos**: ApexCharts v5.3.5 + Interactive + Responsive
- [ ] **Real-time**: WebSocket updates + Live data + Notifications
- [ ] **Export**: PDF + PNG + Data + Reports + Scheduled
- [ ] **Filters**: Advanced + Saved + Contextual + Shareable
- [ ] **Widgets**: Drag & drop + Configurable + Custom
- [ ] **Performance**: <2s load + Cached + Optimized queries

### Búsqueda y Notificaciones ✅
- [ ] **Búsqueda**: Multi-entity + Contextual + Real-time + Advanced filters
- [ ] **Resultados**: Highlighted + Paginated + Exportable + Saved
- [ ] **Notificaciones**: WebSocket + Multi-channel + Smart alerts
- [ ] **Preferencias**: Per user + Per type + Schedules + Quiet hours
- [ ] **Push**: Browser + PWA + Mobile + Digest options
- [ ] **Delivery**: Guaranteed + Retry + Fallback + Tracking

### Testing y Calidad ✅
- [ ] **Cobertura**: ≥90% críticos, ≥80% global medida y verificada
- [ ] **Unit Tests**: Todos los servicios + componentes + hooks
- [ ] **Integration**: API + Database + External services + Workflows
- [ ] **E2E**: Playwright + Cross-browser + Mobile + Scenarios
- [ ] **Performance**: Load + Stress + Memory + Benchmarks
- [ ] **Visual**: Regression + Responsive + Accessibility + Contrast
- [ ] **Security**: OWASP + Dependencies + Penetration + Audit
- [ ] **Manual**: Accessibility + Usability + User acceptance

### Accesibilidad WCAG 2.2 AA ✅
- [ ] **Keyboard**: Tab order + Focus management + Shortcuts
- [ ] **Screen Reader**: ARIA + Semantic + Announcements + Navigation
- [ ] **Visual**: Contrast AA/AAA + Scalable fonts + Color-blind friendly
- [ ] **Motor**: Large targets + Sticky focus + Voice control support
- [ ] **Cognitive**: Clear navigation + Consistent + Help + Error recovery
- [ ] **Testing**: Automated (axe-core) + Manual + User testing
- [ ] **Documentation**: Accessibility guide + User manual + Support

### CI/CD y Deployment ✅
- [ ] **Pipeline**: GitHub Actions + Multi-stage + Parallel execution
- [ ] **Quality Gates**: Coverage + Security + Performance + Accessibility
- [ ] **Docker**: Multi-stage + Security scan + Resource limits
- [ ] **Environments**: Dev + Staging + Prod + Feature branches
- [ ] **Monitoring**: Health checks + Alerts + Metrics + Logs
- [ ] **Rollback**: Automatic + Manual + Database + Infrastructure
- [ ] **Feature Flags**: Gradual rollout + A/B testing + Kill switches
- [ ] **Documentation**: Deployment guide + Runbooks + Recovery procedures

### Seguridad y Operaciones ✅
- [ ] **Authentication**: JWT + OAuth + Multi-factor + Session management
- [ ] **Authorization**: RBAC + Permissions + Audit + Compliance
- [ ] **Data Protection**: Encryption + Sanitization + Privacy + GDPR
- [ ] **Infrastructure**: HTTPS + Secrets + Firewall + Monitoring
- [ ] **Compliance**: Security audit + Penetration testing + Documentation
- [ ] **Incident Response**: Runbooks + Escalation + Recovery + Post-mortem
- [ ] **Backup**: Automated + Tested + Encrypted + Offsite
- [ ] **Monitoring**: 24/7 + Alerting + Dashboards + SLA tracking

</llm:section>

## =====
<llm:section id="unified_implementation_plan" type="implementation_plan">
## Plan de Implementación Unificado

### Metodología TDD Consolidada
Todo el sistema sigue **Test-Driven Development** estricto:

1. **Red**: Escribir test que falle definiendo comportamiento esperado
2. **Green**: Implementar código mínimo para hacer pasar el test
3. **Refactor**: Mejorar código manteniendo tests verdes
4. **Document**: Documentar decisiones basadas en tests
5. **Integrate**: Integrar con sistema existente
6. **Validate**: Validar cumplimiento de criterios de aceptación

### Orden de Implementación (40-45 días)

#### Fase 1: Fundaciones (10-12 días)
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

#### Fase 2: Google Integration (8-10 días)
**Días 13-15: Backend Google**
- Tests para Google Classroom API
- Implementación GoogleService + ClassroomService
- Modo dual (Google/Mock)
- Endpoints dashboard por rol

**Días 16-18: Frontend Google**
- Tests para componentes Google
- Selector de modo + Lista de cursos
- Dashboards por rol con ApexCharts v5.3.5
- Métricas básicas y visualización

**Días 19-21: Métricas y Dashboards**
- Tests para métricas avanzadas
- KPIs educativos + agregaciones
- Dashboards interactivos
- Cache y optimización

**Días 22-23: Integración Google**
- Tests de integración completa
- Validación modo dual
- Performance tuning
- Documentación Google

#### Fase 3: Visualización Avanzada (8-10 días)
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

#### Fase 4: Integración Completa (10-12 días)
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

### Criterios de Finalización por Fase

#### Fase 1 - Fundaciones ✅
- [ ] Backend: FastAPI + JWT + OAuth funcionando
- [ ] Frontend: Next.js + Auth + Layout responsivo
- [ ] Testing: ≥80% cobertura + CI básico
- [ ] Integration: Frontend-Backend comunicación
- [ ] Error Prevention: AsyncMock + CORS tests + Server health

#### Fase 2 - Google Integration ✅
- [ ] Backend: Google API + Modo dual + Dashboards
- [ ] Frontend: Google UI + ApexCharts + Dashboards rol
- [ ] Testing: Google mocks + Integration tests
- [ ] Error Prevention: Rate limiting + Fallback + API mocks
- [ ] Performance: <2s dashboard load

#### Fase 3 - Visualización Avanzada ✅
- [ ] Backend: Búsqueda + Notificaciones + WebSocket
- [ ] Frontend: UI avanzada + Gráficos interactivos
- [ ] Error Prevention: WebSocket + Gráficos + Real-time
- [ ] Testing: E2E scenarios + Performance
- [ ] Accessibility: Keyboard + Screen reader básico

#### Fase 4 - Production Ready ✅
- [ ] Google: Sync bidireccional + Backup + Webhooks
- [ ] Error Prevention: Todos los sistemas estables + Monitoring
- [ ] Accessibility: WCAG 2.2 AA completo
- [ ] Testing: ≥90% críticos + Security + Load
- [ ] CI/CD: Pipeline completo + Docker + Monitoring

### Validación Final del Sistema
- [ ] **Todos los DoD completados**: 100% criterios de aceptación
- [ ] **Testing exhaustivo**: Cobertura + E2E + Performance + Security
- [ ] **Accesibilidad validada**: WCAG 2.2 AA + User testing
- [ ] **Performance optimizado**: Core Web Vitals + Mobile
- [ ] **Security auditado**: OWASP + Penetration + Dependencies
- [ ] **Documentation completa**: User + Admin + Developer + API
- [ ] **Production deployment**: CI/CD + Monitoring + Backup
- [ ] **User acceptance**: Stakeholder approval + Training

</llm:section>

## =====
<llm:section id="unified_conclusion" type="conclusion">
## Conclusión del Contrato Unificado

### Resumen Ejecutivo
Este contrato unificado consolida las mejores prácticas y funcionalidades de los 4 stages originales en un sistema integral de dashboard educativo. El enfoque TDD garantiza alta calidad, mantenibilidad y robustez desde el primer día.

### Beneficios del Enfoque Unificado
1. **Coherencia Arquitectónica**: Diseño consistente en todo el sistema
2. **Optimización Global**: Performance y UX optimizados end-to-end
3. **Testing Integral**: Cobertura completa con enfoque TDD
4. **Accesibilidad Nativa**: WCAG 2.2 AA integrado desde el diseño
5. **Production Ready**: CI/CD + Security + Monitoring desde el inicio

### Tecnologías Validadas
- **Backend**: Python 3.11.4 + FastAPI + Pydantic v2 + Google Classroom API
- **Frontend**: Next.js 13.5.6 LTS + React 18.2.0 + React Query v4 + ApexCharts v5.3.5
- **DevOps**: Docker + GitHub Actions + Trivy + pnpm 8.x
- **Testing**: pytest + Vitest + Playwright + axe-core

### Métricas de Éxito
- **Cobertura Testing**: ≥90% módulos críticos, ≥80% global
- **Performance**: <2s dashboard load, Core Web Vitals optimizado
- **Accessibility**: WCAG 2.2 AA compliance validado
- **Security**: 0 vulnerabilidades CRITICAL, audit completo
- **Uptime**: 99.9% disponibilidad con monitoring 24/7

### Próximos Pasos
1. **Implementación**: Seguir plan de 40-45 días con TDD estricto
2. **Validación**: Criterios de aceptación por fase
3. **Deployment**: Production ready con CI/CD completo
4. **Operación**: Monitoring + Support + Continuous improvement

**Este contrato representa la implementación más robusta y completa del Dashboard Educativo, integrando todas las funcionalidades requeridas con las mejores prácticas de la industria.**

</llm:section>