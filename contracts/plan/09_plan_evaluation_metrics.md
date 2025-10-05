---
title: "ClassSphere - Métricas de Evaluación"
version: "1.0"
type: "strategy_document"
context_priority: "MEDIUM"
date: "2025-10-05"
---

[← Plan Principal](01_plan_index.md)

# Métricas de Evaluación

## Métricas de Calidad del Plan

### 1. Precisión del Plan

**Objetivo:** ≥95%

**Medición:**
```
Precisión = (Especificaciones cumplidas / Especificaciones totales) × 100
```

**Especificaciones a verificar:**
- [ ] FastAPI 0.104.1 especificado
- [ ] Pydantic v2 especificado
- [ ] Next.js 15 especificado
- [ ] React 19 especificado
- [ ] JWT authentication especificado
- [ ] OAuth 2.0 Google especificado
- [ ] ApexCharts 5.3.5 especificado
- [ ] Vitest + Playwright especificado
- [ ] Puerto 8000 especificado
- [ ] Cobertura ≥80% especificada
- [ ] TDD estricto especificado
- [ ] Chunking por prioridad especificado
- [ ] Estructura anti lost-in-the-middle especificada
- [ ] Logs estructurados especificados
- [ ] Principio de cero confianza especificado
- [ ] WCAG 2.2 AA especificado
- [ ] CI/CD pipeline especificado
- [ ] Docker deployment especificado
- [ ] Mocks Google API especificados
- [ ] Comandos de verificación especificados

**Comando de verificación:**
```bash
# Script de validación de precisión
python scripts/validate_plan_precision.py
```

---

### 2. Completitud del Plan

**Objetivo:** 100%

**Medición:**
```
Completitud = (Fases documentadas / Fases requeridas) × 100
```

**Fases requeridas:**
- [x] Fase 1: Fundaciones (12 días)
- [x] Fase 2: Google Integration (10 días)
- [x] Fase 3: Visualización Avanzada (10 días)
- [x] Fase 4: Integración Completa (13 días)

**Documentos requeridos:**
- [x] 01_plan_index.md
- [x] 02_plan_fase1_fundaciones.md
- [x] 03_plan_fase2_google_integration.md
- [x] 04_plan_fase3_visualizacion.md
- [x] 05_plan_fase4_integracion.md
- [x] 06_plan_testing_strategy.md
- [x] 07_plan_security_protocols.md
- [x] 08_plan_context_management.md
- [x] 09_plan_evaluation_metrics.md

**Comando de verificación:**
```bash
# Verificar todos los archivos existen
ls -la contracts/plan/*.md | wc -l
# Debe retornar: 9
```

---

### 3. Coherencia Semántica

**Objetivo:** ≥85%

**Medición:**
```
Coherencia = (Términos consistentes / Términos totales) × 100
```

**Términos a verificar consistencia:**
- FastAPI 0.104.1 (no FastAPI 0.104, no FastAPI 0.105)
- Next.js 15 (no Next.js 13, no Next.js 14)
- React 19 (no React 18)
- Pydantic v2 (no Pydantic v1)
- ApexCharts 5.3.5 (no ApexCharts 3.x)
- Puerto 8000 (no puerto 8080, no puerto variable)
- Cobertura ≥80% (consistente en todo el plan)
- WCAG 2.2 AA (no WCAG 2.1, no WCAG 2.2 AAA)

**Script de validación:**
```python
#!/usr/bin/env python3
"""
Validar coherencia semántica del plan
"""
import re
from pathlib import Path

def validate_semantic_coherence():
    """Validar coherencia de términos"""
    plan_dir = Path("contracts/plan")
    
    terms = {
        "FastAPI": r"FastAPI\s+0\.104\.1",
        "Next.js": r"Next\.js\s+15",
        "React": r"React\s+19",
        "Pydantic": r"Pydantic\s+v2",
        "Puerto": r"puerto\s+8000",
        "Cobertura": r"≥80%"
    }
    
    results = {}
    for term, pattern in terms.items():
        count = 0
        for file in plan_dir.glob("*.md"):
            content = file.read_text()
            matches = re.findall(pattern, content, re.IGNORECASE)
            count += len(matches)
        results[term] = count
    
    return results

if __name__ == "__main__":
    results = validate_semantic_coherence()
    print("Coherencia Semántica:")
    for term, count in results.items():
        print(f"  {term}: {count} menciones")
```

---

### 4. Seguridad (Cero Confianza)

**Objetivo:** 100%

**Medición:**
```
Seguridad = (Protocolos implementados / Protocolos requeridos) × 100
```

**Protocolos requeridos:**
- [x] Principio de cero confianza documentado
- [x] SAST (Bandit, Semgrep) especificado
- [x] SCA (Safety, pip-audit, npm audit) especificado
- [x] Detección de secretos (TruffleHog) especificado
- [x] Container scan (Trivy) especificado
- [x] Prompt engineering de seguridad documentado
- [x] Security headers configurados
- [x] Escaneo automático en CI/CD
- [x] Manejo seguro de secretos
- [x] Protocolo de respuesta a incidentes

**Comando de verificación:**
```bash
# Verificar protocolos de seguridad
grep -c "Cero Confianza" contracts/plan/07_plan_security_protocols.md
grep -c "SAST" contracts/plan/07_plan_security_protocols.md
grep -c "SCA" contracts/plan/07_plan_security_protocols.md
```

---

## Métricas de Calidad Técnica

### 1. Test Coverage Backend

**Objetivo:** ≥80% global, ≥90% críticos

**Comando de medición:**
```bash
cd backend
pytest tests/ --cov=src --cov-report=term-missing --cov-report=json

# Extraer porcentaje
cat coverage.json | jq '.totals.percent_covered'
```

**Módulos críticos:**
- app/core/security.py (≥95%)
- app/services/auth_service.py (≥90%)
- app/api/endpoints/auth.py (≥90%)
- app/middleware/* (≥90%)

---

### 2. Test Coverage Frontend

**Objetivo:** ≥80% global

**Comando de medición:**
```bash
cd frontend
npm run test -- --coverage --json --outputFile=coverage.json

# Extraer porcentaje
cat coverage.json | jq '.total.lines.pct'
```

**Componentes críticos:**
- components/auth/* (≥90%)
- hooks/useAuth.ts (≥90%)
- components/dashboard/* (≥85%)

---

### 3. Security Score

**Objetivo:** 100% (sin errores HIGH/CRITICAL)

**Comando de medición:**
```bash
# Backend
bandit -r backend/src/ -ll -f json -o bandit-report.json
cat bandit-report.json | jq '.metrics._totals.SEVERITY'

# Frontend
npm audit --json > npm-audit.json
cat npm-audit.json | jq '.metadata.vulnerabilities'

# Containers
trivy image --format json classsphere-backend:latest > trivy-backend.json
cat trivy-backend.json | jq '.[0].Vulnerabilities | length'
```

---

### 4. Performance Score

**Objetivo:** <2s carga de página

**Comando de medición:**
```bash
# Lighthouse
lighthouse http://localhost:3000 --output=json --output-path=lighthouse.json

# Extraer performance score
cat lighthouse.json | jq '.categories.performance.score * 100'

# Time to Interactive
cat lighthouse.json | jq '.audits.interactive.numericValue / 1000'
```

---

## Métricas de TDD Compliance

### 1. Tests Escritos Antes de Implementación

**Objetivo:** 100%

**Medición:**
```
TDD Compliance = (Features con tests primero / Features totales) × 100
```

**Verificación por fase:**
- Fase 1: Tests escritos antes de cada implementación
- Fase 2: Mocks antes de integración real
- Fase 3: Tests E2E antes de features
- Fase 4: Tests de seguridad antes de deploy

**Comando de verificación:**
```bash
# Verificar commits con tests primero
git log --all --grep="test:" --oneline | wc -l
git log --all --grep="feat:" --oneline | wc -l

# Ratio debe ser ≥1
```

---

### 2. Cobertura por Fase

**Objetivo:** ≥80% cada fase

| Fase | Objetivo | Comando de Verificación |
|------|----------|------------------------|
| Fase 1 | ≥80% | `pytest tests/ --cov=src --cov-fail-under=80` |
| Fase 2 | ≥85% | `pytest tests/ --cov=src --cov-fail-under=85` |
| Fase 3 | ≥85% | `pytest tests/ --cov=src --cov-fail-under=85` |
| Fase 4 | ≥90% | `pytest tests/ --cov=src --cov-fail-under=90` |

---

## Métricas de Context Management

### 1. Token Count por Chunk

**Objetivo:** <2000 tokens (CRITICAL), <1500 (HIGH), <1000 (MEDIUM), <800 (LOW)

**Comando de medición:**
```bash
# Contar tokens aproximados (palabras × 1.3)
for file in contracts/plan/*.md; do
    words=$(wc -w < "$file")
    tokens=$((words * 13 / 10))
    echo "$file: ~$tokens tokens"
done
```

**Validación:**
```python
#!/usr/bin/env python3
"""
Validar token counts por prioridad
"""
from pathlib import Path

def estimate_tokens(text: str) -> int:
    """Estimar tokens (aproximación)"""
    words = len(text.split())
    return int(words * 1.3)

def validate_token_limits():
    """Validar límites de tokens"""
    limits = {
        "01_plan_index.md": 2000,  # CRITICAL
        "02_plan_fase1_fundaciones.md": 2000,  # CRITICAL
        "03_plan_fase2_google_integration.md": 1500,  # HIGH
        "04_plan_fase3_visualizacion.md": 1000,  # MEDIUM
        "05_plan_fase4_integracion.md": 800,  # LOW
    }
    
    plan_dir = Path("contracts/plan")
    results = {}
    
    for filename, limit in limits.items():
        file_path = plan_dir / filename
        if file_path.exists():
            content = file_path.read_text()
            tokens = estimate_tokens(content)
            within_limit = tokens <= limit
            results[filename] = {
                "tokens": tokens,
                "limit": limit,
                "within_limit": within_limit
            }
    
    return results

if __name__ == "__main__":
    results = validate_token_limits()
    print("Token Limits Validation:")
    for file, data in results.items():
        status = "✅" if data["within_limit"] else "❌"
        print(f"{status} {file}: {data['tokens']}/{data['limit']} tokens")
```

---

### 2. Lost-in-Middle Risk

**Objetivo:** Low risk en INICIO y FINAL, Medium en MEDIO

**Comando de verificación:**
```bash
# Verificar estructura en cada archivo
for file in contracts/plan/*.md; do
    echo "=== $file ==="
    grep -c "## 🎯 INICIO:" "$file"
    grep -c "## 📅 MEDIO:" "$file"
    grep -c "## ✅ FINAL:" "$file"
done
```

---

### 3. Context Recovery Time

**Objetivo:** <5 minutos

**Comando de medición:**
```bash
# Medir tiempo de recuperación
time python scripts/recover_context.py

# Debe completar en <5 minutos
```

---

### 4. Chunking Effectiveness

**Objetivo:** ≥90%

**Medición:**
```
Effectiveness = (Info crítica en posiciones óptimas / Info crítica total) × 100
```

**Posiciones óptimas:**
- INICIO: Objetivos, dependencias, comandos de verificación
- FINAL: Checklist, próximos pasos, comandos de validación

---

## Dashboard de Métricas

### Script de Reporte Completo

**scripts/generate_metrics_report.py**
```python
#!/usr/bin/env python3
"""
Generar reporte completo de métricas
"""
import json
import subprocess
from datetime import datetime
from pathlib import Path


def run_command(cmd: str) -> str:
    """Ejecutar comando y retornar output"""
    try:
        result = subprocess.run(
            cmd,
            shell=True,
            capture_output=True,
            text=True,
            timeout=60
        )
        return result.stdout.strip()
    except Exception as e:
        return f"Error: {e}"


def generate_report():
    """Generar reporte de métricas"""
    report = {
        "timestamp": datetime.now().isoformat(),
        "project": "ClassSphere",
        "version": "1.0",
        "metrics": {}
    }
    
    # Plan Quality
    plan_files = list(Path("contracts/plan").glob("*.md"))
    report["metrics"]["plan_completeness"] = {
        "files_count": len(plan_files),
        "target": 9,
        "percentage": (len(plan_files) / 9) * 100
    }
    
    # Backend Coverage
    backend_cov = run_command(
        "cd backend && pytest tests/ --cov=src --cov-report=json -q && "
        "cat coverage.json | jq '.totals.percent_covered'"
    )
    report["metrics"]["backend_coverage"] = {
        "percentage": float(backend_cov) if backend_cov else 0,
        "target": 80
    }
    
    # Frontend Coverage
    frontend_cov = run_command(
        "cd frontend && npm run test -- --coverage --silent && "
        "cat coverage/coverage-summary.json | jq '.total.lines.pct'"
    )
    report["metrics"]["frontend_coverage"] = {
        "percentage": float(frontend_cov) if frontend_cov else 0,
        "target": 80
    }
    
    # Security
    bandit_issues = run_command(
        "bandit -r backend/src/ -ll -f json 2>/dev/null | "
        "jq '.metrics._totals.SEVERITY.HIGH + .metrics._totals.SEVERITY.CRITICAL'"
    )
    report["metrics"]["security_issues"] = {
        "count": int(bandit_issues) if bandit_issues else 0,
        "target": 0
    }
    
    # Save report
    report_file = Path("/tmp/classsphere_metrics_report.json")
    with open(report_file, "w") as f:
        json.dump(report, f, indent=2)
    
    print(f"✅ Metrics report generated: {report_file}")
    print(json.dumps(report, indent=2))
    
    return report


if __name__ == "__main__":
    generate_report()
```

**Comando de ejecución:**
```bash
python scripts/generate_metrics_report.py
```

---

## Criterios de Éxito Global

### Checklist de Validación Final

**Plan:**
- [ ] Precisión ≥95%
- [ ] Completitud 100%
- [ ] Coherencia semántica ≥85%
- [ ] Seguridad 100%

**Técnico:**
- [ ] Backend coverage ≥80%
- [ ] Frontend coverage ≥80%
- [ ] Security score 100%
- [ ] Performance <2s

**TDD:**
- [ ] TDD compliance 100%
- [ ] Tests antes de implementación
- [ ] Cobertura por fase cumplida

**Context:**
- [ ] Token counts dentro de límites
- [ ] Lost-in-middle risk bajo
- [ ] Context recovery <5min
- [ ] Chunking effectiveness ≥90%

### Comando de Validación Global

```bash
#!/bin/bash
# Validación completa de métricas

echo "🔍 Validando métricas del plan..."

# 1. Completitud
FILES=$(ls contracts/plan/*.md | wc -l)
echo "📁 Archivos del plan: $FILES/9"

# 2. Backend coverage
cd backend
BACKEND_COV=$(pytest tests/ --cov=src -q 2>/dev/null | grep "TOTAL" | awk '{print $4}' | tr -d '%')
echo "🧪 Backend coverage: ${BACKEND_COV}%"

# 3. Frontend coverage
cd ../frontend
FRONTEND_COV=$(npm run test -- --coverage --silent 2>/dev/null | grep "All files" | awk '{print $10}' | tr -d '%')
echo "🧪 Frontend coverage: ${FRONTEND_COV}%"

# 4. Security
cd ..
SECURITY_ISSUES=$(bandit -r backend/src/ -ll -q 2>/dev/null | grep "Total issues" | awk '{print $4}')
echo "🔒 Security issues: ${SECURITY_ISSUES}"

# 5. Resumen
echo ""
echo "📊 Resumen de Métricas:"
echo "  Plan Completitud: $(($FILES * 100 / 9))%"
echo "  Backend Coverage: ${BACKEND_COV}%"
echo "  Frontend Coverage: ${FRONTEND_COV}%"
echo "  Security Issues: ${SECURITY_ISSUES}"

# Validar criterios
if [ $FILES -eq 9 ] && [ ${BACKEND_COV:-0} -ge 80 ] && [ ${FRONTEND_COV:-0} -ge 80 ] && [ ${SECURITY_ISSUES:-1} -eq 0 ]; then
    echo ""
    echo "✅ Todas las métricas cumplen los criterios de éxito"
    exit 0
else
    echo ""
    echo "❌ Algunas métricas no cumplen los criterios"
    exit 1
fi
```

---

[← Plan Principal](01_plan_index.md)
