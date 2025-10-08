# 🚀 Quick Start - TDD Implementation

**Branch**: `audit-security-improvements`  
**Status**: Ready to start Sprint 1  
**First Task**: CORS Restringido

---

## ⚡ Comenzar Ahora

### 1️⃣ Task Inmediata: CORS Tests (30 minutos)

```bash
# 1. Crear archivo de test
cd backend
touch internal/adapters/http/cors_test.go
```

```go
// internal/adapters/http/cors_test.go
package http

import (
    "net/http"
    "net/http/httptest"
    "testing"
    "github.com/stretchr/testify/assert"
)

func TestCORS_AllowedOrigin(t *testing.T) {
    // TODO: Implementar
    t.Skip("Implementar test de origen permitido")
}

func TestCORS_DisallowedOrigin(t *testing.T) {
    // TODO: Implementar
    t.Skip("Implementar test de origen bloqueado")
}
```

```bash
# 2. Ejecutar tests (deben fallar o skipear)
go test ./internal/adapters/http -v -run TestCORS

# 3. Implementar configuración CORS
# Ver AUDIT_IMPLEMENTATION_PLAN.md Task 1.1

# 4. Re-ejecutar tests (deben pasar)
go test ./internal/adapters/http -v -run TestCORS
```

---

## 📋 Checklist Diario

### Día 1: CORS (4h)
- [ ] Escribir tests CORS (30 min)
- [ ] Ejecutar tests (deben fallar) ✅ RED
- [ ] Implementar CORS config (2h)
- [ ] Tests pasan ✅ GREEN
- [ ] Refactorizar (30 min) ✅ REFACTOR
- [ ] Documentar (30 min)
- [ ] Commit: "feat: implement restricted CORS with tests"

### Día 2: Rate Limiting (6h)
- [ ] Escribir tests Rate Limiting (1h)
- [ ] Ejecutar tests (deben fallar) ✅ RED
- [ ] Implementar middleware (3h)
- [ ] Tests pasan ✅ GREEN
- [ ] Refactorizar (1h)
- [ ] Documentar (1h)
- [ ] Commit: "feat: implement rate limiting with Redis support"

### Día 3: Frontend Logging (4h)
- [ ] Escribir tests LoggerService (1h)
- [ ] Ejecutar tests (deben fallar) ✅ RED
- [ ] Implementar LoggerService (1h)
- [ ] Reemplazar console.log (1.5h)
- [ ] Tests pasan ✅ GREEN
- [ ] Configurar ESLint (30 min)
- [ ] Commit: "feat: replace console.log with LoggerService"

### Día 4: Actualizar Dependencias (3h)
- [ ] Audit vulnerabilidades actuales (30 min)
- [ ] Actualizar Go dependencies (1h)
- [ ] Actualizar npm dependencies (1h)
- [ ] Tests pasan (30 min)
- [ ] Commit: "chore: update dependencies and fix vulnerabilities"

---

## 🎯 Objetivos Sprint 1 (Semana 1-2)

**Meta**: Resolver 4 vulnerabilidades críticas  
**Tiempo**: 17 horas (~2 días)

### Success Criteria
```bash
✅ CORS: curl test pasa
✅ Rate Limit: 429 después de límite
✅ Logs: Zero console.log en production build
✅ Deps: govulncheck y npm audit limpios
✅ Tests: Cobertura ≥94.4%
```

---

## 📊 Comandos Útiles

### TDD Workflow

```bash
# 1. RED - Tests fallan
go test ./internal/adapters/http -v -run TestCORS
# FAIL

# 2. GREEN - Implementar mínimo necesario
# ... escribir código ...
go test ./internal/adapters/http -v -run TestCORS
# PASS

# 3. REFACTOR - Mejorar código
# ... refactorizar ...
go test ./internal/adapters/http -v -run TestCORS
# PASS (debe seguir pasando)
```

### Verificación Continua

```bash
# Coverage
go test ./... -coverprofile=coverage.out
go tool cover -html=coverage.out

# Linting
golangci-lint run ./...

# Security
govulncheck ./...

# Frontend
cd frontend
npm test
npm run lint
```

### Git Workflow

```bash
# Después de cada task completada
git add .
git commit -m "feat: <descripción>"

# Después de completar Sprint 1
git push origin audit-security-improvements

# Crear PR
gh pr create --title "Security improvements - Sprint 1" \
  --body "Implements critical security fixes from audit report"
```

---

## 🔥 Prioridad HOY

**Start with**: Task 1.1 - CORS Restringido

1. ✍️ Escribir test que falla
2. ✅ Implementar solución mínima
3. 🔄 Refactorizar
4. 📝 Documentar
5. 🚀 Commit

**Archivo**: `backend/internal/adapters/http/cors_test.go`  
**Tiempo**: 4 horas  
**Output esperado**: CORS configurado y testeado

---

## 💡 Tips TDD

1. **Red**: Test debe fallar por la razón correcta
2. **Green**: Código mínimo para pasar test
3. **Refactor**: Mejorar sin romper tests
4. **Repeat**: Siguiente funcionalidad

### Mantras TDD
- "Write the test you wish you had"
- "Fake it till you make it"
- "Triangulate when uncertain"
- "Refactor mercilessly"

---

**Next Step**: `cd backend && touch internal/adapters/http/cors_test.go`

**Questions?** Ver [AUDIT_IMPLEMENTATION_PLAN.md](./AUDIT_IMPLEMENTATION_PLAN.md) para detalles completos.

