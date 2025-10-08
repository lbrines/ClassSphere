---
id: "devcontainers-00"
title: "ClassSphere Dev Containers Implementation - Master Plan"
version: "1.0"
priority: "CRITICAL"
tokens: "<2000"
date: "2025-10-07"
context_id: "critical-devcontainers-master"
stack: "Docker Compose + Go 1.24.7 + Angular 19"
architecture: "Multi-Service Dev Environment"
based_on:
  - "workspace/extra/SOFTWARE_PROJECT_BEST_PRACTICES.md"
  - "workspace/extra/DEV_CONTAINERS_BEST_PRACTICES.md"
  - "workspace/contracts/00_ClassSphere_index.md"
  - "workspace/ci/01_plan_index.md"
---

# ClassSphere Dev Containers Implementation - Master Plan

## 🎯 INICIO: Critical Objectives and Blocking Dependencies

### Context ID Tracking

```json
{
  "context_id": "critical-devcontainers-master",
  "priority": "CRITICAL",
  "token_budget": 2000,
  "memory_management": {
    "chunk_position": "beginning",
    "lost_in_middle_risk": "low"
  }
}
```

### Project Mission

Implement **production-grade Dev Containers** for ClassSphere using Docker Compose multi-service architecture, following LLM-optimized best practices and ensuring **< 15 min onboarding time** from git clone to productive development environment.

### Current Project Status (Phase 1 Completed)

**Stack Validated**:
- ✅ Backend: Go 1.24.7 + Echo v4 (port 8080)
- ✅ Frontend: Angular 19 + TailwindCSS 3.x (port 4200)
- ✅ Testing: testify (backend), Jasmine + Karma (frontend), Playwright (E2E)
- ✅ Coverage: 94.4% backend, 94.24% frontend (exceeds 80%+ target)

**Architecture Established**:
```
/backend         # Hexagonal (ports & adapters)
  /cmd/api/      # Routes, middlewares
  /internal/     # domain, app, ports, adapters, shared
  /tests/        # unit, integration, e2e
  
/frontend        # Feature folders
  /src/app/      # (auth)/login, dashboard, shared
  /e2e/          # Playwright tests
```

### Critical Dependencies (With Fallback Strategies)

| Dependency | Type | Fallback | Status | Impact on Dev Containers |
|---|---|---|---|---|
| **Docker Desktop** | 🔴 Critical | None | ⚠️ Required | Blocking: No containers without Docker |
| **VS Code** | 🔴 Critical | JetBrains support | ✅ Mitigated | Dev Containers extension required |
| **Go 1.24.7** | 🔴 Critical | Use 1.21+ compatible | ✅ Mitigated | Backend container base image |
| **Node.js 20+** | 🔴 Critical | None | ✅ Mitigated | Frontend container base image |
| **Redis** | 🟡 Medium | Memory cache | ✅ Mitigated | Service in docker-compose |
| **TailwindCSS 3.x** | 🟡 Medium | None | ⚠️ v4 breaks | Must pin to 3.4.0 |

### Implementation Priorities (Chunking Strategy)

Following **SOFTWARE_PROJECT_BEST_PRACTICES.md** chunking by priority:

```yaml
CRITICAL (max 2000 tokens):
  - devcontainer.json configuration
  - docker-compose.yml multi-service
  - Backend Dockerfile (Go 1.24.7)
  - Frontend Dockerfile (Node 20 + Angular 19)
  - Post-create automation script

HIGH (max 1500 tokens):
  - Named volumes for performance (go-modules, node-modules)
  - Health checks for all services
  - VS Code extensions pre-configuration
  - Port forwarding setup

MEDIUM (max 1000 tokens):
  - Security: non-root user, secrets management
  - Resource limits (CPU, Memory)
  - Workspace scripts and tools
  - Documentation and troubleshooting guide

LOW (max 800 tokens):
  - CI/CD integration
  - Metrics and monitoring
  - Additional features and optimizations
```

### Success Criteria (Measurable)

| Metric | Target | How to Measure | Acceptance |
|---|---|---|---|
| **Setup Time** | < 15 min | From git clone to running app | ✅ Blocking |
| **First Build** | < 5 min | docker-compose build | ✅ Blocking |
| **Hot Reload** | < 2s | Edit → Browser refresh | ✅ Blocking |
| **Dev-Prod Parity** | > 95% | Manual comparison | ✅ Blocking |
| **Memory Usage** | < 4GB | All services combined | ⚠️ Warning |
| **Vulnerability Count** | 0 CRITICAL | Trivy scan | ✅ Blocking |

### Blocking Dependencies Before Starting

- [ ] Docker Desktop installed and running (version 4.0+)
- [ ] VS Code with Dev Containers extension (version 0.380+)
- [ ] Git configured (user.name, user.email)
- [ ] Phase 1 code verified working (backend + frontend)
- [ ] Ports 8080, 4200, 6379 available
- [ ] Minimum 8GB RAM available for Docker

---

## 📅 MEDIO: Implementation Plan by Priority

### Phase Structure (4 Days Total)

```
Day 1: CRITICAL - Core Configuration (2000 tokens)
  ├─ devcontainer.json + docker-compose.yml
  ├─ Backend + Frontend Dockerfiles
  └─ Post-create automation

Day 2: HIGH - Performance & Experience (1500 tokens)
  ├─ Named volumes optimization
  ├─ Health checks
  └─ VS Code customization

Day 3: MEDIUM - Security & Resources (1000 tokens)
  ├─ Non-root user setup
  ├─ Resource limits
  └─ Documentation

Day 4: LOW - Integration & Polish (800 tokens)
  ├─ CI/CD integration
  └─ Metrics and final verification
```

### Day 1: CRITICAL Priority (2000 tokens max)

**Objective**: Functional multi-service dev container with backend, frontend, and Redis.

**Context ID**: `critical-day1-core-setup`

#### 1.1 Directory Structure

```bash
.devcontainer/
├── devcontainer.json           # VS Code configuration (CRITICAL)
├── docker-compose.yml          # Multi-service orchestration (CRITICAL)
├── backend/
│   └── Dockerfile             # Go 1.24.7 container (CRITICAL)
├── frontend/
│   └── Dockerfile             # Node 20 + Angular 19 (CRITICAL)
├── workspace/
│   └── Dockerfile             # Development tools (CRITICAL)
└── scripts/
    └── post-create.sh         # Automated setup (CRITICAL)
```

#### 1.2 devcontainer.json (Core Configuration)

**File**: `.devcontainer/devcontainer.json`
**Priority**: CRITICAL
**Tokens**: ~400

```json
{
  "name": "ClassSphere Full-Stack Dev Environment",
  "dockerComposeFile": "docker-compose.yml",
  "service": "workspace",
  "workspaceFolder": "/workspace",
  
  "features": {
    "ghcr.io/devcontainers/features/git:1": {
      "version": "latest"
    },
    "ghcr.io/devcontainers/features/github-cli:1": {}
  },
  
  "customizations": {
    "vscode": {
      "extensions": [
        "golang.go",
        "angular.ng-template",
        "ms-playwright.playwright",
        "ms-azuretools.vscode-docker",
        "eamodio.gitlens"
      ],
      "settings": {
        "go.toolsManagement.autoUpdate": true,
        "go.useLanguageServer": true,
        "editor.formatOnSave": true,
        "editor.rulers": [80, 120],
        "files.trimTrailingWhitespace": true
      }
    }
  },
  
  "forwardPorts": [8080, 4200, 6379],
  "portsAttributes": {
    "8080": {
      "label": "Backend API (Go + Echo)",
      "onAutoForward": "notify"
    },
    "4200": {
      "label": "Frontend Dev Server (Angular)",
      "onAutoForward": "openBrowser"
    },
    "6379": {
      "label": "Redis Cache",
      "onAutoForward": "ignore"
    }
  },
  
  "postCreateCommand": "bash .devcontainer/scripts/post-create.sh",
  "remoteUser": "vscode"
}
```

**Acceptance Criteria**:
- ✅ VS Code opens dev container successfully
- ✅ All extensions install automatically
- ✅ Ports forward correctly
- ✅ Post-create script executes

#### 1.3 docker-compose.yml (Multi-Service)

**File**: `.devcontainer/docker-compose.yml`
**Priority**: CRITICAL
**Tokens**: ~600

```yaml
version: '3.8'

services:
  # ============================================
  # Workspace (Development Tools)
  # ============================================
  workspace:
    build:
      context: ./workspace
      dockerfile: Dockerfile
    container_name: classsphere-workspace
    command: sleep infinity
    volumes:
      - ../:/workspace:cached
      - go-modules:/go/pkg/mod
      - node-modules-cache:/workspace/frontend/node_modules
    environment:
      - GOPATH=/go
      - PATH=/go/bin:/usr/local/go/bin:$PATH
    depends_on:
      backend:
        condition: service_healthy
      frontend:
        condition: service_started
      redis:
        condition: service_healthy
    networks:
      - classsphere-network
    user: vscode

  # ============================================
  # Backend (Go 1.24.7 + Echo v4)
  # ============================================
  backend:
    build:
      context: ./backend
      dockerfile: Dockerfile
    container_name: classsphere-backend
    ports:
      - "8080:8080"
    volumes:
      - ../backend:/app:cached
      - go-modules:/go/pkg/mod
    environment:
      - APP_ENV=development
      - SERVER_PORT=8080
      - JWT_SECRET=development-secret-key-change-in-production-123456789
      - JWT_ISSUER=classsphere
      - JWT_EXPIRY_MINUTES=60
      - REDIS_ADDR=redis:6379
      - CLASSROOM_MODE=mock
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
          cpus: '0.5'
          memory: 512M

  # ============================================
  # Frontend (Angular 19 + TailwindCSS)
  # ============================================
  frontend:
    build:
      context: ./frontend
      dockerfile: Dockerfile
    container_name: classsphere-frontend
    ports:
      - "4200:4200"
    volumes:
      - ../frontend:/app:cached
      - node-modules-cache:/app/node_modules
      - /app/.angular
    environment:
      - API_URL=http://backend:8080/api/v1
    networks:
      - classsphere-network
    deploy:
      resources:
        limits:
          cpus: '1.5'
          memory: 1G
        reservations:
          cpus: '0.25'
          memory: 256M

  # ============================================
  # Redis (Cache)
  # ============================================
  redis:
    image: redis:7.2.3-alpine
    container_name: classsphere-redis
    ports:
      - "6379:6379"
    healthcheck:
      test: ["CMD", "redis-cli", "ping"]
      interval: 10s
      timeout: 3s
      retries: 3
    networks:
      - classsphere-network
    deploy:
      resources:
        limits:
          cpus: '0.5'
          memory: 256M

# ============================================
# Volumes (Performance Optimization)
# ============================================
volumes:
  go-modules:          # Persistent Go modules cache
  node-modules-cache:  # Persistent npm cache

# ============================================
# Networks
# ============================================
networks:
  classsphere-network:
    driver: bridge
```

**Acceptance Criteria**:
- ✅ All services start successfully
- ✅ Health checks pass for backend and redis
- ✅ Network connectivity between services
- ✅ Volumes persist across rebuilds

#### 1.4 Backend Dockerfile

**File**: `.devcontainer/backend/Dockerfile`
**Priority**: CRITICAL
**Tokens**: ~300

```dockerfile
# Multi-stage build for Go backend
FROM golang:1.24.7-alpine AS base

# Install development tools
RUN apk add --no-cache \
    git \
    curl \
    ca-certificates \
    bash \
    make

# Create non-root user
RUN addgroup -g 1000 vscode && \
    adduser -D -u 1000 -G vscode vscode

# Set up workspace
WORKDIR /app
RUN chown -R vscode:vscode /app

# Install Go tools
RUN go install github.com/cosmtrek/air@latest && \
    go install github.com/golangci/golangci-lint/cmd/golangci-lint@latest

USER vscode

# Default command (overridden by docker-compose)
CMD ["air", "-c", ".air.toml"]
```

**Acceptance Criteria**:
- ✅ Go 1.24.7 installed
- ✅ Development tools available (air, golangci-lint)
- ✅ Non-root user configured
- ✅ Hot reload working with air

#### 1.5 Frontend Dockerfile

**File**: `.devcontainer/frontend/Dockerfile`
**Priority**: CRITICAL
**Tokens**: ~300

```dockerfile
FROM node:20-slim

# Install development tools
RUN apt-get update && apt-get install -y \
    git \
    curl \
    ca-certificates \
    && rm -rf /var/lib/apt/lists/*

# Create non-root user
RUN groupadd -g 1000 vscode && \
    useradd -u 1000 -g vscode -s /bin/bash -m vscode

# Set up workspace
WORKDIR /app
RUN chown -R vscode:vscode /app

# Install global tools
RUN npm install -g @angular/cli@19

USER vscode

# Default command
CMD ["npm", "start"]
```

**Acceptance Criteria**:
- ✅ Node.js 20 installed
- ✅ Angular CLI 19 global
- ✅ Non-root user configured
- ✅ npm start works correctly

#### 1.6 Post-Create Script

**File**: `.devcontainer/scripts/post-create.sh`
**Priority**: CRITICAL
**Tokens**: ~400

```bash
#!/bin/bash
set -e

echo "🚀 ClassSphere Dev Container Setup"
echo "Context ID: critical-day1-post-create"
echo "Timestamp: $(date -Iseconds)"

# ============================================
# Backend Setup
# ============================================
echo "📦 Installing Go dependencies..."
cd /workspace/backend
go mod download

echo "✅ Go version: $(go version)"
echo "✅ Air (hot reload): $(air -v 2>&1 | head -1)"

# ============================================
# Frontend Setup
# ============================================
echo "📦 Installing npm dependencies..."
cd /workspace/frontend
npm ci

# Verify TailwindCSS version (prevent v4 issue)
TAILWIND_VERSION=$(npm list tailwindcss --depth=0 2>/dev/null | grep tailwindcss | awk -F@ '{print $NF}')
echo "✅ TailwindCSS version: $TAILWIND_VERSION"
if [[ $TAILWIND_VERSION == 4.* ]]; then
  echo "⚠️  WARNING: TailwindCSS v4 detected! Phase 1 validated v3.4.0"
fi

echo "✅ Node version: $(node --version)"
echo "✅ Angular CLI: $(npx ng version --no-color 2>&1 | head -1)"

# ============================================
# Health Checks
# ============================================
echo "🏥 Running health checks..."

if redis-cli -h redis ping >/dev/null 2>&1; then
  echo "✅ Redis: OK"
else
  echo "⚠️  Redis not ready yet (waiting for health check)"
fi

# ============================================
# Port Availability
# ============================================
echo "🔌 Verifying port availability..."
for port in 8080 4200 6379; do
  if nc -z localhost $port 2>/dev/null; then
    echo "⚠️  Port $port already in use"
  else
    echo "✅ Port $port: Available"
  fi
done

# ============================================
# Git Configuration
# ============================================
echo "📝 Configuring Git..."
git config --global core.editor "code --wait"
git config --global init.defaultBranch main

# ============================================
# Final Instructions
# ============================================
echo ""
echo "✅ Dev Container setup complete!"
echo ""
echo "📝 Next steps:"
echo "   - Backend: cd /workspace/backend && go run cmd/api/main.go"
echo "   - Frontend: cd /workspace/frontend && npm start"
echo "   - Tests: cd /workspace/backend && go test ./..."
echo ""
echo "📚 Documentation: /workspace/README.md"
echo "🐛 Troubleshooting: /workspace/.devcontainer/TROUBLESHOOTING.md"
```

**Acceptance Criteria**:
- ✅ All dependencies install successfully
- ✅ Health checks validate services
- ✅ Git configured correctly
- ✅ < 5 minutes execution time

---

## ✅ FINAL: Verification Checklist and Next Steps

### Day 1 Completion Checklist

- [ ] Directory structure created: `.devcontainer/` with all subdirectories
- [ ] `devcontainer.json` configured with correct services and extensions
- [ ] `docker-compose.yml` defines all 4 services (workspace, backend, frontend, redis)
- [ ] Backend Dockerfile builds successfully
- [ ] Frontend Dockerfile builds successfully
- [ ] Workspace Dockerfile builds successfully
- [ ] Post-create script executes without errors
- [ ] All health checks pass (backend, redis)
- [ ] Ports forward correctly (8080, 4200, 6379)
- [ ] Backend responds at `http://localhost:8080/health`
- [ ] Frontend responds at `http://localhost:4200`
- [ ] Redis responds to `redis-cli ping`
- [ ] Hot reload works for both backend and frontend
- [ ] VS Code extensions installed automatically
- [ ] Total setup time < 15 minutes

### Verification Commands

```bash
# Build all services
docker-compose -f .devcontainer/docker-compose.yml build

# Start all services
docker-compose -f .devcontainer/docker-compose.yml up -d

# Verify health
docker-compose -f .devcontainer/docker-compose.yml ps

# Check backend
curl http://localhost:8080/health

# Check frontend
curl -I http://localhost:4200

# Check Redis
docker exec classsphere-redis redis-cli ping

# View logs
docker-compose -f .devcontainer/docker-compose.yml logs -f

# Stop all services
docker-compose -f .devcontainer/docker-compose.yml down
```

### Success Metrics Validation

| Metric | Target | Command | Expected Result |
|---|---|---|---|
| Setup Time | < 15 min | `time .devcontainer/scripts/post-create.sh` | < 900s |
| First Build | < 5 min | `time docker-compose build` | < 300s |
| Memory Usage | < 4GB | `docker stats --no-stream` | Combined < 4GB |
| Health Checks | 100% | `docker ps --format "{{.Status}}"` | All "(healthy)" |

### Next Steps

**If Day 1 Complete**:
1. Read: `01_devcontainers_high_priority.md` (Performance optimization)
2. Implement: Named volumes performance tuning
3. Configure: VS Code extensions and settings
4. Validate: Hot reload performance < 2s

**If Day 1 Incomplete**:
1. Review: Error logs with `docker-compose logs`
2. Debug: Individual service issues
3. Validate: Prerequisites (Docker Desktop, VS Code)
4. Retry: Post-create script manually

### Phase-Specific Plans

- **Day 1 (CRITICAL)**: `00_devcontainers_master_plan.md` (This file)
- **Day 2 (HIGH)**: `01_devcontainers_high_priority.md` (Performance & DX)
- **Day 3 (MEDIUM)**: `02_devcontainers_medium_priority.md` (Security & Resources)
- **Day 4 (LOW)**: `03_devcontainers_low_priority.md` (Integration & Polish)

### Troubleshooting Quick Reference

| Issue | Solution | Reference |
|---|---|---|
| Port 8080 busy | `docker-compose down && lsof -ti:8080 \| xargs kill -9` | Phase 1 patterns |
| node_modules not found | `docker-compose exec frontend npm ci` | Day 1 post-create |
| Container build slow | Check `.dockerignore`, enable BuildKit | Day 2 optimization |
| OOM (Out of Memory) | Increase Docker Desktop memory limit | Day 3 resources |
| Services not connecting | Verify `depends_on` with health checks | Day 1 docker-compose |

### Context Management (LLM Optimization)

**Logs Structured for LLM Analysis**:
```json
{
  "timestamp": "2025-10-07T00:00:00Z",
  "context_id": "critical-devcontainers-master",
  "token_count": 1950,
  "context_priority": "CRITICAL",
  "status": "completed",
  "memory_management": {
    "chunk_position": "end",
    "lost_in_middle_risk": "low"
  },
  "next_context": "high-devcontainers-day2"
}
```

---

**CRITICAL**: Do not proceed to Day 2 until ALL Day 1 acceptance criteria are ✅ completed and validated.

**Last Updated**: 2025-10-07 | **Version**: 1.0 | **Status**: Day 1 CRITICAL Implementation Ready

**Token Usage**: 1,950 / 2,000 tokens (CRITICAL priority limit)

