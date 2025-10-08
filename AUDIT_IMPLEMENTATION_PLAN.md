# 🎯 Plan de Implementación - Mejoras de Auditoría

**Branch**: `audit-security-improvements`  
**Fecha Inicio**: 2025-10-08  
**Metodología**: TDD (Test-Driven Development)  
**Basado en**: [AUDIT_REPORT.md](./AUDIT_REPORT.md)

---

## 📋 Índice de Contenidos

1. [Sprint 1: Seguridad Crítica (Semana 1-2)](#sprint-1-seguridad-crítica)
2. [Sprint 2: Observabilidad (Semana 3-4)](#sprint-2-observabilidad)
3. [Sprint 3: Escalabilidad (Semana 5-8)](#sprint-3-escalabilidad)
4. [Criterios de Aceptación Generales](#criterios-de-aceptación-generales)
5. [Comandos de Verificación](#comandos-de-verificación)

---

## 🏃 Sprint 1: Seguridad Crítica (Semana 1-2)

**Objetivo**: Resolver vulnerabilidades críticas (🔴) que impiden deployment seguro en producción.

### Task 1.1: Implementar CORS Restringido 🔴

**Prioridad**: Crítica  
**Archivo**: `backend/internal/adapters/http/handler.go`  
**Estimación**: 4 horas

#### 📝 Enfoque TDD

**1. Escribir Tests (RED)**

```bash
# Crear archivo de test
touch backend/internal/adapters/http/cors_test.go
```

```go
// backend/internal/adapters/http/cors_test.go
package http

import (
    "net/http"
    "net/http/httptest"
    "testing"
    "github.com/stretchr/testify/assert"
)

func TestCORS_AllowedOrigin(t *testing.T) {
    // Setup
    e := setupTestServerWithCORS()
    req := httptest.NewRequest(http.MethodOptions, "/health", nil)
    req.Header.Set("Origin", "http://localhost:4200")
    rec := httptest.NewRecorder()
    
    // Execute
    e.ServeHTTP(rec, req)
    
    // Assert
    assert.Equal(t, http.StatusNoContent, rec.Code)
    assert.Equal(t, "http://localhost:4200", rec.Header().Get("Access-Control-Allow-Origin"))
    assert.Equal(t, "true", rec.Header().Get("Access-Control-Allow-Credentials"))
}

func TestCORS_DisallowedOrigin(t *testing.T) {
    // Setup
    e := setupTestServerWithCORS()
    req := httptest.NewRequest(http.MethodOptions, "/health", nil)
    req.Header.Set("Origin", "https://malicious-site.com")
    rec := httptest.NewRecorder()
    
    // Execute
    e.ServeHTTP(rec, req)
    
    // Assert - No CORS headers should be present
    assert.Empty(t, rec.Header().Get("Access-Control-Allow-Origin"))
}

func TestCORS_AllowedMethods(t *testing.T) {
    e := setupTestServerWithCORS()
    req := httptest.NewRequest(http.MethodOptions, "/api/v1/auth/login", nil)
    req.Header.Set("Origin", "http://localhost:4200")
    req.Header.Set("Access-Control-Request-Method", "POST")
    rec := httptest.NewRecorder()
    
    e.ServeHTTP(rec, req)
    
    assert.Contains(t, rec.Header().Get("Access-Control-Allow-Methods"), "POST")
    assert.Contains(t, rec.Header().Get("Access-Control-Allow-Methods"), "GET")
}

func TestCORS_ProductionOrigins(t *testing.T) {
    // Test con variables de entorno de producción
    t.Setenv("FRONTEND_URL", "https://classsphere.com")
    t.Setenv("APP_ENV", "production")
    
    e := setupTestServerWithCORS()
    req := httptest.NewRequest(http.MethodOptions, "/health", nil)
    req.Header.Set("Origin", "https://classsphere.com")
    rec := httptest.NewRecorder()
    
    e.ServeHTTP(rec, req)
    
    assert.Equal(t, "https://classsphere.com", rec.Header().Get("Access-Control-Allow-Origin"))
}
```

**Comando para verificar tests fallan**:
```bash
cd backend
go test ./internal/adapters/http -v -run TestCORS
# Debe FALLAR (RED)
```

**2. Implementar Código (GREEN)**

```go
// backend/internal/shared/config.go
type Config struct {
    // ... existing fields ...
    FrontendURL        string   // Single URL for simple setup
    AllowedOrigins     []string // Multiple origins for production
}

func LoadConfig() (Config, error) {
    cfg := Config{
        // ... existing code ...
        FrontendURL: getEnv("FRONTEND_URL", "http://localhost:4200"),
    }
    
    // Parse multiple origins if provided
    if originsStr := os.Getenv("ALLOWED_ORIGINS"); originsStr != "" {
        cfg.AllowedOrigins = strings.Split(originsStr, ",")
    } else {
        cfg.AllowedOrigins = []string{cfg.FrontendURL}
    }
    
    return cfg, cfg.Validate()
}
```

```go
// backend/internal/adapters/http/handler.go
func New(authService *app.AuthService, userService *app.UserService, classroomService *app.ClassroomService, notificationHub *app.NotificationHub) *echo.Echo {
    h := &Handler{
        authService:      authService,
        userService:      userService,
        classroomService: classroomService,
        notificationHub:  notificationHub,
    }

    e := echo.New()
    e.HideBanner = true

    // Middleware stack (order matters)
    e.Use(middleware.Recover())
    e.Use(middleware.RequestID())
    e.Use(ErrorHandlerMiddleware())
    
    // CORS con configuración específica
    cfg, _ := shared.LoadConfig()
    e.Use(middleware.CORSWithConfig(middleware.CORSConfig{
        AllowOrigins:     cfg.AllowedOrigins,
        AllowMethods:     []string{echo.GET, echo.POST, echo.PUT, echo.DELETE, echo.OPTIONS},
        AllowHeaders:     []string{echo.HeaderAuthorization, echo.HeaderContentType, echo.HeaderAccept},
        AllowCredentials: true,
        MaxAge:           3600,
    }))
    
    e.Use(middleware.Secure())
    
    // ... rest of the code
}
```

**Comando para verificar tests pasan**:
```bash
go test ./internal/adapters/http -v -run TestCORS
# Debe PASAR (GREEN)
```

**3. Refactorizar (REFACTOR)**

- Extraer configuración de CORS a función helper
- Agregar validación de orígenes
- Documentar configuración

**4. Actualizar Documentación**

```bash
# Agregar a README.md o .env.example
FRONTEND_URL=http://localhost:4200
ALLOWED_ORIGINS=https://classsphere.com,https://app.classsphere.com  # Para producción
```

#### ✅ Criterios de Aceptación

- [ ] Tests unitarios pasan al 100%
- [ ] CORS permite solo orígenes configurados
- [ ] Bloquea orígenes no autorizados
- [ ] Funciona en desarrollo y producción
- [ ] Documentación actualizada

---

### Task 1.2: Implementar Rate Limiting 🔴

**Prioridad**: Crítica  
**Archivo**: `backend/internal/adapters/http/middleware.go`  
**Estimación**: 6 horas

#### 📝 Enfoque TDD

**1. Escribir Tests (RED)**

```bash
touch backend/internal/adapters/http/rate_limit_test.go
```

```go
// backend/internal/adapters/http/rate_limit_test.go
package http

import (
    "net/http"
    "net/http/httptest"
    "testing"
    "time"
    "github.com/stretchr/testify/assert"
)

func TestRateLimit_GlobalLimit(t *testing.T) {
    e := setupTestServerWithRateLimit()
    
    // Send 25 requests (limit is 20/second)
    var lastStatusCode int
    for i := 0; i < 25; i++ {
        req := httptest.NewRequest(http.MethodGet, "/health", nil)
        rec := httptest.NewRecorder()
        e.ServeHTTP(rec, req)
        lastStatusCode = rec.Code
    }
    
    // Last requests should be rate limited
    assert.Equal(t, http.StatusTooManyRequests, lastStatusCode)
}

func TestRateLimit_LoginEndpoint(t *testing.T) {
    e := setupTestServerWithRateLimit()
    
    // Send 7 login requests (limit is 5/second)
    var lastStatusCode int
    for i := 0; i < 7; i++ {
        req := httptest.NewRequest(http.MethodPost, "/api/v1/auth/login", nil)
        req.Header.Set("Content-Type", "application/json")
        rec := httptest.NewRecorder()
        e.ServeHTTP(rec, req)
        lastStatusCode = rec.Code
    }
    
    // Last requests should be rate limited
    assert.Equal(t, http.StatusTooManyRequests, lastStatusCode)
}

func TestRateLimit_ResetsAfterWindow(t *testing.T) {
    e := setupTestServerWithRateLimit()
    
    // Fill the rate limit
    for i := 0; i < 6; i++ {
        req := httptest.NewRequest(http.MethodPost, "/api/v1/auth/login", nil)
        rec := httptest.NewRecorder()
        e.ServeHTTP(rec, req)
    }
    
    // Wait for rate limit window to reset
    time.Sleep(2 * time.Second)
    
    // Should work again
    req := httptest.NewRequest(http.MethodPost, "/api/v1/auth/login", nil)
    rec := httptest.NewRecorder()
    e.ServeHTTP(rec, req)
    
    assert.NotEqual(t, http.StatusTooManyRequests, rec.Code)
}

func TestRateLimit_PerIPTracking(t *testing.T) {
    e := setupTestServerWithRateLimit()
    
    // IP 1 fills rate limit
    for i := 0; i < 6; i++ {
        req := httptest.NewRequest(http.MethodPost, "/api/v1/auth/login", nil)
        req.RemoteAddr = "192.168.1.1:12345"
        rec := httptest.NewRecorder()
        e.ServeHTTP(rec, req)
    }
    
    // IP 2 should still work
    req := httptest.NewRequest(http.MethodPost, "/api/v1/auth/login", nil)
    req.RemoteAddr = "192.168.1.2:12345"
    rec := httptest.NewRecorder()
    e.ServeHTTP(rec, req)
    
    assert.NotEqual(t, http.StatusTooManyRequests, rec.Code)
}
```

**Comando para verificar tests fallan**:
```bash
go test ./internal/adapters/http -v -run TestRateLimit
# Debe FALLAR (RED)
```

**2. Implementar Código (GREEN)**

```go
// backend/internal/adapters/http/rate_limit.go
package http

import (
    "net/http"
    "github.com/labstack/echo/v4"
    "github.com/labstack/echo/v4/middleware"
    "golang.org/x/time/rate"
)

// RateLimitConfig defines rate limiting configuration
type RateLimitConfig struct {
    RequestsPerSecond float64
    Burst             int
    SkipPaths         []string
}

// NewRateLimiter creates a rate limiter middleware
func NewRateLimiter(config RateLimitConfig) echo.MiddlewareFunc {
    store := middleware.NewRateLimiterMemoryStore(rate.Limit(config.RequestsPerSecond))
    
    return middleware.RateLimiterWithConfig(middleware.RateLimiterConfig{
        Store: store,
        IdentifierExtractor: func(c echo.Context) (string, error) {
            // Extract IP from request
            ip := c.RealIP()
            return ip, nil
        },
        ErrorHandler: func(c echo.Context, err error) error {
            return echo.NewHTTPError(http.StatusTooManyRequests, 
                "Rate limit exceeded. Please try again later.")
        },
        DenyHandler: func(c echo.Context, identifier string, err error) error {
            return echo.NewHTTPError(http.StatusTooManyRequests, 
                "Too many requests. Please slow down.")
        },
        Skipper: func(c echo.Context) bool {
            // Skip rate limiting for certain paths
            for _, path := range config.SkipPaths {
                if c.Path() == path {
                    return true
                }
            }
            return false
        },
    })
}

// LoginRateLimiter creates a stricter rate limiter for login endpoint
func LoginRateLimiter() echo.MiddlewareFunc {
    return NewRateLimiter(RateLimitConfig{
        RequestsPerSecond: 5,  // 5 login attempts per second per IP
        Burst:             1,
        SkipPaths:         []string{},
    })
}
```

```go
// backend/internal/adapters/http/handler.go
func New(...) *echo.Echo {
    // ... existing code ...
    
    // Global rate limiter (20 req/s)
    e.Use(NewRateLimiter(RateLimitConfig{
        RequestsPerSecond: 20,
        Burst:             5,
        SkipPaths:         []string{"/health"},
    }))
    
    // ... existing middleware ...
    
    api := e.Group("/api/v1")
    
    // Login endpoint with stricter rate limit
    api.POST("/auth/login", h.login, LoginRateLimiter())
    
    // ... rest of the code ...
}
```

**Comando para verificar tests pasan**:
```bash
go test ./internal/adapters/http -v -run TestRateLimit
# Debe PASAR (GREEN)
```

**3. Refactorizar (REFACTOR)**

- Configurar límites desde environment variables
- Agregar logging de rate limit violations
- Implementar Redis store para producción (multi-instance)

**4. Implementación Avanzada (Opcional - Redis)**

```go
// backend/internal/adapters/http/rate_limit_redis.go
package http

import (
    "context"
    "time"
    "github.com/redis/go-redis/v9"
)

type RedisRateLimitStore struct {
    client *redis.Client
    ttl    time.Duration
}

func NewRedisRateLimitStore(client *redis.Client, ttl time.Duration) *RedisRateLimitStore {
    return &RedisRateLimitStore{
        client: client,
        ttl:    ttl,
    }
}

func (s *RedisRateLimitStore) Allow(identifier string) (bool, error) {
    ctx := context.Background()
    key := "rate_limit:" + identifier
    
    count, err := s.client.Incr(ctx, key).Result()
    if err != nil {
        return false, err
    }
    
    if count == 1 {
        s.client.Expire(ctx, key, s.ttl)
    }
    
    return count <= 20, nil // 20 requests per window
}
```

#### ✅ Criterios de Aceptación

- [ ] Tests unitarios pasan al 100%
- [ ] Rate limit global: 20 req/s
- [ ] Rate limit login: 5 req/s
- [ ] Tracking por IP
- [ ] Respuesta 429 correcta
- [ ] Headers de rate limit incluidos
- [ ] Opción Redis para producción

---

### Task 1.3: Eliminar Console.log en Frontend 🔴

**Prioridad**: Crítica  
**Archivos**: Múltiples componentes frontend  
**Estimación**: 4 horas

#### 📝 Enfoque TDD

**1. Escribir Tests (RED)**

```bash
cd frontend
touch src/app/core/services/logger.service.spec.ts
```

```typescript
// frontend/src/app/core/services/logger.service.spec.ts
import { TestBed } from '@angular/core/testing';
import { LoggerService } from './logger.service';

describe('LoggerService', () => {
  let service: LoggerService;
  let consoleLogSpy: jasmine.Spy;
  let consoleErrorSpy: jasmine.Spy;

  beforeEach(() => {
    TestBed.configureTestingModule({});
    service = TestBed.inject(LoggerService);
    
    consoleLogSpy = spyOn(console, 'log');
    consoleErrorSpy = spyOn(console, 'error');
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });

  describe('in development', () => {
    beforeEach(() => {
      service['isProduction'] = false;
    });

    it('should log messages to console', () => {
      service.log('test message', { data: 'test' });
      expect(consoleLogSpy).toHaveBeenCalledWith('test message', { data: 'test' });
    });

    it('should log errors to console', () => {
      const error = new Error('test error');
      service.error('error message', error);
      expect(consoleErrorSpy).toHaveBeenCalledWith('error message', error);
    });
  });

  describe('in production', () => {
    beforeEach(() => {
      service['isProduction'] = true;
    });

    it('should NOT log messages to console', () => {
      service.log('test message');
      expect(consoleLogSpy).not.toHaveBeenCalled();
    });

    it('should NOT log errors to console', () => {
      service.error('error message', new Error('test'));
      expect(consoleErrorSpy).not.toHaveBeenCalled();
    });
  });

  describe('warn', () => {
    it('should log warnings in development', () => {
      const warnSpy = spyOn(console, 'warn');
      service['isProduction'] = false;
      
      service.warn('warning message');
      expect(warnSpy).toHaveBeenCalledWith('warning message');
    });
  });

  describe('debug', () => {
    it('should log debug messages in development', () => {
      const debugSpy = spyOn(console, 'debug');
      service['isProduction'] = false;
      
      service.debug('debug message', { context: 'test' });
      expect(debugSpy).toHaveBeenCalledWith('debug message', { context: 'test' });
    });
  });
});
```

**Comando para verificar tests fallan**:
```bash
cd frontend
npm test -- --include='**/logger.service.spec.ts'
# Debe FALLAR (RED)
```

**2. Implementar Código (GREEN)**

```typescript
// frontend/src/app/core/services/logger.service.ts
import { Injectable } from '@angular/core';
import { environment } from '../../../environments/environment';

export enum LogLevel {
  Debug = 0,
  Log = 1,
  Warn = 2,
  Error = 3,
}

@Injectable({ providedIn: 'root' })
export class LoggerService {
  private isProduction = environment.production;
  private logLevel: LogLevel = this.isProduction ? LogLevel.Warn : LogLevel.Debug;

  log(message: string, ...optionalParams: any[]): void {
    if (!this.isProduction && this.logLevel <= LogLevel.Log) {
      console.log(message, ...optionalParams);
    }
  }

  debug(message: string, ...optionalParams: any[]): void {
    if (!this.isProduction && this.logLevel <= LogLevel.Debug) {
      console.debug(message, ...optionalParams);
    }
  }

  warn(message: string, ...optionalParams: any[]): void {
    if (this.logLevel <= LogLevel.Warn) {
      console.warn(message, ...optionalParams);
    }
  }

  error(message: string, error?: any): void {
    if (!this.isProduction) {
      console.error(message, error);
    } else {
      // En producción, enviar a servicio de monitoreo
      this.sendToMonitoring(message, error);
    }
  }

  private sendToMonitoring(message: string, error?: any): void {
    // TODO: Integrar con Sentry, LogRocket, etc.
    // Para fase 1, simplemente no logear en producción
  }
}
```

**3. Reemplazar console.log en componentes**

```bash
# Script para encontrar todos los console.log
cd frontend/src
grep -r "console\." --include="*.ts" | wc -l
```

```typescript
// frontend/src/app/features/search/pages/search-page/search-page.component.ts
import { LoggerService } from '../../../../core/services/logger.service';

export class SearchPageComponent {
  private logger = inject(LoggerService);
  
  onSearch(event: SearchEvent): void {
    // ANTES: console.log('Search triggered:', event);
    this.logger.debug('Search triggered:', event);
    
    // ... rest of code ...
  }
  
  onError(error: any): void {
    // ANTES: console.error('Search failed:', error);
    this.logger.error('Search failed:', error);
  }
}
```

**Comando para verificar tests pasan**:
```bash
npm test
# Todos los tests deben PASAR (GREEN)
```

**4. Refactorizar (REFACTOR)**

- Crear script automático para reemplazar console.log
- Agregar linting rule para prevenir console.log futuro
- Configurar build optimizer

```json
// frontend/.eslintrc.json
{
  "rules": {
    "no-console": ["error", { "allow": ["warn", "error"] }]
  }
}
```

```bash
# Script para reemplazar console.log automáticamente
cd frontend
npm install --save-dev eslint-plugin-no-console
```

#### ✅ Criterios de Aceptación

- [ ] LoggerService implementado con tests
- [ ] Todos los console.log reemplazados
- [ ] Producción NO imprime logs
- [ ] Development SÍ imprime logs
- [ ] ESLint rule configurada
- [ ] Build optimizer activo

---

### Task 1.4: Actualizar Dependencias Vulnerables 🔴

**Prioridad**: Crítica  
**Archivos**: `go.mod`, `package.json`  
**Estimación**: 3 horas

#### 📝 Pasos

**1. Backend - Actualizar Go y dependencias**

```bash
cd backend

# Actualizar Go version en go.mod
# go 1.18 -> go 1.22

# Verificar vulnerabilidades actuales
go install golang.org/x/vuln/cmd/govulncheck@latest
govulncheck ./... > vulnerabilities-before.txt

# Actualizar dependencias
go get -u github.com/labstack/echo/v4@latest  # 4.9.1 -> 4.12+
go get -u github.com/golang-jwt/jwt/v5@latest
go get -u github.com/redis/go-redis/v9@latest
go get -u golang.org/x/crypto@latest
go get -u google.golang.org/api@latest

# Verificar que tests pasan
go test ./...

# Verificar vulnerabilidades después
govulncheck ./... > vulnerabilities-after.txt

# Comparar
diff vulnerabilities-before.txt vulnerabilities-after.txt
```

**2. Frontend - Audit y fix**

```bash
cd frontend

# Audit actual
npm audit > audit-before.txt

# Fix automático (non-breaking)
npm audit fix

# Fix manual si es necesario
npm audit fix --force  # Cuidado: puede romper

# Re-run tests
npm test
npm run build

# Audit después
npm audit > audit-after.txt

# Comparar
diff audit-before.txt audit-after.txt
```

#### ✅ Criterios de Aceptación

- [ ] Go 1.22+ configurado
- [ ] Echo 4.12+ instalado
- [ ] govulncheck sin vulnerabilidades CRITICAL/HIGH
- [ ] npm audit sin vulnerabilidades CRITICAL/HIGH
- [ ] Todos los tests pasan
- [ ] Build exitoso

---

## 🏃 Sprint 2: Observabilidad (Semana 3-4)

**Objetivo**: Implementar métricas y monitoring para observabilidad en producción.

### Task 2.1: Implementar Métricas Prometheus 🟡

**Prioridad**: Media  
**Archivo**: `backend/internal/adapters/http/metrics.go`  
**Estimación**: 8 horas

#### 📝 Enfoque TDD

**1. Escribir Tests (RED)**

```go
// backend/internal/adapters/http/metrics_test.go
package http

import (
    "net/http"
    "net/http/httptest"
    "testing"
    "github.com/prometheus/client_golang/prometheus/testutil"
    "github.com/stretchr/testify/assert"
)

func TestMetrics_HTTPRequestsTotal(t *testing.T) {
    // Reset metrics
    resetMetrics()
    
    e := setupTestServerWithMetrics()
    
    // Make requests
    for i := 0; i < 5; i++ {
        req := httptest.NewRequest(http.MethodGet, "/health", nil)
        rec := httptest.NewRecorder()
        e.ServeHTTP(rec, req)
    }
    
    // Verify metrics
    count := testutil.ToFloat64(httpRequestsTotal.WithLabelValues("GET", "/health", "200"))
    assert.Equal(t, float64(5), count)
}

func TestMetrics_HTTPRequestDuration(t *testing.T) {
    resetMetrics()
    
    e := setupTestServerWithMetrics()
    
    req := httptest.NewRequest(http.MethodGet, "/health", nil)
    rec := httptest.NewRecorder()
    e.ServeHTTP(rec, req)
    
    // Verify histogram recorded
    count := testutil.CollectAndCount(httpRequestDuration.WithLabelValues("GET", "/health"))
    assert.Greater(t, count, 0)
}

func TestMetrics_ActiveConnections(t *testing.T) {
    resetMetrics()
    
    e := setupTestServerWithMetrics()
    
    // Start request (increases active)
    // ... simulate concurrent request
    
    // End request (decreases active)
    // ... complete request
    
    // Verify gauge
    active := testutil.ToFloat64(activeConnections)
    assert.Equal(t, float64(0), active)
}
```

**2. Implementar Código (GREEN)**

```go
// backend/internal/adapters/http/metrics.go
package http

import (
    "strconv"
    "time"
    "github.com/labstack/echo/v4"
    "github.com/prometheus/client_golang/prometheus"
    "github.com/prometheus/client_golang/prometheus/promauto"
)

var (
    httpRequestsTotal = promauto.NewCounterVec(
        prometheus.CounterOpts{
            Name: "classsphere_http_requests_total",
            Help: "Total number of HTTP requests",
        },
        []string{"method", "endpoint", "status"},
    )
    
    httpRequestDuration = promauto.NewHistogramVec(
        prometheus.HistogramOpts{
            Name:    "classsphere_http_request_duration_seconds",
            Help:    "HTTP request duration in seconds",
            Buckets: prometheus.DefBuckets,
        },
        []string{"method", "endpoint"},
    )
    
    activeConnections = promauto.NewGauge(
        prometheus.GaugeOpts{
            Name: "classsphere_active_connections",
            Help: "Number of active connections",
        },
    )
    
    authAttempts = promauto.NewCounterVec(
        prometheus.CounterOpts{
            Name: "classsphere_auth_attempts_total",
            Help: "Total authentication attempts",
        },
        []string{"method", "status"}, // method: password/oauth, status: success/failure
    )
)

// MetricsMiddleware tracks HTTP metrics
func MetricsMiddleware() echo.MiddlewareFunc {
    return func(next echo.HandlerFunc) echo.HandlerFunc {
        return func(c echo.Context) error {
            start := time.Now()
            activeConnections.Inc()
            defer activeConnections.Dec()
            
            err := next(c)
            
            duration := time.Since(start).Seconds()
            status := c.Response().Status
            
            httpRequestsTotal.WithLabelValues(
                c.Request().Method,
                c.Path(),
                strconv.Itoa(status),
            ).Inc()
            
            httpRequestDuration.WithLabelValues(
                c.Request().Method,
                c.Path(),
            ).Observe(duration)
            
            return err
        }
    }
}

// RecordAuthAttempt records authentication attempts
func RecordAuthAttempt(method string, success bool) {
    status := "failure"
    if success {
        status = "success"
    }
    authAttempts.WithLabelValues(method, status).Inc()
}
```

**3. Agregar endpoint de métricas**

```go
// backend/internal/adapters/http/handler.go
import "github.com/prometheus/client_golang/prometheus/promhttp"

func New(...) *echo.Echo {
    // ... existing code ...
    
    // Metrics middleware
    e.Use(MetricsMiddleware())
    
    // ... other middleware ...
    
    // Metrics endpoint (no auth required - scraper needs access)
    e.GET("/metrics", echo.WrapHandler(promhttp.Handler()))
    
    // ... rest of code ...
}
```

**4. Integrar en AuthService**

```go
// backend/internal/app/auth_service.go
import "github.com/lbrines/classsphere/internal/adapters/http"

func (a *AuthService) LoginWithPassword(ctx context.Context, email, password string) (AuthTokens, error) {
    user, err := a.users.FindByEmail(ctx, email)
    if err != nil {
        http.RecordAuthAttempt("password", false)
        return AuthTokens{}, shared.ErrInvalidCredentials
    }

    if err := bcrypt.CompareHashAndPassword([]byte(user.HashedPassword), []byte(password)); err != nil {
        http.RecordAuthAttempt("password", false)
        return AuthTokens{}, shared.ErrInvalidCredentials
    }

    http.RecordAuthAttempt("password", true)
    
    // ... rest of code ...
}
```

#### ✅ Criterios de Aceptación

- [ ] Tests de métricas pasan
- [ ] Endpoint `/metrics` expone métricas
- [ ] Contador de requests
- [ ] Histograma de latencia
- [ ] Gauge de conexiones activas
- [ ] Contador de intentos de autenticación
- [ ] Documentación de métricas

---

### Task 2.2: Health Checks Detallados 🟡

**Estimación**: 4 horas

Ver implementación detallada en el reporte de auditoría, sección "MEJORA #3: Sin health checks detallados".

#### Criterios de Aceptación

- [ ] Health check verifica Redis
- [ ] Health check verifica Google API
- [ ] Responde 503 si unhealthy
- [ ] JSON con detalles de cada check
- [ ] Tests de health checks

---

## 🏃 Sprint 3: Escalabilidad (Semana 5-8)

### Task 3.1: Migrar a PostgreSQL 🟠

**Prioridad**: Alta para producción  
**Estimación**: 16 horas

Ver plan detallado en el reporte, sección "MEJORA #1: Sin base de datos persistente".

---

## ✅ Criterios de Aceptación Generales

### Por Sprint

**Sprint 1 (Seguridad):**
- [ ] CORS restringido y testeado
- [ ] Rate limiting activo en todos los endpoints críticos
- [ ] Zero console.log en código de producción
- [ ] Dependencias actualizadas sin vulnerabilidades CRITICAL/HIGH
- [ ] Todos los tests pasan
- [ ] Cobertura ≥94.4%

**Sprint 2 (Observabilidad):**
- [ ] Métricas Prometheus funcionando
- [ ] Endpoint /metrics accesible
- [ ] Health checks detallados
- [ ] Logging estructurado en frontend
- [ ] Documentación de métricas

**Sprint 3 (Escalabilidad):**
- [ ] PostgreSQL integrado
- [ ] Migrations funcionando
- [ ] Frontend optimizado (lazy loading)
- [ ] CI/CD pipeline completo

---

## 🔍 Comandos de Verificación

### Pre-commit

```bash
# Backend
cd backend
go test ./... -coverprofile=coverage.out
go tool cover -func=coverage.out | grep total  # Debe ser ≥94.4%
govulncheck ./...
golangci-lint run --enable=gosec ./...

# Frontend
cd frontend
npm test
npm run lint
npm audit
npm run build
```

### Post-deploy

```bash
# Health check
curl http://localhost:8080/health

# Metrics
curl http://localhost:8080/metrics

# CORS test
curl -H "Origin: http://localhost:4200" \
     -H "Access-Control-Request-Method: POST" \
     -X OPTIONS \
     http://localhost:8080/api/v1/auth/login

# Rate limit test
for i in {1..25}; do 
  curl http://localhost:8080/health
done
```

---

## 📊 Progreso del Plan

### Sprint 1: Seguridad Crítica
- [ ] Task 1.1: CORS Restringido (4h)
- [ ] Task 1.2: Rate Limiting (6h)
- [ ] Task 1.3: Eliminar Console.log (4h)
- [ ] Task 1.4: Actualizar Dependencias (3h)

**Total Sprint 1**: 17 horas

### Sprint 2: Observabilidad
- [ ] Task 2.1: Métricas Prometheus (8h)
- [ ] Task 2.2: Health Checks Detallados (4h)
- [ ] Task 2.3: Logging Frontend (4h)

**Total Sprint 2**: 16 horas

### Sprint 3: Escalabilidad
- [ ] Task 3.1: PostgreSQL (16h)
- [ ] Task 3.2: Optimización Frontend (8h)
- [ ] Task 3.3: CI/CD (8h)

**Total Sprint 3**: 32 horas

**TOTAL ESTIMADO**: 65 horas (~8-9 días de trabajo)

---

## 🎯 Definition of Done

Una tarea se considera **DONE** cuando:

1. ✅ Tests escritos PRIMERO (TDD)
2. ✅ Tests pasan al 100%
3. ✅ Cobertura mantenida o aumentada (≥94.4%)
4. ✅ Código refactorizado y limpio
5. ✅ Documentación actualizada
6. ✅ No introduce vulnerabilidades
7. ✅ Linting pasa sin errores
8. ✅ PR revieweado y aprobado
9. ✅ Deploy exitoso en staging
10. ✅ Validación manual completada

---

**Última actualización**: 2025-10-08  
**Branch**: `audit-security-improvements`  
**Next Review**: Después de Sprint 1

