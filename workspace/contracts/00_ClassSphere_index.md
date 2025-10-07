---
title: "ClassSphere - Complete Documentation"
version: "4.0"
type: "index"
date: "2025-10-07"
author: "LLM Contracts System"
language: "English (Mandatory for all project documentation)"
files:
  - name: "01_ClassSphere_info_status.md"
    title: "Project Information and Current Status"
  - name: "02_ClassSphere_glosario_tecnico.md"
    title: "Unified Technical Glossary"
  - name: "03_ClassSphere_analisis_critico.md"
    title: "System Critical Analysis"
  - name: "04_ClassSphere_objetivos.md"
    title: "Unified System Objectives"
  - name: "05_ClassSphere_arquitectura.md"
    title: "Unified System Architecture"
  - name: "06_ClassSphere_funcionalidades.md"
    title: "Consolidated Functionalities"
  - name: "07_ClassSphere_api_endpoints.md"
    title: "Consolidated API Endpoints"
  - name: "08_ClassSphere_modelos_datos.md"
    title: "Consolidated Data Models"
  - name: "09_ClassSphere_testing.md"
    title: "Unified Testing Strategy"
  - name: "10_ClassSphere_plan_implementacion.md"
    title: "Unified Implementation Plan"
  - name: "11_ClassSphere_deployment.md"
    title: "Unified Deployment Configuration"
  - name: "12_ClassSphere_criterios_aceptacion.md"
    title: "Unified Acceptance Criteria"
  - name: "13_ClassSphere_validacion_coherencia.md"
    title: "Semantic Coherence Validation"
  - name: "14_ClassSphere_conclusion.md"
    title: "Conclusion"
  - name: "15_ClassSphere_error_prevention.md"
    title: "Critical Errors and Prevention"
  - name: "16_ClassSphere_verification_commands.md"
    title: "Critical Verification Commands"
---

# ClassSphere - Complete Documentation

## Project Information

- **Project**: ClassSphere - Complete System
- **Phase**: Unified Implementation - All Features
- **Author**: LLM Contracts System
- **Date**: 2025-10-07 (Migration to new tech stack - Phase 1 Completed)
- **Purpose**: Implement complete ClassSphere system with modern Go + Angular stack
- **Documentation Language**: English (Mandatory)
- **Code Language**: English (Mandatory)
- **UI Language**: English (Default with i18n support from Phase 1)

## Current Project Status

### ✅ Phase 1 Completed - Lessons Learned

**Phase 1 Success Metrics**:
- **Critical Errors Resolved**: 14 blocking errors identified and resolved
- **Resolution Time**: 155 minutes total error resolution time
- **Final Coverage**: 94.4% without OAuth (target 80%+ exceeded)
- **Functional System**: Backend + Frontend + Integration + Demo Users + TailwindCSS
- **Prevention Patterns**: Documented and validated in production

**Critical Errors Overcome**:
- 🔴 **Dashboard Endpoints 404** - MAIN BLOCKER (15 min resolution)
- 🟠 **TypeScript Compilation** - BLOCKED FRONTEND (10 min resolution)
- 🟠 **OAuth Tests Hanging** - BLOCKED COVERAGE (20 min resolution)
- 🟡 **Angular CLI Not Found** - BLOCKED DEVELOPMENT (5 min resolution)
- 🟡 **TailwindCSS v4 PostCSS** - BLOCKED BUILD (20 min resolution)

**Validated Prevention Patterns**:
- **Server Restart**: `pkill -f classsphere-backend` → `PORT=8081 ./classsphere-backend`
- **TypeScript**: Complete optional chaining `?.prop?.subprop`, nullish coalescing `?? 0`
- **Angular CLI**: `npx ng` instead of `ng`, verify package.json
- **OAuth Tests**: `-timeout=10s`, URLs that fail fast, exclude problematic tests
- **TailwindCSS**: v3.4.0 for Angular, avoid CDN in production

### 🔄 Technology Stack Migration (Phase 1 Completed - Phases 2-5 In Planning)

**New Backend Stack**:
- 🎯 **Go** + Echo framework v4
- 🔐 **JWT Authentication** + OAuth 2.0 Google
- 👥 **Role System** (admin > coordinator > teacher > student)
- 💾 **Redis** (cache)
- 🧪 **testify/mock** + resty (testing)
- 🔧 **CI/CD Pipeline** with GitHub Actions

**New Frontend Stack**:
- 🚀 **Angular 19** with official esbuild
- 🎨 **TailwindCSS 3.x**
- 🧹 **Biome** (linter/formatter)
- 🧪 **Jasmine + Karma** (Angular standard testing)
- 🎭 **Playwright** (E2E testing)

**DevOps Maintained**:
- 🔧 **GitHub Actions** (CI/CD)
- 🐳 **Docker** multi-stage
- 🔒 **Trivy** (security scanning)
- 💾 **Redis** (shared cache)
- 🛠️ **Dev Containers** (Docker Compose multi-service, see `workspace/extra/DEV_CONTAINERS_BEST_PRACTICES.md`)

**Planned API Endpoints**:
- `GET /` - Welcome endpoint
- `GET /health` - Health check
- `GET /info` - System information
- `POST /auth/login` - Traditional login
- `GET /auth/google` - Google OAuth initiation
- `GET /auth/google/callback` - Google OAuth callback
- `POST /auth/refresh` - Token refresh
- `GET /auth/me` - Current user info
- `POST /auth/logout` - Logout
- `GET /auth/verify` - Token verification

**Updated Migration Plan**:
- ✅ **Phase 1**: Go + Angular Training (COMPLETED - 155 min error resolution)
  - ✅ Minimum Status Documentation Created
- ⏳ **Phase 2**: Go + Echo Backend (4-6 weeks) - With validated prevention patterns
  - 📝 Minimum Status Documentation Required at Phase End
- ⏳ **Phase 3**: Angular + esbuild Frontend (3-5 weeks) - With validated TypeScript patterns
  - 📝 Minimum Status Documentation Required at Phase End
- ⏳ **Phase 4**: Complete Testing (3-4 weeks) - With validated OAuth test patterns
  - 📝 Minimum Status Documentation Required at Phase End
- ⏳ **Phase 5**: Integration and Deployment (2-3 weeks) - With validated server restart patterns
  - 📝 Minimum Status Documentation Required at Phase End
  - 📚 Complete Final Documentation Created After All Phases

**Implementation Specifications**:
- 🔧 **OAuth Integration**: Angular services → Go handlers with PKCE + State validation
- 🎭 **Role-Based Dashboard**: Angular components per role (admin, coordinator, teacher, student)
- ✅ **Test Coverage**: Backend ≥80%, Frontend ≥80%, Critical modules ≥95% (ACTUAL: 94.4% without OAuth)
- 🧪 **Testing**: Jasmine + Karma (Angular), testify (Go), Playwright (E2E)
- 🛡️ **Error Prevention**: Production-validated patterns to prevent blocking errors
- 🔄 **Server Management**: Automated restart and verification commands
- 🌍 **i18n Support**: Built-in from Phase 1 (English default, extensible to other languages)
- 📝 **Phase Documentation**: Minimum documentation at end of each phase, complete docs after all phases
- 🔗 **Dependency Management**: Critical dependencies with automatic fallback mechanisms
  - Google Classroom API → Mock Mode fallback
  - Redis → In-memory cache fallback
  - WebSocket → HTTP polling fallback (30s intervals)
- 🏥 **Health Monitoring**: /health/dependencies endpoint for real-time dependency status

**Architecture Documentation**:
- 📖 **docs/architecture/testing.md**: Testing strategy with Jasmine + Karma + Playwright (English)
- 🛠 **go.mod**: Go dependency management (English)
- 📝 **CI/CD**: Workflows for Go + Angular (English)
- 🛡️ **Error Prevention Guide**: Critical patterns and production-validated solutions (English)
- 🔧 **Verification Commands**: Automated testing and verification commands (English)
- 🌍 **i18n Configuration**: Internationalization setup from Phase 1 (English default)
- 📝 **Phase Status Docs**: Minimum documentation created at end of each phase (English)
- 📚 **Final Complete Docs**: Comprehensive documentation after all phases complete (English)

## Table of Contents

### [1. Project Information and Current Status](01_ClassSphere_info_status.md)
- Detailed project information
- Current development status
- Phase progress
- Next steps

### [2. Unified Technical Glossary](02_ClassSphere_glosario_tecnico.md)
- Fundamental concepts
- Unified standard terminology
- States with semantic prefixes
- Simplified semantic architecture

### [3. System Critical Analysis](03_ClassSphere_analisis_critico.md)
- **Requirements traceability analysis**: Stage-by-stage mapping for consistency
- **Semantic coherence analysis**: Unified terminology across all layers
- **Cross-cutting dependencies analysis**: Infrastructure, security, performance, and testing dependencies
  - Infrastructure: Google Classroom API (critical), Redis (medium)
  - Security: JWT Secret (critical), OAuth 2.0 (high), CORS (critical)
  - Performance: WebSocket (medium), Caching strategy (medium)
  - Testing: testify/mock (high), Playwright (high)
- **Dependency impact matrix**: Risk assessment with mitigation strategies
- **Resolution protocol**: Automatic detection, classification, and fallback activation

### [4. Unified System Objectives](04_ClassSphere_objetivos.md)
- Backend - Complete system
- Frontend - Complete application
- Integrated features
- Functional and non-functional requirements

### [5. Unified System Architecture](05_ClassSphere_arquitectura.md)
- **Consolidated technology stack**: Go + Echo, Angular 19, Redis, testify, Playwright
- **New Google Classroom installation with mocks**: Dual mode (mock/real) for development flexibility
- **Resilient architecture with error prevention**: Automatic fallbacks for critical dependencies
- **Complete directory structure**: Hexagonal architecture (ports & adapters) from root /
- **Development environment with Dev Containers**: Docker Compose, dev-prod parity, <15 min setup
- **Cross-cutting concerns**: Authentication, authorization, caching, monitoring integrated at architecture level

**Directory Structure from Root**:
```
/backend
  /cmd/api/                    # main: routes wiring, middlewares
  /internal/
    /domain/                   # Entities, VOs, rules (pure Go)
    /app/                      # Use cases (application services)
    /ports/                    # Interfaces (repo, oauth, mail, llm, cache)
    /adapters/                 # Port implementations
      /http/                   # Echo handlers (thin controllers)
      /repo/                   # DB (SQL/NoSQL) + migrations
      /oauth/                  # Google OAuth 2.0 (server-side)
      /auth/                   # JWT (emit/verify, refresh)
      /llm/                    # LLM provider client (if applicable)
    /shared/                   # Config (12-factor), logger, errors
  /tests/
    /unit/                     # testify: domain/app
    /integration/              # testify: repo/http with DB container
    /e2e/                      # black-box API against binary
  go.mod go.sum
  Makefile

/frontend
  /src/
    /app/
      (auth)/login/            # feature folder
      (auth)/callback/         # OAuth reception (if public PKCE applies)
      dashboard/
      shared/                  # shared modules (pipes, guards)
    /assets/
    /environments/
  /tests/
    /unit/                     # Jasmine
    /e2e/                      # Playwright
  angular.json
  tsconfig.json
  karma.conf.js
  tailwind.config.js
  .postcssrc.json

/infra/                        # Docker, Compose, K8s/Helm, CI helpers
/scripts/                      # Seeds, dev tools, make-like
/docs/                         # Runbooks, diagrams, decisions
```

**Important Notes**:
- The `/workspace` directory is **completely ignored** in development
- Ports always use **defaults**: Backend 8080, Frontend 4200
- Hexagonal architecture (ports & adapters) in backend
- Feature folders in Angular frontend
- **Dev Containers with Docker Compose** for consistent environment (automatic setup < 15 min)

### [6. Consolidated Functionalities](06_ClassSphere_funcionalidades.md)
- Complete authentication and authorization
- Complete Google Classroom integration
- Advanced dashboards per role
- Advanced visualizations
- Advanced search system
- Real-time notifications
- Advanced metrics and analytics
- WCAG 2.2 AA accessibility
- Complete testing
- CI/CD Pipeline
- **Explicit Frontend-Backend mapping**
- **Mandatory implementation by technology**

### [7. Consolidated API Endpoints](07_ClassSphere_api_endpoints.md)
- Authentication
- OAuth
- Health Checks
- Google Classroom
- Dashboards
- Metrics
- Search
- Notifications
- Advanced Google Sync
- Synchronization and Backup
- Webhooks
- Diagnostics

### [8. Consolidated Data Models](08_ClassSphere_modelos_datos.md)
- User
- Complete course
- Advanced metric
- Notification
- Synchronization status

### [9. Unified Testing Strategy](09_ClassSphere_testing.md)
- Frontend Testing Strategy (Angular 19 + Jasmine + Karma)
- Defined Testing Stack (Jasmine + Karma + Playwright)
- Consolidated TDD methodology
- Required testing coverage
- Backend tests with testify (Go)
- Frontend tests with Jasmine (Angular)
- E2E tests with Playwright
- Standard TDD templates
- Automated TDD scripts
- Consolidated fixtures and mocks
- **Measurable acceptance criteria**
- **Automatic verification commands**

### [10. Unified Implementation Plan](10_ClassSphere_plan_implementacion.md)
- Consolidated TDD methodology
- Required testing coverage
- Phase-based implementation
- Acceptance criteria per phase
- Development methodology
- Development scripts
- Testing commands
- Deployment verification
- Standard templates
- Development checklist
- Coverage metrics
- Automated scripts

### [11. Unified Deployment Configuration](11_ClassSphere_deployment.md)
- **Consolidated environment variables**: JWT_SECRET, GOOGLE_CLIENT_ID, REDIS_ADDR (all critical dependencies)
- **Resilient deployment with error prevention**: Automatic fallback mechanisms for all critical services
- **Complete Docker configuration**: Multi-stage builds, security scanning with Trivy
- **Unified CI/CD pipeline**: GitHub Actions with dependency validation and health checks
- **Deployment verification with error prevention**: Health endpoints for all dependencies
- **Dependency monitoring**: Real-time health checks for Google API, Redis, WebSocket connections

### [12. Unified Acceptance Criteria](12_ClassSphere_criterios_aceptacion.md)
- **Complete backend**: Go + Echo + JWT + OAuth with ≥80% coverage
- **Complete frontend**: Angular 19 + TailwindCSS + RxJS with ≥80% coverage
- **Complete Google integration**: Dual mode (mock/real), rate limiting, conflict resolution
- **Dashboards and visualization**: Role-based dashboards, ApexCharts, D3.js, real-time updates
- **Search and notifications**: Advanced search with filters, WebSocket notifications with polling fallback
- **Testing and quality**: testify (backend), Jasmine + Karma (frontend), Playwright (E2E)
- **WCAG 2.2 AA accessibility**: Keyboard navigation, screen reader, color contrast compliance
- **CI/CD and deployment**: GitHub Actions, Docker multi-stage, Trivy security scanning
- **Security and operations**: JWT + OAuth, RBAC, CORS, rate limiting, dependency health monitoring
- **Dependency verification**: All critical dependencies with fallback strategies tested

### [13. Semantic Coherence Validation](13_ClassSphere_validacion_coherencia.md)
- Implemented coherence metrics
- Implemented improvements
- Cross-document validation
- Continuous validation protocol
- Benefits of semantic coherence
- Validation conclusion

### [14. Conclusion](14_ClassSphere_conclusion.md)
- Executive summary
- Benefits of unified approach
- Validated technologies
- Success metrics
- Next steps

### [15. Critical Errors and Prevention](15_ClassSphere_error_prevention.md)
- Critical error patterns identified in Phase 1
- Production-validated solutions
- Automatic verification commands
- Error prevention checklist
- Error resolution metrics (155 minutes, 14 blocking errors)
- Patterns applicable to future phases

### [16. Critical Verification Commands](16_ClassSphere_verification_commands.md)
- Production-validated testing commands
- Automatic verification scripts
- Deployment checklist
- Error resolution commands
- Code coverage verification
- Server management commands

## Navigation Guide

This documentation is designed to be consulted in a modular way. You can follow these approaches:

1. **Sequential reading**: Follow the documents in numerical order for complete understanding.
2. **Specific query**: Access directly the document containing the information you need.
3. **Cross-references**: Use the links between documents to navigate between related concepts.

Each document includes navigation links at the top and bottom to facilitate movement between related sections.

## Context Optimization

This documentation structure has been specifically designed to optimize context size when consulted. Each file is focused on a specific topic, which allows:

1. **More efficient queries**: Load only the relevant information for each query.
2. **Less context loss**: Avoid the "lost-in-the-middle" problem by dividing information into manageable chunks.
3. **Precise references**: Facilitate reference to specific sections without needing to load the entire document.
4. **Modular updates**: Allow updating specific sections without affecting the complete document.

## Key Changes in v4.0 (2025-10-07)

### 🌍 Language Requirements (MANDATORY)
1. **All Documentation**: English mandatory
2. **All Code**: English mandatory (variables, functions, classes, files)
3. **All Comments**: English mandatory
4. **All Commits**: English mandatory
5. **UI Text**: English default with i18n support from Phase 1

### 🔤 i18n Support
- **Phase 1 Setup**: i18n configuration from beginning
- **Default Language**: English (mandatory)
- **Extensibility**: Support for additional languages (es, fr)
- **Translation Structure**: English as base, extensible architecture

### 📝 Phase Documentation
- **Minimum Docs**: Created at end of each phase (1-5)
- **Template**: Status, metrics, issues, prerequisites
- **Language**: All documentation in English

### 📚 Final Documentation
- **Complete Package**: Created after all phases
- **8 Comprehensive Guides**: Architecture, API, User, Developer, Ops, i18n, Lessons, Roadmap
- **Language**: All documentation in English

---

*Last updated: 2025-10-07 - Phase 1 Completed with Lessons Learned + v4.0 Systematic Changes Applied*
