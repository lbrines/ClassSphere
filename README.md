# ClassSphere

**Educational Dashboard Platform with Google Classroom Integration**

![Status](https://img.shields.io/badge/status-Phase%203%20Partial-yellow)
![Coverage](https://img.shields.io/badge/coverage-94.4%25-brightgreen)
![Go](https://img.shields.io/badge/Go-1.24.7-00ADD8?logo=go)
![Angular](https://img.shields.io/badge/Angular-19-DD0031?logo=angular)

---

## 🎯 Overview

ClassSphere is a comprehensive educational platform that integrates with Google Classroom to provide role-based dashboards, real-time analytics, and advanced search capabilities for administrators, coordinators, teachers, and students.

### Key Features

- ✅ **Multi-Role Dashboards**: Customized views for Admin, Coordinator, Teacher, and Student
- ✅ **Google Classroom Integration**: Dual mode (Mock/Real) for development and production
- ✅ **Real-Time Search**: Advanced search across students, courses, and assignments
- ✅ **Notifications System**: Real-time notifications with WebSocket support
- ✅ **OAuth 2.0**: Secure Google authentication with PKCE and State
- ✅ **Role-Based Access Control**: Fine-grained permissions system
- ✅ **Analytics & Charts**: ApexCharts integration for data visualization

---

## 🚀 Quick Start

### Option 1: Dev Containers (Recommended)

**Requirements**: Docker Desktop + VS Code

```bash
# 1. Clone repository
git clone <repo-url>
cd ClassSphere

# 2. Open in VS Code
code .

# 3. Reopen in Dev Container
# F1 → "Dev Containers: Reopen in Container"
# Wait ~3-5 minutes for setup

# 4. Services start automatically
# Backend: http://localhost:8080
# Frontend: http://localhost:4200
```

**Documentation**: See [.devcontainer/README.md](.devcontainer/README.md)

---

### Option 2: Manual Setup

#### Prerequisites
- Go 1.24.7+
- Node.js 20+
- Redis (optional, falls back to memory cache)

#### Backend Setup
```bash
cd backend

# Install dependencies
go mod download

# Set environment variables
export JWT_SECRET="development-secret-key-change-in-production-123456789"
export GOOGLE_CLIENT_ID="your-client-id"
export GOOGLE_CLIENT_SECRET="your-client-secret"
export GOOGLE_REDIRECT_URL="http://localhost:4200/auth/callback"
export CLASSROOM_MODE="mock"  # or "google"

# Run server
go run cmd/api/main.go
# Server running on http://localhost:8080
```

#### Frontend Setup
```bash
cd frontend

# Install dependencies
npm ci

# Run dev server
npm start
# Server running on http://localhost:4200
```

---

## 📚 Documentation

### For Developers
- **[Backend README](backend/README.md)** - Backend setup, API overview, testing
- **[Frontend README](frontend/README.md)** - Frontend setup, components, testing
- **[API Documentation](API_DOCUMENTATION.md)** - Complete API reference
- **[Architecture](ARCHITECTURE.md)** - System design and patterns
- **[Dev Containers](.devcontainer/README.md)** - Containerized development environment

### For Operations
- **[Deployment Guide](DEPLOYMENT.md)** - Docker, environment variables, production
- **[Security](SECURITY.md)** - OAuth, JWT, secrets management

### For Contributors
- **[Contributing Guide](CONTRIBUTING.md)** - How to contribute, coding standards
- **[Testing Strategy](workspace/ci/06_plan_testing_strategy.md)** - TDD approach

---

## 🛠️ Technology Stack

### Backend
- **Language**: Go 1.24.7
- **Framework**: Echo v4
- **Authentication**: JWT + OAuth 2.0 Google (PKCE + State)
- **Testing**: testify/mock + httptest
- **Cache**: Redis
- **Port**: 8080
- **Architecture**: Hexagonal (Ports & Adapters)

### Frontend
- **Framework**: Angular 19
- **Bundler**: esbuild
- **Styling**: TailwindCSS 3.x
- **Testing**: Jasmine + Karma + Playwright
- **Charts**: ApexCharts
- **Port**: 4200
- **Architecture**: Feature Folders

### DevOps
- **Containers**: Docker multi-service (Dev Containers)
- **CI/CD**: GitHub Actions
- **Security**: Trivy (SAST, SCA)
- **Linting**: golangci-lint (Go), Biome (TypeScript)

---

## 🧪 Testing

### Backend (94.4% coverage)
```bash
cd backend

# Run all tests
go test ./...

# With coverage
go test -coverprofile=coverage.out ./...
go tool cover -html=coverage.out

# Target: ≥80% (Actual: 94.4% ✅)
```

### Frontend
```bash
cd frontend

# Unit tests (Jasmine + Karma)
npm test

# E2E tests (Playwright)
npx playwright test

# With coverage
npm test -- --code-coverage
```

---

## 🔐 Environment Variables

### Required (Backend)
```bash
JWT_SECRET=<min-32-characters>
GOOGLE_CLIENT_ID=<your-client-id>.apps.googleusercontent.com
GOOGLE_CLIENT_SECRET=GOCSPX-<your-secret>
GOOGLE_REDIRECT_URL=http://localhost:4200/auth/callback
```

### Optional
```bash
SERVER_PORT=8080
REDIS_ADDR=localhost:6379
CLASSROOM_MODE=mock  # or "google"
GOOGLE_CREDENTIALS_FILE=/path/to/credentials.json
```

See [.env.example](backend/.env.example) for complete list.

---

## 📖 API Overview

**Base URL**: `http://localhost:8080/api/v1`

### Public Endpoints
- `GET /health` - Health check
- `POST /auth/login` - Email/password login
- `GET /auth/oauth/google` - Initiate Google OAuth
- `GET /auth/oauth/callback` - OAuth callback

### Protected Endpoints (JWT Required)
- `GET /users/me` - Current user profile
- `GET /google/courses` - List Google Classroom courses
- `GET /dashboard/{role}` - Role-specific dashboard (admin, coordinator, teacher, student)

**Full Documentation**: See [API_DOCUMENTATION.md](API_DOCUMENTATION.md)

---

## 🏗️ Project Structure

```
ClassSphere/
├── backend/              # Go 1.24.7 + Echo v4
│   ├── cmd/api/          # Main application entry
│   ├── internal/         # Business logic (hexagonal)
│   │   ├── domain/       # Entities
│   │   ├── app/          # Use cases
│   │   ├── ports/        # Interfaces
│   │   └── adapters/     # Implementations
│   └── tests/            # Unit + integration tests
│
├── frontend/             # Angular 19
│   └── src/app/
│       ├── features/     # Business features
│       ├── core/         # Services, guards, models
│       └── shared/       # Reusable components
│
├── .devcontainer/        # Dev Containers (4 services)
│   ├── docker-compose.yml
│   └── */Dockerfile
│
└── workspace/            # Documentation & planning
    ├── contracts/        # Specifications (12 docs)
    ├── ci/               # Development plans (10 docs)
    └── extra/            # Best practices guides
```

---

## 🎓 Demo Users

| Role | Email | Password |
|------|-------|----------|
| Admin | `admin@classsphere.edu` | `admin123` |
| Coordinator | `coordinator@classsphere.edu` | `coord123` |
| Teacher | `teacher@classsphere.edu` | `teach123` |
| Student | `student@classsphere.edu` | `stud123` |

**Note**: These are bcrypt-hashed in the database.

---

## 🔄 Development Workflow

### Using Dev Containers
```bash
# All services start automatically
# Backend: http://localhost:8080
# Frontend: http://localhost:4200
# Redis: localhost:6379

# Run backend tests
cd /workspace/backend && go test ./...

# Run frontend tests
cd /workspace/frontend && npm test
```

### Manual Development
```bash
# Terminal 1: Backend
cd backend && go run cmd/api/main.go

# Terminal 2: Frontend
cd frontend && npm start

# Terminal 3: Tests
cd backend && go test ./... -v
```

---

## 📊 Project Status

### Phase 1: Foundations ✅ COMPLETED
- Backend: Go 1.24.7 + Echo v4
- Frontend: Angular 19 + TailwindCSS
- Authentication: JWT + OAuth 2.0
- Testing: 94.4% coverage

### Phase 2: Google Integration ✅ COMPLETED
- Google Classroom API integration
- Dual mode (Mock/Real)
- Role-based dashboards
- Dashboard endpoints for 4 roles

### Phase 3: Advanced Features 🟡 PARTIAL
- ✅ Advanced search (students, courses, assignments)
- ✅ Notifications system
- ✅ ApexCharts integration
- ⏳ WebSocket real-time (polling fallback implemented)

### Phase 4: Production & Integration ⏳ PENDING
- Production deployment
- Monitoring & alerting
- Performance optimization
- Final E2E validation

---

## 🤝 Contributing

We welcome contributions! Please read [CONTRIBUTING.md](CONTRIBUTING.md) for details on:
- Code of conduct
- Development process
- Coding standards
- Pull request process

---

## 📄 License

[License information here]

---

## 🆘 Support

### Documentation
- Dev Containers: `.devcontainer/README.md`
- Troubleshooting: `.devcontainer/TROUBLESHOOTING.md`
- Testing Guide: `.devcontainer/TESTING_GUIDE.md`

### Commands
```bash
# Health check (Dev Containers)
bash .devcontainer/scripts/verify-health.sh

# View logs
docker-compose -f .devcontainer/docker-compose.yml logs -f

# Restart services
docker-compose -f .devcontainer/docker-compose.yml restart
```

---

**Version**: 1.0  
**Last Updated**: 2025-10-08  
**Maintained by**: ClassSphere Development Team

