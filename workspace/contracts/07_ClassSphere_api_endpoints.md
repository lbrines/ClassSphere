---
title: "ClassSphere - Consolidated API Endpoints"
version: "4.0"
type: "documentation"
language: "English (Mandatory)"
date: "2025-10-07"
related_files:
  - "00_ClassSphere_index.md"
  - "06_ClassSphere_funcionalidades.md"
  - "08_ClassSphere_modelos_datos.md"
---

[← Funcionalidades Consolidadas](06_ClassSphere_funcionalidades.md) | [Índice](00_ClassSphere_index.md) | [Siguiente → Modelos de Datos](08_ClassSphere_modelos_datos.md)

# API Endpoints Consolidados

## Autenticación (Stage 1)
```
POST /api/v1/auth/login                # JWT login
POST /api/v1/auth/refresh              # Token refresh
POST /api/v1/auth/logout               # Logout
GET  /api/v1/auth/profile              # User profile
```

## OAuth (Stage 1)
```
GET  /api/v1/oauth/google/url          # OAuth URL
GET  /api/v1/oauth/google/callback     # OAuth callback
POST /api/v1/oauth/google/revoke       # Revoke tokens
GET  /api/v1/oauth/status              # OAuth status
```

## Health Checks (Stage 1-4)
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

## Google Classroom (Stage 2)
```
GET  /api/v1/google/status             # Connection status
GET  /api/v1/google/courses            # List courses
GET  /api/v1/google/courses/:id        # Course details
GET  /api/v1/google/courses/:id/students # Course students
POST /api/v1/google/sync/courses       # Sync courses
```

## Dashboards (Stage 2)
```
GET /api/v1/dashboard/admin            # Admin dashboard
GET /api/v1/dashboard/coordinator      # Coordinator dashboard
GET /api/v1/dashboard/teacher          # Teacher dashboard
GET /api/v1/dashboard/student          # Student dashboard
```

## Métricas (Stage 2-3)
```
GET /api/v1/metrics/overview           # General metrics
GET /api/v1/metrics/courses/:id        # Course metrics
GET /api/v1/metrics/students/:id       # Student metrics
GET /api/v1/insights/metrics           # Advanced metrics
GET /api/v1/insights/trends            # Trends analysis
GET /api/v1/insights/predictions       # Basic predictions
```

## Búsqueda (Stage 3)
```
GET  /api/v1/search/:entity            # Search by entity
GET  /api/v1/entity/:type/:id          # Entity details
GET  /api/v1/search/filters            # Available filters
POST /api/v1/search/save               # Save search
```

## Notificaciones (Stage 3)
```
GET  /api/v1/notifications             # Get notifications
PUT  /api/v1/notifications/:id/read    # Mark as read
GET  /api/v1/notifications/preferences # Get preferences
PUT  /api/v1/notifications/preferences # Update preferences
WS   /api/v1/ws/notifications          # WebSocket notifications
```

## Google Sync Avanzado (Stage 4)
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

## Sincronización y Backup (Stage 4)
```
GET  /api/v1/sync/status               # Status (SYNC_IDLE|SYNC_RUNNING|SYNC_COMPLETE|SYNC_ERROR)
POST /api/v1/sync/start                # Start sync process
POST /api/v1/sync/stop                 # Stop sync process
GET  /api/v1/sync/logs                 # Sync logs
GET  /api/v1/sync/conflicts            # List conflicts (CONFLICT_PENDING|CONFLICT_RESOLVED)
POST /api/v1/sync/conflicts/:id/resolve # Resolve conflict
GET  /api/v1/backup                    # List backups
POST /api/v1/backup/create             # Create backup
POST /api/v1/backup/:id/restore        # Restore backup
```

## Webhooks (Stage 4)
```
POST /api/v1/webhooks/google/course    # Course webhook
POST /api/v1/webhooks/google/student   # Student webhook
POST /api/v1/webhooks/google/assignment # Assignment webhook
GET  /api/v1/webhooks/status           # Webhooks status
```

## Diagnóstico (Stage 4)
```
GET /api/v1/diagnostics/google         # Google connection diagnostics
GET /api/v1/diagnostics/permissions    # Permissions diagnostics
GET /api/v1/monitoring/api-usage       # API usage monitoring
GET /api/v1/monitoring/performance     # Performance metrics
```

## Detalles de Endpoints Principales

### Autenticación JWT

**POST /api/v1/auth/login**
```json
// Request
{
  "email": "user@example.com",
  "password": "securePassword123"
}

// Response
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer",
  "expires_in": 3600,
  "user": {
    "id": "user-001",
    "email": "user@example.com",
    "role": "Teacher",
    "name": "John Smith"
  }
}
```

### OAuth Google

**GET /api/v1/oauth/google/url**
```json
// Response
{
  "url": "https://accounts.google.com/o/oauth2/v2/auth?client_id=...",
  "state": "random-state-string",
  "code_verifier": "random-code-verifier",
  "expires_in": 600
}
```

### Google Classroom Courses

**GET /api/v1/google/courses**
```json
// Response
{
  "courses": [
    {
      "id": "course-001",
      "googleId": "123456789",
      "name": "eCommerce Specialist",
      "section": "Section A",
      "status": "COURSE_ACTIVE",
      "studentCount": 150
    },
    {
      "id": "course-002",
      "googleId": "987654321",
      "name": "Digital Marketing",
      "section": "Section B",
      "status": "COURSE_ACTIVE",
      "studentCount": 120
    }
  ],
  "pagination": {
    "total": 10,
    "page": 1,
    "pageSize": 10,
    "hasMore": false
  }
}
```

### Sincronización

**POST /api/v1/sync/start**
```json
// Request
{
  "entities": ["courses", "students", "assignments"],
  "options": {
    "forceUpdate": false,
    "conflictResolution": "auto"
  }
}

// Response
{
  "syncId": "sync-001",
  "status": "SYNC_RUNNING",
  "startedAt": "2025-10-04T10:00:00Z",
  "estimatedCompletion": "2025-10-04T10:15:00Z"
}
```

## Referencias a Otros Documentos

- Para detalles sobre las funcionalidades, consulte [Funcionalidades Consolidadas](06_ClassSphere_funcionalidades.md).
- Para detalles sobre los modelos de datos, consulte [Modelos de Datos](08_ClassSphere_modelos_datos.md).
- Para detalles sobre la estrategia de testing, consulte [Estrategia de Testing](09_ClassSphere_testing.md).

---

[← Funcionalidades Consolidadas](06_ClassSphere_funcionalidades.md) | [Índice](00_ClassSphere_index.md) | [Siguiente → Modelos de Datos](08_ClassSphere_modelos_datos.md)
