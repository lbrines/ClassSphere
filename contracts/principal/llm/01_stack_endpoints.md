---
title: "Stack Tecnológico + API Endpoints"
version: "1.0-LLM"
type: "technical-spec"
---

# Stack Tecnológico + Arquitectura + API Endpoints

## Stack Consolidado

### Backend (Go + Echo)
```go
// Dependencias principales
- Go 1.21+
- Echo v4 (framework web)
- JWT-go (autenticación)
- Google OAuth 2.0
- Redis (caché)
- testify/mock (testing)
- httptest (HTTP testing)
```

### Frontend (Angular 19)
```typescript
// Dependencias principales
- Angular 19 (framework)
- esbuild (bundler oficial)
- TypeScript 5.x
- RxJS (reactive programming)
- TailwindCSS 3.x
- Jasmine + Karma (testing)
- Playwright (E2E)
```

### DevOps
```yaml
- Docker (multi-stage)
- GitHub Actions (CI/CD)
- Trivy (security scanning)
- Redis (caché compartido)
```

## Arquitectura de Servicios

### Backend Go + Echo
```go
package main

import (
    "github.com/labstack/echo/v4"
    "github.com/labstack/echo/v4/middleware"
)

func main() {
    e := echo.New()
    
    // Middleware
    e.Use(middleware.Logger())
    e.Use(middleware.Recover())
    e.Use(middleware.CORS())
    
    // Routes
    e.GET("/", handleWelcome)
    e.GET("/health", handleHealth)
    
    // Auth routes
    auth := e.Group("/auth")
    auth.POST("/login", handleLogin)
    auth.GET("/google", handleGoogleOAuth)
    auth.GET("/google/callback", handleGoogleCallback)
    
    // Protected routes
    api := e.Group("/api/v1")
    api.Use(middleware.JWT([]byte("secret")))
    api.GET("/dashboard/:role", handleDashboard)
    
    e.Logger.Fatal(e.Start(":8080"))
}
```

### Frontend Angular + Services
```typescript
// AuthService
@Injectable({ providedIn: 'root' })
export class AuthService {
  private currentUserSubject: BehaviorSubject<User | null>;
  public currentUser: Observable<User | null>;

  constructor(private http: HttpClient) {
    this.currentUserSubject = new BehaviorSubject<User | null>(null);
    this.currentUser = this.currentUserSubject.asObservable();
  }

  login(email: string, password: string): Observable<User> {
    return this.http.post<User>('/api/auth/login', { email, password })
      .pipe(tap(user => this.currentUserSubject.next(user)));
  }
}
```

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

## Ejemplos de Endpoints Principales

### Autenticación JWT
```json
// POST /api/v1/auth/login
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

### Google Classroom Courses
```json
// GET /api/v1/google/courses
{
  "courses": [
    {
      "id": "course-001",
      "googleId": "123456789",
      "name": "eCommerce Specialist",
      "section": "Section A",
      "status": "COURSE_ACTIVE",
      "studentCount": 150
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
```json
// POST /api/v1/sync/start
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

## Funcionalidades por Rol

### Admin Dashboard
- Vista general del sistema + KPIs institucionales
- Gestión de usuarios + permisos + configuración
- Análisis de tendencias + comparativas entre programas
- Métricas de uso del sistema + performance
- Panel de administración Google + sincronización
- Herramientas de backup + diagnóstico

### Coordinator Dashboard
- Métricas de programas asignados + análisis comparativo
- Seguimiento de teachers + evaluación de rendimiento
- Análisis de cohortes + predicción de resultados
- Reportes automáticos + exportación
- Gestión de cursos por programa

### Teacher Dashboard
- Análisis detallado de cursos propios
- Identificación automática de students en riesgo
- Herramientas de seguimiento + intervención
- Gestión de assignments + grades sincronizadas
- Analytics de participación + engagement

### Student Dashboard
- Progreso personalizado + metas individuales
- Calendario integrado + recordatorios
- Comparativas anónimas + gamificación
- Recomendaciones de estudio + recursos
- Notificaciones personalizadas

## Mapeo Frontend-Backend

### Autenticación
- **POST /api/v1/auth/login** → `useAuth.login()` → `LoginForm` component
- **GET /api/v1/auth/me** → `useAuth.checkAuth()` → `AuthGuard` component
- **POST /api/v1/oauth/google** → `useAuth.getGoogleAuthUrl()` → `OAuthButton` component
- **POST /api/v1/auth/logout** → `useAuth.logout()` → Navigation components

### Dashboards
- **GET /api/v1/dashboard/admin** → `useDashboardData(role='admin')` → `AdminDashboard`
- **GET /api/v1/dashboard/coordinator** → `useDashboardData(role='coordinator')` → `CoordinatorDashboard`
- **GET /api/v1/dashboard/teacher** → `useDashboardData(role='teacher')` → `TeacherDashboard`
- **GET /api/v1/dashboard/student** → `useDashboardData(role='student')` → `StudentDashboard`

### Error Handling
- **401** → redirect /login
- **403** → access denied
- **500** → error boundary

## Estructura de Directorios

```
/
├── backend/
│   ├── handlers/          # API endpoints
│   ├── services/          # Business logic
│   ├── models/            # Data models
│   ├── middleware/        # Auth, CORS, etc.
│   └── tests/             # Unit tests
├── frontend/
│   ├── src/app/
│   │   ├── components/    # Angular components
│   │   ├── services/      # Angular services
│   │   ├── guards/        # Route guards
│   │   └── models/        # TypeScript interfaces
│   └── tests/             # Unit + E2E tests
└── scripts/               # Deployment scripts
```

---

**Versión**: 1.0-LLM | **Consolidado**: Arquitectura + Endpoints + Funcionalidades
