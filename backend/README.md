# ClassSphere Backend

**Go 1.24.7 + Echo v4 REST API**

![Coverage](https://img.shields.io/badge/coverage-94.4%25-brightgreen)
![Go](https://img.shields.io/badge/Go-1.24.7-00ADD8?logo=go)
![Tests](https://img.shields.io/badge/tests-150+-success)

---

## 🎯 Overview

RESTful API backend for ClassSphere educational platform, implementing hexagonal architecture with comprehensive test coverage.

### Key Features

- ✅ **JWT Authentication**: Secure token-based auth with refresh tokens
- ✅ **OAuth 2.0 Google**: PKCE + State parameter implementation
- ✅ **Role-Based Access Control**: 4 roles (admin, coordinator, teacher, student)
- ✅ **Google Classroom Integration**: Dual mode (Mock/Real) with fallback
- ✅ **Redis Caching**: Session management with memory fallback
- ✅ **94.4% Test Coverage**: 150+ tests with testify/mock

---

## 🚀 Quick Start

### Prerequisites
- Go 1.24.7+ installed
- Redis (optional)

### Run Server

```bash
# Set environment variables
export JWT_SECRET="development-secret-key-change-in-production-123456789"
export GOOGLE_CLIENT_ID="your-client-id.apps.googleusercontent.com"
export GOOGLE_CLIENT_SECRET="GOCSPX-your-secret"
export GOOGLE_REDIRECT_URL="http://localhost:4200/auth/callback"
export CLASSROOM_MODE="mock"

# Install dependencies
go mod download

# Run server
go run cmd/api/main.go

# Server running on http://localhost:8080
```

### Run with Hot Reload (Air)

```bash
# Install Air
go install github.com/cosmtrek/air@latest

# Run with hot reload
air -c .air.toml

# Edit code → server restarts automatically
```

---

## 📖 API Endpoints

**Base URL**: `http://localhost:8080/api/v1`

### Public Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/health` | GET | Health check (returns `{"status":"ok"}`) |
| `/auth/login` | POST | Email/password login → JWT token |
| `/auth/oauth/google` | GET | Initiate Google OAuth flow |
| `/auth/oauth/callback` | GET | OAuth callback → JWT token |

### Protected Endpoints (JWT Required)

| Endpoint | Method | Roles | Description |
|----------|--------|-------|-------------|
| `/users/me` | GET | All | Current user profile |
| `/admin/ping` | GET | Admin | Admin-only test endpoint |
| `/google/courses` | GET | All | List Google Classroom courses |
| `/classroom/courses` | GET | All | Alias for /google/courses |
| `/dashboard/admin` | GET | Admin | Admin dashboard data |
| `/dashboard/coordinator` | GET | Coordinator | Coordinator dashboard data |
| `/dashboard/teacher` | GET | Teacher | Teacher dashboard data |
| `/dashboard/student` | GET | Student | Student dashboard data |

**Full API Reference**: See [../API_DOCUMENTATION.md](../API_DOCUMENTATION.md)

---

## 🏗️ Architecture

### Hexagonal Architecture (Ports & Adapters)

```
backend/
├── cmd/api/                    # Application entry point
│   ├── main.go                 # Server setup, routes, DI
│   └── main_test.go            # Integration tests
│
├── internal/
│   ├── domain/                 # Business entities (pure Go)
│   │   ├── user.go
│   │   ├── role.go
│   │   └── classroom.go
│   │
│   ├── app/                    # Use cases (business logic)
│   │   ├── auth_service.go
│   │   ├── user_service.go
│   │   └── classroom_service.go
│   │
│   ├── ports/                  # Interfaces
│   │   ├── repo.go
│   │   ├── oauth.go
│   │   ├── cache.go
│   │   └── classroom.go
│   │
│   ├── adapters/               # Port implementations
│   │   ├── http/               # Echo handlers
│   │   ├── repo/               # Memory repository
│   │   ├── oauth/              # Google OAuth
│   │   ├── cache/              # Redis cache
│   │   └── google/             # Classroom API
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

**Design Patterns**:
- **Hexagonal Architecture**: Business logic isolated from infrastructure
- **Dependency Injection**: Services composed in main.go
- **Repository Pattern**: Abstract data persistence
- **Strategy Pattern**: Mock/Google classroom providers

---

## 🧪 Testing

### Run All Tests

```bash
# All tests
go test ./...

# With coverage
go test -coverprofile=coverage.out ./...

# View coverage report
go tool cover -html=coverage.out

# Coverage summary
go tool cover -func=coverage.out | grep total
# total: (statements) 94.4%
```

### Run Specific Test Suites

```bash
# Domain tests
go test ./internal/domain/...

# Application tests
go test ./internal/app/...

# Integration tests
go test ./internal/adapters/...

# Specific test
go test ./internal/app -run TestAuthService_Login
```

### Test with Verbose Output

```bash
go test ./... -v
```

### Coverage by Package

```bash
go test ./... -coverprofile=coverage.out
go tool cover -func=coverage.out
```

**Current Coverage** (2025-10-08):
- **Total**: 94.4%
- **Domain**: 97%+
- **Application**: 96%+
- **Adapters**: 92%+
- **Target**: ≥80% (exceeded by +14.4%)

See [TESTING.md](TESTING.md) for detailed testing guide.

---

## 🔧 Configuration

### Environment Variables

#### Required
- `JWT_SECRET` - JWT signing secret (min 32 characters)
- `GOOGLE_CLIENT_ID` - Google OAuth client ID
- `GOOGLE_CLIENT_SECRET` - Google OAuth client secret
- `GOOGLE_REDIRECT_URL` - OAuth callback URL

#### Optional
- `SERVER_PORT` - Server port (default: 8080)
- `APP_ENV` - Environment (development/staging/production)
- `JWT_ISSUER` - JWT issuer (default: classsphere)
- `JWT_EXPIRY_MINUTES` - Token expiry (default: 60)
- `REDIS_ADDR` - Redis address (default: localhost:6379)
- `REDIS_PASSWORD` - Redis password
- `REDIS_DB` - Redis database number (default: 0)
- `CLASSROOM_MODE` - Integration mode (mock/google, default: mock)
- `GOOGLE_CREDENTIALS_FILE` - Google API credentials JSON path

### Config File

See `.env.example` for complete configuration template.

---

## 🔐 Authentication Flow

### JWT Login
```bash
# 1. Login with credentials
curl -X POST http://localhost:8080/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"admin@classsphere.edu","password":"admin123"}'

# Response:
# {
#   "accessToken": "eyJhbGc...",
#   "expiresAt": "2025-10-08T10:00:00Z",
#   "user": {
#     "id": "1",
#     "name": "Admin User",
#     "email": "admin@classsphere.edu",
#     "role": "admin"
#   }
# }

# 2. Use token in protected requests
curl http://localhost:8080/api/v1/users/me \
  -H "Authorization: Bearer eyJhbGc..."
```

### OAuth 2.0 Google Flow
```bash
# 1. Initiate OAuth flow (redirect to Google)
curl http://localhost:8080/api/v1/auth/oauth/google

# 2. User authenticates with Google

# 3. Google redirects to callback
GET /api/v1/auth/oauth/callback?code=...&state=...

# 4. Backend exchanges code for token and returns JWT
```

---

## 🎨 Dual Mode: Mock vs Google

### Mock Mode (Development)
```bash
export CLASSROOM_MODE=mock

# Uses mock data generator
# No Google API credentials needed
# Consistent data for testing
```

### Google Mode (Production)
```bash
export CLASSROOM_MODE=google
export GOOGLE_CREDENTIALS_FILE=/path/to/credentials.json

# Connects to real Google Classroom API
# Requires valid credentials
# Falls back to mock if credentials invalid
```

### Query Mode Parameter
```bash
# Force mock mode
curl http://localhost:8080/api/v1/google/courses?mode=mock

# Force google mode (if available)
curl http://localhost:8080/api/v1/google/courses?mode=google
```

---

## 🛠️ Development Tools

### Makefile Commands

```bash
# Build binary
make build

# Run tests
make test

# Run with coverage
make coverage

# Lint code
make lint

# Format code
make fmt

# Clean build artifacts
make clean
```

### Linting

```bash
# Install golangci-lint
go install github.com/golangci/golangci-lint/cmd/golangci-lint@latest

# Run linter
golangci-lint run ./...

# Auto-fix
golangci-lint run --fix ./...
```

---

## 🐳 Docker

### Build Production Image

```bash
# Build for production
docker build -f .devcontainer/backend/Dockerfile --target production -t classsphere-backend:1.0.0 .

# Run container
docker run -p 8080:8080 \
  -e JWT_SECRET="your-secret" \
  -e GOOGLE_CLIENT_ID="your-id" \
  classsphere-backend:1.0.0
```

### Dev Containers

See [../.devcontainer/README.md](../.devcontainer/README.md) for complete Dev Containers setup.

---

## 📊 Performance

### Metrics
- **Startup Time**: < 2 seconds
- **Memory Usage**: ~55 MB (idle)
- **Request Latency**: < 50ms (p95)
- **Coverage**: 94.4%

### Benchmarks

```bash
# Run benchmarks
go test -bench=. -benchmem ./...

# Specific benchmark
go test -bench=BenchmarkAuthService ./internal/app/...
```

---

## 🔍 Troubleshooting

### Port 8080 Already in Use

```bash
# Find process
lsof -i :8080

# Kill process
kill -9 <PID>

# Or use different port
export SERVER_PORT=8081
```

### Redis Connection Error

```bash
# Check Redis is running
redis-cli ping

# Or disable Redis (uses memory cache)
# Comment out Redis configuration
```

### Tests Failing

```bash
# Clear test cache
go clean -testcache

# Run specific failing test with verbose
go test ./internal/app -v -run TestAuthService_Login

# Check coverage for untested code
go test -coverprofile=coverage.out ./...
go tool cover -func=coverage.out | grep -E "0.0%"
```

---

## 📚 Additional Resources

- **[Architecture Documentation](../ARCHITECTURE.md)** - Detailed design patterns
- **[API Documentation](../API_DOCUMENTATION.md)** - Complete API reference
- **[Testing Strategy](../workspace/ci/06_plan_testing_strategy.md)** - TDD approach
- **[Security Protocols](../workspace/ci/07_plan_security_protocols.md)** - Security best practices

---

**Version**: 1.0  
**Last Updated**: 2025-10-08  
**Test Coverage**: 94.4%

