---
title: "ClassSphere - Arquitectura del Sistema Unificado"
version: "3.0"
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
- Go 1.21+ (lenguaje compilado)
- Echo v4 (framework web)
- Go structs (validación con tags)
- Google Classroom API (fuente de datos principal)
- WebSockets (notificaciones)
- Redis (cache compartido)
- testify + mock (testing)
- resty (HTTP client)

# Frontend
- Angular 19 (framework)
- esbuild (bundler oficial desde Angular 17)
- Vite (dev server integrado)
- TypeScript 5.x
- RxJS (reactive programming)
- TailwindCSS 3.x
- Jasmine + Karma (testing unit)
- Playwright (testing E2E)
- Biome (linter/formatter)

# DevOps
- Docker (multi-stage)
- GitHub Actions (CI/CD)
- Trivy (security scanning)
- Redis (cache compartido)
```

## Instalación Nueva Google Classroom con Mocks

Siguiendo la definición de [Instalación Nueva Google Classroom](02_ClassSphere_glosario_tecnico.md#instalación-nueva-google-classroom) del Glosario Técnico:

**Implementación**: Proceso de instalación desde cero con sistema de mocks preconfigurados
**Componentes**: Google Classroom API service, sistema de alternancia mock/real, tests unitarios con mocks controlados
**Configuración**: Flexible para diferentes entornos (desarrollo, testing, producción)

## Arquitectura Resiliente con Prevención de Errores

### 1. Arquitectura Estándar Moderna

**Go Structs**: Validación con tags y custom validators
**Echo Middleware**: Sistema de middleware para autenticación, CORS, rate limiting
**Angular Services**: Inyección de dependencias nativa
**RxJS Observables**: Manejo reactivo de datos y eventos

#### 1.1. Arquitectura de Servicios Go

**Ejemplo de Servicio Go con Echo:**
```go
// AuthService maneja autenticación JWT y OAuth
type AuthService struct {
    jwtSecret []byte
    redis     *redis.Client
}

func NewAuthService(secret string, redisClient *redis.Client) *AuthService {
    return &AuthService{
        jwtSecret: []byte(secret),
        redis:     redisClient,
    }
}

func (s *AuthService) GenerateToken(userID string, role string) (string, error) {
    claims := jwt.MapClaims{
        "user_id": userID,
        "role":    role,
        "exp":     time.Now().Add(time.Hour * 24).Unix(),
    }
    token := jwt.NewWithClaims(jwt.SigningMethodHS256, claims)
    return token.SignedString(s.jwtSecret)
}
```

**Ejemplo de Componente Angular:**
```typescript
// AuthService en Angular con RxJS
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
      .pipe(
        tap(user => this.currentUserSubject.next(user))
      );
  }
}
```

### 2. Infraestructura Estándar

**Backend Go**:
- Puerto 8080 (estándar Go)
- Graceful shutdown
- Health checks en /health
- Metrics en /metrics

**Frontend Angular**:
- Puerto 4200 (desarrollo con ng serve)
- Puerto 80/443 (producción con nginx)
- Server-side rendering opcional
- Progressive Web App (PWA) capabilities

### 3. Redis Compartido

**Uso en Backend (Go)**:
- Sesión de usuario
- Cache de respuestas API
- Rate limiting

**Uso en Frontend (Angular)**:
- No acceso directo (solo via backend)
- Cache de datos en localStorage/sessionStorage

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

**Arquitectura de Servicios Backend (Go + Echo):**
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
    
    // Start server
    e.Logger.Fatal(e.Start(":8080"))
}
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

- Stack de testing definido (Jasmine + Karma + Playwright)
- Testing en Go con testify
- Ejemplos de configuración y uso
- Estrategias de testing E2E

## Referencias a Otros Documentos

- Para detalles sobre términos técnicos, consulte el [Glosario Técnico](02_ClassSphere_glosario_tecnico.md).
- Para los objetivos del sistema, consulte [Objetivos del Sistema](04_ClassSphere_objetivos.md).
- Para las funcionalidades del sistema, consulte [Funcionalidades Consolidadas](06_ClassSphere_funcionalidades.md).
- Para la estrategia de testing completa, consulte [Estrategia de Testing](09_ClassSphere_testing.md).

---

[← Objetivos del Sistema](04_ClassSphere_objetivos.md) | [Índice](00_ClassSphere_index.md) | [Siguiente → Funcionalidades Consolidadas](06_ClassSphere_funcionalidades.md)
