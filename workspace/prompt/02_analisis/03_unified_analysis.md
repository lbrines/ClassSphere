---
id: "03"
title: "Unified Analysis - Plan or Contracts"
category: "Análisis"
priority: "VARIABLE"
version: "2.0"
stack: "Go 1.21+ + Angular 19"
target: "/workspace/plan/ OR /workspace/contracts/"
date: "2025-10-07"
---

# PROMPT: Análisis Unificado de Plan y Especificaciones ClassSphere

## OBJETIVO PRINCIPAL
Realizar análisis completo de 8 métricas (trazabilidad, coherencia, dependencias, patrones, completitud, complejidad, riesgos y calidad) para el plan de desarrollo (`/workspace/plan/`) o las especificaciones (`/workspace/contracts/`).

## PREGUNTA INICIAL

¿Este análisis es para:
1. **Plan de desarrollo** (`/workspace/plan/`)
2. **Especificaciones** (`/workspace/contracts/`)

**Por favor, responde con "plan" o "contracts" para proceder.**

---

## ANÁLISIS DEL PLAN (`/workspace/plan/`)

### Métrica 1: Trazabilidad del Plan
**Objetivo**: Verificar que cada requisito de las especificaciones esté cubierto en el plan de desarrollo.

**Scope**: `/workspace/plan/` - Prioridad: ALTA - Criterio: ≥95% cobertura

**Comandos de verificación:**
```bash
# Verificar stack Go + Angular
grep -r "Go 1.21\|Angular 19\|Echo v4\|testify" workspace/plan/

# Verificar autenticación
grep -r "JWT\|OAuth 2.0\|Google" workspace/plan/

# Verificar funcionalidades
grep -r "Dashboard\|WebSocket\|WCAG 2.2 AA" workspace/plan/

# Contar menciones por requisito
for req in "Go" "Angular" "JWT" "OAuth" "WebSocket" "testify"; do
  echo "$req: $(grep -rc "$req" workspace/plan/ | awk -F: '{sum+=$2} END {print sum}')"
done
```

### Métrica 2: Coherencia del Plan
**Objetivo**: Validar consistencia de términos técnicos en todo el plan.

**Scope**: `/workspace/plan/` - Prioridad: ALTA - Criterio: ≥85% coherencia

**Términos a validar:**
- **Stack**: Go 1.21+, Angular 19, Echo v4, testify, Jasmine, Karma, Playwright
- **Puertos**: 8080 (backend), 4200 (frontend)
- **Cobertura**: ≥80% global, ≥90% módulos críticos
- **Metodología**: TDD-RunFix+, Cero confianza, WCAG 2.2 AA

**Comandos:**
```bash
# Verificar coherencia de stack
grep -r "Go 1.21" workspace/plan/ | wc -l
grep -r "Angular 19" workspace/plan/ | wc -l
grep -r "Echo v4" workspace/plan/ | wc -l

# Verificar puertos
grep -r "8080" workspace/plan/ | wc -l  # Backend
grep -r "4200" workspace/plan/ | wc -l  # Frontend

# Verificar que NO mencione tecnologías obsoletas
grep -r "FastAPI\|Next.js\|React\|Jest\|Vitest" workspace/plan/
# No debe retornar nada

# Verificar metodología
grep -r "TDD-RunFix+" workspace/plan/ | wc -l
grep -r "cero confianza\|zero trust" workspace/plan/ | wc -l
```

### Métrica 3: Dependencias del Plan
**Objetivo**: Verificar que dependencias críticas entre fases estén documentadas.

**Scope**: `/workspace/plan/` - Prioridad: ALTA - Criterio: 100% documentadas

**Comandos:**
```bash
# Buscar dependencias en cada fase
grep -A 10 "Dependencias Bloqueantes" workspace/plan/03_plan_fase2*.md
grep -A 10 "Dependencias Bloqueantes" workspace/plan/04_plan_fase3*.md
grep -A 10 "Dependencias Bloqueantes" workspace/plan/05_plan_fase4*.md

# Verificar menciones de dependencias
grep -r "Fase 1 completada" workspace/plan/03_plan_fase2*.md
grep -r "Fase 2 completada" workspace/plan/04_plan_fase3*.md
grep -r "Fase 3 completada" workspace/plan/05_plan_fase4*.md
```

### Métrica 4: Patrones del Plan
**Objetivo**: Verificar consistencia de patrones arquitectónicos y metodológicos.

**Scope**: `/workspace/plan/` - Prioridad: MEDIA - Criterio: ≥80% consistencia

**Patrones a validar:**
1. **TDD-RunFix+** (Red-Green-Refactor-Validate-Document-Integrate)
2. **Context-Aware** (Chunking por prioridad CRITICAL→LOW)
3. **Anti Lost-in-the-Middle** (INICIO-MEDIO-FINAL)
4. **Cero Confianza** (Verificación obligatoria, SAST/SCA)
5. **Logs Estructurados** (JSON, context_id)
6. **Arquitectura Hexagonal** (Ports & Adapters en backend)

**Comandos:**
```bash
# TDD-RunFix+
grep -c "TDD-RunFix+\|Red-Green-Refactor" workspace/plan/*.md

# Estructura anti lost-in-the-middle
for file in workspace/plan/0[2-5]*.md; do
  echo "$file:"
  grep -c "## 🎯 INICIO:" "$file"
  grep -c "## 📅 MEDIO:" "$file"
  grep -c "## ✅ FINAL:" "$file"
done

# Arquitectura hexagonal
grep -c "hexagonal\|ports.*adapters" workspace/plan/*.md
```

### Métrica 5: Completitud del Plan
**Objetivo**: Validar que todas las funcionalidades estén cubiertas.

**Scope**: `/workspace/plan/` - Prioridad: MEDIA - Criterio: ≥95% cobertura

**Funcionalidades clave:**
1. Autenticación (JWT + OAuth 2.0)
2. Google Classroom Integration
3. Dashboards por rol (4 tipos)
4. Visualizaciones avanzadas
5. Sistema de búsqueda
6. Notificaciones real-time
7. Métricas y analytics
8. Accesibilidad WCAG 2.2 AA
9. Testing completo
10. CI/CD Pipeline

**Comandos:**
```bash
# Verificar cada funcionalidad
for func in "JWT" "OAuth" "Dashboard" "WebSocket" "WCAG" "CI/CD" "testify"; do
  echo "$func: $(grep -rc "$func" workspace/plan/ | awk -F: '{sum+=$2} END {print sum}') menciones"
done
```

### Métrica 6: Complejidad del Plan
**Objetivo**: Analizar complejidad de instrucciones para ejecutabilidad.

**Scope**: `/workspace/plan/` - Prioridad: BAJA - Criterio: ≤MEDIUM

**Comandos:**
```bash
# Contar días en cada fase
for file in workspace/plan/0[2-5]*.md; do
  echo "$file: $(grep -c "^### Día" "$file") días"
done

# Buscar condicionales
grep -c "if\|cuando\|si.*entonces" workspace/plan/0[2-5]*.md

# Buscar anidación profunda
grep -E "^####|^#####" workspace/plan/0[2-5]*.md
```

### Métrica 7: Riesgos del Plan
**Objetivo**: Identificar y validar mitigación de riesgos técnicos.

**Scope**: `/workspace/plan/` - Prioridad: BAJA - Criterio: 100% mitigados

**Riesgos clave:**
1. Google API no disponible → Mocks completos
2. Incompatibilidad versiones → Versiones específicas
3. Tests colgados → Timeouts configurados
4. Performance lenta → Métricas < 2s
5. Vulnerabilidades → SAST/SCA/Trivy
6. Context overflow → Chunking por prioridad
7. Baja cobertura → TDD estricto ≥80%
8. OAuth failures → PKCE + State validation

**Comandos:**
```bash
# Verificar mitigaciones
grep -r "mock" workspace/plan/03_plan_fase2*.md
grep -r "timeout" workspace/plan/06_plan_testing*.md
grep -r "SAST\|SCA\|Trivy" workspace/plan/07_plan_security*.md
grep -r "chunking\|prioridad" workspace/plan/08_plan_context*.md
```

### Métrica 8: Calidad del Plan
**Objetivo**: Evaluar calidad global usando métricas objetivas.

**Scope**: `/workspace/plan/` - Prioridad: BAJA - Criterio: ≥90% calidad

**Fórmulas:**
```
Precisión = (Specs cumplidas / Specs totales) × 100 → ≥95%
Completitud = (Archivos creados / Archivos requeridos) × 100 → 100%
Coherencia = (Términos consistentes / Términos totales) × 100 → ≥85%
Seguridad = (Protocolos implementados / Protocolos requeridos) × 100 → 100%
Calidad Global = (Precisión + Completitud + Coherencia + Seguridad) / 4 → ≥90%
```

**Comandos:**
```bash
# Completitud
ls workspace/plan/*.md | wc -l  # Debe ser 10

# Coherencia
grep -rc "Go 1.21\|Angular 19" workspace/plan/ | awk -F: '{sum+=$2} END {print sum}'

# Seguridad
grep -c "SAST\|SCA\|Trivy\|cero confianza" workspace/plan/07_plan_security*.md
```

---

## ANÁLISIS DE ESPECIFICACIONES (`/workspace/contracts/`)

### Métrica 1: Trazabilidad de Especificaciones
**Objetivo**: Verificar que requisitos estén claramente definidos y trazables.

**Scope**: `/workspace/contracts/` - Prioridad: ALTA - Criterio: 100% identificables

**Comandos:**
```bash
# Contar requisitos por tipo
grep -c "^### " workspace/contracts/04_ClassSphere_objetivos.md
grep -c "^## " workspace/contracts/06_ClassSphere_funcionalidades.md

# Verificar stack tecnológico
grep -r "Go 1.21\|Angular 19\|Echo v4" workspace/contracts/
```

### Métrica 2: Coherencia de Especificaciones
**Objetivo**: Validar consistencia de términos técnicos.

**Scope**: `/workspace/contracts/` - Prioridad: ALTA - Criterio: ≥85% coherencia

**Comandos:**
```bash
# Verificar coherencia de stack
grep -r "Go 1.21" workspace/contracts/ | wc -l
grep -r "Angular 19" workspace/contracts/ | wc -l

# Verificar que NO mencione tecnologías obsoletas
grep -r "FastAPI\|Next.js\|React" workspace/contracts/
# No debe retornar nada
```

### Métrica 3: Dependencias de Especificaciones
**Objetivo**: Verificar que dependencias entre componentes estén identificadas.

**Comandos:**
```bash
# Buscar menciones de dependencias
grep -r "requiere\|depende\|necesita" workspace/contracts/

# Verificar documentación de dependencias
grep -A 5 "Dependencias" workspace/contracts/10_ClassSphere_plan_implementacion.md
```

### Métrica 4: Patrones de Especificaciones
**Objetivo**: Verificar que patrones arquitectónicos estén claramente definidos.

**Comandos:**
```bash
# Buscar patrones
grep -c "TDD\|hexagonal\|ports.*adapters" workspace/contracts/*.md
grep -c "Context-Aware" workspace/contracts/*.md
grep -c "Cero Confianza" workspace/contracts/*.md
```

### Métrica 5: Completitud de Especificaciones
**Objetivo**: Verificar cobertura de áreas del sistema.

**Comandos:**
```bash
# Contar archivos
ls workspace/contracts/*.md | wc -l

# Contar secciones por área
for file in workspace/contracts/*.md; do
  echo "$(basename $file): $(grep -c "^##" $file) secciones"
done
```

### Métrica 6: Complejidad de Especificaciones
**Objetivo**: Evaluar claridad y simplicidad.

**Comandos:**
```bash
# Contar niveles de encabezados
grep -E "^#{4,}" workspace/contracts/*.md | wc -l

# Contar palabras por archivo
wc -w workspace/contracts/*.md
```

### Métrica 7: Riesgos de Especificaciones
**Objetivo**: Verificar que riesgos técnicos estén identificados.

**Comandos:**
```bash
# Buscar menciones de riesgos
grep -r "riesgo\|risk\|problema" workspace/contracts/

# Buscar mitigaciones
grep -r "mitigación\|mitigation\|solución" workspace/contracts/
```

### Métrica 8: Calidad de Especificaciones
**Objetivo**: Evaluar calidad global.

**Métricas:**
- Claridad ≥90%
- Completitud 100%
- Coherencia ≥85%
- Trazabilidad 100%

---

## EJECUCIÓN DEL ANÁLISIS

**Basado en tu respuesta:**

### Si respondes "plan":
```bash
# Ejecutar análisis para /workspace/plan/
# Usar comandos de la sección "ANÁLISIS DEL PLAN"
# Generar resumen ejecutivo con resultados del plan
```

### Si respondes "contracts":
```bash
# Ejecutar análisis para /workspace/contracts/
# Usar comandos de la sección "ANÁLISIS DE ESPECIFICACIONES"
# Generar resumen ejecutivo con resultados de especificaciones
```

---

## OUTPUT ESPERADO: RESUMEN EJECUTIVO

```markdown
# Resumen Ejecutivo: Análisis Unificado [Plan/Contracts]

## 🎯 Objetivo Cumplido
Análisis completo de 8 métricas para [workspace/plan/ o workspace/contracts/].

## 📊 Resultados Principales

### Métrica 1: Trazabilidad
- **Valor**: X%
- **Objetivo**: ≥95% (plan) o 100% (contracts)
- **Estado**: ✅ PASS / ⚠️ NEEDS IMPROVEMENT
- **Detalles**: [Requisitos cubiertos/identificados]

### Métrica 2: Coherencia
- **Valor**: X%
- **Objetivo**: ≥85%
- **Estado**: ✅ PASS / ⚠️ NEEDS IMPROVEMENT
- **Stack verificado**:
  - Go 1.21+: [X] menciones
  - Angular 19: [X] menciones
  - Echo v4: [X] menciones
  - testify: [X] menciones
  - Puertos 8080/4200: Verificados
  - NO tecnologías obsoletas: ✅

### Métrica 3: Dependencias
- **Valor**: X% documentadas
- **Objetivo**: 100%
- **Estado**: ✅ PASS / ⚠️ NEEDS IMPROVEMENT
- **Detalles**: [Dependencias entre fases/componentes]

### Métrica 4: Patrones
- **Valor**: X% consistencia
- **Objetivo**: ≥80%
- **Estado**: ✅ PASS / ⚠️ NEEDS IMPROVEMENT
- **Patrones verificados**:
  - TDD-RunFix+: [X] menciones
  - Estructura INICIO-MEDIO-FINAL: [4/4] o [N/A]
  - Hexagonal: [X] menciones
  - Cero confianza: [X] menciones

### Métrica 5: Completitud
- **Valor**: X%
- **Objetivo**: ≥95%
- **Estado**: ✅ PASS / ⚠️ NEEDS IMPROVEMENT
- **Funcionalidades cubiertas**: [X/10]

### Métrica 6: Complejidad
- **Valor**: [LOW/MEDIUM/HIGH]
- **Objetivo**: ≤MEDIUM
- **Estado**: ✅ PASS / ⚠️ NEEDS IMPROVEMENT
- **Detalles**: [Pasos/día, comandos/paso, anidación]

### Métrica 7: Riesgos
- **Valor**: [X/8] riesgos mitigados
- **Objetivo**: 100%
- **Estado**: ✅ PASS / ⚠️ NEEDS IMPROVEMENT
- **Riesgos críticos**: [Listar]

### Métrica 8: Calidad Global
- **Valor**: X%
- **Objetivo**: ≥90%
- **Estado**: ✅ EXCELLENT / GOOD / ACCEPTABLE / NEEDS IMPROVEMENT
- **Fórmula**: (Precisión + Completitud + Coherencia + Seguridad) / 4

## ⚠️ Hallazgos Críticos

**Gaps identificados:**
1. [Gap 1]: Descripción - Severidad: [HIGH/MEDIUM/LOW]
2. [Gap 2]: Descripción - Severidad: [HIGH/MEDIUM/LOW]

**Inconsistencias encontradas:**
1. [Inconsistencia 1]: Descripción
2. [Inconsistencia 2]: Descripción

## ✅ Recomendaciones

### Inmediatas (CRITICAL)
1. [Acción requerida inmediatamente]
2. [Otra acción crítica]

### A corto plazo (HIGH)
3. [Acción importante]
4. [Otra acción importante]

### A largo plazo (MEDIUM/LOW)
5. [Mejora continua]
6. [Optimización]

## 📈 Estado General

**Calificación**: ✅ EXCELLENT (90-100%) / GOOD (80-89%) / ACCEPTABLE (70-79%) / NEEDS IMPROVEMENT (<70%)

**Resumen**:
- Trazabilidad: [X%]
- Coherencia: [X%]
- Dependencias: [X%]
- Patrones: [X%]
- Completitud: [X%]
- Complejidad: [LOW/MEDIUM/HIGH]
- Riesgos: [X/8]
- Calidad: [X%]

**Promedio**: [X%]

**Próxima verificación**: Después de próxima actualización
**Frecuencia recomendada**: Después de cambios mayores
```

---

## OPCIÓN ADICIONAL: COMPARACIÓN PLAN ↔ SPECS

Si además quieres **comparar plan con especificaciones**:

**Comandos adicionales:**
```bash
# Comparar stack tecnológico
diff <(grep "Go 1.21" workspace/contracts/05_ClassSphere_arquitectura.md | head -1) \
     <(grep "Go 1.21" workspace/plan/02_plan_fase1_fundaciones.md | head -1)

# Comparar timestamps
git log -1 --format="%ai" workspace/contracts/
git log -1 --format="%ai" workspace/plan/

# Contar requisitos
CONTRACTS_COUNT=$(grep -rc "Go\|Angular\|JWT\|OAuth" workspace/contracts/ | awk -F: '{sum+=$2} END {print sum}')
PLAN_COUNT=$(grep -rc "Go\|Angular\|JWT\|OAuth" workspace/plan/ | awk -F: '{sum+=$2} END {print sum}')

echo "Contracts: $CONTRACTS_COUNT, Plan: $PLAN_COUNT"
echo "Sincronización: $(echo "scale=2; $PLAN_COUNT * 100 / $CONTRACTS_COUNT" | bc)%"
```

**Output adicional:**
```markdown
## 🔄 Sincronización Plan ↔ Specs

**Sincronización**: X% (objetivo: ≥98%)
**Specs más reciente**: [timestamp]
**Plan más reciente**: [timestamp]
**Diferencia**: [X] minutos/horas

**Estado**: ✅ SYNCHRONIZED / ⚠️ NEEDS_SYNC
```

---

*Última actualización: 2025-10-07*

