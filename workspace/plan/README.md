# ClassSphere Development Plan

**Version**: 1.0  
**Date**: 2025-10-07  
**Status**: Ready for Execution  
**Duration**: 45 days (15-20 weeks)

## 🚀 Quick Start for LLMs

This development plan is designed for execution by Large Language Models with strict Test-Driven Development (TDD) methodology and context-aware structure.

### Step 1: Read Main Index
```bash
cat workspace/plan/01_plan_index.md
```

This provides:
- Critical objectives and blocking dependencies
- Phase summaries (4 phases, 45 days)
- Security protocols
- Testing strategy
- Evaluation metrics

### Step 2: Start Phase 1
```bash
cat workspace/plan/02_plan_fase1_fundaciones.md
```

Begin with Day 1: Backend Go setup

### Step 3: Follow Daily Instructions

Each phase file contains:
- **🎯 INICIO**: Critical objectives (beginning)
- **📅 MEDIO**: Day-by-day implementation (middle)
- **✅ FINAL**: Verification checklist (end)

This structure prevents "lost-in-the-middle" context issues.

## 📚 Plan Structure

```
workspace/plan/
├── 01_plan_index.md                      # Main index (CRITICAL, 2000 tokens)
├── 02_plan_fase1_fundaciones.md          # Phase 1: Foundations (CRITICAL, 2000 tokens)
├── 03_plan_fase2_google_integration.md   # Phase 2: Google (HIGH, 1500 tokens)
├── 04_plan_fase3_visualizacion.md        # Phase 3: Visualization (MEDIUM, 1000 tokens)
├── 05_plan_fase4_integracion.md          # Phase 4: Integration (LOW, 800 tokens)
├── 06_plan_testing_strategy.md           # Testing strategy
├── 07_plan_security_protocols.md         # Security protocols
├── 08_plan_context_management.md         # Context management for LLMs
├── 09_plan_evaluation_metrics.md         # Evaluation metrics
└── README.md                             # This file
```

## 🎯 Technology Stack

### Backend (Go 1.21+)
- **Framework**: Echo v4
- **Authentication**: JWT + OAuth 2.0 Google
- **Cache**: Redis
- **Testing**: testify + httptest
- **Port**: 8080 (mandatory, never alternate)

### Frontend (Angular 19)
- **Bundler**: esbuild (official)
- **Language**: TypeScript 5.x
- **Styling**: TailwindCSS 3.x
- **State**: RxJS observables
- **Testing**: Jasmine + Karma + Playwright
- **Port**: 4200 (mandatory, never alternate)

### DevOps
- **CI/CD**: GitHub Actions
- **Containers**: Docker multi-stage
- **Security**: Trivy scanning

## 📊 Development Phases

### Phase 1: Fundaciones (12 days) - CRITICAL
**File**: `02_plan_fase1_fundaciones.md`

- Backend: Go + Echo + JWT + OAuth 2.0
- Frontend: Angular 19 + Auth UI
- Testing: testify + Jasmine
- Ports: 8080 (backend), 4200 (frontend)
- Coverage: ≥80% global, ≥90% critical

### Phase 2: Google Integration (10 days) - HIGH
**File**: `03_plan_fase2_google_integration.md`

- Google Classroom API
- Dual mode (Google/Mock)
- Role-based dashboards (4 types)
- ApexCharts integration
- Coverage maintained: ≥80%

### Phase 3: Visualización (10 days) - MEDIUM
**File**: `04_plan_fase3_visualizacion.md`

- Advanced search (multi-entity)
- Real-time notifications (WebSocket)
- Interactive charts (ApexCharts + D3.js)
- Notification center
- Coverage maintained: ≥80%

### Phase 4: Integración (13 days) - LOW
**File**: `05_plan_fase4_integracion.md`

- Bidirectional Google sync
- WCAG 2.2 AA accessibility
- CI/CD pipeline complete
- Docker optimization
- Coverage: ≥90% critical, ≥80% global

## 🧪 Testing Requirements

### Coverage Thresholds
- **Global**: ≥80% lines, ≥65% branches
- **Critical Modules**: ≥90% lines, ≥80% branches
- **Security Components**: ≥95% lines, ≥85% branches

### Testing Stack
- **Backend**: testify + httptest
- **Frontend**: Jasmine + Karma + Angular Testing Library
- **E2E**: Playwright
- **Coverage**: go test -cover + karma-coverage

### TDD Methodology (Strict)
1. **Red**: Write failing test
2. **Green**: Implement minimum code to pass
3. **Refactor**: Improve code keeping tests green
4. **Repeat**: For every feature

## 🔒 Security Protocols

### Zero Trust Principle
- SAST with Trivy
- SCA for dependencies
- Secrets detection
- JWT validation
- OAuth 2.0 PKCE + State

### Security Checklist
- All endpoints authenticated
- Role-based authorization
- Rate limiting enabled
- CORS configured
- No secrets in code

## 📈 Context Management for LLMs

### Chunking by Priority
```yaml
CRITICAL: max 2000 tokens (auth, config, main)
HIGH: max 1500 tokens (services, integrations)
MEDIUM: max 1000 tokens (components, charts)
LOW: max 800 tokens (admin, accessibility)
```

### Anti Lost-in-the-Middle Structure
Every plan file uses:
- **🎯 INICIO**: Critical info (beginning)
- **📅 MEDIO**: Implementation details (middle)
- **✅ FINAL**: Verification (end)

This structure ensures critical information appears at start and end, where LLMs have strongest attention.

## 🎓 Validation Commands

### Backend
```bash
# Install dependencies
go mod tidy

# Run tests
go test ./... -v -cover

# Check coverage (must be ≥80%)
go test ./... -coverprofile=coverage.out
go tool cover -html=coverage.out

# Run server (port 8080 mandatory)
go run cmd/api/main.go

# Health check
curl http://localhost:8080/health
```

### Frontend
```bash
# Install dependencies
npm install

# Run tests
ng test

# Check coverage (must be ≥80%)
ng test --code-coverage

# Run development server (port 4200 mandatory)
ng serve --port 4200

# Build production
ng build --configuration production
```

### Integration
```bash
# Start backend (terminal 1)
cd backend && go run cmd/api/main.go

# Start frontend (terminal 2)
cd frontend && ng serve --port 4200

# Run E2E tests (terminal 3)
cd frontend && npx playwright test

# Open browser
open http://localhost:4200
```

## 📝 Key Principles

### 1. Port Standards (Mandatory)
- Backend: **8080** (never alternate)
- Frontend: **4200** (never alternate)
- Redis: 6379 (default)

### 2. Hexagonal Architecture (Backend)
```
domain → app → ports → adapters
  ↓
Pure business logic → Use cases → Interfaces → Implementations
```

### 3. TDD Strict Enforcement
- No production code without failing test first
- Tests must be readable and maintainable
- Coverage thresholds enforced in CI/CD

### 4. Context-Aware Development
- Prioritize critical components
- Use anti lost-in-middle structure
- Track token counts
- Enable context recovery

## 🚦 Success Indicators

### Phase Completion Criteria
- [ ] All tests passing (100%)
- [ ] Coverage thresholds met
- [ ] All acceptance criteria verified
- [ ] Documentation updated
- [ ] No critical security issues

### Project Completion Criteria
- [ ] All 4 phases complete (45 days)
- [ ] System deployed to production
- [ ] WCAG 2.2 AA compliant
- [ ] Zero critical vulnerabilities
- [ ] Full documentation generated

## 📖 How to Use This Plan

### For LLMs
1. Read `01_plan_index.md` for overview
2. Start with `02_plan_fase1_fundaciones.md`
3. Follow day-by-day instructions
4. Run validation commands after each day
5. Move to next phase when criteria met

### For Developers
1. Clone repository
2. Read this README
3. Install prerequisites (Go 1.21+, Node.js 18+, Redis)
4. Follow phase files sequentially
5. Maintain test coverage ≥80%

### For Project Managers
1. Review `01_plan_index.md` for milestones
2. Track progress via phase completion
3. Monitor test coverage metrics
4. Verify acceptance criteria
5. Review security scan results

## 🛠️ Prerequisites

### Required Software
- Go 1.21 or higher
- Node.js 18 or higher
- Redis (latest stable)
- Docker (latest stable)
- Git

### Optional Tools
- tmux (for terminal management)
- make (for build automation)
- Postman (for API testing)

### Environment Setup
```bash
# Verify Go installation
go version  # Must be 1.21+

# Verify Node.js installation
node --version  # Must be 18+

# Verify Redis
redis-server --version

# Verify Docker
docker --version
```

## 📞 Support

### Documentation References
- **Testing Strategy**: `06_plan_testing_strategy.md`
- **Security Protocols**: `07_plan_security_protocols.md`
- **Context Management**: `08_plan_context_management.md`
- **Evaluation Metrics**: `09_plan_evaluation_metrics.md`

### Common Issues
- **Port conflicts**: Use cleanup scripts in plan files
- **Test failures**: Check coverage thresholds
- **Redis connection**: Ensure Redis server running
- **OAuth errors**: Verify Google credentials

## 🎯 Next Steps

1. **Read Main Index**: `cat workspace/plan/01_plan_index.md`
2. **Review Phase 1**: `cat workspace/plan/02_plan_fase1_fundaciones.md`
3. **Setup Environment**: Install prerequisites
4. **Start Day 1**: Backend Go setup
5. **Follow TDD**: Write tests first, always

---

**Project**: ClassSphere  
**Architecture**: Hexagonal (Backend) + Feature-based (Frontend)  
**Methodology**: TDD-RunFix+ with Context-Aware Development  
**Target**: Production-ready educational management system

*This plan is optimized for LLM execution with strict testing requirements and context management.*

**Last updated**: 2025-10-07  
**Version**: 1.0  
**Status**: ✅ Ready for Execution
