# ClassSphere Architecture

**Version**: 1.0  
**Last Updated**: 2025-10-08  
**Stack**: Go 1.24.7 + Echo v4 (Backend), Angular 19 (Frontend)

---

## 🎯 System Overview

```
┌──────────────────────────────────────────────────────────────┐
│                        ClassSphere                            │
│          Educational Dashboard Platform                       │
└──────────────────────────────────────────────────────────────┘
                              │
        ┌─────────────────────┼─────────────────────┐
        │                     │                     │
        ▼                     ▼                     ▼
┌──────────────┐      ┌──────────────┐      ┌──────────────┐
│   Frontend   │◄────►│   Backend    │◄────►│   Google     │
│  Angular 19  │      │  Go + Echo   │      │  Classroom   │
│  Port 4200   │      │  Port 8080   │      │     API      │
└──────────────┘      └──────────────┘      └──────────────┘
                              │
                              ▼
                      ┌──────────────┐
                      │    Redis     │
                      │    Cache     │
                      │  Port 6379   │
                      └──────────────┘
```

---

## 📖 Backend Architecture: Hexagonal (Ports & Adapters)

### 1. Design Philosophy

**Hexagonal Architecture** (Alistair Cockburn) - Also known as Ports & Adapters

**Core Principles**:
1. **Business logic isolated** from infrastructure
2. **Dependency inversion** - domain doesn't depend on adapters
3. **Testability** - mock external dependencies easily
4. **Flexibility** - swap implementations without changing core

### 2. Layer Structure

```
┌─────────────────────────────────────────────────────────────┐
│                    HTTP / Echo Framework                     │
│                  (internal/adapters/http/)                   │
│  Routes, Handlers, Middleware                                │
└───────────────────────────┬─────────────────────────────────┘
                            │ Calls
                            ▼
┌─────────────────────────────────────────────────────────────┐
│                 Application Layer (Use Cases)                │
│                    (internal/app/)                           │
│  AuthService, UserService, ClassroomService                  │
│  Business Logic, Orchestration                               │
└───────────────────────────┬─────────────────────────────────┘
                            │ Uses
                            ▼
┌─────────────────────────────────────────────────────────────┐
│                    Domain Layer (Entities)                   │
│                    (internal/domain/)                        │
│  User, Role, Course, ClassroomSnapshot                       │
│  Pure Business Entities (no dependencies)                    │
└───────────────────────────┬─────────────────────────────────┘
                            │ Defined by
                            ▼
┌─────────────────────────────────────────────────────────────┐
│                    Ports (Interfaces)                        │
│                    (internal/ports/)                         │
│  UserRepository, OAuthProvider, Cache, ClassroomProvider     │
└───────────────────────────┬─────────────────────────────────┘
                            │ Implemented by
                            ▼
┌─────────────────────────────────────────────────────────────┐
│                 Adapters (Implementations)                   │
│                  (internal/adapters/)                        │
│  /repo/    - Memory repository                               │
│  /oauth/   - Google OAuth 2.0                                │
│  /cache/   - Redis cache                                     │
│  /google/  - Google Classroom API                            │
└─────────────────────────────────────────────────────────────┘
```

### 3. Directory Structure

```
backend/
├── cmd/api/
│   ├── main.go                 # Application entry, DI container
│   └── main_test.go            # Integration tests
│
├── internal/
│   ├── domain/                 # 🟦 DOMAIN LAYER (Pure)
│   │   ├── user.go
│   │   ├── role.go
│   │   └── classroom.go        # Business entities
│   │
│   ├── app/                    # 🟩 APPLICATION LAYER (Use Cases)
│   │   ├── auth_service.go     # Authentication logic
│   │   ├── user_service.go     # User management
│   │   ├── classroom_service.go # Classroom aggregation
│   │   └── dashboard_models.go # Dashboard data structures
│   │
│   ├── ports/                  # 🟨 PORTS (Interfaces)
│   │   ├── repo.go             # UserRepository interface
│   │   ├── oauth.go            # OAuthProvider interface
│   │   ├── cache.go            # Cache interface
│   │   └── classroom.go        # ClassroomProvider interface
│   │
│   ├── adapters/               # 🟥 ADAPTERS (Infrastructure)
│   │   ├── http/               # HTTP adapter (Echo)
│   │   │   ├── handler.go
│   │   │   └── middleware.go
│   │   ├── repo/               # Database adapter
│   │   │   └── memory_repo.go
│   │   ├── oauth/              # OAuth adapter
│   │   │   └── google_oauth.go
│   │   ├── cache/              # Cache adapter
│   │   │   └── redis_cache.go
│   │   └── google/             # Google Classroom adapter
│   │       ├── classroom_service.go
│   │       └── mock_data.go
│   │
│   └── shared/                 # Cross-cutting concerns
│       ├── config.go
│       ├── logger.go
│       ├── errors.go
│       └── middleware.go
│
└── tests/
    ├── unit/                   # Unit tests
    └── integration/            # Integration tests
```

### 4. Dependency Flow

```
HTTP Request
     ↓
Handler (adapter/http)
     ↓
Service (app)                ← Orchestrates business logic
     ↓
Domain (entities)            ← Pure business rules
     ↓
Port (interface)             ← Defines contract
     ↓
Adapter (implementation)     ← External systems
     ↓
External System (DB, API, Cache)
```

**Key Insight**: Dependencies point INWARD. Domain has zero external dependencies.

---

## 🎨 Frontend Architecture: Feature Folders

### 1. Design Philosophy

**Feature-Based Organization** - Group by business capability, not technical layer.

**Core Principles**:
1. **Feature isolation** - Each feature is self-contained
2. **Shared core** - Services, guards, models in core/
3. **Reusable UI** - Common components in shared/
4. **Lazy loading** - Features loaded on demand (future)

### 2. Layer Structure

```
┌─────────────────────────────────────────────────────────────┐
│                    Features (Business Logic)                 │
│  /auth, /dashboard, /search, /notifications                  │
│  Components, Pages, Feature-specific logic                   │
└───────────────────────────┬─────────────────────────────────┘
                            │ Uses
                            ▼
┌─────────────────────────────────────────────────────────────┐
│                    Core (Application Services)               │
│  AuthService, ClassroomService, SearchService                │
│  Guards, Interceptors, Models                                │
└───────────────────────────┬─────────────────────────────────┘
                            │ Uses
                            ▼
┌─────────────────────────────────────────────────────────────┐
│                    Shared (Reusable UI)                      │
│  ApexChartComponent, LoginFormComponent, etc.                │
│  Common utilities and pipes                                  │
└─────────────────────────────────────────────────────────────┘
```

### 3. Directory Structure

```
frontend/src/app/
├── features/                   # 🎯 FEATURES (Business capabilities)
│   ├── auth/
│   │   └── pages/login/        # Login page + OAuth
│   │
│   ├── dashboard/
│   │   ├── components/         # Dashboard-specific components
│   │   │   ├── dashboard-view.component.ts
│   │   │   ├── google-connect.component.ts
│   │   │   └── mode-selector.component.ts
│   │   ├── pages/              # Role-specific dashboards
│   │   │   ├── admin/
│   │   │   ├── coordinator/
│   │   │   ├── teacher/
│   │   │   └── student/
│   │   └── dashboard.component.ts
│   │
│   ├── search/
│   │   ├── components/
│   │   │   ├── search-bar/
│   │   │   └── search-results/
│   │   └── pages/search-page/
│   │
│   └── notifications/
│       └── components/
│           ├── notification-badge/
│           └── notification-center/
│
├── core/                       # 🎮 CORE (Application logic)
│   ├── guards/
│   │   ├── auth.guard.ts       # Protect routes (JWT check)
│   │   └── role.guard.ts       # Role-based access
│   │
│   ├── interceptors/
│   │   └── auth.interceptor.ts # Inject JWT in requests
│   │
│   ├── models/
│   │   ├── user.model.ts
│   │   ├── auth.model.ts
│   │   ├── classroom.model.ts
│   │   ├── search.model.ts
│   │   └── notification.model.ts
│   │
│   └── services/
│       ├── auth.service.ts         # Authentication state
│       ├── classroom.service.ts    # Google Classroom data
│       ├── search.service.ts       # Search functionality
│       ├── notification.service.ts # Notifications
│       ├── websocket.service.ts    # Real-time comms
│       └── navigation.service.ts   # Navigation helpers
│
└── shared/                     # 🔧 SHARED (Reusable UI)
    └── components/
        ├── apex-chart/         # ApexCharts wrapper
        ├── drill-down-chart/   # Interactive charts
        ├── login-form/         # Reusable login form
        ├── oauth-button/       # Google OAuth button
        └── not-found/          # 404 page
```

### 4. Component Communication

```
Component (Feature)
     ↓ inject
Service (Core)
     ↓ HTTP
Backend API
     ↓
Database/Cache/Google API
```

**State Management**: RxJS + Angular Signals (no NgRx needed yet)

---

## 🔄 Data Flow

### Authentication Flow

```
1. User submits credentials
   Frontend (LoginPage)
        ↓ POST /auth/login
   Backend (Handler)
        ↓ calls
   AuthService
        ↓ validates
   UserRepository
        ↓ bcrypt compare
   Database
        ↓ generates
   JWT Token
        ↓ returns
   Frontend (stores in localStorage)

2. Subsequent requests include JWT
   Frontend (AuthInterceptor)
        ↓ adds header
   HTTP Request + Authorization: Bearer <token>
        ↓
   Backend (AuthMiddleware)
        ↓ validates
   JWT verification
        ↓ injects
   User context
        ↓
   Handler processes request
```

### Dashboard Data Flow

```
User navigates to /dashboard/admin
        ↓
Frontend (AdminDashboardComponent)
        ↓ inject
ClassroomService.getDashboard('admin')
        ↓ HTTP GET
Backend /api/v1/dashboard/admin?mode=mock
        ↓
Handler → ClassroomService.Dashboard(user, mode)
        ↓
ClassroomProvider (Mock or Google)
        ↓
Snapshot (courses, students, assignments)
        ↓ aggregate
Dashboard Data (summary, charts, highlights)
        ↓ HTTP response
Frontend renders dashboard
```

---

## 🔌 Integration Points

### 1. Frontend ↔ Backend

**Protocol**: HTTP REST  
**Authentication**: JWT Bearer Token  
**Format**: JSON  
**CORS**: Configured for localhost:4200

```typescript
// Frontend Service
getMe(): Observable<User> {
  return this.http.get<User>(`${API_URL}/users/me`);
  // AuthInterceptor adds: Authorization: Bearer <token>
}
```

```go
// Backend Handler
func (h *Handler) me(c echo.Context) error {
    user := CurrentUser(c) // From AuthMiddleware
    return c.JSON(200, user)
}
```

---

### 2. Backend ↔ Google Classroom

**Protocol**: Google REST API + OAuth 2.0  
**Authentication**: Service Account or OAuth User Token  
**Mode**: Dual (Mock/Google) with fallback

```go
// Classroom Provider Interface
type ClassroomProvider interface {
    Mode() string
    Snapshot(ctx context.Context) (ClassroomSnapshot, error)
}

// Mock Implementation (always available)
type MockClassroomService struct { ... }

// Google Implementation (requires credentials)
type GoogleClassroomService struct {
    client *classroom.Service
}
```

**Fallback Strategy**:
```
1. Try requested mode (google or mock)
2. If google fails → fallback to mock with warning log
3. Always return data (never error due to integration failure)
```

---

### 3. Frontend ↔ Backend Real-Time

**Current**: HTTP Polling (30s interval)  
**Future**: WebSocket (implemented, not production-ready)

```typescript
// Polling Implementation
this.classroomService.getDashboard('admin')
  .pipe(
    switchMap(() => timer(30000).pipe(
      switchMap(() => this.classroomService.getDashboard('admin'))
    ))
  )
  .subscribe(data => this.dashboardData = data);
```

---

## 🔐 Security Architecture

### 1. Authentication Layers

```
┌────────────────────────────────────────┐
│  Frontend AuthGuard                    │  ← Prevent route access
│  (client-side, UX only)                │
└──────────────┬─────────────────────────┘
               │ JWT in localStorage
               ▼
┌────────────────────────────────────────┐
│  Backend AuthMiddleware                │  ← Validate JWT
│  (server-side, SECURITY)               │
└──────────────┬─────────────────────────┘
               │ Extract user from JWT
               ▼
┌────────────────────────────────────────┐
│  Backend RoleMiddleware                │  ← Check permissions
│  (server-side, AUTHORIZATION)          │
└────────────────────────────────────────┘
```

**Security Principle**: Never trust frontend. All security enforced on backend.

### 2. JWT Structure

```json
{
  "sub": "user-id",
  "email": "admin@classsphere.edu",
  "role": "admin",
  "iss": "classsphere",
  "exp": 1696770000,
  "iat": 1696766400
}
```

**Signing**: HS256 with `JWT_SECRET` environment variable

### 3. OAuth 2.0 Flow (PKCE)

```
User clicks "Login with Google"
        ↓
Frontend → Backend /auth/oauth/google
        ↓
Backend generates:
  - PKCE code_verifier (random)
  - code_challenge = SHA256(code_verifier)
  - state (CSRF token)
  - Stores in cache: {state → code_verifier}
        ↓
Backend redirects to Google:
  ?code_challenge=...&state=...
        ↓
User authenticates with Google
        ↓
Google redirects to Frontend callback:
  ?code=...&state=...
        ↓
Frontend → Backend /auth/oauth/callback
        ↓
Backend:
  1. Validates state (CSRF check)
  2. Retrieves code_verifier from cache
  3. Exchanges code for Google token (with code_verifier)
  4. Gets user info from Google
  5. Creates/finds user in database
  6. Generates JWT
        ↓
Frontend receives JWT, stores in localStorage
```

---

## 📊 Data Models

### Core Entities

```go
// User - Authentication entity
type User struct {
    ID    string
    Name  string
    Email string
    Role  Role  // admin, coordinator, teacher, student
}

// ClassroomSnapshot - Aggregated Google Classroom data
type ClassroomSnapshot struct {
    Mode        string       // "mock" or "google"
    GeneratedAt time.Time
    Courses     []Course
}

// Course - Enriched course data
type Course struct {
    ID               string
    Name             string
    Section          string
    Program          string
    Teachers         []CourseTeacher
    Students         []CourseStudent
    Assignments      []CourseAssignment
    LastActivity     time.Time
}
```

### Dashboard Models

```go
// DashboardData - Role-specific dashboard view
type DashboardData struct {
    Role        string
    GeneratedAt time.Time
    Mode        string
    Summary     []MetricSummary
    Charts      []ChartConfig
    Highlights  []Highlight
    Alerts      []string
    Courses     []CourseOverview
    Timeline    []TimelineItem
}
```

Full models in `backend/internal/app/dashboard_models.go`

---

## 🧪 Testing Strategy

### Test Pyramid

```
         ╱╲
        ╱E2E╲        ← Playwright (10%)
       ╱──────╲
      ╱ Integ  ╲     ← httptest + mock (30%)
     ╱──────────╲
    ╱    Unit    ╲   ← testify (60%)
   ╱──────────────╲
```

### Backend Testing Layers

**1. Unit Tests** (Domain + App):
```go
// internal/domain/role_test.go
func TestRole_IsValid(t *testing.T) {
    assert.True(t, RoleAdmin.IsValid())
    assert.False(t, Role("invalid").IsValid())
}

// internal/app/auth_service_test.go (with mocks)
func TestAuthService_Login(t *testing.T) {
    mockRepo := &MockUserRepository{}
    mockCache := &MockCache{}
    service := NewAuthService(mockRepo, mockCache, ...)
    
    token, err := service.Login(ctx, "email", "password")
    assert.NoError(t, err)
    assert.NotEmpty(t, token)
}
```

**2. Integration Tests** (Adapters):
```go
// internal/adapters/http/handler_test.go
func TestHandler_Login(t *testing.T) {
    e := setupTestServer()
    req := httptest.NewRequest(POST, "/auth/login", body)
    rec := httptest.NewRecorder()
    
    e.ServeHTTP(rec, req)
    
    assert.Equal(t, 200, rec.Code)
}
```

**3. E2E Tests** (Full flow):
```go
// cmd/api/main_test.go
func TestOAuthFlow(t *testing.T) {
    // Start real server
    // Call /oauth/google
    // Mock Google callback
    // Verify JWT returned
}
```

**Coverage**: 94.4% (target 80%+)

---

## 🚀 Deployment

### Development (Dev Containers)

```bash
# All services start automatically
docker-compose -f .devcontainer/docker-compose.yml up -d

# Backend runs on: http://localhost:8080
# Frontend runs on: http://localhost:4200
# Redis runs on: localhost:6379
```

### Production (Docker Multi-Stage)

```bash
# Build production image
docker build \
  -f .devcontainer/backend/Dockerfile \
  --target production \
  -t classsphere-backend:1.0.0 \
  .

# Run production container
docker run -d \
  -p 8080:8080 \
  -e JWT_SECRET="$JWT_SECRET" \
  -e GOOGLE_CLIENT_ID="$GOOGLE_CLIENT_ID" \
  -e GOOGLE_CLIENT_SECRET="$GOOGLE_CLIENT_SECRET" \
  -e CLASSROOM_MODE="google" \
  classsphere-backend:1.0.0
```

**Image Size**:
- Development: ~800 MB (with tools)
- Production: ~10-15 MB (static binary)

See [DEPLOYMENT.md](DEPLOYMENT.md) for complete guide.

---

## 🔧 Configuration Management

### Environment-Based Config

```go
// internal/shared/config.go
type Config struct {
    // Server
    ServerPort string
    AppEnv     string
    
    // JWT
    JWTSecret       string
    JWTIssuer       string
    JWTExpiryMinutes int
    
    // Google OAuth
    GoogleClientID     string
    GoogleClientSecret string
    GoogleRedirectURL  string
    
    // Google Classroom
    ClassroomMode       string // "mock" or "google"
    GoogleCredentials   string // Path to credentials.json
    
    // Redis
    RedisAddr     string
    RedisPassword string
    RedisDB       int
}
```

**Loading Priority**:
1. Environment variables (highest)
2. .env file
3. Defaults (lowest)

---

## 📈 Performance Considerations

### Caching Strategy

```
Request → AuthMiddleware (checks Redis for user)
              ↓ Hit: return cached
              ↓ Miss: validate JWT + cache user
          Handler
```

**Cache Keys**:
- `user:{userID}` - User profile (TTL: 1 hour)
- `oauth:state:{state}` - PKCE verifier (TTL: 10 minutes)
- `dashboard:{role}:{mode}` - Dashboard data (TTL: 5 minutes)

### Database Queries

**Current**: Memory repository (O(n) lookup)  
**Future**: PostgreSQL with indexes (O(log n))

---

## 🔗 External Dependencies

### Go Modules

```go
// Core
github.com/labstack/echo/v4            // Web framework
github.com/golang-jwt/jwt/v5           // JWT tokens

// Google Integration
golang.org/x/oauth2                    // OAuth 2.0
google.golang.org/api/classroom/v1     // Classroom API

// Database & Cache
github.com/go-redis/redis/v8           // Redis client

// Testing
github.com/stretchr/testify            // Assertions
github.com/alicebob/miniredis/v2       // Redis mock
```

Full list in `go.mod`

---

## 🎯 Design Decisions

### 1. Hexagonal Architecture

**Why**: 
- Testability (94.4% coverage achieved)
- Flexibility (swap implementations easily)
- Clear boundaries (domain isolated)

**Trade-off**: More files, initial complexity

---

### 2. Memory Repository (Current)

**Why**:
- Phase 1 simplicity
- No database setup needed
- Faster tests

**Future**: Migrate to PostgreSQL with GORM

---

### 3. Dual Mode (Mock/Google)

**Why**:
- Development without Google API access
- Testing with consistent data
- Fallback for production resilience

**Implementation**: Strategy pattern with provider interface

---

### 4. Echo Framework

**Why**:
- Lightweight and fast
- Middleware-friendly
- Well-documented
- Standard in Go ecosystem

**Alternative considered**: Gin (similar, chose Echo for middleware flexibility)

---

## 📚 Additional Resources

- **[API Documentation](API_DOCUMENTATION.md)** - Complete API reference
- **[Backend README](backend/README.md)** - Setup and testing
- **[Security](SECURITY.md)** - Security protocols
- **[Testing Strategy](workspace/ci/06_plan_testing_strategy.md)** - TDD approach

---

**Version**: 1.0  
**Last Updated**: 2025-10-08  
**Architecture**: Hexagonal (Backend), Feature Folders (Frontend)

