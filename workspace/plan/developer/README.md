# ClassSphere Development Plan

**Version**: 4.0  
**Date**: 2025-10-07  
**Stack**: Go 1.24.7 + Angular 19  
**Status**: Phase 1 Completed (94.4% coverage)

---

## 🎯 Quick Start for LLMs

This directory contains the **complete step-by-step development plan** for ClassSphere system implementation.

### Plan Structure

```
workspace/ci/
├── README.md                           (This file)
├── 01_plan_index.md                   (Master plan index - START HERE)
├── 02_plan_fase1_fundaciones.md       (Phase 1: 12 days)
├── 03_plan_fase2_google_integration.md (Phase 2: 10 days)
├── 04_plan_fase3_visualizacion.md     (Phase 3: 10 days)
├── 05_plan_fase4_integracion.md       (Phase 4: 13 days)
├── 06_plan_testing_strategy.md         (Testing methodology)
├── 07_plan_security_protocols.md       (Security best practices)
├── 08_plan_context_management.md       (LLM context optimization)
└── 09_plan_evaluation_metrics.md       (Success criteria)
```

---

## 📚 Technology Stack

### Backend
- **Language**: Go 1.24.7
- **Framework**: Echo v4 (web framework)
- **Authentication**: JWT + OAuth 2.0 Google (PKCE + State)
- **Testing**: testify/assert + testify/mock + httptest
- **Cache**: Redis
- **Port**: 8080 (default)

### Frontend
- **Framework**: Angular 19
- **Build**: esbuild (official from Angular 17+)
- **Styling**: TailwindCSS 3.x
- **Testing**: Jasmine + Karma (unit) + Playwright (E2E)
- **Linter**: Biome
- **Port**: 4200 (default)

### DevOps
- **CI/CD**: GitHub Actions
- **Containers**: Docker multi-stage builds
- **Security**: Trivy scanning
- **Environment**: Dev Containers with Docker Compose

---

## 🚀 How to Use This Plan

### For LLMs (Recommended Workflow)

1. **START**: Read `01_plan_index.md` first
2. **UNDERSTAND**: Review objectives, dependencies, and evaluation criteria
3. **EXECUTE**: Follow phases sequentially (02 → 03 → 04 → 05)
4. **VALIDATE**: Use verification commands at each checkpoint
5. **ITERATE**: Apply TDD-RunFix+ methodology strictly

### For Humans

1. Review `01_plan_index.md` for overview
2. Check current phase status in contracts: `../contracts/00_ClassSphere_index.md`
3. Follow detailed instructions in phase files
4. Validate with acceptance criteria in `../contracts/12_ClassSphere_criterios_aceptacion.md`

---

## ✅ Current Status

### Phase 1: Foundations (COMPLETED ✅)
- **Backend**: Go + Echo + JWT + OAuth ✅
- **Coverage**: 94.4% (target: 80%) ✅
- **Errors Resolved**: 14 blocking errors ✅
- **Time**: 155 minutes total resolution ✅
- **Status**: Production-validated patterns documented ✅

### Phase 2-5: Pending ⏳
- Phase 2: Google Integration (10 days)
- Phase 3: Advanced Visualization (10 days)
- Phase 4: Complete Integration (13 days)
- Phase 5: Production Deployment (TBD)

---

## 📋 Key Principles

### 1. TDD-RunFix+ Methodology
```
Red → Green → Refactor → Validate Patterns → Document → Integrate
```

### 2. Coverage Requirements
- **Global**: ≥80% lines, ≥65% branches
- **Critical Modules**: ≥90% lines, ≥80% branches
- **Security Components**: ≥95% lines, ≥85% branches

### 3. Context Management (LLM-Optimized)
- **Chunking**: By priority (CRITICAL → HIGH → MEDIUM → LOW)
- **Structure**: Anti lost-in-the-middle (BEGINNING-MIDDLE-END)
- **Token Budget**: 2000 (CRITICAL), 1500 (HIGH), 1000 (MEDIUM), 800 (LOW)

### 4. Ports (NEVER CHANGE)
- Backend: **8080** (Go + Echo standard)
- Frontend: **4200** (Angular default)

### 5. Architecture
- Backend: **Hexagonal** (ports & adapters)
- Frontend: **Feature folders** (Angular best practice)

---

## 🔍 Validation Commands

### Quick Health Check
```bash
# Verify plan structure
ls -la workspace/ci/*.md | wc -l  # Should be 10

# Check for obsolete tech references (should return 0)
grep -r "FastAPI\|Next.js\|React\|Jest\|Vitest" workspace/ci/

# Verify stack consistency
grep -r "Go 1.24\|Go 1.21" workspace/ci/ | wc -l
grep -r "Angular 19" workspace/ci/ | wc -l
grep -r "Echo v4" workspace/ci/ | wc -l
```

### Phase Validation
```bash
# Test anti lost-in-the-middle structure
for file in workspace/ci/02*.md workspace/ci/03*.md workspace/ci/04*.md workspace/ci/05*.md; do
  echo "=== $file ==="
  grep -c "## 🎯 INICIO:" "$file" || echo "Missing INICIO"
  grep -c "## 📅 MEDIO:" "$file" || echo "Missing MEDIO"
  grep -c "## ✅ FINAL:" "$file" || echo "Missing FINAL"
done
```

---

## 📖 Documentation References

### Contracts (Specifications)
- `../contracts/00_ClassSphere_index.md` - Master index
- `../contracts/03_ClassSphere_analisis_critico.md` - Critical analysis
- `../contracts/04_ClassSphere_objetivos.md` - System objectives
- `../contracts/10_ClassSphere_plan_implementacion.md` - Implementation plan
- `../contracts/12_ClassSphere_criterios_aceptacion.md` - Acceptance criteria

### Best Practices
- `../extra/SOFTWARE_PROJECT_BEST_PRACTICES.md` - General best practices
- `../extra/TDD_BEST_PRACTICES.md` - TDD methodology
- `../extra/DEV_CONTAINERS_BEST_PRACTICES.md` - Dev environment

---

## 🎯 Success Metrics

### Precision (Target: ≥95%)
- Code follows specifications exactly
- No hallucinated features or technologies
- Stack consistency maintained

### Completeness (Target: 100%)
- All required features implemented
- All acceptance criteria met
- No missing critical functionality

### Coherence (Target: ≥85%)
- Consistent terminology across documents
- Cross-reference accuracy
- Logical flow in implementation

### Technical Excellence
- Test coverage ≥80% (global), ≥90% (critical)
- Zero critical security vulnerabilities
- Performance: <2s page load, <500ms API response
- Accessibility: WCAG 2.2 AA compliance

---

## 🆘 Troubleshooting

### Common Issues

**Issue**: Tests failing with "port already in use"
```bash
# Solution: Kill existing processes
pkill -f classsphere-backend
lsof -ti:8080 | xargs kill -9
```

**Issue**: Angular CLI not found
```bash
# Solution: Use npx
npx ng version
npx ng serve
```

**Issue**: TypeScript compilation errors
```bash
# Solution: Use optional chaining and nullish coalescing
user?.profile?.name ?? 'Unknown'
```

**Issue**: OAuth tests hanging
```bash
# Solution: Add timeout
go test ./... -timeout=10s
```

---

## 📞 Support

For questions or issues:
1. Check `../contracts/15_ClassSphere_error_prevention.md` for validated solutions
2. Review `../contracts/16_ClassSphere_verification_commands.md` for diagnostic commands
3. Consult Phase 1 lessons learned in `../contracts/00_ClassSphere_index.md`

---

## 🔄 Plan Updates

This plan is synchronized with:
- **Contracts**: `../contracts/` (specifications source of truth)
- **Version**: 4.0
- **Last Updated**: 2025-10-07

Any changes to contracts should trigger plan review and updates.

---

**Ready to start? → Read `01_plan_index.md`** 🚀

