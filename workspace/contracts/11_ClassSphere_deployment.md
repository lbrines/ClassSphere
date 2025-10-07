---
title: "ClassSphere - Unified Deployment Configuration"
version: "4.0"
type: "documentation"
language: "English (Mandatory)"
related_files:
  - "00_ClassSphere_index.md"
  - "10_ClassSphere_plan_implementacion.md"
  - "12_ClassSphere_criterios_aceptacion.md"
---

[← Plan de Implementación](10_ClassSphere_plan_implementacion.md) | [Índice](00_ClassSphere_index.md) | [Siguiente → Criterios de Aceptación](12_ClassSphere_criterios_aceptacion.md)

# Configuración de Deployment Unificada

## Variables de Entorno Consolidadas

### Backend Go (.env)
```env
# Ambiente
ENVIRONMENT=production
SERVER_PORT=8080  # Go + Echo default port

# Database & Cache
REDIS_ADDR=localhost:6379
REDIS_PASSWORD=
REDIS_DB=0

# JWT & OAuth
JWT_SECRET=production-secret-change-this
JWT_ISSUER=classsphere
JWT_EXPIRY_MINUTES=1440  # 24 hours
GOOGLE_CLIENT_ID=your-google-client-id
GOOGLE_CLIENT_SECRET=your-google-client-secret
GOOGLE_REDIRECT_URL=https://your-domain.com/auth/callback
GOOGLE_CREDENTIALS_FILE=/path/to/credentials.json

# Google Classroom API
CLASSROOM_MODE=mock  # mock | google

# CORS
CORS_ORIGINS=https://your-domain.com,http://localhost:4200
CORS_ALLOW_CREDENTIALS=true

# Rate Limiting
RATE_LIMIT_REQUESTS=100
RATE_LIMIT_DURATION=1m

# Logging
LOG_LEVEL=info
LOG_FORMAT=json

# i18n Configuration
DEFAULT_LANGUAGE=en
SUPPORTED_LANGUAGES=en,es,fr
I18N_FALLBACK_LANGUAGE=en
```

### Frontend Angular (environment.prod.ts)
```typescript
// src/environments/environment.prod.ts
export const environment = {
  production: true,
  apiUrl: 'https://api.your-domain.com/api/v1',  // Backend Go API
  wsUrl: 'wss://api.your-domain.com/ws',
  googleClientId: 'your-google-client-id',
  defaultMode: 'mock',  // mock | google
  features: {
    accessibility: true,
    highContrast: true,
    notifications: true
  },
  performance: {
    searchDebounceMs: 300,
    cacheTimeout: 300000
  },
  ports: {
    backend: 8080,   // Go + Echo default
    frontend: 4200   // Angular default
  }
};
```

## Deployment Resiliente con Prevención de Errores

### 1. Problemas de Servidor como Deployment Estándar

**Metodología**: Servidor resiliente es parte integral del deployment

**Deployment with Resilient Server:**
```go
// ✅ STANDARD DEPLOYMENT - Resilient server
package main

import (
    "context"
    "log"
    "net/http"
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

    // Startup - optional external services (new installation)
    if err := verifyGoogleAPIAccess(); err != nil {
        log.Printf("Warning: Google Classroom API unavailable: %v", err)
    }
    
    if err := initRedis(); err != nil {
        log.Printf("Warning: Redis unavailable: %v", err)
    }

    // Routes
    e.GET("/health", healthHandler)
    e.POST("/auth/login", loginHandler)

    // Start server
    go func() {
        if err := e.Start(":8080"); err != nil && err != http.ErrServerClosed {
            e.Logger.Fatal("shutting down the server")
        }
    }()

    // Graceful shutdown
    quit := make(chan os.Signal, 1)
    signal.Notify(quit, os.Interrupt)
    <-quit
    
    ctx, cancel := context.WithTimeout(context.Background(), 10*time.Second)
    defer cancel()
    
    // Cleanup
    if err := cleanupServices(); err != nil {
        log.Printf("Warning: Cleanup error: %v", err)
    }
    
    if err := e.Shutdown(ctx); err != nil {
        e.Logger.Fatal(err)
    }
}
```

**Deployment with Resilient Health Check:**
```go
// ✅ STANDARD DEPLOYMENT - Resilient health check
package handlers

import (
    "net/http"
    "time"

    "github.com/labstack/echo/v4"
)

type HealthResponse struct {
    Status    string            `json:"status"`
    Timestamp string            `json:"timestamp"`
    Services  map[string]string `json:"services,omitempty"`
    Error     string            `json:"error,omitempty"`
}

func HealthHandler(c echo.Context) error {
    // Health check always responds, even with errors
    services, err := checkExternalServices()
    
    if err != nil {
        return c.JSON(http.StatusOK, HealthResponse{
            Status:    "degraded",
            Timestamp: time.Now().Format(time.RFC3339),
            Error:     err.Error(),
        })
    }
    
    return c.JSON(http.StatusOK, HealthResponse{
        Status:    "healthy",
        Timestamp: time.Now().Format(time.RFC3339),
        Services:  services,
    })
}

func checkExternalServices() (map[string]string, error) {
    // Verify external services resiliently (new installation)
    services := make(map[string]string)
    
    // Google Classroom API (optional) - new installation
    if err := verifyGoogleClassroomAPI(); err != nil {
        services["google_classroom_api"] = "unavailable"
    } else {
        services["google_classroom_api"] = "available"
    }
    
    // Redis (optional)
    if err := verifyRedis(); err != nil {
        services["redis"] = "unavailable"
    } else {
        services["redis"] = "available"
    }
    
    return services, nil
}
```

### 2. Port 8080 Busy as Standard Deployment

**Methodology**: Port 8080 as mandatory deployment standard

**Deployment with Fixed Port:**
```bash
# ✅ STANDARD DEPLOYMENT - Port 8080 mandatory
#!/bin/bash
# Script de deployment estándar
set -e

echo "🧹 Deployment: Cleaning previous processes..."
pkill -f classsphere-backend || true
sleep 2

echo "🔍 Deployment: Port 8080 verification..."
if lsof -Pi :8080 -sTCP:LISTEN -t >/dev/null 2>&1; then
    echo "⚠️  Deployment: Port busy. Automatic cleanup..."
    pkill -f "port 8080" || true
    sleep 3
fi

echo "🚀 Deployment: Starting server on port 8080..."
./classsphere-backend &
SERVER_PID=$!

echo "⏳ Deployment: Waiting for server to start..."
sleep 5

echo "🔍 Deployment: Health check verification..."
curl -f http://127.0.0.1:8080/health || {
    echo "❌ Deployment: Health check failed"
    kill $SERVER_PID 2>/dev/null || true
    exit 1
}

echo "✅ Deployment: Server running correctly on port 8080"
echo "📊 Deployment: Server PID: $SERVER_PID"
```

**Deployment with Port Verification:**
```go
// ✅ STANDARD DEPLOYMENT - Port verification
package deployment

import (
    "fmt"
    "net"
    "os/exec"
    "strconv"
    "strings"
    "time"
)

// PortManager manages port 8080 for deployment
type PortManager struct{}

// IsPortAvailable checks if the port is available
func (pm *PortManager) IsPortAvailable(port int) bool {
    address := fmt.Sprintf("127.0.0.1:%d", port)
    listener, err := net.Listen("tcp", address)
    if err != nil {
        return false
    }
    listener.Close()
    return true
}

// KillProcessOnPort kills process on specific port
func (pm *PortManager) KillProcessOnPort(port int) bool {
    cmd := exec.Command("lsof", "-ti", fmt.Sprintf(":%d", port))
    output, err := cmd.Output()
    if err != nil {
        return false
    }

    pids := strings.Split(strings.TrimSpace(string(output)), "\n")
    for _, pid := range pids {
        if pid != "" {
            killCmd := exec.Command("kill", "-9", pid)
            if err := killCmd.Run(); err != nil {
                fmt.Printf("Warning: Error killing process on port %d: %v\n", port, err)
            }
        }
    }
    return true
}

// EnsurePortAvailable ensures the port is available
func (pm *PortManager) EnsurePortAvailable(port int) bool {
    if pm.IsPortAvailable(port) {
        return true
    }

    fmt.Printf("Port %d busy, attempting to free...\n", port)
    pm.KillProcessOnPort(port)
    time.Sleep(2 * time.Second)

    return pm.IsPortAvailable(port)
```

### 3. Errores de Infraestructura como Deployment Estándar

**Metodología**: Errores de infraestructura son parte integral del deployment

**Deployment con Resolución Automática:**
```python
# ✅ DEPLOYMENT ESTÁNDAR - Resolución automática de errores
import asyncio
import logging
from typing import Dict, Any, Optional

class DeploymentManager:
    """Gestor de deployment con resolución automática de errores"""
    
    def __init__(self):
        self.services: Dict[str, Any] = {}
        self.error_count: Dict[str, int] = {}
        self.max_retries = 3
    
    async def deploy_service(self, name: str, service: Any) -> bool:
        """Deploy servicio con resolución automática de errores"""
        try:
            await service.start()
            self.services[name] = service
            self.error_count[name] = 0
            print(f"✅ Deployment: {name} iniciado correctamente")
            return True
        except Exception as e:
            print(f"❌ Deployment: Error en {name}: {e}")
            return await self._handle_deployment_error(name, service, e)
    
    async def _handle_deployment_error(self, name: str, service: Any, error: Exception) -> bool:
        """Manejar error de deployment con reintentos"""
        self.error_count[name] = self.error_count.get(name, 0) + 1
        
        if self.error_count[name] < self.max_retries:
            print(f"🔄 Deployment: Reintentando {name} (intento {self.error_count[name]})")
            await asyncio.sleep(2 ** self.error_count[name])  # Backoff exponencial
            return await self.deploy_service(name, service)
        else:
            print(f"❌ Deployment: {name} falló después de {self.max_retries} intentos")
            return False
    
    async def health_check_all(self) -> Dict[str, bool]:
        """Verificar salud de todos los servicios desplegados"""
        health_status = {}
        
        for name, service in self.services.items():
            try:
                if hasattr(service, 'health_check'):
                    health_status[name] = await service.health_check()
                else:
                    health_status[name] = True
            except Exception as e:
                print(f"Warning: Error en health check de {name}: {e}")
                health_status[name] = False
        
        return health_status

class ResilientService:
    """Servicio resiliente para deployment"""
    
    def __init__(self, name: str):
        self.name = name
        self.running = False
    
    async def start(self):
        """Iniciar servicio de forma resiliente"""
        try:
            # Lógica de inicio del servicio
            self.running = True
        except Exception as e:
            print(f"Warning: Error iniciando {self.name}: {e}")
            raise
    
    async def health_check(self) -> bool:
        """Verificar salud del servicio"""
        try:
            return self.running
        except Exception as e:
            print(f"Warning: Error en health check de {self.name}: {e}")
            return False
```

**Deployment con Script de Inicio Estándar:**
```bash
# ✅ DEPLOYMENT ESTÁNDAR - Script de inicio resiliente
#!/bin/bash
# Script de deployment estándar con resolución automática
set -e

echo "🚀 Deployment: Iniciando ClassSphere..."

# Función de limpieza
cleanup() {
    echo "🧹 Deployment: Limpieza de procesos..."
    pkill -f classsphere-backend || true
    pkill -f "port 8080" || true
    exit 0
}

# Configurar trap para limpieza
trap cleanup SIGINT SIGTERM

# Verificar puerto 8080
echo "🔍 Deployment: Verificando puerto 8080..."
if lsof -Pi :8080 -sTCP:LISTEN -t >/dev/null 2>&1; then
    echo "⚠️  Deployment: Puerto ocupado. Limpieza automática..."
    pkill -f "port 8080" || true
    sleep 3
fi

# Iniciar servidor
echo "🚀 Deployment: Iniciando servidor en puerto 8080..."
./classsphere-backend &
SERVER_PID=$!

# Esperar inicio
echo "⏳ Deployment: Esperando inicio del servidor..."
sleep 5

# Verificar health check
echo "🔍 Deployment: Verificando health check..."
for i in {1..5}; do
    if curl -f http://127.0.0.1:8080/health >/dev/null 2>&1; then
        echo "✅ Deployment: Servidor funcionando correctamente"
        break
    else
        echo "⏳ Deployment: Esperando servidor... (intento $i/5)"
        sleep 2
    fi
done

# Verificar servicios externos (opcional)
echo "🔍 Deployment: Verificando servicios externos..."
curl -s -o /dev/null -w "%{http_code}" https://classroom.googleapis.com/v1/courses?key=TEST_KEY | grep -q "200\|401" && echo "✅ Deployment: Google Classroom API disponible (instalación nueva)" || echo "⚠️  Deployment: Google Classroom API no disponible"
pgrep redis-server && echo "✅ Deployment: Redis disponible" || echo "⚠️  Deployment: Redis no disponible"

echo "🎉 Deployment: ClassSphere iniciado correctamente"
echo "📊 Deployment: PID del servidor: $SERVER_PID"
echo "🌐 Deployment: Servidor disponible en http://127.0.0.1:8080"

# Mantener script corriendo
wait $SERVER_PID
```

## Docker Configuration Completa

### Backend Dockerfile
```dockerfile
# Multi-stage build para optimizar tamaño (Go + Echo)
FROM golang:1.24-alpine AS builder

WORKDIR /app

# Copy go mod files
COPY go.mod go.sum ./
RUN go mod download

# Copy source code
COPY . .

# Build the application
RUN CGO_ENABLED=0 GOOS=linux go build -a -installsuffix cgo -o classsphere-backend ./cmd/api

# Production stage
FROM alpine:latest AS production

# Install ca-certificates for HTTPS
RUN apk --no-cache add ca-certificates curl

# Usuario no-root para seguridad
RUN adduser -D -u 1000 appuser

WORKDIR /app

# Copy binary from builder
COPY --from=builder --chown=appuser:appuser /app/classsphere-backend .

USER appuser

# Healthcheck
HEALTHCHECK --interval=30s --timeout=10s --retries=3 \
    CMD curl -f http://localhost:8080/health || exit 1

EXPOSE 8080
CMD ["./classsphere-backend"]
```

### Frontend Dockerfile
```dockerfile
# Multi-stage build (Angular 19)
FROM node:20-alpine AS builder

WORKDIR /app

# Copy package files
COPY package*.json ./

# Install dependencies
RUN npm ci --legacy-peer-deps

# Copy source code
COPY . .

# Build Angular app for production
RUN npm run build -- --configuration production

# Production stage with nginx
FROM nginx:alpine AS production

# Copy custom nginx config
COPY nginx.conf /etc/nginx/nginx.conf

# Copy built Angular app
COPY --from=builder /app/dist/frontend/browser /usr/share/nginx/html

# Create non-root user
RUN adduser -D -u 1000 appuser && \
    chown -R appuser:appuser /usr/share/nginx/html && \
    chown -R appuser:appuser /var/cache/nginx && \
    chown -R appuser:appuser /var/log/nginx && \
    touch /var/run/nginx.pid && \
    chown -R appuser:appuser /var/run/nginx.pid

USER appuser

# Healthcheck
HEALTHCHECK --interval=30s --timeout=10s --retries=3 \
    CMD wget --quiet --tries=1 --spider http://localhost:4200/ || exit 1

EXPOSE 4200
CMD ["nginx", "-g", "daemon off;"]
```

### docker-compose.yml
```yaml
version: '3.8'

services:
  backend:
    build:
      context: ./backend
      dockerfile: Dockerfile
    container_name: classsphere-backend
    ports:
      - "8080:8080"  # Go + Echo default port
    environment:
      - APP_ENV=production
      - SERVER_PORT=8080
      - JWT_SECRET=${JWT_SECRET}
      - JWT_ISSUER=classsphere
      - JWT_EXPIRY_MINUTES=1440
      - GOOGLE_CLIENT_ID=${GOOGLE_CLIENT_ID}
      - GOOGLE_CLIENT_SECRET=${GOOGLE_CLIENT_SECRET}
      - GOOGLE_REDIRECT_URL=${GOOGLE_REDIRECT_URL}
      - GOOGLE_CREDENTIALS_FILE=/app/credentials.json
      - CLASSROOM_MODE=mock
      - REDIS_ADDR=redis:6379
      - REDIS_PASSWORD=
      - REDIS_DB=0
    volumes:
      - ./credentials.json:/app/credentials.json:ro
    depends_on:
      redis:
        condition: service_healthy
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8080/health"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 40s
    networks:
      - classsphere-network
    deploy:
      resources:
        limits:
          cpus: '2.0'
          memory: 2G
        reservations:
          cpus: '1.0'
          memory: 1G

  frontend:
    build:
      context: ./frontend
      dockerfile: Dockerfile
    container_name: classsphere-frontend
    ports:
      - "4200:4200"  # Angular default port
    environment:
      - API_URL=http://backend:8080/api/v1
    depends_on:
      backend:
        condition: service_healthy
    healthcheck:
      test: ["CMD", "wget", "--quiet", "--tries=1", "--spider", "http://localhost:4200/"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 40s
    networks:
      - classsphere-network

  redis:
    image: redis:7.2.3-alpine
    container_name: classsphere-redis
    ports:
      - "6379:6379"
    volumes:
      - redis_data:/data
    healthcheck:
      test: ["CMD", "redis-cli", "ping"]
      interval: 30s
      timeout: 10s
      retries: 3
    networks:
      - classsphere-network
    command: redis-server --appendonly yes

networks:
  classsphere-network:
    driver: bridge

volumes:
  redis_data:
    driver: local
```

## CI/CD Pipeline Unificado

### .github/workflows/deploy.yml
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

## Verificación de Deployment con Prevención de Errores

### 1. Verificación Automática de Servicios

**Metodología**: Verificación automática como parte integral del deployment

**Script de Verificación de Deployment:**
```bash
# ✅ DEPLOYMENT ESTÁNDAR - Verificación automática
#!/bin/bash
# Script de verificación de deployment
set -e

echo "🔍 Deployment: Verificando servicios..."

# Verificar servidor en puerto 8080
echo "🔍 Deployment: Verificando servidor en puerto 8080..."
if curl -f http://127.0.0.1:8080/health >/dev/null 2>&1; then
    echo "✅ Deployment: Servidor funcionando correctamente"
else
    echo "❌ Deployment: Servidor no responde"
    exit 1
fi

# Verificar servicios externos (opcional)
echo "🔍 Deployment: Verificando servicios externos..."
curl -s -o /dev/null -w "%{http_code}" https://classroom.googleapis.com/v1/courses?key=TEST_KEY | grep -q "200\|401" && echo "✅ Deployment: Google Classroom API disponible (instalación nueva)" || echo "⚠️  Deployment: Google Classroom API no disponible"
pgrep redis-server && echo "✅ Deployment: Redis disponible" || echo "⚠️  Deployment: Redis no disponible"

# Verificar endpoints críticos
echo "🔍 Deployment: Verificando endpoints críticos..."
curl -f http://127.0.0.1:8080/health >/dev/null 2>&1 && echo "✅ Deployment: Health endpoint OK" || echo "❌ Deployment: Health endpoint falló"
curl -f http://127.0.0.1:8080/api/v1/users/me >/dev/null 2>&1 && echo "✅ Deployment: Auth endpoint OK" || echo "⚠️  Deployment: Auth endpoint requiere autenticación"

echo "🎉 Deployment: Verificación completada exitosamente"
```

### 2. Verificación de Puerto 8080

**Metodología**: Puerto 8080 (Go + Echo) como estándar de verificación obligatorio

**Verificación de Puerto con Scripts:**
```bash
# ✅ DEPLOYMENT ESTÁNDAR - Verificación de puerto 8080
#!/bin/bash
# Script de verificación de puerto 8080
set -e

echo "🔍 Deployment: Verificando puerto 8080..."

# Verificar si el puerto está en uso
if lsof -Pi :8080 -sTCP:LISTEN -t >/dev/null 2>&1; then
    echo "✅ Deployment: Puerto 8080 en uso"
    
    # Verificar que sea nuestro proceso
    PID=$(lsof -ti :8080)
    PROCESS=$(ps -p $PID -o comm= 2>/dev/null || echo "unknown")
    
    if [[ "$PROCESS" == *"classsphere"* ]]; then
        echo "✅ Deployment: Puerto 8080 usado por classsphere-backend (PID: $PID)"
    else
        echo "⚠️  Deployment: Puerto 8080 usado por otro proceso: $PROCESS (PID: $PID)"
    fi
else
    echo "❌ Deployment: Puerto 8080 no está en uso"
    exit 1
fi

# Verificar conectividad
echo "🔍 Deployment: Verificando conectividad..."
if curl -f http://127.0.0.1:8080/health >/dev/null 2>&1; then
    echo "✅ Deployment: Conectividad OK"
else
    echo "❌ Deployment: Sin conectividad"
    exit 1
fi

echo "🎉 Deployment: Puerto 8080 verificado correctamente"
```

## Referencias a Otros Documentos

- Para detalles sobre el plan de implementación, consulte [Plan de Implementación](10_ClassSphere_plan_implementacion.md).
- Para detalles sobre los criterios de aceptación, consulte [Criterios de Aceptación](12_ClassSphere_criterios_aceptacion.md).
- Para detalles sobre la validación de coherencia semántica, consulte [Validación de Coherencia Semántica](13_ClassSphere_validacion_coherencia.md).

---

[← Plan de Implementación](10_ClassSphere_plan_implementacion.md) | [Índice](00_ClassSphere_index.md) | [Siguiente → Criterios de Aceptación](12_ClassSphere_criterios_aceptacion.md)
