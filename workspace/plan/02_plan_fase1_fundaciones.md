---
id: "02"
title: "Phase 1: Fundaciones - Backend Go + Frontend Angular"
priority: "CRITICAL"
version: "1.0"
date: "2025-10-07"
duration: "12 days"
max_tokens: 2000
---

# Phase 1: Fundaciones (Days 1-12)

## 🎯 INICIO: PHASE OBJECTIVES AND CRITICAL DEPENDENCIES

### Phase Overview
Establish complete foundations for ClassSphere with Go 1.24.7 backend (Echo v4) and Angular 19 frontend, implementing authentication (JWT + OAuth 2.0 Google), role system, and comprehensive testing infrastructure.

### Critical Dependencies
1. **Go 1.24.7** installed and configured
2. **Node.js 18+** for Angular development
3. **Redis** for caching and sessions
4. **Git** for version control
5. **Docker** for containerization

### Success Criteria
- ✅ Backend running on port 8080 (mandatory, never alternate)
- ✅ Frontend running on port 4200 (mandatory, never alternate)
- ✅ JWT authentication working
- ✅ OAuth 2.0 Google integration complete
- ✅ Role system (admin > coordinator > teacher > student)
- ✅ Test coverage ≥80% global, ≥90% critical modules
- ✅ All tests passing (100%)

### Technology Stack
```yaml
Backend:
  Language: Go 1.24.7
  Framework: Echo v4
  Authentication: JWT + OAuth 2.0 Google
  Cache: Redis
  Testing: testify + httptest
  Port: 8080 (mandatory)

Frontend:
  Framework: Angular 19
  Bundler: esbuild (official)
  Language: TypeScript 5.x
  Styling: TailwindCSS 3.x
  State: RxJS observables
  Testing: Jasmine + Karma + Playwright
  Port: 4200 (mandatory)
```

## 📅 MEDIO: DETAILED IMPLEMENTATION (Day by Day)

### BACKEND IMPLEMENTATION (Days 1-6)

#### Day 1: Go Backend Setup + Project Structure
**Duration**: 8 hours  
**Priority**: CRITICAL

**1.1 Initialize Go Module**
```bash
# Create backend directory
mkdir -p /backend
cd /backend

# Initialize Go module
go mod init github.com/yourusername/classsphere

# Install core dependencies
go get github.com/labstack/echo/v4
go get github.com/labstack/echo/v4/middleware
go get github.com/golang-jwt/jwt/v5
go get github.com/redis/go-redis/v9
go get github.com/stretchr/testify
```

**1.2 Create Hexagonal Architecture Structure**
```bash
backend/
├── cmd/
│   └── api/
│       └── main.go                # Application entry point
├── internal/
│   ├── domain/
│   │   ├── user.go               # User entity
│   │   └── role.go               # Role value object
│   ├── app/
│   │   ├── auth_service.go       # Auth use cases
│   │   └── user_service.go       # User use cases
│   ├── ports/
│   │   ├── repo.go               # Repository interfaces
│   │   ├── cache.go              # Cache interface
│   │   └── oauth.go              # OAuth interface
│   ├── adapters/
│   │   ├── http/
│   │   │   ├── handler.go        # HTTP handlers
│   │   │   └── middleware.go     # Middleware
│   │   ├── repo/
│   │   │   └── memory_repo.go    # In-memory repository
│   │   ├── cache/
│   │   │   └── redis_cache.go    # Redis implementation
│   │   └── oauth/
│   │       └── google_oauth.go   # Google OAuth implementation
│   └── shared/
│       ├── config.go             # Configuration (12-factor)
│       ├── logger.go             # Structured logging
│       └── errors.go             # Error types
├── tests/
│   ├── unit/                     # Unit tests
│   └── integration/              # Integration tests
├── go.mod
├── go.sum
├── Makefile
└── .env.example
```

**1.3 Create main.go with Graceful Shutdown**
```go
// cmd/api/main.go
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
    e.Use(middleware.CORS())
    
    // Routes
    e.GET("/", handleWelcome)
    e.GET("/health", handleHealth)
    
    // Start server in goroutine
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

func handleWelcome(c echo.Context) error {
    return c.JSON(200, map[string]string{
        "message": "Welcome to ClassSphere API",
        "version": "1.0.0",
    })
}

func handleHealth(c echo.Context) error {
    return c.JSON(200, map[string]string{
        "status": "healthy",
    })
}
```

**1.4 TDD: Write Tests First**
```go
// tests/integration/health_test.go
package integration

import (
    "net/http"
    "net/http/httptest"
    "testing"
    
    "github.com/labstack/echo/v4"
    "github.com/stretchr/testify/assert"
)

func TestHealthEndpoint(t *testing.T) {
    // ARRANGE
    e := echo.New()
    req := httptest.NewRequest(http.MethodGet, "/health", nil)
    rec := httptest.NewRecorder()
    c := e.NewContext(req, rec)
    
    // ACT
    err := handleHealth(c)
    
    // ASSERT
    assert.NoError(t, err)
    assert.Equal(t, 200, rec.Code)
}
```

**1.5 Validation Commands**
```bash
# Run tests
go test ./... -v

# Check coverage
go test ./... -cover

# Run server
go run cmd/api/main.go

# Health check
curl http://localhost:8080/health
```

#### Day 2: JWT Authentication Implementation
**Duration**: 8 hours  
**Priority**: CRITICAL

**2.1 Domain Layer: User Entity**
```go
// internal/domain/user.go
package domain

import "time"

type Role string

const (
    RoleAdmin       Role = "admin"
    RoleCoordinator Role = "coordinator"
    RoleTeacher     Role = "teacher"
    RoleStudent     Role = "student"
)

type User struct {
    ID           string    `json:"id"`
    Email        string    `json:"email"`
    PasswordHash string    `json:"-"` // Never expose
    Role         Role      `json:"role"`
    Name         string    `json:"name"`
    CreatedAt    time.Time `json:"created_at"`
    UpdatedAt    time.Time `json:"updated_at"`
}
```

**2.2 Application Layer: Auth Service**
```go
// internal/app/auth_service.go
package app

import (
    "errors"
    "time"
    
    "github.com/golang-jwt/jwt/v5"
    "golang.org/x/crypto/bcrypt"
)

type AuthService struct {
    jwtSecret []byte
    userRepo  UserRepository
}

func NewAuthService(secret string, repo UserRepository) *AuthService {
    return &AuthService{
        jwtSecret: []byte(secret),
        userRepo:  repo,
    }
}

func (s *AuthService) Login(email, password string) (string, error) {
    // Find user
    user, err := s.userRepo.FindByEmail(email)
    if err != nil {
        return "", errors.New("invalid credentials")
    }
    
    // Verify password
    if err := bcrypt.CompareHashAndPassword(
        []byte(user.PasswordHash), 
        []byte(password),
    ); err != nil {
        return "", errors.New("invalid credentials")
    }
    
    // Generate JWT token
    return s.generateToken(user)
}

func (s *AuthService) generateToken(user *User) (string, error) {
    claims := jwt.MapClaims{
        "user_id": user.ID,
        "email":   user.Email,
        "role":    user.Role,
        "exp":     time.Now().Add(24 * time.Hour).Unix(),
    }
    
    token := jwt.NewWithClaims(jwt.SigningMethodHS256, claims)
    return token.SignedString(s.jwtSecret)
}

func (s *AuthService) VerifyToken(tokenString string) (*User, error) {
    token, err := jwt.Parse(tokenString, func(token *jwt.Token) (interface{}, error) {
        return s.jwtSecret, nil
    })
    
    if err != nil || !token.Valid {
        return nil, errors.New("invalid token")
    }
    
    claims := token.Claims.(jwt.MapClaims)
    userID := claims["user_id"].(string)
    
    return s.userRepo.FindByID(userID)
}
```

**2.3 TDD: Auth Service Tests**
```go
// tests/unit/auth_service_test.go
package unit

import (
    "testing"
    
    "github.com/stretchr/testify/assert"
    "github.com/stretchr/testify/mock"
)

type MockUserRepo struct {
    mock.Mock
}

func (m *MockUserRepo) FindByEmail(email string) (*User, error) {
    args := m.Called(email)
    return args.Get(0).(*User), args.Error(1)
}

func TestAuthService_Login_Success(t *testing.T) {
    // ARRANGE
    mockRepo := new(MockUserRepo)
    authService := NewAuthService("secret", mockRepo)
    
    expectedUser := &User{
        ID:    "user-001",
        Email: "test@example.com",
        PasswordHash: "$2a$10$...", // bcrypt hash
        Role:  RoleStudent,
    }
    
    mockRepo.On("FindByEmail", "test@example.com").Return(expectedUser, nil)
    
    // ACT
    token, err := authService.Login("test@example.com", "password123")
    
    // ASSERT
    assert.NoError(t, err)
    assert.NotEmpty(t, token)
    mockRepo.AssertExpectations(t)
}

func TestAuthService_Login_InvalidPassword(t *testing.T) {
    // ARRANGE
    mockRepo := new(MockUserRepo)
    authService := NewAuthService("secret", mockRepo)
    
    expectedUser := &User{
        ID:    "user-001",
        Email: "test@example.com",
        PasswordHash: "$2a$10$...",
        Role:  RoleStudent,
    }
    
    mockRepo.On("FindByEmail", "test@example.com").Return(expectedUser, nil)
    
    // ACT
    token, err := authService.Login("test@example.com", "wrongpassword")
    
    // ASSERT
    assert.Error(t, err)
    assert.Empty(t, token)
    assert.Equal(t, "invalid credentials", err.Error())
}
```

**2.4 HTTP Adapter: Auth Endpoints**
```go
// internal/adapters/http/auth_handler.go
package http

import (
    "net/http"
    
    "github.com/labstack/echo/v4"
)

type AuthHandler struct {
    authService *app.AuthService
}

func NewAuthHandler(authService *app.AuthService) *AuthHandler {
    return &AuthHandler{authService: authService}
}

func (h *AuthHandler) Login(c echo.Context) error {
    var req struct {
        Email    string `json:"email" validate:"required,email"`
        Password string `json:"password" validate:"required"`
    }
    
    if err := c.Bind(&req); err != nil {
        return c.JSON(http.StatusBadRequest, map[string]string{
            "error": "invalid request",
        })
    }
    
    token, err := h.authService.Login(req.Email, req.Password)
    if err != nil {
        return c.JSON(http.StatusUnauthorized, map[string]string{
            "error": "invalid credentials",
        })
    }
    
    return c.JSON(http.StatusOK, map[string]interface{}{
        "token": token,
        "user": map[string]string{
            "email": req.Email,
        },
    })
}
```

**2.5 Validation Commands**
```bash
# Run unit tests
go test ./tests/unit/... -v -cover

# Run integration tests
go test ./tests/integration/... -v -cover

# Check coverage (must be ≥80%)
go test ./... -coverprofile=coverage.out
go tool cover -html=coverage.out

# Test login endpoint
curl -X POST http://localhost:8080/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"admin@classsphere.edu","password":"admin123"}'
```

#### Day 3: OAuth 2.0 Google Integration
**Duration**: 8 hours  
**Priority**: CRITICAL

**3.1 Google OAuth Configuration**
```go
// internal/adapters/oauth/google_oauth.go
package oauth

import (
    "context"
    "encoding/json"
    "fmt"
    "net/http"
    
    "golang.org/x/oauth2"
    "golang.org/x/oauth2/google"
)

type GoogleOAuth struct {
    config *oauth2.Config
}

func NewGoogleOAuth(clientID, clientSecret, redirectURL string) *GoogleOAuth {
    return &GoogleOAuth{
        config: &oauth2.Config{
            ClientID:     clientID,
            ClientSecret: clientSecret,
            RedirectURL:  redirectURL,
            Scopes: []string{
                "https://www.googleapis.com/auth/userinfo.email",
                "https://www.googleapis.com/auth/userinfo.profile",
            },
            Endpoint: google.Endpoint,
        },
    }
}

func (g *GoogleOAuth) GetAuthURL(state string) string {
    return g.config.AuthCodeURL(state, oauth2.AccessTypeOffline)
}

func (g *GoogleOAuth) ExchangeCode(code string) (*oauth2.Token, error) {
    return g.config.Exchange(context.Background(), code)
}

func (g *GoogleOAuth) GetUserInfo(token *oauth2.Token) (*GoogleUser, error) {
    client := g.config.Client(context.Background(), token)
    resp, err := client.Get("https://www.googleapis.com/oauth2/v2/userinfo")
    if err != nil {
        return nil, err
    }
    defer resp.Body.Close()
    
    var user GoogleUser
    if err := json.NewDecoder(resp.Body).Decode(&user); err != nil {
        return nil, err
    }
    
    return &user, nil
}

type GoogleUser struct {
    ID            string `json:"id"`
    Email         string `json:"email"`
    VerifiedEmail bool   `json:"verified_email"`
    Name          string `json:"name"`
    Picture       string `json:"picture"`
}
```

**3.2 OAuth HTTP Endpoints**
```go
// internal/adapters/http/oauth_handler.go
package http

import (
    "net/http"
    
    "github.com/labstack/echo/v4"
)

type OAuthHandler struct {
    googleOAuth *oauth.GoogleOAuth
    authService *app.AuthService
}

func NewOAuthHandler(googleOAuth *oauth.GoogleOAuth, authService *app.AuthService) *OAuthHandler {
    return &OAuthHandler{
        googleOAuth: googleOAuth,
        authService: authService,
    }
}

func (h *OAuthHandler) GoogleLogin(c echo.Context) error {
    state := generateRandomState() // Implement CSRF protection
    url := h.googleOAuth.GetAuthURL(state)
    
    // Store state in session/cookie for verification
    c.SetCookie(&http.Cookie{
        Name:     "oauth_state",
        Value:    state,
        HttpOnly: true,
        Secure:   true,
        SameSite: http.SameSiteStrictMode,
    })
    
    return c.JSON(http.StatusOK, map[string]string{
        "url": url,
    })
}

func (h *OAuthHandler) GoogleCallback(c echo.Context) error {
    // Verify state
    stateCookie, err := c.Cookie("oauth_state")
    if err != nil || stateCookie.Value != c.QueryParam("state") {
        return c.JSON(http.StatusBadRequest, map[string]string{
            "error": "invalid state",
        })
    }
    
    // Exchange code for token
    code := c.QueryParam("code")
    token, err := h.googleOAuth.ExchangeCode(code)
    if err != nil {
        return c.JSON(http.StatusInternalServerError, map[string]string{
            "error": "failed to exchange code",
        })
    }
    
    // Get user info
    googleUser, err := h.googleOAuth.GetUserInfo(token)
    if err != nil {
        return c.JSON(http.StatusInternalServerError, map[string]string{
            "error": "failed to get user info",
        })
    }
    
    // Create or update user in system
    user, err := h.authService.FindOrCreateFromGoogle(googleUser)
    if err != nil {
        return c.JSON(http.StatusInternalServerError, map[string]string{
            "error": "failed to create user",
        })
    }
    
    // Generate JWT token
    jwtToken, err := h.authService.GenerateToken(user)
    if err != nil {
        return c.JSON(http.StatusInternalServerError, map[string]string{
            "error": "failed to generate token",
        })
    }
    
    return c.JSON(http.StatusOK, map[string]interface{}{
        "token": jwtToken,
        "user": user,
    })
}
```

**3.3 TDD: OAuth Tests**
```go
// tests/integration/oauth_test.go
package integration

import (
    "net/http"
    "net/http/httptest"
    "testing"
    
    "github.com/stretchr/testify/assert"
)

func TestOAuth_GoogleLogin(t *testing.T) {
    // ARRANGE
    e := setupTestServer()
    req := httptest.NewRequest(http.MethodGet, "/auth/google", nil)
    rec := httptest.NewRecorder()
    
    // ACT
    e.ServeHTTP(rec, req)
    
    // ASSERT
    assert.Equal(t, http.StatusOK, rec.Code)
    
    var response map[string]string
    json.Unmarshal(rec.Body.Bytes(), &response)
    
    assert.Contains(t, response["url"], "accounts.google.com")
    assert.Contains(t, response["url"], "client_id")
}
```

**3.4 Validation Commands**
```bash
# Set environment variables
export GOOGLE_CLIENT_ID="your-client-id"
export GOOGLE_CLIENT_SECRET="your-client-secret"
export GOOGLE_REDIRECT_URL="http://localhost:8080/auth/google/callback"

# Run OAuth tests
go test ./tests/integration/oauth_test.go -v

# Test OAuth flow manually
curl http://localhost:8080/auth/google
# Follow the URL and complete OAuth flow
```

#### Days 4-6: Role System, Redis, and Middleware
**Summary**: Implement role-based authorization, Redis caching, rate limiting, and comprehensive middleware for authentication, CORS, and logging.

**Key Components**:
- Role-based middleware (CheckRole)
- Redis session store
- Rate limiting per endpoint
- JWT middleware
- CORS configuration
- Request logging
- Error handling middleware

**Tests**: Unit tests for each middleware, integration tests for authorization flows

**Validation**: ≥80% coverage, all tests passing, Redis connected

### FRONTEND IMPLEMENTATION (Days 7-12)

#### Day 7: Angular 19 Setup + Project Structure
**Duration**: 8 hours  
**Priority**: CRITICAL

**7.1 Create Angular Project**
```bash
# Install Angular CLI
npm install -g @angular/cli@19

# Create new project
ng new classsphere-frontend \
  --routing=true \
  --style=scss \
  --strict=true \
  --skip-git=false

cd classsphere-frontend

# Install dependencies
npm install @angular/common@19 @angular/core@19
npm install tailwindcss@3 postcss autoprefixer
npm install rxjs@7
npm install @angular/forms@19
```

**7.2 Configure TailwindCSS**
```bash
# Initialize Tailwind
npx tailwindcss init

# Configure tailwind.config.js
cat > tailwind.config.js << 'EOF'
module.exports = {
  content: [
    "./src/**/*.{html,ts}",
  ],
  theme: {
    extend: {},
  },
  plugins: [],
}
EOF

# Add to styles.scss
echo '@tailwind base;' > src/styles.scss
echo '@tailwind components;' >> src/styles.scss
echo '@tailwind utilities;' >> src/styles.scss
```

**7.3 Project Structure**
```bash
src/
├── app/
│   ├── core/
│   │   ├── services/
│   │   │   ├── auth.service.ts
│   │   │   └── api.service.ts
│   │   ├── guards/
│   │   │   └── auth.guard.ts
│   │   └── interceptors/
│   │       └── auth.interceptor.ts
│   ├── shared/
│   │   ├── components/
│   │   └── pipes/
│   ├── features/
│   │   ├── auth/
│   │   │   ├── login/
│   │   │   └── callback/
│   │   └── dashboard/
│   │       ├── admin/
│   │       ├── coordinator/
│   │       ├── teacher/
│   │       └── student/
│   ├── app.component.ts
│   ├── app.routes.ts
│   └── app.config.ts
├── environments/
│   ├── environment.ts
│   └── environment.prod.ts
└── main.ts
```

**7.4 Angular Configuration**
```typescript
// src/app/app.config.ts
import { ApplicationConfig, provideZoneChangeDetection } from '@angular/core';
import { provideRouter } from '@angular/router';
import { provideHttpClient, withInterceptors } from '@angular/common/http';

import { routes } from './app.routes';
import { authInterceptor } from './core/interceptors/auth.interceptor';

export const appConfig: ApplicationConfig = {
  providers: [
    provideZoneChangeDetection({ eventCoalescing: true }),
    provideRouter(routes),
    provideHttpClient(withInterceptors([authInterceptor]))
  ]
};
```

**7.5 Validation Commands**
```bash
# Run development server
ng serve --port 4200

# Run tests
ng test

# Build production
ng build --configuration production

# Check linting
npx biome check src/
```

#### Days 8-12: Authentication UI, Services, and Routing
**Summary**: Implement LoginForm component, AuthService, AuthGuard, OAuth flow, role-based routing, and comprehensive Jasmine tests.

**Key Components**:
- LoginForm component with reactive forms
- AuthService with RxJS observables
- AuthGuard for protected routes
- OAuth callback handling
- Role-based dashboard routing
- HTTP interceptor for JWT tokens

**Tests**: Component tests with Jasmine, service tests, E2E tests with Playwright

**Validation**: ≥80% coverage, all tests passing, UI responsive

## ✅ FINAL: VERIFICATION CHECKLIST AND NEXT STEPS

### Phase 1 Acceptance Criteria

**Backend Verification**:
- [ ] Server running on port 8080
- [ ] Health endpoint responds: `curl http://localhost:8080/health`
- [ ] Login endpoint working
- [ ] OAuth Google flow complete
- [ ] JWT tokens generated and verified
- [ ] Role system implemented
- [ ] Redis connected
- [ ] Tests passing: `go test ./... -v`
- [ ] Coverage ≥80%: `go test ./... -cover`

**Frontend Verification**:
- [ ] App running on port 4200
- [ ] LoginForm component renders
- [ ] OAuth button redirects to Google
- [ ] AuthGuard protects routes
- [ ] JWT token stored in localStorage
- [ ] Role-based routing working
- [ ] Tests passing: `ng test`
- [ ] Coverage ≥80%: `ng test --code-coverage`

**Integration Verification**:
- [ ] Frontend can call backend API
- [ ] Login flow end-to-end works
- [ ] OAuth flow end-to-end works
- [ ] Protected routes require authentication
- [ ] Role-based access working
- [ ] Error handling displays user-friendly messages

### Commands for Complete Validation

```bash
# Backend
cd /backend
go test ./... -v -cover
go run cmd/api/main.go

# Frontend
cd /frontend
ng test --code-coverage
ng serve --port 4200

# Integration
# Open browser: http://localhost:4200
# Test login with: admin@classsphere.edu / admin123
# Test OAuth Google flow
# Test role-based dashboards
```

### Next Steps

1. **Review Phase 1 Results**: Verify all acceptance criteria met
2. **Read Phase 2 Plan**: `cat workspace/plan/03_plan_fase2_google_integration.md`
3. **Begin Phase 2**: Google Classroom API integration
4. **Maintain Test Coverage**: Continue TDD practices
5. **Document Lessons Learned**: Update phase documentation

### Troubleshooting

**Backend Port Issues**:
```bash
# Check port 8080
lsof -i :8080
# Kill if needed
kill -9 $(lsof -t -i:8080)
```

**Frontend Issues**:
```bash
# Clear Angular cache
rm -rf .angular/
# Reinstall dependencies
rm -rf node_modules package-lock.json
npm install
```

**Redis Connection**:
```bash
# Start Redis
redis-server
# Test connection
redis-cli ping
```

---

*Phase 1 establishes the complete foundation for ClassSphere with modern Go + Angular stack, strict TDD, and comprehensive testing.*

**Last updated**: 2025-10-07  
**Status**: Ready for execution  
**Duration**: 12 days

