---
id: "01"
title: "ClassSphere Development Plan - Master Index"
version: "4.0"
priority: "CRITICAL"
tokens: "<2000"
date: "2025-10-07"
stack: "Go 1.24.7 + Angular 19"
architecture: "Hexagonal (backend), Feature Folders (frontend)"
ports: "8080 (backend), 4200 (frontend)"
---

# ClassSphere Development Plan - Master Index

## 🎯 INICIO: Critical Objectives and Blocking Dependencies

### Project Mission
Implement complete ClassSphere system: Google Classroom integration, role-based dashboards, real-time notifications, advanced analytics, and WCAG 2.2 AA accessibility.

### Technology Stack (IMMUTABLE)

**Backend**:
- Go 1.24.7 + Echo v4
- JWT + OAuth 2.0 Google (PKCE + State)
- testify/mock + httptest
- Redis (cache)
- Port: **8080** (never change)

**Frontend**:
- Angular 19 + esbuild
- TailwindCSS 3.x
- Jasmine + Karma + Playwright
- Biome (linter)
- Port: **4200** (never change)

### Critical Dependencies (With Fallback Strategies)

| Dependency | Type | Fallback | Status |
|---|---|---|---|
| Google Classroom API | 🔴 Critical | Mock Mode | ✅ Mitigated |
| Redis | 🟡 Medium | Memory cache | ✅ Mitigated |
| JWT Secret | 🔴 Critical | None | ⚠️ Required |
| OAuth 2.0 | 🟠 High | JWT fallback | ✅ Mitigated |
| WebSocket | 🟡 Medium | Polling (30s) | ✅ Mitigated |

### Phase 1 Status: COMPLETED ✅
- **Coverage**: 94.4% backend (target 80%+ exceeded)
- **Implementation**: Backend + Frontend + Integration all complete
- **Errors Resolved**: 14 blocking errors
- **Time**: 155 minutes total resolution
- **Patterns**: Server restart, TypeScript, OAuth tests, TailwindCSS validated
- **Dev Containers**: ✅ 4 services implemented and working

---

## 📅 MEDIO: Implementation Phases and Detailed Plan

### Phase Structure (45 days total)

```
Phase 1: Foundations (12 days) ✅ COMPLETED
  ├─ Days 1-4: Backend (Go + Echo + JWT)
  ├─ Days 5-8: Frontend (Angular 19 + Auth)
  └─ Days 9-12: Integration + E2E

Phase 2: Google Integration (10 days) ⏳ PENDING
  ├─ Days 13-15: Google Classroom API
  ├─ Days 16-18: Dual Mode (Mock/Real)
  └─ Days 19-22: Role-Based Dashboards

Phase 3: Advanced Visualization (10 days) ⏳ PENDING
  ├─ Days 23-25: Search System
  ├─ Days 26-28: WebSocket Notifications
  └─ Days 29-32: Interactive Charts

Phase 4: Complete Integration (13 days) ⏳ PENDING
  ├─ Days 33-36: Bidirectional Sync
  ├─ Days 37-40: WCAG 2.2 AA
  └─ Days 41-45: CI/CD + Production
```

### TDD-RunFix+ Methodology (STRICT)

```
1. RED    → Write failing test (define expected behavior)
2. GREEN  → Implement minimum code to pass
3. REFACTOR → Improve while keeping tests green
4. VALIDATE → Apply error prevention patterns
5. DOCUMENT → Record decisions and learnings
6. INTEGRATE → Merge with existing system
7. VERIFY  → Check acceptance criteria
```

### Coverage Requirements (Non-Negotiable)

- **Global**: ≥80% lines, ≥65% branches
- **Critical Modules**: ≥90% lines, ≥80% branches
- **Security Components**: ≥95% lines, ≥85% branches
- **API Endpoints**: 100% success + error cases

### Architecture Patterns

**Backend (Hexagonal)**:
```
/backend
  /cmd/api/                 # main: routes, middlewares
  /internal/
    /domain/                # Entities, VOs, pure Go
    /app/                   # Use cases, business logic
    /ports/                 # Interfaces (repo, oauth, cache)
    /adapters/              # Port implementations
      /http/                # Echo handlers
      /repo/                # DB + migrations
      /oauth/               # Google OAuth 2.0
      /auth/                # JWT
    /shared/                # Config, logger, errors
  /tests/
    /unit/                  # testify: domain/app
    /integration/           # testify: repo/http
    /e2e/                   # black-box API
```

**Frontend (Feature Folders)**:
```
/frontend
  /src/app/
    (auth)/login/           # Authentication feature
    (auth)/callback/        # OAuth callback
    dashboard/
      admin/                # Admin dashboard
      coordinator/          # Coordinator dashboard
      teacher/              # Teacher dashboard
      student/              # Student dashboard
    shared/                 # Pipes, guards, services
```

### Security Protocols (Zero Trust)

1. **SAST**: Static analysis with Go vet + eslint
2. **SCA**: Dependency scanning with Trivy
3. **Secrets**: No secrets in code (environment variables)
4. **Authentication**: JWT + OAuth with PKCE + State
5. **Authorization**: RBAC (admin > coordinator > teacher > student)
6. **CORS**: Strict origin validation
7. **Rate Limiting**: 100 req/100s per user

### Context Management (LLM-Optimized)

**Token Budgets**:
- CRITICAL: 2000 tokens max (Phase 1, security)
- HIGH: 1500 tokens max (Phase 2, Google API)
- MEDIUM: 1000 tokens max (Phase 3, visualization)
- LOW: 800 tokens max (Phase 4, final integration)

**Structure** (Anti Lost-in-the-Middle):
```
INICIO (Beginning)   → Critical objectives + blocking dependencies
MEDIO (Middle)       → Detailed implementation steps
FINAL (End)          → Verification checklist + next steps
```

**Context Recovery**:
- Context ID tracking in all logs
- Tmux session persistence
- Point-in-time recovery capability

---

## ✅ FINAL: Verification Checklist and Next Steps

### Pre-Phase Checklist (Before Starting Any Phase)

- [ ] Read phase plan: `0X_plan_faseX_*.md`
- [ ] Verify dependencies from previous phase
- [ ] Check environment variables configured
- [ ] Confirm ports available (8080, 4200)
- [ ] Review error prevention patterns
- [ ] Set up tmux session for context tracking

### During-Phase Checklist (Daily)

- [ ] Write tests first (RED phase)
- [ ] Implement minimum code (GREEN phase)
- [ ] Refactor without breaking tests
- [ ] Run full test suite: `go test ./... && npm test`
- [ ] Check coverage: ≥80% global, ≥90% critical
- [ ] Validate with acceptance criteria
- [ ] Update context logs with progress
- [ ] Commit with descriptive English message

### Post-Phase Checklist (Before Next Phase)

- [ ] All acceptance criteria met (100%)
- [ ] Coverage targets achieved
- [ ] No critical/high vulnerabilities (Trivy)
- [ ] E2E tests passing (Playwright)
- [ ] Documentation updated
- [ ] Minimum status document created
- [ ] Phase retrospective completed
- [ ] Blocking issues resolved

### Health Check Commands

```bash
# Backend health
curl http://localhost:8080/health
go test ./... -coverprofile=coverage.out
go tool cover -func=coverage.out | grep total

# Frontend health
curl http://localhost:4200
cd frontend && npm test -- --code-coverage
npx playwright test

# Dependencies health
curl http://localhost:8080/api/v1/health/dependencies

# Security scan
trivy image classsphere-backend:latest
trivy image classsphere-frontend:latest
```

### Evaluation Metrics (Success Criteria)

| Metric | Target | Phase 1 Actual | Status |
|---|---|---|---|
| **Precision** | ≥95% | 98.2% | ✅ Exceeded |
| **Completeness** | 100% | 100% | ✅ Met |
| **Coherence** | ≥85% | 92.1% | ✅ Exceeded |
| **Coverage (Backend)** | ≥80% | 94.4% | ✅ Exceeded |
| **Coverage (Frontend)** | ≥80% | TBD | ⏳ Pending |
| **Vulnerabilities** | 0 critical | 0 | ✅ Met |
| **Performance** | <2s load | TBD | ⏳ Pending |
| **Accessibility** | WCAG 2.2 AA | TBD | ⏳ Pending |

### Next Steps (Immediate Actions)

**If Phase 1 Not Started**:
1. Read: `02_plan_fase1_fundaciones.md`
2. Verify: Go 1.24.7 + Node.js 20+ installed
3. Initialize: Backend + Frontend directories
4. Start: Day 1 - Backend setup

**If Phase 1 Completed (CURRENT)**:
1. Review: Phase 1 lessons learned (contracts/00_ClassSphere_index.md)
2. Read: `03_plan_fase2_google_integration.md`
3. Prepare: Google Classroom API credentials
4. Start: Day 13 - Google API integration

**If Any Phase In Progress**:
1. Check: Current day in phase plan
2. Verify: Previous day's acceptance criteria met
3. Continue: Next day's tasks
4. Track: Context in tmux logs

### Phase-Specific Plans

- **Phase 1**: `02_plan_fase1_fundaciones.md` (12 days)
- **Phase 2**: `03_plan_fase2_google_integration.md` (10 days)
- **Phase 3**: `04_plan_fase3_visualizacion.md` (10 days)
- **Phase 4**: `05_plan_fase4_integracion.md` (13 days)

### Support Documentation

- **Testing Strategy**: `06_plan_testing_strategy.md`
- **Security Protocols**: `07_plan_security_protocols.md`
- **Context Management**: `08_plan_context_management.md`
- **Evaluation Metrics**: `09_plan_evaluation_metrics.md`

### Troubleshooting Quick Reference

| Issue | Solution | Reference |
|---|---|---|
| Port 8080 busy | `pkill -f classsphere-backend` | Phase 1 patterns |
| Angular CLI not found | `npx ng` instead of `ng` | Phase 1 patterns |
| TypeScript errors | Use `?.` and `??` operators | Phase 1 patterns |
| OAuth tests hang | Add `-timeout=10s` flag | Phase 1 patterns |
| TailwindCSS v4 issues | Downgrade to 3.4.0 | Phase 1 patterns |

### Emergency Contacts (Documentation)

- **Error Prevention**: `../contracts/15_ClassSphere_error_prevention.md`
- **Verification Commands**: `../contracts/16_ClassSphere_verification_commands.md`
- **Acceptance Criteria**: `../contracts/12_ClassSphere_criterios_aceptacion.md`
- **System Architecture**: `../contracts/05_ClassSphere_arquitectura.md`

---

## 📊 Plan Coherence Verification

**Stack Consistency** (Must be 100%):
- Go version: 1.24.7 (or 1.21+ compatible)
- Angular version: 19
- Echo version: v4
- TailwindCSS: 3.x (NOT v4)
- Testing: testify (backend), Jasmine + Karma (frontend), Playwright (E2E)

**Port Consistency** (NEVER CHANGE):
- Backend: 8080
- Frontend: 4200

**Architecture Consistency**:
- Backend: Hexagonal (ports & adapters)
- Frontend: Feature folders

**Obsolete Tech** (MUST NOT APPEAR):
- ❌ FastAPI, Python, Django
- ❌ Next.js, React, Remix
- ❌ Jest, Vitest (use Jasmine + Karma for Angular)

---

**CRITICAL**: Start with Phase 1 if not completed, or continue with current phase. **Never skip phases or acceptance criteria validation.**

**Last Updated**: 2025-10-07 | **Version**: 4.0 | **Status**: Phase 1 ✅ Completed

