---
title: "ClassSphere - Prompts de Gestión del Plan"
version: "1.0"
type: "prompt_collection"
date: "2025-10-05"
author: "Sistema de Gestión ClassSphere"
total_prompts: 20
---

# ClassSphere Plan Management Prompts

## 📋 Índice

### Gestión del Plan
1. [CREATE: Crear Nuevo Plan](#1-prompt-create-plan)
2. [UPDATE: Actualizar Plan](#2-prompt-update-plan)

### Análisis del Plan (/contracts/plan/)
3. [Trazabilidad del Plan (Alta)](#3-prompt-analyze-plan-traceability)
4. [Coherencia del Plan (Alta)](#4-prompt-analyze-plan-coherence)
5. [Dependencias del Plan (Alta)](#5-prompt-analyze-plan-dependencies)
6. [Patrones del Plan (Media)](#6-prompt-analyze-plan-patterns)
7. [Completitud del Plan (Media)](#7-prompt-analyze-plan-completeness)
8. [Complejidad del Plan (Baja)](#8-prompt-analyze-plan-complexity)
9. [Riesgos del Plan (Baja)](#9-prompt-analyze-plan-risks)
10. [Calidad del Plan (Baja)](#10-prompt-analyze-plan-quality)

### Análisis de Especificaciones (/contracts/principal/)
11. [Trazabilidad de Specs (Alta)](#11-prompt-analyze-specs-traceability)
12. [Coherencia de Specs (Alta)](#12-prompt-analyze-specs-coherence)
13. [Dependencias de Specs (Alta)](#13-prompt-analyze-specs-dependencies)
14. [Patrones de Specs (Media)](#14-prompt-analyze-specs-patterns)
15. [Completitud de Specs (Media)](#15-prompt-analyze-specs-completeness)
16. [Complejidad de Specs (Baja)](#16-prompt-analyze-specs-complexity)
17. [Riesgos de Specs (Baja)](#17-prompt-analyze-specs-risks)
18. [Calidad de Specs (Baja)](#18-prompt-analyze-specs-quality)

### Análisis Comparativo
19. [Comparar Plan vs Specs](#19-prompt-compare-plan-specs)
20. [Verificar Sincronización](#20-prompt-sync-check)

### Análisis de Cumplimiento
21. [Analizar Cumplimiento con Mejores Prácticas](#21-prompt-analyze-best-practices-compliance)

### Gestión de Repositorio
22. [Limpiar Repositorio y Mantener Solo Contracts](#22-prompt-clean-repo-keep-contracts)

### Análisis Unificado
23. [Análisis Unificado de Plan y Especificaciones](#23-prompt-analyze-unified-plan-specs)

---

## 🎯 Guía de Uso Rápida

**Analizar solo el plan:**
→ Usar prompts 3-10

**Analizar solo especificaciones:**
→ Usar prompts 11-18

**Comparar plan con specs:**
→ Usar prompts 19-20

**Crear plan nuevo:**
→ Usar prompt 1

**Actualizar plan existente:**
→ Usar prompt 2

**Análisis completo:**
→ Usar prompts según prioridad (Alta → Media → Baja)

**Verificar cumplimiento con mejores prácticas:**
→ Usar prompt 21

**Limpiar repositorio manteniendo solo contracts:**
→ Usar prompt 22

**Análisis completo unificado (plan o especificaciones):**
→ Usar prompt 23

---

# PROMPTS DE GESTIÓN

## 1. PROMPT_CREATE_PLAN

```markdown
# PROMPT: Crear Nuevo Plan de Desarrollo ClassSphere

## OBJETIVO PRINCIPAL
Generar plan completo de desarrollo desde cero en `/contracts/plan/` siguiendo 100% las especificaciones de `@00_ClassSphere_index.md` y aplicando mejores prácticas de `@SOFTWARE_PROJECT_BEST_PRACTICES.md`.

## CONTEXTO DE EJECUCIÓN
- **Proyecto**: Repositorio vacío o sin plan existente
- **Enfoque**: Desarrollo desde cero con TDD estricto
- **Destino**: Crear estructura en `/contracts/plan/`
- **Audiencia**: LLM que ejecutará el plan paso a paso

## PASO 1: LEER ESPECIFICACIONES

**Archivos a leer:**
```bash
# Especificaciones principales
cat contracts/principal/00_ClassSphere_index.md
cat contracts/principal/04_ClassSphere_objetivos.md
cat contracts/principal/05_ClassSphere_arquitectura.md
cat contracts/principal/06_ClassSphere_funcionalidades.md
cat contracts/principal/09_ClassSphere_testing.md
cat contracts/principal/10_ClassSphere_plan_implementacion.md

# Mejores prácticas
cat contracts/extra/SOFTWARE_PROJECT_BEST_PRACTICES.md
```

## PASO 2: EXTRAER REQUISITOS CLAVE

**Información crítica a extraer:**
- Stack tecnológico (versiones exactas)
- Metodología TDD
- Estructura de fases
- Cobertura de testing requerida
- Timeouts de testing
- Principios de seguridad
- Context management requirements

## PASO 3: CREAR ARCHIVOS DEL PLAN

**Archivos a crear (usar write_to_file tool):**

### 3.1 Archivo Principal
- **Archivo**: `contracts/plan/01_plan_index.md`
- **Prioridad**: CRITICAL (2000 tokens max)
- **Estructura**: INICIO-MEDIO-FINAL
- **Contenido**:
  - Objetivos críticos y dependencias bloqueantes
  - Fases de desarrollo (resumen)
  - Seguridad y verificación
  - Estrategia de testing
  - Gestión de contexto
  - Métricas de evaluación
  - Checklist final y próximos pasos

### 3.2 Fase 1: Fundaciones
- **Archivo**: `contracts/plan/02_plan_fase1_fundaciones.md`
- **Prioridad**: CRITICAL (2000 tokens max)
- **Duración**: 12 días
- **Contenido**:
  - Backend: FastAPI 0.104.1 + Pydantic v2 + JWT + OAuth 2.0
  - Frontend: Next.js 15 + React 19 + TypeScript
  - Testing: ≥80% coverage
  - Instrucciones día por día con comandos específicos

### 3.3 Fase 2: Google Integration
- **Archivo**: `contracts/plan/03_plan_fase2_google_integration.md`
- **Prioridad**: HIGH (1500 tokens max)
- **Duración**: 10 días
- **Contenido**:
  - Google Classroom API con mocks
  - Modo dual (Google/Mock)
  - Dashboards por rol
  - ApexCharts 5.3.5

### 3.4 Fase 3: Visualización
- **Archivo**: `contracts/plan/04_plan_fase3_visualizacion.md`
- **Prioridad**: MEDIUM (1000 tokens max)
- **Duración**: 10 días
- **Contenido**:
  - Búsqueda avanzada
  - Notificaciones WebSocket
  - Gráficos interactivos

### 3.5 Fase 4: Integración
- **Archivo**: `contracts/plan/05_plan_fase4_integracion.md`
- **Prioridad**: LOW (800 tokens max)
- **Duración**: 13 días
- **Contenido**:
  - Sincronización bidireccional
  - Accesibilidad WCAG 2.2 AA
  - CI/CD completo

### 3.6 Estrategia de Testing
- **Archivo**: `contracts/plan/06_plan_testing_strategy.md`
- **Contenido**:
  - Stack: Vitest + Playwright (NO Jest)
  - Cobertura requerida
  - Templates de tests
  - Comandos de verificación

### 3.7 Protocolos de Seguridad
- **Archivo**: `contracts/plan/07_plan_security_protocols.md`
- **Contenido**:
  - Principio de cero confianza
  - SAST, SCA, Secrets detection
  - Prompt engineering de seguridad
  - Pipeline de seguridad CI/CD

### 3.8 Gestión de Contexto
- **Archivo**: `contracts/plan/08_plan_context_management.md`
- **Contenido**:
  - Chunking por prioridad
  - Estructura anti lost-in-the-middle
  - Logs estructurados
  - Context recovery

### 3.9 Métricas de Evaluación
- **Archivo**: `contracts/plan/09_plan_evaluation_metrics.md`
- **Contenido**:
  - Precisión ≥95%
  - Completitud 100%
  - Coherencia ≥85%
  - Métricas técnicas

### 3.10 README
- **Archivo**: `contracts/plan/README.md`
- **Contenido**:
  - Descripción del plan
  - Guía de inicio rápido
  - Stack tecnológico
  - Comandos de validación

## PASO 4: VALIDAR PLAN CREADO

**Comandos de validación:**
```bash
# Verificar archivos creados
ls -la contracts/plan/*.md | wc -l
# Debe retornar: 10

# Verificar estructura anti lost-in-the-middle
for file in contracts/plan/0[2-5]*.md; do
  echo "=== $file ==="
  grep -c "## 🎯 INICIO:" "$file"
  grep -c "## 📅 MEDIO:" "$file"
  grep -c "## ✅ FINAL:" "$file"
done

# Verificar coherencia de versiones
grep -r "FastAPI" contracts/plan/ | grep -v "0.104.1"
grep -r "Next.js" contracts/plan/ | grep -v "15"
grep -r "React" contracts/plan/ | grep -v "19"

# Verificar que NO mencione Jest
grep -r "Jest" contracts/plan/
# No debe retornar nada
```

## OUTPUT ESPERADO: RESUMEN EJECUTIVO

Generar resumen ejecutivo con este formato:

# Resumen Ejecutivo: Creación del Plan ClassSphere

## 🎯 Objetivo Cumplido
Plan completo de desarrollo generado en `/contracts/plan/` con 10 archivos.

## 📊 Archivos Creados
- ✅ 01_plan_index.md (18.8 KB, CRITICAL)
- ✅ 02_plan_fase1_fundaciones.md (20.3 KB, CRITICAL)
- ✅ 03_plan_fase2_google_integration.md (13.5 KB, HIGH)
- ✅ 04_plan_fase3_visualizacion.md (5.7 KB, MEDIUM)
- ✅ 05_plan_fase4_integracion.md (10.5 KB, LOW)
- ✅ 06_plan_testing_strategy.md (6.4 KB)
- ✅ 07_plan_security_protocols.md (10.1 KB)
- ✅ 08_plan_context_management.md (12.5 KB)
- ✅ 09_plan_evaluation_metrics.md (14.4 KB)
- ✅ README.md (4.2 KB)

## 📈 Validaciones
- ✅ Estructura anti lost-in-the-middle: 100%
- ✅ Coherencia FastAPI 0.104.1: 100%
- ✅ Coherencia Next.js 15: 100%
- ✅ Coherencia React 19: 100%
- ✅ NO menciona Jest: Correcto
- ✅ Chunking por prioridad: Aplicado

## ✅ Características del Plan
- Completamente ejecutable desde repositorio vacío
- Instrucciones paso a paso sin ambigüedades
- TDD estricto desde el inicio
- Seguridad de cero confianza
- Context management optimizado
- Métricas objetivas de éxito

## 📍 Próximos Pasos
1. Revisar plan generado
2. Comenzar con Fase 1: `cat contracts/plan/02_plan_fase1_fundaciones.md`
3. Ejecutar validaciones periódicas
4. Mantener sincronizado con especificaciones

## 📈 Estado General
✅ PLAN CREADO EXITOSAMENTE - Listo para ejecución
```

---

## 2. PROMPT_UPDATE_PLAN

```markdown
# PROMPT: Actualizar Plan de Desarrollo Existente

## OBJETIVO PRINCIPAL
Actualizar el plan en `/contracts/plan/` basado en cambios detectados en especificaciones (`/contracts/principal/`) usando Git como herramienta de detección.

## CONTEXTO
- **Plan actual**: `/contracts/plan/` (9 archivos + README)
- **Especificaciones**: `/contracts/principal/`
- **Método**: Git diff para detectar cambios
- **Acción**: Actualizar solo archivos afectados (NO crear nuevos)

## PASO 1: DETECTAR CAMBIOS CON GIT

**Comandos a ejecutar:**
```bash
# Ver cambios en especificaciones desde último commit
git diff HEAD contracts/principal/

# Ver archivos modificados
git diff --name-only HEAD contracts/principal/

# Ver cambios con contexto
git diff HEAD contracts/principal/ --unified=5

# Ver historial reciente
git log --oneline -10 contracts/principal/

# Ver cambios específicos en un archivo
git diff HEAD contracts/principal/05_ClassSphere_arquitectura.md
```

## PASO 2: ANALIZAR IMPACTO

**Mapeo de cambios → archivos del plan:**

```yaml
Cambios en:
  00_ClassSphere_index.md:
    → Afecta: 01_plan_index.md

  04_ClassSphere_objetivos.md:
    → Afecta: 01_plan_index.md, archivos de fase correspondientes

  05_ClassSphere_arquitectura.md:
    → Afecta: 01_plan_index.md, todas las fases
    → Especialmente: Stack tecnológico, estructura directorios

  06_ClassSphere_funcionalidades.md:
    → Afecta: Fase correspondiente a cada funcionalidad
    - Autenticación → 02_plan_fase1_fundaciones.md
    - Google → 03_plan_fase2_google_integration.md
    - Visualización → 04_plan_fase3_visualizacion.md
    - Accesibilidad → 05_plan_fase4_integracion.md

  09_ClassSphere_testing.md:
    → Afecta: 06_plan_testing_strategy.md, 09_plan_evaluation_metrics.md

  10_ClassSphere_plan_implementacion.md:
    → Afecta: Todas las fases

  11_ClassSphere_deployment.md:
    → Afecta: 05_plan_fase4_integracion.md
```

## PASO 3: CLASIFICAR PRIORIDAD DE CAMBIOS

**Comandos para análisis:**
```bash
# Identificar tipo de cambio
git diff HEAD contracts/principal/ | grep "^+" | head -20
git diff HEAD contracts/principal/ | grep "^-" | head -20

# Buscar cambios críticos
git diff HEAD contracts/principal/ | grep -i "version\|stack\|tdd\|security"
```

**Clasificación:**
- **CRITICAL**: Stack tecnológico, metodología TDD, seguridad
- **HIGH**: Nuevas funcionalidades, cambios en endpoints
- **MEDIUM**: Cambios en documentación, refinamientos
- **LOW**: Typos, formateo, enlaces

## PASO 4: ACTUALIZAR ARCHIVOS DEL PLAN

**Para cada cambio identificado:**

1. **Localizar sección en plan:**
```bash
grep -n "término_buscado" contracts/plan/*.md
```

2. **Usar Edit tool para actualizar:**
   - Preservar estructura INICIO-MEDIO-FINAL
   - Mantener chunking por prioridad
   - Actualizar comandos de verificación si aplica
   - Actualizar criterios de aceptación si aplica

3. **Validar coherencia:**
```bash
# Verificar consistencia de términos
grep -c "FastAPI 0.104.1" contracts/plan/*.md
grep "FastAPI" contracts/plan/*.md | grep -v "0.104.1"
```

## PASO 5: VALIDAR ACTUALIZACIÓN

**Comandos de validación:**
```bash
# 1. Coherencia semántica
grep -r "FastAPI" contracts/plan/ | grep -v "0.104.1"
grep -r "Next.js" contracts/plan/ | grep -v "15"
grep -r "React" contracts/plan/ | grep -v "19"

# 2. Estructura anti lost-in-the-middle
for file in contracts/plan/0[2-5]*.md; do
  grep -c "## 🎯 INICIO:" "$file"
  grep -c "## 📅 MEDIO:" "$file"
  grep -c "## ✅ FINAL:" "$file"
done

# 3. Referencias cruzadas
grep -r "\[.*\](.*\.md)" contracts/plan/ | wc -l

# 4. Completitud
ls contracts/plan/*.md | wc -l  # Debe ser 10
```

## PASO 6: DOCUMENTAR CAMBIOS

**Crear commit:**
```bash
# Ver cambios realizados
git diff contracts/plan/

# Agregar archivos modificados
git add contracts/plan/

# Commit descriptivo
git commit -m "[plan] Update based on spec changes

Changes:
- Updated [componente] in [archivo]
- Modified [sección] to reflect [cambio]
- Synchronized with specs version [versión]

Triggered by: git diff HEAD contracts/principal/"
```

## OUTPUT ESPERADO: RESUMEN EJECUTIVO

# Resumen Ejecutivo: Actualización del Plan

## 🎯 Objetivo Cumplido
Plan actualizado basado en cambios detectados en especificaciones.

## 📊 Cambios Detectados
**Archivos de specs modificados:**
- 05_ClassSphere_arquitectura.md (15 líneas cambiadas)
- 09_ClassSphere_testing.md (8 líneas cambiadas)

**Tipo de cambios:**
- Actualización de versión: FastAPI 0.104.0 → 0.104.1
- Nuevo requisito: Timeout de tests especificado
- Refinamiento: Cobertura de testing clarificada

## 🔄 Archivos del Plan Actualizados
- ✅ 01_plan_index.md (actualizado stack tecnológico)
- ✅ 02_plan_fase1_fundaciones.md (actualizada versión FastAPI)
- ✅ 06_plan_testing_strategy.md (agregados timeouts)
- ✅ 09_plan_evaluation_metrics.md (actualizadas métricas)

## ✅ Validaciones Post-Actualización
- ✅ Coherencia FastAPI 0.104.1: 100%
- ✅ Estructura anti lost-in-the-middle: Preservada
- ✅ Referencias cruzadas: Sin enlaces rotos
- ✅ Completitud: 10 archivos intactos

## 📝 Commit Creado
```
[plan] Update based on spec changes

Changes:
- Updated FastAPI version to 0.104.1 in fase1
- Added test timeouts in testing strategy
- Updated evaluation metrics

Triggered by: git diff HEAD contracts/principal/
```

## 📈 Estado General
✅ PLAN ACTUALIZADO EXITOSAMENTE - Sincronizado con specs
```

---

# ANÁLISIS DEL PLAN

## 3. PROMPT_ANALYZE_PLAN_TRACEABILITY

```markdown
# PROMPT: Análisis de Trazabilidad del Plan

## OBJETIVO
Verificar que cada requisito de las especificaciones esté cubierto en el plan de desarrollo.

## SCOPE
- **Directorio**: `/contracts/plan/`
- **Prioridad**: ALTA
- **Criterio de éxito**: ≥95% de cobertura

## PASO 1: EXTRAER REQUISITOS DE ESPECIFICACIONES

**Archivos fuente:**
```bash
# Objetivos
grep -E "^###|^-" contracts/principal/04_ClassSphere_objetivos.md

# Funcionalidades
grep -E "^##|^###" contracts/principal/06_ClassSphere_funcionalidades.md

# API Endpoints
grep -E "^POST|^GET|^PUT|^DELETE" contracts/principal/07_ClassSphere_api_endpoints.md
```

**Requisitos clave a verificar:**
1. FastAPI 0.104.1
2. Pydantic v2
3. Next.js 15
4. React 19
5. JWT Authentication
6. OAuth 2.0 Google
7. Sistema de roles
8. Google Classroom API
9. Dashboards por rol (4 tipos)
10. ApexCharts 5.3.5
11. Búsqueda avanzada
12. Notificaciones WebSocket
13. Accesibilidad WCAG 2.2 AA
14. CI/CD Pipeline
15. Testing ≥80% coverage

## PASO 2: BUSCAR COBERTURA EN PLAN

**Comandos:**
```bash
# Verificar cada requisito
grep -r "FastAPI 0.104.1" contracts/plan/
grep -r "Pydantic v2" contracts/plan/
grep -r "Next.js 15" contracts/plan/
grep -r "React 19" contracts/plan/
grep -r "JWT" contracts/plan/
grep -r "OAuth 2.0" contracts/plan/
grep -r "Google Classroom" contracts/plan/
grep -r "ApexCharts 5.3.5" contracts/plan/
grep -r "WebSocket" contracts/plan/
grep -r "WCAG 2.2 AA" contracts/plan/

# Contar menciones
for req in "FastAPI" "Next.js" "React" "JWT" "OAuth" "WebSocket"; do
  echo "$req: $(grep -rc "$req" contracts/plan/ | awk -F: '{sum+=$2} END {print sum}')"
done
```

## PASO 3: IDENTIFICAR GAPS

**Análisis:**
- Requisitos sin cobertura
- Requisitos parcialmente cubiertos
- Requisitos obsoletos en plan

## OUTPUT ESPERADO: RESUMEN EJECUTIVO

# Resumen Ejecutivo: Trazabilidad del Plan

## 🎯 Objetivo Cumplido
Análisis de cobertura de requisitos en el plan de desarrollo.

## 📊 Resultados Principales
**Requisitos analizados:** 15
**Requisitos cubiertos:** 15
**Cobertura:** 100%

### Desglose por Requisito
- ✅ FastAPI 0.104.1: 12 menciones en 5 archivos
- ✅ Pydantic v2: 8 menciones en 3 archivos
- ✅ Next.js 15: 10 menciones en 4 archivos
- ✅ React 19: 9 menciones en 4 archivos
- ✅ JWT Authentication: 15 menciones en 3 archivos
- ✅ OAuth 2.0 Google: 18 menciones en 3 archivos
- ✅ Sistema de roles: 7 menciones en 2 archivos
- ✅ Google Classroom API: 25 menciones en 4 archivos
- ✅ Dashboards por rol: 12 menciones en 2 archivos
- ✅ ApexCharts 5.3.5: 6 menciones en 2 archivos
- ✅ Búsqueda avanzada: 8 menciones en 2 archivos
- ✅ Notificaciones WebSocket: 10 menciones en 2 archivos
- ✅ WCAG 2.2 AA: 5 menciones en 1 archivo
- ✅ CI/CD Pipeline: 9 menciones en 2 archivos
- ✅ Testing ≥80%: 15 menciones en 4 archivos

## ⚠️ Hallazgos Críticos
Ninguno - Todos los requisitos están cubiertos.

## ✅ Recomendaciones
1. Mantener sincronización con especificaciones
2. Ejecutar este análisis después de cada actualización de specs
3. Agregar requisitos nuevos inmediatamente al plan

## 📈 Estado General
✅ PASS (100% cobertura, objetivo: ≥95%)
```

---

## 4. PROMPT_ANALYZE_PLAN_COHERENCE

```markdown
# PROMPT: Análisis de Coherencia del Plan

## OBJETIVO
Validar consistencia de términos técnicos en todo el plan de desarrollo.

## SCOPE
- **Directorio**: `/contracts/plan/`
- **Prioridad**: ALTA
- **Criterio de éxito**: ≥85% de coherencia

## TÉRMINOS A VALIDAR

**Versiones de tecnologías:**
- FastAPI: debe ser "0.104.1" siempre
- Next.js: debe ser "15" siempre
- React: debe ser "19" siempre
- Pydantic: debe ser "v2" siempre
- ApexCharts: debe ser "5.3.5" siempre
- TypeScript: debe ser "5.1.6" siempre
- Tailwind CSS: debe ser "3.3.3" siempre

**Configuraciones:**
- Puerto: debe ser "8000" siempre
- Cobertura: debe ser "≥80%" siempre
- Testing: debe ser "Vitest + Playwright" (NO Jest)

**Metodología:**
- TDD: debe ser "estricto" o "Red-Green-Refactor"
- Seguridad: debe ser "cero confianza"
- Accesibilidad: debe ser "WCAG 2.2 AA"

## COMANDOS DE VERIFICACIÓN

```bash
# Verificar versiones
grep -r "FastAPI" contracts/plan/ | grep -v "0.104.1"
grep -r "Next\.js" contracts/plan/ | grep -v "15"
grep -r "React" contracts/plan/ | grep -v "19"
grep -r "Pydantic" contracts/plan/ | grep -v "v2"
grep -r "ApexCharts" contracts/plan/ | grep -v "5.3.5"

# Verificar configuraciones
grep -r "puerto" contracts/plan/ | grep -v "8000"
grep -r "coverage\|cobertura" contracts/plan/ | grep -v "80%"

# Verificar que NO mencione Jest
grep -r "Jest" contracts/plan/

# Contar menciones correctas
echo "FastAPI 0.104.1: $(grep -rc "FastAPI 0.104.1" contracts/plan/ | awk -F: '{sum+=$2} END {print sum}')"
echo "Next.js 15: $(grep -rc "Next.js 15" contracts/plan/ | awk -F: '{sum+=$2} END {print sum}')"
echo "React 19: $(grep -rc "React 19" contracts/plan/ | awk -F: '{sum+=$2} END {print sum}')"
```

## OUTPUT ESPERADO: RESUMEN EJECUTIVO

# Resumen Ejecutivo: Coherencia del Plan

## 🎯 Objetivo Cumplido
Validación de consistencia de términos técnicos en el plan.

## 📊 Resultados Principales

### Versiones de Tecnologías
- ✅ FastAPI 0.104.1: 100% consistente (12/12 menciones)
- ✅ Next.js 15: 100% consistente (10/10 menciones)
- ✅ React 19: 100% consistente (9/9 menciones)
- ✅ Pydantic v2: 100% consistente (8/8 menciones)
- ✅ ApexCharts 5.3.5: 100% consistente (6/6 menciones)

### Configuraciones
- ✅ Puerto 8000: 100% consistente (8/8 menciones)
- ✅ Cobertura ≥80%: 100% consistente (15/15 menciones)
- ✅ Testing Vitest+Playwright: 100% consistente (NO Jest encontrado)

### Metodología
- ✅ TDD estricto: Mencionado consistentemente
- ✅ Cero confianza: Mencionado consistentemente
- ✅ WCAG 2.2 AA: Mencionado consistentemente

## ⚠️ Hallazgos Críticos
Ninguno - Todos los términos son consistentes.

## ✅ Recomendaciones
1. Mantener esta coherencia en futuras actualizaciones
2. Usar Edit tool con replace_all para cambios globales
3. Ejecutar este análisis después de cada actualización

## 📈 Estado General
✅ PASS (100% coherencia, objetivo: ≥85%)
```

---

## 5. PROMPT_ANALYZE_PLAN_DEPENDENCIES

```markdown
# PROMPT: Análisis de Dependencias del Plan

## OBJETIVO
Verificar que dependencias críticas entre fases estén documentadas y sean correctas.

## SCOPE
- **Directorio**: `/contracts/plan/`
- **Prioridad**: ALTA
- **Criterio de éxito**: 100% de dependencias documentadas

## DEPENDENCIAS A VALIDAR

**Fase 2 (Google Integration) requiere:**
- Fase 1 completada (100%)
- OAuth 2.0 configurado
- Sistema de roles funcionando
- JWT tokens funcionando

**Fase 3 (Visualización) requiere:**
- Fase 2 completada (100%)
- WebSocket support configurado
- ApexCharts integrado
- Dashboards base funcionando

**Fase 4 (Integración) requiere:**
- Fase 3 completada (100%)
- Tests E2E funcionando
- Google API mocks validados
- Performance < 2s validado

## COMANDOS DE VERIFICACIÓN

```bash
# Buscar sección de dependencias en cada fase
grep -A 10 "Dependencias Bloqueantes" contracts/plan/03_plan_fase2*.md
grep -A 10 "Dependencias Bloqueantes" contracts/plan/04_plan_fase3*.md
grep -A 10 "Dependencias Bloqueantes" contracts/plan/05_plan_fase4*.md

# Verificar menciones de dependencias
grep -r "Fase 1 completada" contracts/plan/03_plan_fase2*.md
grep -r "Fase 2 completada" contracts/plan/04_plan_fase3*.md
grep -r "Fase 3 completada" contracts/plan/05_plan_fase4*.md

# Verificar dependencias técnicas
grep -r "OAuth 2.0" contracts/plan/03_plan_fase2*.md
grep -r "WebSocket" contracts/plan/04_plan_fase3*.md
grep -r "Tests E2E" contracts/plan/05_plan_fase4*.md
```

## OUTPUT ESPERADO: RESUMEN EJECUTIVO

# Resumen Ejecutivo: Dependencias del Plan

## 🎯 Objetivo Cumplido
Validación de dependencias entre fases del plan.

## 📊 Resultados Principales

### Fase 2: Google Integration
**Dependencias documentadas:**
- ✅ Fase 1 completada (100%): Documentado
- ✅ OAuth 2.0 configurado: Documentado
- ✅ Sistema de roles funcionando: Documentado
- ✅ JWT tokens funcionando: Documentado

**Ubicación:** `03_plan_fase2_google_integration.md` líneas 15-22

### Fase 3: Visualización Avanzada
**Dependencias documentadas:**
- ✅ Fase 2 completada (100%): Documentado
- ✅ WebSocket support configurado: Documentado
- ✅ ApexCharts integrado: Documentado
- ✅ Dashboards base funcionando: Documentado

**Ubicación:** `04_plan_fase3_visualizacion.md` líneas 12-18

### Fase 4: Integración Completa
**Dependencias documentadas:**
- ✅ Fase 3 completada (100%): Documentado
- ✅ Tests E2E funcionando: Documentado
- ✅ Google API mocks validados: Documentado
- ✅ Performance < 2s validado: Documentado

**Ubicación:** `05_plan_fase4_integracion.md` líneas 14-20

## ⚠️ Hallazgos Críticos
Ninguno - Todas las dependencias están documentadas.

## ✅ Recomendaciones
1. Verificar cumplimiento de dependencias antes de iniciar cada fase
2. Agregar comandos de verificación de dependencias
3. Documentar dependencias nuevas inmediatamente

## 📈 Estado General
✅ PASS (100% dependencias documentadas)
```

---

## 6. PROMPT_ANALYZE_PLAN_PATTERNS

```markdown
# PROMPT: Análisis de Patrones del Plan

## OBJETIVO
Verificar consistencia de patrones arquitectónicos y metodológicos en el plan.

## SCOPE
- **Directorio**: `/contracts/plan/`
- **Prioridad**: MEDIA
- **Criterio de éxito**: ≥80% de consistencia

## PATRONES A VALIDAR

**1. TDD Estricto (Red-Green-Refactor)**
- Debe mencionarse en todas las fases
- Debe incluir ejemplos de ciclo TDD
- Tests antes de implementación

**2. Context-Aware Services**
- Chunking por prioridad (CRITICAL→LOW)
- Límites de tokens especificados
- Context ID único

**3. Anti Lost-in-the-Middle**
- Estructura INICIO-MEDIO-FINAL
- Información crítica en INICIO y FINAL
- Detalle en MEDIO

**4. Cero Confianza**
- Verificación obligatoria
- Escaneo automático (SAST, SCA)
- Prompt engineering de seguridad

**5. Logs Estructurados**
- Formato JSON
- Campos obligatorios
- Ubicación en /tmp/

## COMANDOS DE VERIFICACIÓN

```bash
# TDD
grep -c "Red-Green-Refactor\|TDD" contracts/plan/*.md

# Context-Aware
grep -c "Context-Aware\|chunking\|prioridad" contracts/plan/*.md

# Anti Lost-in-the-Middle
for file in contracts/plan/0[2-5]*.md; do
  echo "$file:"
  grep -c "## 🎯 INICIO:" "$file"
  grep -c "## 📅 MEDIO:" "$file"
  grep -c "## ✅ FINAL:" "$file"
done

# Cero Confianza
grep -c "cero confianza\|zero trust" contracts/plan/*.md

# Logs Estructurados
grep -c "JSON\|/tmp/classsphere" contracts/plan/*.md
```

## OUTPUT ESPERADO: RESUMEN EJECUTIVO

# Resumen Ejecutivo: Patrones del Plan

## 🎯 Objetivo Cumplido
Validación de consistencia de patrones arquitectónicos.

## 📊 Resultados Principales

### TDD Estricto
- **Menciones totales:** 25
- **Archivos con patrón:** 8/10
- **Consistencia:** 95%
- ✅ Presente en todas las fases

### Context-Aware Services
- **Menciones totales:** 18
- **Archivos con patrón:** 6/10
- **Consistencia:** 85%
- ✅ Chunking por prioridad aplicado

### Anti Lost-in-the-Middle
- **Archivos de fase con estructura:** 4/4
- **Consistencia:** 100%
- ✅ Estructura INICIO-MEDIO-FINAL completa

### Cero Confianza
- **Menciones totales:** 12
- **Archivos con patrón:** 4/10
- **Consistencia:** 90%
- ✅ Protocolos de seguridad documentados

### Logs Estructurados
- **Menciones totales:** 15
- **Archivos con patrón:** 5/10
- **Consistencia:** 88%
- ✅ Formato JSON especificado

## ⚠️ Hallazgos Críticos
Ninguno - Todos los patrones están presentes y consistentes.

## ✅ Recomendaciones
1. Mantener aplicación de patrones en actualizaciones
2. Agregar ejemplos de patrones en nuevas secciones
3. Documentar nuevos patrones si se introducen

## 📈 Estado General
✅ PASS (91% consistencia promedio, objetivo: ≥80%)
```

---

## 7. PROMPT_ANALYZE_PLAN_COMPLETENESS

```markdown
# PROMPT: Análisis de Completitud del Plan

## OBJETIVO
Validar que todas las funcionalidades de las especificaciones estén cubiertas en el plan.

## SCOPE
- **Directorio**: `/contracts/plan/`
- **Prioridad**: MEDIA
- **Criterio de éxito**: ≥95% de cobertura funcional

## FUNCIONALIDADES A VERIFICAR

**Del archivo 06_ClassSphere_funcionalidades.md:**

1. Autenticación y Autorización
   - JWT Authentication
   - OAuth 2.0 Google
   - Sistema de roles
   - Session management

2. Google Classroom Integration
   - Modo dual (Google/Mock)
   - API Integration completa
   - Sincronización bidireccional
   - Conflict resolution

3. Dashboards por Rol
   - Admin Dashboard
   - Coordinator Dashboard
   - Teacher Dashboard
   - Student Dashboard

4. Visualizaciones Avanzadas
   - ApexCharts interactivos
   - D3.js integration
   - Real-time updates
   - Export features

5. Sistema de Búsqueda
   - Multi-entity search
   - Contextual filters
   - Real-time results
   - Saved searches

6. Notificaciones
   - WebSocket real-time
   - Multi-channel
   - Smart alerts
   - Preferences

7. Métricas y Analytics
   - KPIs educativos
   - Predictive analytics
   - Real-time metrics
   - Custom metrics

8. Accesibilidad
   - WCAG 2.2 AA
   - Keyboard navigation
   - Screen reader
   - High contrast

9. Testing
   - Unit tests ≥80%
   - Integration tests
   - E2E tests
   - Performance tests

10. CI/CD Pipeline
    - GitHub Actions
    - Quality gates
    - Docker
    - Monitoring

## COMANDOS DE VERIFICACIÓN

```bash
# Verificar cada funcionalidad
for func in "JWT" "OAuth" "Dashboard" "ApexCharts" "WebSocket" "WCAG" "CI/CD"; do
  echo "$func: $(grep -rc "$func" contracts/plan/ | awk -F: '{sum+=$2} END {print sum}') menciones"
done

# Verificar dashboards por rol
grep -r "AdminDashboard\|CoordinatorDashboard\|TeacherDashboard\|StudentDashboard" contracts/plan/

# Verificar testing
grep -r "Unit.*test\|Integration.*test\|E2E.*test" contracts/plan/

# Contar funcionalidades cubiertas
grep -E "^###|^##" contracts/plan/0[2-5]*.md | wc -l
```

## OUTPUT ESPERADO: RESUMEN EJECUTIVO

# Resumen Ejecutivo: Completitud del Plan

## 🎯 Objetivo Cumplido
Validación de cobertura funcional del plan.

## 📊 Resultados Principales

**Funcionalidades totales:** 10
**Funcionalidades cubiertas:** 10
**Cobertura:** 100%

### Desglose por Funcionalidad

1. ✅ **Autenticación y Autorización**
   - JWT: 15 menciones
   - OAuth 2.0: 18 menciones
   - Roles: 7 menciones
   - Ubicación: Fase 1

2. ✅ **Google Classroom Integration**
   - Modo dual: 12 menciones
   - API Integration: 25 menciones
   - Sync: 8 menciones
   - Ubicación: Fase 2 y 4

3. ✅ **Dashboards por Rol**
   - 4 dashboards documentados
   - Componentes específicos
   - Ubicación: Fase 2

4. ✅ **Visualizaciones Avanzadas**
   - ApexCharts: 6 menciones
   - Interactividad: Documentada
   - Ubicación: Fase 2 y 3

5. ✅ **Sistema de Búsqueda**
   - Búsqueda avanzada: 8 menciones
   - Filtros: Documentados
   - Ubicación: Fase 3

6. ✅ **Notificaciones**
   - WebSocket: 10 menciones
   - Real-time: Documentado
   - Ubicación: Fase 3

7. ✅ **Métricas y Analytics**
   - KPIs: Documentados
   - Analytics: 5 menciones
   - Ubicación: Fase 2 y 3

8. ✅ **Accesibilidad**
   - WCAG 2.2 AA: 5 menciones
   - Completo en Fase 4
   - Ubicación: Fase 4

9. ✅ **Testing**
   - Estrategia completa
   - Archivo dedicado
   - Ubicación: 06_plan_testing_strategy.md

10. ✅ **CI/CD Pipeline**
    - GitHub Actions: 9 menciones
    - Docker: Documentado
    - Ubicación: Fase 4

## ⚠️ Hallazgos Críticos
Ninguno - Todas las funcionalidades están cubiertas.

## ✅ Recomendaciones
1. Mantener cobertura al agregar nuevas funcionalidades
2. Actualizar plan cuando specs agreguen features
3. Verificar implementación vs plan periódicamente

## 📈 Estado General
✅ PASS (100% cobertura, objetivo: ≥95%)
```

---

## 8. PROMPT_ANALYZE_PLAN_COMPLEXITY

```markdown
# PROMPT: Análisis de Complejidad del Plan

## OBJETIVO
Analizar complejidad de instrucciones para asegurar ejecutabilidad por LLM.

## SCOPE
- **Directorio**: `/contracts/plan/`
- **Prioridad**: BAJA
- **Criterio de éxito**: Complejidad ≤ MEDIUM

## MÉTRICAS DE COMPLEJIDAD

**Por archivo de fase:**
- Días totales
- Pasos promedio por día
- Comandos promedio por paso
- Condicionales por sección
- Nivel de anidación

**Umbrales:**
- Pasos por día: ≤10
- Comandos por paso: ≤5
- Condicionales: ≤3
- Anidación: ≤2 niveles

## COMANDOS DE ANÁLISIS

```bash
# Contar días en cada fase
for file in contracts/plan/0[2-5]*.md; do
  echo "$file:"
  grep -c "^### Día" "$file"
done

# Contar pasos/comandos
awk '/^### Día/,/^### Día/ {
  if(/^#### |^\*\*/) steps++
  if(/```bash/) commands++
} END {
  print "Steps:", steps
  print "Commands:", commands
}' contracts/plan/02_plan_fase1*.md

# Buscar condicionales
grep -c "if\|cuando\|si.*entonces" contracts/plan/0[2-5]*.md

# Buscar anidación profunda
grep -E "^####|^#####|^######" contracts/plan/0[2-5]*.md
```

## OUTPUT ESPERADO: RESUMEN EJECUTIVO

# Resumen Ejecutivo: Complejidad del Plan

## 🎯 Objetivo Cumplido
Análisis de complejidad de instrucciones del plan.

## 📊 Resultados por Fase

### Fase 1: Fundaciones
- **Días:** 12
- **Pasos promedio/día:** 4.5
- **Comandos promedio/paso:** 3.2
- **Condicionales:** 2
- **Nivel anidación:** 2
- **Complejidad:** MEDIUM
- ✅ Dentro de umbrales

### Fase 2: Google Integration
- **Días:** 10
- **Pasos promedio/día:** 3.8
- **Comandos promedio/paso:** 2.9
- **Condicionales:** 1
- **Nivel anidación:** 2
- **Complejidad:** LOW
- ✅ Dentro de umbrales

### Fase 3: Visualización
- **Días:** 10
- **Pasos promedio/día:** 3.5
- **Comandos promedio/paso:** 2.5
- **Condicionales:** 1
- **Nivel anidación:** 2
- **Complejidad:** LOW
- ✅ Dentro de umbrales

### Fase 4: Integración
- **Días:** 13
- **Pasos promedio/día:** 4.0
- **Comandos promedio/paso:** 3.0
- **Condicionales:** 2
- **Nivel anidación:** 2
- **Complejidad:** MEDIUM
- ✅ Dentro de umbrales

## ⚠️ Hallazgos Críticos
Ninguno - Complejidad dentro de límites aceptables.

## ✅ Recomendaciones
1. Mantener pasos simples y directos
2. Evitar condicionales complejos
3. Dividir días con >10 pasos
4. Limitar comandos por paso a 5

## 📈 Estado General
✅ PASS (Complejidad promedio: LOW-MEDIUM, objetivo: ≤MEDIUM)
```

---

## 9. PROMPT_ANALYZE_PLAN_RISKS

```markdown
# PROMPT: Análisis de Riesgos del Plan

## OBJETIVO
Identificar y validar mitigación de riesgos técnicos en el plan.

## SCOPE
- **Directorio**: `/contracts/plan/`
- **Prioridad**: BAJA
- **Criterio de éxito**: 100% de riesgos mitigados

## RIESGOS A VALIDAR

**1. Dependencias Externas**
- **Riesgo:** Google API no disponible
- **Mitigación esperada:** Mocks completos

**2. Compatibilidad de Versiones**
- **Riesgo:** Incompatibilidad entre librerías
- **Mitigación esperada:** Versiones específicas documentadas

**3. Timeouts de Testing**
- **Riesgo:** Tests que cuelgan indefinidamente
- **Mitigación esperada:** Timeouts configurados

**4. Performance**
- **Riesgo:** Carga lenta de dashboards
- **Mitigación esperada:** Métricas < 2s documentadas

**5. Security Vulnerabilities**
- **Riesgo:** Vulnerabilidades en dependencias
- **Mitigación esperada:** Escaneo automático (SAST, SCA, Trivy)

**6. Context Window Overflow**
- **Riesgo:** Pérdida de contexto en LLM
- **Mitigación esperada:** Chunking por prioridad

**7. Testing Coverage**
- **Riesgo:** Código sin tests
- **Mitigación esperada:** TDD estricto, coverage ≥80%

**8. OAuth Failures**
- **Riesgo:** Fallos en autenticación Google
- **Mitigación esperada:** PKCE + State validation

## COMANDOS DE VERIFICACIÓN

```bash
# Verificar mitigaciones
grep -r "mock" contracts/plan/03_plan_fase2*.md
grep -r "timeout" contracts/plan/06_plan_testing*.md
grep -r "performance\|<2s" contracts/plan/
grep -r "SAST\|SCA\|Trivy" contracts/plan/07_plan_security*.md
grep -r "chunking\|prioridad" contracts/plan/08_plan_context*.md
grep -r "TDD\|coverage" contracts/plan/
grep -r "PKCE\|State validation" contracts/plan/02_plan_fase1*.md
```

## OUTPUT ESPERADO: RESUMEN EJECUTIVO

# Resumen Ejecutivo: Riesgos del Plan

## 🎯 Objetivo Cumplido
Validación de mitigación de riesgos técnicos.

## 📊 Resultados por Riesgo

### 1. Dependencias Externas
- **Severidad:** HIGH
- **Mitigación:** ✅ Documentada
- **Detalles:** Mock service completo en Fase 2
- **Ubicación:** 03_plan_fase2_google_integration.md

### 2. Compatibilidad de Versiones
- **Severidad:** HIGH
- **Mitigación:** ✅ Documentada
- **Detalles:** Versiones específicas en todos los archivos
- **Ubicación:** Todas las fases

### 3. Timeouts de Testing
- **Severidad:** MEDIUM
- **Mitigación:** ✅ Documentada
- **Detalles:** 30s unit, 60s integration, 120s E2E
- **Ubicación:** 06_plan_testing_strategy.md

### 4. Performance
- **Severidad:** MEDIUM
- **Mitigación:** ✅ Documentada
- **Detalles:** Métricas < 2s especificadas
- **Ubicación:** 09_plan_evaluation_metrics.md

### 5. Security Vulnerabilities
- **Severidad:** CRITICAL
- **Mitigación:** ✅ Documentada
- **Detalles:** SAST, SCA, Trivy en CI/CD
- **Ubicación:** 07_plan_security_protocols.md

### 6. Context Window Overflow
- **Severidad:** MEDIUM
- **Mitigación:** ✅ Documentada
- **Detalles:** Chunking CRITICAL→LOW
- **Ubicación:** 08_plan_context_management.md

### 7. Testing Coverage
- **Severidad:** HIGH
- **Mitigación:** ✅ Documentada
- **Detalles:** TDD estricto, ≥80% coverage
- **Ubicación:** 06_plan_testing_strategy.md

### 8. OAuth Failures
- **Severidad:** HIGH
- **Mitigación:** ✅ Documentada
- **Detalles:** PKCE + State validation
- **Ubicación:** 02_plan_fase1_fundaciones.md

## ⚠️ Hallazgos Críticos
Ninguno - Todos los riesgos están mitigados.

## ✅ Recomendaciones
1. Revisar mitigaciones durante implementación
2. Agregar nuevos riesgos identificados
3. Actualizar mitigaciones si cambian tecnologías
4. Ejecutar análisis de riesgos periódicamente

## 📈 Estado General
✅ PASS (8/8 riesgos mitigados, 100%)
```

---

## 10. PROMPT_ANALYZE_PLAN_QUALITY

```markdown
# PROMPT: Análisis de Calidad del Plan

## OBJETIVO
Evaluar calidad global del plan usando métricas objetivas.

## SCOPE
- **Directorio**: `/contracts/plan/`
- **Prioridad**: BAJA
- **Criterio de éxito**: Calidad ≥90%

## MÉTRICAS A CALCULAR

**1. Precisión**
```
Precisión = (Especificaciones cumplidas / Especificaciones totales) × 100
Objetivo: ≥95%
```

**2. Completitud**
```
Completitud = (Archivos creados / Archivos requeridos) × 100
Objetivo: 100%
```

**3. Coherencia**
```
Coherencia = (Términos consistentes / Términos totales) × 100
Objetivo: ≥85%
```

**4. Seguridad**
```
Seguridad = (Protocolos implementados / Protocolos requeridos) × 100
Objetivo: 100%
```

**5. Calidad Global**
```
Calidad = (Precisión + Completitud + Coherencia + Seguridad) / 4
Objetivo: ≥90%
```

## COMANDOS DE CÁLCULO

```bash
# Precisión - contar specs cumplidas
SPECS_TOTAL=20
SPECS_CUMPLIDAS=$(grep -rc "FastAPI 0.104.1\|Next.js 15\|React 19" contracts/plan/ | awk -F: '{sum+=$2} END {print sum}')
PRECISION=$((SPECS_CUMPLIDAS * 100 / SPECS_TOTAL))

# Completitud - contar archivos
FILES_REQUIRED=10
FILES_CREATED=$(ls contracts/plan/*.md | wc -l)
COMPLETITUD=$((FILES_CREATED * 100 / FILES_REQUIRED))

# Coherencia - verificar términos
TERMS_TOTAL=10
TERMS_CONSISTENT=$(grep -r "FastAPI 0.104.1" contracts/plan/ | wc -l)
COHERENCIA=$((TERMS_CONSISTENT * 100 / TERMS_TOTAL))

# Seguridad - contar protocolos
PROTOCOLS_REQUIRED=5
PROTOCOLS_IMPLEMENTED=$(grep -c "SAST\|SCA\|Trivy\|PKCE\|Cero Confianza" contracts/plan/07_plan_security*.md)
SEGURIDAD=$((PROTOCOLS_IMPLEMENTED * 100 / PROTOCOLS_REQUIRED))

# Calidad global
CALIDAD=$(( (PRECISION + COMPLETITUD + COHERENCIA + SEGURIDAD) / 4 ))
```

## OUTPUT ESPERADO: RESUMEN EJECUTIVO

# Resumen Ejecutivo: Calidad del Plan

## 🎯 Objetivo Cumplido
Evaluación de calidad global del plan de desarrollo.

## 📊 Métricas Principales

### 1. Precisión
- **Valor:** 96%
- **Objetivo:** ≥95%
- **Estado:** ✅ PASS
- **Detalles:** 19/20 especificaciones cumplidas

### 2. Completitud
- **Valor:** 100%
- **Objetivo:** 100%
- **Estado:** ✅ PASS
- **Detalles:** 10/10 archivos creados

### 3. Coherencia
- **Valor:** 95%
- **Objetivo:** ≥85%
- **Estado:** ✅ PASS
- **Detalles:** Términos consistentes en todo el plan

### 4. Seguridad
- **Valor:** 100%
- **Objetivo:** 100%
- **Estado:** ✅ PASS
- **Detalles:** Todos los protocolos implementados

### 5. Calidad Global
- **Valor:** 97.75%
- **Objetivo:** ≥90%
- **Estado:** ✅ EXCELLENT
- **Clasificación:** EXCELLENT (≥90%)

## 📈 Desglose Detallado

**Fortalezas:**
- ✅ Completitud perfecta (100%)
- ✅ Seguridad completa (100%)
- ✅ Alta precisión (96%)
- ✅ Excelente coherencia (95%)

**Áreas de Mejora:**
- Agregar especificación faltante para 100% precisión

## ✅ Recomendaciones
1. Mantener calidad en actualizaciones futuras
2. Ejecutar este análisis después de cambios mayores
3. Documentar nuevas métricas si se introducen
4. Celebrar la excelente calidad lograda 🎉

## 📈 Estado General
✅ EXCELLENT (97.75% calidad, objetivo: ≥90%)

**Clasificación:**
- 90-100%: EXCELLENT ← **Aquí estamos**
- 80-89%: GOOD
- 70-79%: ACCEPTABLE
- <70%: NEEDS IMPROVEMENT
```

---

# ANÁLISIS DE ESPECIFICACIONES

## 11. PROMPT_ANALYZE_SPECS_TRACEABILITY

```markdown
# PROMPT: Análisis de Trazabilidad de Especificaciones

## OBJETIVO
Verificar que todos los requisitos en especificaciones estén claramente definidos y sean trazables.

## SCOPE
- **Directorio**: `/contracts/principal/`
- **Prioridad**: ALTA
- **Criterio de éxito**: 100% de requisitos identificables

## PASO 1: EXTRAER REQUISITOS

**Archivos a analizar:**
```bash
# Objetivos
grep -E "^###|^-" contracts/principal/04_ClassSphere_objetivos.md

# Funcionalidades
grep -E "^##|^###" contracts/principal/06_ClassSphere_funcionalidades.md

# API Endpoints
grep -E "^POST|^GET|^PUT|^DELETE" contracts/principal/07_ClassSphere_api_endpoints.md

# Testing
grep -E "^###|^-" contracts/principal/09_ClassSphere_testing.md
```

## PASO 2: VERIFICAR CLARIDAD

**Criterios de claridad:**
- Requisito tiene ID o nombre único
- Descripción clara y sin ambigüedades
- Criterios de aceptación definidos
- Prioridad especificada

## PASO 3: VERIFICAR TRAZABILIDAD

**Comandos:**
```bash
# Contar requisitos por tipo
echo "Objetivos backend: $(grep -c "^### " contracts/principal/04_ClassSphere_objetivos.md)"
echo "Funcionalidades: $(grep -c "^## " contracts/principal/06_ClassSphere_funcionalidades.md)"
echo "Endpoints: $(grep -c "^POST\|^GET\|^PUT\|^DELETE" contracts/principal/07_ClassSphere_api_endpoints.md)"

# Verificar referencias cruzadas
grep -r "consulte\|ver\|referencia" contracts/principal/
```

## OUTPUT ESPERADO: RESUMEN EJECUTIVO

# Resumen Ejecutivo: Trazabilidad de Especificaciones

## 🎯 Objetivo Cumplido
Validación de claridad y trazabilidad de requisitos en especificaciones.

## 📊 Resultados Principales

**Requisitos identificados:** 150
**Requisitos claros:** 150
**Requisitos trazables:** 150
**Claridad:** 100%

### Desglose por Documento

**04_ClassSphere_objetivos.md:**
- Objetivos backend: 15
- Objetivos frontend: 12
- Objetivos integrados: 8
- ✅ Todos claros y trazables

**06_ClassSphere_funcionalidades.md:**
- Funcionalidades principales: 10
- Subfuncionalidades: 45
- ✅ Todas con descripción clara

**07_ClassSphere_api_endpoints.md:**
- Endpoints documentados: 50
- ✅ Todos con método, path y descripción

**09_ClassSphere_testing.md:**
- Estrategias: 5
- Requisitos de cobertura: 10
- ✅ Todos medibles

## ⚠️ Hallazgos Críticos
Ninguno - Todos los requisitos son claros y trazables.

## ✅ Recomendaciones
1. Mantener este nivel de claridad en actualizaciones
2. Agregar IDs únicos a nuevos requisitos
3. Documentar criterios de aceptación siempre
4. Mantener referencias cruzadas actualizadas

## 📈 Estado General
✅ PASS (100% trazabilidad)
```

---

## 12. PROMPT_ANALYZE_SPECS_COHERENCE

```markdown
# PROMPT: Análisis de Coherencia de Especificaciones

## OBJETIVO
Validar consistencia de términos técnicos en las especificaciones.

## SCOPE
- **Directorio**: `/contracts/principal/`
- **Prioridad**: ALTA
- **Criterio de éxito**: ≥85% de coherencia

## TÉRMINOS A VALIDAR

**Versiones:**
- FastAPI, Next.js, React, Pydantic, ApexCharts

**Configuraciones:**
- Puerto, Cobertura, Testing stack

**Metodología:**
- TDD, Seguridad, Accesibilidad

## COMANDOS DE VERIFICACIÓN

```bash
# Verificar versiones
grep -r "FastAPI" contracts/principal/ | grep -v "0.104.1"
grep -r "Next\.js" contracts/principal/ | grep -v "15"
grep -r "React" contracts/principal/ | grep -v "19"

# Verificar configuraciones
grep -r "puerto" contracts/principal/ | grep -v "8000"

# Contar menciones correctas
echo "FastAPI 0.104.1: $(grep -rc "FastAPI 0.104.1" contracts/principal/ | awk -F: '{sum+=$2} END {print sum}')"
```

## OUTPUT ESPERADO: RESUMEN EJECUTIVO

# Resumen Ejecutivo: Coherencia de Especificaciones

## 🎯 Objetivo Cumplido
Validación de consistencia de términos en especificaciones.

## 📊 Resultados Principales

### Versiones de Tecnologías
- ✅ FastAPI 0.104.1: 100% consistente (8/8)
- ✅ Next.js 15: 100% consistente (6/6)
- ✅ React 19: 100% consistente (5/5)
- ✅ Pydantic v2: 100% consistente (4/4)

### Configuraciones
- ✅ Puerto 8000: 100% consistente (5/5)
- ✅ Cobertura ≥80%: 100% consistente (10/10)

## ⚠️ Hallazgos Críticos
Ninguno - Todos los términos son consistentes.

## ✅ Recomendaciones
1. Mantener coherencia en actualizaciones
2. Validar nuevos términos antes de agregar
3. Usar búsqueda/reemplazo global para cambios

## 📈 Estado General
✅ PASS (100% coherencia, objetivo: ≥85%)
```

---

## 13. PROMPT_ANALYZE_SPECS_DEPENDENCIES

```markdown
# PROMPT: Análisis de Dependencias de Especificaciones

## OBJETIVO
Verificar que dependencias entre componentes estén identificadas en especificaciones.

## SCOPE
- **Directorio**: `/contracts/principal/`
- **Prioridad**: ALTA
- **Criterio de éxito**: 100% de dependencias identificadas

## DEPENDENCIAS A BUSCAR

**Dependencias técnicas:**
- OAuth requiere JWT
- Dashboards requieren autenticación
- Visualizaciones requieren datos
- Sync requiere Google API

**Dependencias de fase:**
- Fase 2 requiere Fase 1
- Fase 3 requiere Fase 2
- Fase 4 requiere Fase 3

## COMANDOS

```bash
# Buscar menciones de dependencias
grep -r "requiere\|depende\|necesita" contracts/principal/

# Verificar documentación de dependencias
grep -A 5 "Dependencias" contracts/principal/10_ClassSphere_plan_implementacion.md
```

## OUTPUT ESPERADO: RESUMEN EJECUTIVO

# Resumen Ejecutivo: Dependencias de Especificaciones

## 🎯 Objetivo Cumplido
Validación de identificación de dependencias.

## 📊 Resultados Principales

**Dependencias identificadas:** 15
**Dependencias documentadas:** 15
**Cobertura:** 100%

### Dependencias Técnicas
- ✅ OAuth → JWT: Documentado
- ✅ Dashboards → Auth: Documentado
- ✅ Visualizaciones → Datos: Documentado
- ✅ Sync → Google API: Documentado

### Dependencias de Fase
- ✅ Fase 2 → Fase 1: Documentado
- ✅ Fase 3 → Fase 2: Documentado
- ✅ Fase 4 → Fase 3: Documentado

## ⚠️ Hallazgos Críticos
Ninguno - Todas las dependencias identificadas.

## ✅ Recomendaciones
1. Documentar nuevas dependencias inmediatamente
2. Mantener matriz de dependencias actualizada
3. Validar dependencias antes de implementación

## 📈 Estado General
✅ PASS (100% dependencias identificadas)
```

---

## 14. PROMPT_ANALYZE_SPECS_PATTERNS

```markdown
# PROMPT: Análisis de Patrones de Especificaciones

## OBJETIVO
Verificar que patrones arquitectónicos estén claramente definidos en especificaciones.

## SCOPE
- **Directorio**: `/contracts/principal/`
- **Prioridad**: MEDIA
- **Criterio de éxito**: ≥80% de patrones documentados

## PATRONES A BUSCAR

1. TDD Estricto
2. Context-Aware Services
3. Anti Lost-in-the-Middle
4. Cero Confianza
5. Logs Estructurados

## COMANDOS

```bash
grep -c "TDD\|Test-Driven" contracts/principal/*.md
grep -c "Context-Aware\|contexto" contracts/principal/*.md
grep -c "Lost-in-the-Middle" contracts/principal/*.md
grep -c "Cero Confianza\|Zero Trust" contracts/principal/*.md
```

## OUTPUT ESPERADO: RESUMEN EJECUTIVO

# Resumen Ejecutivo: Patrones de Especificaciones

## 🎯 Objetivo Cumplido
Validación de definición de patrones arquitectónicos.

## 📊 Resultados Principales

**Patrones totales:** 5
**Patrones documentados:** 5
**Cobertura:** 100%

### Desglose por Patrón
- ✅ TDD Estricto: 12 menciones
- ✅ Context-Aware: 8 menciones
- ✅ Anti Lost-in-the-Middle: 6 menciones
- ✅ Cero Confianza: 5 menciones
- ✅ Logs Estructurados: 7 menciones

## ⚠️ Hallazgos Críticos
Ninguno - Todos los patrones están documentados.

## ✅ Recomendaciones
1. Agregar ejemplos de implementación
2. Documentar nuevos patrones si se introducen
3. Mantener consistencia en definiciones

## 📈 Estado General
✅ PASS (100% patrones documentados, objetivo: ≥80%)
```

---

## 15. PROMPT_ANALYZE_SPECS_COMPLETENESS

```markdown
# PROMPT: Análisis de Completitud de Especificaciones

## OBJETIVO
Verificar que todas las áreas del sistema estén documentadas en especificaciones.

## SCOPE
- **Directorio**: `/contracts/principal/`
- **Prioridad**: MEDIA
- **Criterio de éxito**: ≥95% de áreas cubiertas

## ÁREAS A VERIFICAR

1. Arquitectura
2. Funcionalidades
3. API Endpoints
4. Modelos de Datos
5. Testing
6. Deployment
7. Seguridad
8. Accesibilidad

## COMANDOS

```bash
# Verificar archivos de especificaciones
ls contracts/principal/*.md

# Contar secciones por área
for file in contracts/principal/*.md; do
  echo "$(basename $file): $(grep -c "^##" $file) secciones"
done
```

## OUTPUT ESPERADO: RESUMEN EJECUTIVO

# Resumen Ejecutivo: Completitud de Especificaciones

## 🎯 Objetivo Cumplido
Validación de cobertura de áreas del sistema.

## 📊 Resultados Principales

**Áreas totales:** 8
**Áreas documentadas:** 8
**Cobertura:** 100%

### Desglose por Área
- ✅ Arquitectura: 05_ClassSphere_arquitectura.md
- ✅ Funcionalidades: 06_ClassSphere_funcionalidades.md
- ✅ API Endpoints: 07_ClassSphere_api_endpoints.md
- ✅ Modelos de Datos: 08_ClassSphere_modelos_datos.md
- ✅ Testing: 09_ClassSphere_testing.md
- ✅ Deployment: 11_ClassSphere_deployment.md
- ✅ Seguridad: Integrado en múltiples archivos
- ✅ Accesibilidad: 06_ClassSphere_funcionalidades.md

## ⚠️ Hallazgos Críticos
Ninguno - Todas las áreas están documentadas.

## ✅ Recomendaciones
1. Mantener cobertura al agregar nuevas áreas
2. Actualizar documentación regularmente
3. Validar completitud periódicamente

## 📈 Estado General
✅ PASS (100% cobertura, objetivo: ≥95%)
```

---

## 16. PROMPT_ANALYZE_SPECS_COMPLEXITY

```markdown
# PROMPT: Análisis de Complejidad de Especificaciones

## OBJETIVO
Evaluar claridad y simplicidad de las especificaciones.

## SCOPE
- **Directorio**: `/contracts/principal/`
- **Prioridad**: BAJA
- **Criterio de éxito**: Complejidad ≤ MEDIUM

## MÉTRICAS

- Longitud promedio de secciones
- Nivel de anidación
- Uso de jerga técnica
- Claridad de ejemplos

## COMANDOS

```bash
# Contar niveles de encabezados
grep -E "^#{4,}" contracts/principal/*.md | wc -l

# Contar palabras por archivo
for file in contracts/principal/*.md; do
  wc -w "$file"
done
```

## OUTPUT ESPERADO: RESUMEN EJECUTIVO

# Resumen Ejecutivo: Complejidad de Especificaciones

## 🎯 Objetivo Cumplido
Evaluación de claridad de especificaciones.

## 📊 Resultados Principales

**Complejidad promedio:** LOW-MEDIUM
**Claridad:** ALTA

### Desglose por Archivo
- 04_objetivos.md: LOW
- 05_arquitectura.md: MEDIUM
- 06_funcionalidades.md: LOW
- 09_testing.md: MEDIUM

## ⚠️ Hallazgos Críticos
Ninguno - Especificaciones claras y comprensibles.

## ✅ Recomendaciones
1. Mantener claridad en actualizaciones
2. Agregar ejemplos cuando sea necesario
3. Evitar anidación profunda

## 📈 Estado General
✅ PASS (Complejidad LOW-MEDIUM, objetivo: ≤MEDIUM)
```

---

## 17. PROMPT_ANALYZE_SPECS_RISKS

```markdown
# PROMPT: Análisis de Riesgos de Especificaciones

## OBJETIVO
Verificar que riesgos técnicos estén identificados en especificaciones.

## SCOPE
- **Directorio**: `/contracts/principal/`
- **Prioridad**: BAJA
- **Criterio de éxito**: Principales riesgos identificados

## RIESGOS A BUSCAR

1. Dependencias externas
2. Compatibilidad
3. Performance
4. Seguridad
5. Escalabilidad

## COMANDOS

```bash
grep -r "riesgo\|risk\|problema\|issue" contracts/principal/
grep -r "mitigación\|mitigation" contracts/principal/
```

## OUTPUT ESPERADO: RESUMEN EJECUTIVO

# Resumen Ejecutivo: Riesgos de Especificaciones

## 🎯 Objetivo Cumplido
Identificación de riesgos en especificaciones.

## 📊 Resultados Principales

**Riesgos identificados:** 5
**Riesgos con mitigación:** 5
**Cobertura:** 100%

### Riesgos Documentados
- ✅ Google API dependency: Identificado
- ✅ Compatibilidad versiones: Identificado
- ✅ Performance requirements: Identificado
- ✅ Security vulnerabilities: Identificado
- ✅ Context overflow: Identificado

## ⚠️ Hallazgos Críticos
Ninguno - Principales riesgos identificados.

## ✅ Recomendaciones
1. Documentar nuevos riesgos al identificarlos
2. Actualizar mitigaciones regularmente
3. Revisar riesgos antes de cada fase

## 📈 Estado General
✅ PASS (Principales riesgos identificados)
```

---

## 18. PROMPT_ANALYZE_SPECS_QUALITY

```markdown
# PROMPT: Análisis de Calidad de Especificaciones

## OBJETIVO
Evaluar calidad global de las especificaciones.

## SCOPE
- **Directorio**: `/contracts/principal/`
- **Prioridad**: BAJA
- **Criterio de éxito**: Calidad ≥90%

## MÉTRICAS

1. Claridad (≥90%)
2. Completitud (100%)
3. Coherencia (≥85%)
4. Trazabilidad (100%)

## COMANDOS

```bash
# Contar archivos
ls contracts/principal/*.md | wc -l

# Verificar coherencia
grep -r "FastAPI" contracts/principal/ | grep -v "0.104.1"

# Verificar completitud
grep -c "^##" contracts/principal/*.md
```

## OUTPUT ESPERADO: RESUMEN EJECUTIVO

# Resumen Ejecutivo: Calidad de Especificaciones

## 🎯 Objetivo Cumplido
Evaluación de calidad global de especificaciones.

## 📊 Métricas Principales

### 1. Claridad
- **Valor:** 95%
- **Estado:** ✅ PASS

### 2. Completitud
- **Valor:** 100%
- **Estado:** ✅ PASS

### 3. Coherencia
- **Valor:** 100%
- **Estado:** ✅ PASS

### 4. Trazabilidad
- **Valor:** 100%
- **Estado:** ✅ PASS

### 5. Calidad Global
- **Valor:** 98.75%
- **Estado:** ✅ EXCELLENT

## ⚠️ Hallazgos Críticos
Ninguno - Especificaciones de excelente calidad.

## ✅ Recomendaciones
1. Mantener este nivel de calidad
2. Validar calidad después de actualizaciones
3. Usar como referencia para nuevos documentos

## 📈 Estado General
✅ EXCELLENT (98.75% calidad, objetivo: ≥90%)
```

---

# ANÁLISIS COMPARATIVO

## 19. PROMPT_COMPARE_PLAN_SPECS

```markdown
# PROMPT: Comparar Plan con Especificaciones

## OBJETIVO
Verificar que el plan esté completamente sincronizado con las especificaciones.

## SCOPE
- **Source**: `/contracts/principal/` (especificaciones)
- **Target**: `/contracts/plan/` (plan de desarrollo)
- **Prioridad**: ALTA
- **Criterio de éxito**: ≥98% de sincronización

## PASO 1: COMPARAR REQUISITOS

**Comandos:**
```bash
# Extraer requisitos de specs
grep -r "FastAPI\|Next.js\|React\|OAuth\|JWT" contracts/principal/ > /tmp/specs_requirements.txt

# Extraer requisitos de plan
grep -r "FastAPI\|Next.js\|React\|OAuth\|JWT" contracts/plan/ > /tmp/plan_requirements.txt

# Comparar
diff /tmp/specs_requirements.txt /tmp/plan_requirements.txt
```

## PASO 2: COMPARAR VERSIONES

**Comandos:**
```bash
# Versión en specs
SPECS_FASTAPI=$(grep -m1 "FastAPI" contracts/principal/05_ClassSphere_arquitectura.md | grep -oP '\d+\.\d+\.\d+')

# Versión en plan
PLAN_FASTAPI=$(grep -m1 "FastAPI" contracts/plan/02_plan_fase1_fundaciones.md | grep -oP '\d+\.\d+\.\d+')

# Comparar
if [ "$SPECS_FASTAPI" != "$PLAN_FASTAPI" ]; then
  echo "MISMATCH: Specs=$SPECS_FASTAPI, Plan=$PLAN_FASTAPI"
fi
```

## PASO 3: COMPARAR FUNCIONALIDADES

**Comandos:**
```bash
# Funcionalidades en specs
SPECS_FEATURES=$(grep -c "^### " contracts/principal/06_ClassSphere_funcionalidades.md)

# Funcionalidades en plan
PLAN_FEATURES=$(grep -rc "Funcionalidad\|Feature" contracts/plan/0[2-5]*.md | awk -F: '{sum+=$2} END {print sum}')

# Calcular cobertura
COVERAGE=$((PLAN_FEATURES * 100 / SPECS_FEATURES))
echo "Cobertura: $COVERAGE%"
```

## PASO 4: IDENTIFICAR GAPS

**Análisis:**
- Requisitos en specs pero no en plan
- Requisitos en plan pero no en specs
- Versiones desincronizadas
- Funcionalidades faltantes

## OUTPUT ESPERADO: RESUMEN EJECUTIVO

# Resumen Ejecutivo: Comparación Plan vs Especificaciones

## 🎯 Objetivo Cumplido
Verificación de sincronización entre plan y especificaciones.

## 📊 Resultados de Comparación

### 1. Trazabilidad Bidireccional
**Requisitos en specs:** 150
**Requisitos en plan:** 147
**Sincronización:** 98%

**Faltantes en plan:**
- ❌ Requisito de backup automático diario
- ❌ Requisito de notificaciones por Telegram
- ❌ Requisito de exportación a Excel

**Extra en plan:**
- ℹ️ Detalles de implementación tmux (no en specs)

### 2. Coherencia de Versiones
- ✅ FastAPI: 0.104.1 (sincronizado)
- ✅ Next.js: 15 (sincronizado)
- ✅ React: 19 (sincronizado)
- ✅ Pydantic: v2 (sincronizado)
- ✅ ApexCharts: 5.3.5 (sincronizado)

### 3. Cobertura Funcional
**Funcionalidades en specs:** 10
**Funcionalidades en plan:** 10
**Cobertura:** 100%

### 4. Completitud Cruzada
- ✅ Autenticación: Sincronizado
- ✅ Google Integration: Sincronizado
- ✅ Dashboards: Sincronizado
- ✅ Visualizaciones: Sincronizado
- ✅ Testing: Sincronizado
- ✅ CI/CD: Sincronizado
- ✅ Accesibilidad: Sincronizado

## ⚠️ Hallazgos Críticos

**Desincronizaciones encontradas:**
1. **Backup automático diario** no está en plan
   - Severidad: MEDIUM
   - Acción: Agregar a Fase 4

2. **Notificaciones Telegram** no está en plan
   - Severidad: LOW
   - Acción: Agregar a Fase 3 (ya está como mock)

3. **Exportación Excel** no está en plan
   - Severidad: LOW
   - Acción: Agregar a Fase 3

## ✅ Recomendaciones

**Inmediatas:**
1. Actualizar Fase 4 con backup automático diario
2. Verificar que Telegram esté como mock en Fase 3
3. Agregar exportación Excel en Fase 3

**A corto plazo:**
4. Ejecutar este análisis después de cada cambio en specs
5. Mantener sincronización bidireccional
6. Documentar cambios en ambos lados

**A largo plazo:**
7. Automatizar verificación de sincronización
8. Crear matriz de trazabilidad
9. Implementar CI check para sincronización

## 📈 Estado General
⚠️ NEEDS_SYNC (98% sincronización, objetivo: ≥98%)

**Acciones requeridas:** 3
**Prioridad:** MEDIUM
**Tiempo estimado:** 2 horas
```

---

## 20. PROMPT_SYNC_CHECK

```markdown
# PROMPT: Verificar Sincronización Plan-Specs

## OBJETIVO
Verificación rápida de sincronización entre plan y especificaciones.

## SCOPE
- **Source**: `/contracts/principal/`
- **Target**: `/contracts/plan/`
- **Prioridad**: ALTA
- **Criterio de éxito**: 100% sincronizado

## VERIFICACIONES RÁPIDAS

### 1. Versiones de Tecnologías

```bash
# Comparar FastAPI
diff <(grep "FastAPI" contracts/principal/05_ClassSphere_arquitectura.md | head -1) \
     <(grep "FastAPI" contracts/plan/02_plan_fase1_fundaciones.md | head -1)

# Comparar Next.js
diff <(grep "Next.js" contracts/principal/05_ClassSphere_arquitectura.md | head -1) \
     <(grep "Next.js" contracts/plan/02_plan_fase1_fundaciones.md | head -1)

# Comparar React
diff <(grep "React" contracts/principal/05_ClassSphere_arquitectura.md | head -1) \
     <(grep "React" contracts/plan/02_plan_fase1_fundaciones.md | head -1)
```

### 2. Última Modificación

```bash
# Ver última modificación de specs
git log -1 --format="%ai" contracts/principal/

# Ver última modificación de plan
git log -1 --format="%ai" contracts/plan/

# Comparar timestamps
```

### 3. Conteo de Requisitos

```bash
# Contar en specs
SPECS_COUNT=$(grep -rc "FastAPI\|OAuth\|JWT\|WebSocket" contracts/principal/ | awk -F: '{sum+=$2} END {print sum}')

# Contar en plan
PLAN_COUNT=$(grep -rc "FastAPI\|OAuth\|JWT\|WebSocket" contracts/plan/ | awk -F: '{sum+=$2} END {print sum}')

# Comparar
echo "Specs: $SPECS_COUNT, Plan: $PLAN_COUNT"
```

### 4. Cambios Pendientes

```bash
# Ver si hay cambios no sincronizados
git diff HEAD contracts/principal/ --name-only
git diff HEAD contracts/plan/ --name-only
```

## OUTPUT ESPERADO: RESUMEN EJECUTIVO

# Resumen Ejecutivo: Verificación de Sincronización

## 🎯 Objetivo Cumplido
Verificación rápida de sincronización plan-specs.

## 📊 Resultados de Verificación

### 1. Versiones de Tecnologías
- ✅ FastAPI: Sincronizado (0.104.1)
- ✅ Next.js: Sincronizado (15)
- ✅ React: Sincronizado (19)
- ✅ Pydantic: Sincronizado (v2)
- ✅ ApexCharts: Sincronizado (5.3.5)

### 2. Timestamps
- **Specs última modificación:** 2025-10-05 06:45:00
- **Plan última modificación:** 2025-10-05 07:30:00
- **Diferencia:** 45 minutos
- ✅ Plan más reciente que specs

### 3. Conteo de Requisitos
- **Specs:** 150 menciones
- **Plan:** 147 menciones
- **Diferencia:** 3 menciones (2%)
- ⚠️ Pequeña desincronización

### 4. Cambios Pendientes
- **Specs sin commit:** 0 archivos
- **Plan sin commit:** 0 archivos
- ✅ Todo commiteado

## ⚠️ Hallazgos

**Desincronización menor detectada:**
- 3 menciones de requisitos faltantes en plan
- Diferencia: 2%
- Severidad: LOW

## ✅ Recomendaciones

**Si sincronización < 98%:**
1. Ejecutar PROMPT_COMPARE_PLAN_SPECS para análisis detallado
2. Identificar requisitos faltantes
3. Actualizar plan con PROMPT_UPDATE_PLAN

**Si sincronización ≥ 98%:**
1. Monitorear cambios en specs
2. Ejecutar sync check después de cada actualización
3. Mantener sincronización proactiva

## 📈 Estado General
✅ SYNCHRONIZED (98% sync, objetivo: ≥98%)

**Próxima verificación:** Después de próximo cambio en specs
**Frecuencia recomendada:** Después de cada actualización
```

---

## 21. PROMPT_ANALYZE_BEST_PRACTICES_COMPLIANCE

```markdown
# PROMPT: Análisis de Cumplimiento con Mejores Prácticas LLM

## OBJETIVO
Verificar que el plan de desarrollo cumple completamente con las mejores prácticas definidas en @SOFTWARE_PROJECT_BEST_PRACTICES.md.

## SCOPE
- **Source**: @SOFTWARE_PROJECT_BEST_PRACTICES.md (mejores prácticas)
- **Target**: `/contracts/plan/` (plan de desarrollo)
- **Prioridad**: CRITICAL
- **Criterio de éxito**: ≥95% de cumplimiento

## PASO 1: EXTRAER REQUISITOS DE MEJORES PRÁCTICAS

**Archivo fuente:**
```bash
# Leer mejores prácticas
cat contracts/extra/SOFTWARE_PROJECT_BEST_PRACTICES.md
```

**Requisitos clave a verificar:**
1. **Context Window Management**
   - Chunking por prioridad (CRITICAL/HIGH/MEDIUM/LOW)
   - Estructura anti lost-in-the-middle
   - Logs estructurados con context_id

2. **Arquitectura Context-Aware**
   - Servicios conscientes del contexto
   - Gestión de memoria optimizada
   - Identificadores únicos por fase

3. **Seguridad y Verificación**
   - Principio de cero confianza
   - Escaneo automático (SAST, SCA, Secrets)
   - Prompt engineering de seguridad

4. **Métricas de Evaluación**
   - Precisión ≥95%
   - Calidad técnica ≥90%
   - Coherencia semántica ≥85%

5. **Optimización de Recursos**
   - Balance entre tamaño y costo
   - Fine-tuning vs construcción desde cero
   - Gestión eficiente de contexto

## PASO 2: VERIFICAR CUMPLIMIENTO EN PLAN

**Comandos de verificación:**
```bash
# Context Window Management
grep -r "chunking\|prioridad\|CRITICAL\|HIGH\|MEDIUM\|LOW" contracts/plan/
grep -r "lost-in-the-middle\|INICIO.*MEDIO.*FINAL" contracts/plan/
grep -r "context_id\|token_count\|logs estructurados" contracts/plan/

# Arquitectura Context-Aware
grep -r "Context-Aware\|consciente.*contexto\|gestión.*memoria" contracts/plan/
grep -r "identificador.*único\|context.*management" contracts/plan/

# Seguridad y Verificación
grep -r "cero confianza\|zero trust\|SAST\|SCA" contracts/plan/
grep -r "escaneo.*automático\|secrets.*detection" contracts/plan/
grep -r "prompt.*engineering.*seguridad" contracts/plan/

# Métricas de Evaluación
grep -r "precisión.*95\|calidad.*90\|coherencia.*85" contracts/plan/
grep -r "métricas.*evaluación\|medición.*objetiva" contracts/plan/

# Optimización de Recursos
grep -r "balance.*tamaño.*costo\|optimización.*recursos" contracts/plan/
grep -r "fine-tuning\|gestión.*eficiente" contracts/plan/
```

## PASO 3: CALCULAR CUMPLIMIENTO POR CATEGORÍA

**Fórmula de cumplimiento:**
```
Cumplimiento = (Requisitos implementados / Requisitos totales) × 100
```

**Categorías a evaluar:**
1. Context Window Management (5 requisitos)
2. Arquitectura Context-Aware (3 requisitos)
3. Seguridad y Verificación (3 requisitos)
4. Métricas de Evaluación (3 requisitos)
5. Optimización de Recursos (3 requisitos)

## PASO 4: IDENTIFICAR GAPS Y RECOMENDACIONES

**Análisis de gaps:**
- Requisitos no implementados
- Implementación parcial
- Requisitos mal documentados
- Inconsistencias encontradas

## OUTPUT ESPERADO: RESUMEN EJECUTIVO

# Resumen Ejecutivo: Cumplimiento con Mejores Prácticas LLM

## 🎯 Objetivo Cumplido
Verificación de cumplimiento del plan con @SOFTWARE_PROJECT_BEST_PRACTICES.md.

## 📊 Resultados de Cumplimiento

**Cumplimiento global:** 96%
**Criterio de éxito:** ≥95%
**Estado:** ✅ PASS

### Desglose por Categoría

#### 1. Context Window Management
- **Requisitos:** 5
- **Implementados:** 5
- **Cumplimiento:** 100%
- **Estado:** ✅ EXCELLENT

**Detalles:**
- ✅ Chunking por prioridad: CRITICAL/HIGH/MEDIUM/LOW implementado
- ✅ Estructura anti lost-in-the-middle: INICIO-MEDIO-FINAL presente
- ✅ Logs estructurados: context_id y token_count documentados
- ✅ Límites de tokens: 2000/1500/1000/800 especificados
- ✅ Gestión de contexto: Optimizada para LLMs

#### 2. Arquitectura Context-Aware
- **Requisitos:** 3
- **Implementados:** 3
- **Cumplimiento:** 100%
- **Estado:** ✅ EXCELLENT

**Detalles:**
- ✅ Servicios conscientes del contexto: Documentados
- ✅ Gestión de memoria: Optimizada con seguimiento
- ✅ Identificadores únicos: Por fase implementado

#### 3. Seguridad y Verificación
- **Requisitos:** 3
- **Implementados:** 3
- **Cumplimiento:** 100%
- **Estado:** ✅ EXCELLENT

**Detalles:**
- ✅ Principio de cero confianza: Aplicado completamente
- ✅ Escaneo automático: SAST, SCA, Secrets detection
- ✅ Prompt engineering de seguridad: Integrado

#### 4. Métricas de Evaluación
- **Requisitos:** 3
- **Implementados:** 3
- **Cumplimiento:** 100%
- **Estado:** ✅ EXCELLENT

**Detalles:**
- ✅ Precisión ≥95%: Documentada y verificable
- ✅ Calidad técnica ≥90%: Métricas específicas
- ✅ Coherencia semántica ≥85%: Validada

#### 5. Optimización de Recursos
- **Requisitos:** 3
- **Implementados:** 2
- **Cumplimiento:** 67%
- **Estado:** ⚠️ NEEDS IMPROVEMENT

**Detalles:**
- ✅ Balance entre tamaño y costo: Considerado
- ❌ Fine-tuning vs construcción desde cero: No especificado
- ✅ Gestión eficiente de contexto: Implementada

## ⚠️ Hallazgos Críticos

**Gap identificado:**
- **Optimización de Recursos**: Falta especificación de fine-tuning vs construcción desde cero
- **Severidad**: MEDIUM
- **Impacto**: Bajo (no afecta funcionalidad core)

## ✅ Recomendaciones

### Inmediatas
1. **Agregar especificación de fine-tuning**: Documentar cuándo usar fine-tuning vs construcción desde cero
2. **Completar optimización de recursos**: Llegar a 100% cumplimiento

### A corto plazo
3. **Mantener cumplimiento**: Ejecutar este análisis después de cada actualización
4. **Documentar nuevas mejores prácticas**: Si se agregan al documento fuente

### A largo plazo
5. **Automatizar verificación**: Crear script que valide cumplimiento automáticamente
6. **Integrar en CI/CD**: Verificar cumplimiento como parte del pipeline

## 📈 Beneficios del Cumplimiento

### Técnicos
- **Context Management**: Optimización de ventana de contexto para LLMs
- **Seguridad**: Protección completa con principio de cero confianza
- **Calidad**: Métricas objetivas y verificables
- **Eficiencia**: Gestión optimizada de recursos

### Operacionales
- **Mantenibilidad**: Plan estructurado y coherente
- **Escalabilidad**: Arquitectura preparada para crecimiento
- **Confiabilidad**: Verificación automática de cumplimiento
- **Documentación**: Estándares claros y aplicables

## 📈 Estado General
✅ EXCELLENT (96% cumplimiento, objetivo: ≥95%)

**Clasificación:**
- 95-100%: EXCELLENT ← **Aquí estamos**
- 85-94%: GOOD
- 70-84%: ACCEPTABLE
- <70%: NEEDS IMPROVEMENT

**Próxima verificación:** Después de próxima actualización del plan
**Frecuencia recomendada:** Después de cada cambio mayor
```

---

## 22. PROMPT_CLEAN_REPO_KEEP_CONTRACTS

```markdown
# PROMPT: Limpiar Repositorio y Mantener Solo Contracts

## OBJETIVO
Eliminar todo el contenido del repositorio EXCEPTO el directorio `/contracts/` y su contenido, manteniendo el historial de Git completo y creando un commit descriptivo.

## ⚠️ ADVERTENCIA CRÍTICA
Esta operación es **DESTRUCTIVA** e **IRREVERSIBLE**. Asegúrate de:
1. Tener un backup completo del repositorio
2. Estar absolutamente seguro de que quieres eliminar todo excepto `/contracts/`
3. Haber verificado que `/contracts/` contiene todo lo necesario

## CONTEXTO
- **Directorio a preservar**: `/contracts/` y todo su contenido
- **Archivo a preservar**: `CLAUDE.md` (notas de desarrollo)
- **Directorios a eliminar**: backend/, frontend/, scripts/, etc.
- **Historial Git**: Se mantiene intacto
- **Acción**: Crear commit completo documentando la limpieza

## PASO 1: VERIFICAR ESTADO ACTUAL

**Comandos de verificación:**
```bash
# Ver estructura actual del repositorio
tree -L 2 -a

# Ver qué hay en contracts/
ls -la contracts/

# Ver tamaño de contracts/
du -sh contracts/

# Ver archivos en Git
git ls-files

# Ver estado actual
git status
```

## PASO 2: CREAR BACKUP DE SEGURIDAD

**⚠️ OBLIGATORIO antes de continuar:**
```bash
# Crear backup completo
cd ..
tar -czf classsphere-backup-$(date +%Y%m%d-%H%M%S).tar.gz ClassSphere/
ls -lh classsphere-backup-*.tar.gz

# Verificar backup
tar -tzf classsphere-backup-*.tar.gz | head -20

# Volver al repositorio
cd ClassSphere/
```

## PASO 3: IDENTIFICAR ARCHIVOS A ELIMINAR

**Comandos de análisis:**
```bash
# Listar todos los directorios de primer nivel
ls -d */ | grep -v "contracts/"

# Listar todos los archivos de primer nivel
ls -p | grep -v /

# Ver todo lo que NO es contracts/
find . -maxdepth 1 ! -name "." ! -name ".git" ! -name "contracts" -type d
find . -maxdepth 1 ! -name "." ! -name ".git" ! -name "contracts" -type f
```

**Directorios típicos a eliminar:**
- backend/
- frontend/
- scripts/
- .benchmarks/
- node_modules/ (si existe)
- venv/ (si existe)
- __pycache__/ (si existe)

**Archivos típicos a eliminar:**
- README.md (si existe)
- package.json (si existe)
- requirements.txt (si existe)

**Archivos a preservar:**
- CLAUDE.md (notas de desarrollo)
- .gitignore (opcional, puede mantenerse)

## PASO 4: ELIMINAR ARCHIVOS Y DIRECTORIOS

**Comandos de eliminación:**
```bash
# Eliminar directorios (CUIDADO: IRREVERSIBLE)
rm -rf backend/
rm -rf frontend/
rm -rf scripts/
rm -rf .benchmarks/
rm -rf node_modules/
rm -rf venv/
rm -rf __pycache__/

# Eliminar archivos específicos (preservando CLAUDE.md y .gitignore)
rm -f README.md
rm -f package.json
rm -f requirements.txt

# O eliminar todos excepto CLAUDE.md y .gitignore
find . -maxdepth 1 -type f ! -name ".gitignore" ! -name "CLAUDE.md" -delete

# Verificar que contracts/ sigue intacto
ls -la contracts/
tree contracts/ -L 2
```

## PASO 5: VERIFICAR ELIMINACIÓN

**Comandos de verificación:**
```bash
# Ver estructura resultante
tree -L 2 -a

# Debe mostrar solo:
# .
# ├── .git/
# ├── CLAUDE.md
# ├── contracts/
# │   ├── extra/
# │   ├── plan/
# │   ├── principal/
# │   └── prompt/
# └── .gitignore (opcional)

# Ver estado de Git
git status

# Debe mostrar muchos archivos eliminados
```

## PASO 6: AGREGAR CAMBIOS A GIT

**Comandos:**
```bash
# Agregar todos los cambios (eliminaciones)
git add -A

# Verificar qué se va a commitear
git status

# Ver resumen de cambios
git diff --staged --stat

# Ver archivos eliminados
git diff --staged --name-only --diff-filter=D | wc -l
```

## PASO 7: CREAR COMMIT COMPLETO

**Mensaje de commit:**
```bash
git commit -m "[repo] Clean repository - Keep only contracts directory

DESTRUCTIVE OPERATION: Removed all code and kept only documentation.

Directories removed:
- backend/ (FastAPI application code)
- frontend/ (Next.js application code)
- scripts/ (automation scripts)
- .benchmarks/ (performance benchmarks)
- node_modules/ (if existed)
- venv/ (if existed)

Files removed:
- README.md (project readme)
- package.json (frontend dependencies)
- requirements.txt (backend dependencies)
- All other root-level files (except CLAUDE.md)

Directories preserved:
- contracts/ (complete documentation)
  - contracts/extra/ (best practices, guides)
  - contracts/plan/ (development plan)
  - contracts/principal/ (specifications)
  - contracts/prompt/ (management prompts)

Files preserved:
- CLAUDE.md (development notes and context)
- .gitignore (Git ignore rules)

Reason for cleanup:
Repository restructuring to maintain only documentation and specifications.
All implementation code removed to focus on planning and design phase.

Git history:
- Full Git history preserved
- All commits maintained
- Branch history intact

Backup created:
- File: classsphere-backup-YYYYMMDD-HHMMSS.tar.gz
- Location: Parent directory
- Size: [size]

Next steps:
1. Verify contracts/ integrity
2. Push to remote if needed
3. Start fresh implementation from plan
4. Use contracts/plan/ as source of truth

Verification commands:
- tree -L 2 -a
- ls -la contracts/
- git log --oneline -10

Status: ✅ Repository cleaned successfully
Impact: MAJOR - All implementation code removed
Reversibility: Use backup file to restore if needed"
```

## PASO 8: VERIFICAR COMMIT

**Comandos de verificación:**
```bash
# Ver commit creado
git log -1

# Ver estadísticas del commit
git log -1 --stat

# Ver archivos eliminados en el commit
git show HEAD --name-only --diff-filter=D

# Ver archivos que quedan en el repositorio
git ls-files

# Verificar que contracts/ está completo
git ls-files | grep "^contracts/"
```

## PASO 9: VALIDAR INTEGRIDAD DE CONTRACTS

**Comandos de validación:**
```bash
# Verificar estructura de contracts/
tree contracts/

# Verificar archivos principales
ls -la contracts/plan/
ls -la contracts/principal/
ls -la contracts/prompt/
ls -la contracts/extra/

# Contar archivos en contracts/
find contracts/ -type f | wc -l

# Verificar que no hay archivos corruptos
find contracts/ -type f -exec file {} \; | grep -v "text"

# Verificar tamaño total
du -sh contracts/
```

## PASO 10: PUSH A REMOTO (OPCIONAL)

**⚠️ Solo si estás seguro:**
```bash
# Ver remoto configurado
git remote -v

# Push del commit (CUIDADO: esto es permanente en el remoto)
git push origin main

# O crear una nueva rama para la limpieza
git checkout -b repo-cleanup
git push origin repo-cleanup
```

## OUTPUT ESPERADO: RESUMEN EJECUTIVO

# Resumen Ejecutivo: Limpieza de Repositorio

## 🎯 Objetivo Cumplido
Repositorio limpiado exitosamente, manteniendo solo `/contracts/` y historial Git completo.

## 📊 Estadísticas de Limpieza

### Directorios Eliminados
- ✅ backend/ (eliminado)
- ✅ frontend/ (eliminado)
- ✅ scripts/ (eliminado)
- ✅ .benchmarks/ (eliminado)
- ✅ node_modules/ (eliminado, si existía)
- ✅ venv/ (eliminado, si existía)

**Total directorios eliminados:** 6

### Archivos Eliminados
- ✅ README.md
- ✅ package.json
- ✅ requirements.txt
- ✅ Otros archivos de configuración

**Total archivos eliminados:** ~50+

### Contenido Preservado
- ✅ contracts/extra/ (3 archivos)
- ✅ contracts/plan/ (10 archivos)
- ✅ contracts/principal/ (15 archivos)
- ✅ contracts/prompt/ (1 archivo)
- ✅ CLAUDE.md (1 archivo)
- ✅ .gitignore (1 archivo)

**Total archivos preservados:** 31

## 📈 Estructura Resultante

```
ClassSphere/
├── .git/                    # Historial completo preservado
├── CLAUDE.md                # Notas de desarrollo preservadas
├── .gitignore              # Git ignore rules
└── contracts/
    ├── extra/
    │   ├── revision/
    │   ├── DOCKER_BEST_PRACTICES.md
    │   └── SOFTWARE_PROJECT_BEST_PRACTICES.md
    ├── plan/
    │   ├── 01_plan_index.md
    │   ├── 02_plan_fase1_fundaciones.md
    │   ├── 03_plan_fase2_google_integration.md
    │   ├── 04_plan_fase3_visualizacion.md
    │   ├── 05_plan_fase4_integracion.md
    │   ├── 06_plan_testing_strategy.md
    │   ├── 07_plan_security_protocols.md
    │   ├── 08_plan_context_management.md
    │   ├── 09_plan_evaluation_metrics.md
    │   └── README.md
    ├── principal/
    │   ├── 00_ClassSphere_index.md
    │   ├── 01_ClassSphere_info_status.md
    │   ├── ... (15 archivos totales)
    │   └── 14_ClassSphere_conclusion.md
    └── prompt/
        └── manage_plan_prompts.md
```

## ✅ Validaciones Realizadas

- ✅ Backup creado: classsphere-backup-YYYYMMDD-HHMMSS.tar.gz
- ✅ Estructura contracts/ intacta
- ✅ Todos los archivos de contracts/ preservados
- ✅ Historial Git completo mantenido
- ✅ Commit descriptivo creado
- ✅ No hay archivos corruptos
- ✅ Tamaño de contracts/: ~500KB

## 📝 Commit Creado

**Hash:** [commit-hash]
**Mensaje:** [repo] Clean repository - Keep only contracts directory
**Archivos modificados:** ~60 eliminaciones
**Líneas eliminadas:** ~50,000+
**Tamaño reducido:** ~95% del repositorio

## ⚠️ Información Importante

### Reversibilidad
- **Backup disponible:** classsphere-backup-YYYYMMDD-HHMMSS.tar.gz
- **Ubicación:** Directorio padre
- **Restauración:** `tar -xzf classsphere-backup-*.tar.gz`

### Historial Git
- **Commits preservados:** Todos
- **Branches preservados:** Todas
- **Tags preservados:** Todos
- **Acceso a código anterior:** `git checkout <commit-hash>`

### Próximos Pasos
1. ✅ Verificar integridad de contracts/
2. ⏳ Push a remoto (si es necesario)
3. ⏳ Comenzar implementación desde plan
4. ⏳ Usar contracts/plan/ como fuente de verdad

## 📈 Estado General
✅ LIMPIEZA EXITOSA - Repositorio optimizado para documentación

**Impacto:** MAJOR (código eliminado, documentación preservada)
**Reversibilidad:** ALTA (backup completo disponible)
**Riesgo:** BAJO (contracts/ verificado e intacto)
```

---

## ⚠️ CHECKLIST DE SEGURIDAD

Antes de ejecutar este prompt, verifica:

- [ ] **Backup creado y verificado**
- [ ] **Estás en el repositorio correcto**
- [ ] **Entiendes que esto es irreversible sin backup**
- [ ] **Has revisado qué hay en contracts/**
- [ ] **No hay trabajo sin commitear que necesites**
- [ ] **Tienes permisos para hacer esta operación**
- [ ] **Has informado al equipo (si aplica)**

## 🔄 Comandos de Restauración (Si es necesario)

```bash
# Si necesitas restaurar desde backup
cd ..
tar -xzf classsphere-backup-YYYYMMDD-HHMMSS.tar.gz
cd ClassSphere/

# O revertir el commit (antes de push)
git reset --hard HEAD~1

# O crear nueva rama desde commit anterior
git checkout -b restore-code HEAD~1
```

---

## 23. PROMPT_ANALYZE_UNIFIED_PLAN_SPECS

```markdown
# PROMPT: Análisis Unificado de Plan y Especificaciones ClassSphere

## OBJETIVO PRINCIPAL
Realizar análisis completo de trazabilidad, coherencia, dependencias, patrones, completitud, complejidad, riesgos y calidad para el plan de desarrollo (/contracts/plan/) o las especificaciones (/contracts/principal/).

## PREGUNTA INICIAL
¿Este análisis es para:
1. **Plan de desarrollo** (/contracts/plan/)
2. **Especificaciones** (/contracts/principal/)

Por favor, responde con "plan" o "especificaciones" para proceder.

---

## ANÁLISIS DEL PLAN (/contracts/plan/)

### 3. Análisis de Trazabilidad del Plan
Verificar que cada requisito de las especificaciones esté cubierto en el plan de desarrollo.

**Scope:** `/contracts/plan/` - Prioridad: ALTA - Criterio: ≥95% cobertura

**Pasos clave:**
1. Extraer requisitos de especificaciones
2. Buscar cobertura en plan
3. Identificar gaps

**Comandos de verificación:**
```bash
# Verificar requisitos clave
grep -r "FastAPI 0.104.1\|Next.js 15\|React 19" contracts/plan/
grep -r "JWT\|OAuth 2.0\|Google Classroom" contracts/plan/
grep -r "ApexCharts 5.3.5\|WebSocket\|WCAG 2.2 AA" contracts/plan/
```

### 4. Análisis de Coherencia del Plan
Validar consistencia de términos técnicos en todo el plan.

**Scope:** `/contracts/plan/` - Prioridad: ALTA - Criterio: ≥85% coherencia

**Términos a validar:**
- Versiones: FastAPI 0.104.1, Next.js 15, React 19, Pydantic v2, ApexCharts 5.3.5
- Configuraciones: Puerto 8000, Cobertura ≥80%, Testing Vitest + Playwright
- Metodología: TDD estricto, Cero confianza, WCAG 2.2 AA

### 5. Análisis de Dependencias del Plan
Verificar que dependencias críticas entre fases estén documentadas.

**Dependencias a validar:**
- Fase 2 requiere Fase 1 completada
- Fase 3 requiere Fase 2 completada
- Fase 4 requiere Fase 3 completada

### 6. Análisis de Patrones del Plan
Verificar consistencia de patrones arquitectónicos.

**Patrones a validar:**
1. TDD Estricto (Red-Green-Refactor)
2. Context-Aware Services (Chunking por prioridad)
3. Anti Lost-in-the-Middle (INICIO-MEDIO-FINAL)
4. Cero Confianza (Verificación obligatoria)
5. Logs Estructurados (JSON, /tmp/)

### 7. Análisis de Completitud del Plan
Validar cobertura de funcionalidades en especificaciones.

**Funcionalidades a verificar:**
1. Autenticación y Autorización
2. Google Classroom Integration
3. Dashboards por Rol
4. Visualizaciones Avanzadas
5. Sistema de Búsqueda
6. Notificaciones
7. Métricas y Analytics
8. Accesibilidad
9. Testing
10. CI/CD Pipeline

### 8. Análisis de Complejidad del Plan
Analizar complejidad de instrucciones para ejecutabilidad.

**Métricas:**
- Días totales, Pasos promedio/día, Comandos promedio/paso
- Condicionales por sección, Nivel de anidación
- Umbrales: ≤10 pasos/día, ≤5 comandos/paso, ≤3 condicionales

### 9. Análisis de Riesgos del Plan
Identificar y validar mitigación de riesgos técnicos.

**Riesgos a validar:**
1. Dependencias Externas (Google API)
2. Compatibilidad de Versiones
3. Timeouts de Testing
4. Performance
5. Security Vulnerabilities
6. Context Window Overflow
7. Testing Coverage
8. OAuth Failures

### 10. Análisis de Calidad del Plan
Evaluar calidad global usando métricas objetivas.

**Métricas:**
1. Precisión (≥95%)
2. Completitud (100%)
3. Coherencia (≥85%)
4. Seguridad (100%)
5. Calidad Global (≥90%)

---

## ANÁLISIS DE ESPECIFICACIONES (/contracts/principal/)

### 11. Análisis de Trazabilidad de Especificaciones
Verificar que requisitos estén claramente definidos y trazables.

**Scope:** `/contracts/principal/` - Prioridad: ALTA - Criterio: 100% identificables

### 12. Análisis de Coherencia de Especificaciones
Validar consistencia de términos técnicos.

### 13. Análisis de Dependencias de Especificaciones
Verificar que dependencias estén identificadas.

### 14. Análisis de Patrones de Especificaciones
Verificar definición clara de patrones arquitectónicos.

### 15. Análisis de Completitud de Especificaciones
Verificar cobertura de áreas del sistema.

### 16. Análisis de Complejidad de Especificaciones
Evaluar claridad y simplicidad.

### 17. Análisis de Riesgos de Especificaciones
Verificar identificación de riesgos técnicos.

### 18. Análisis de Calidad de Especificaciones
Evaluar calidad global de especificaciones.

---

## EJECUCIÓN DEL ANÁLISIS

**Basado en tu respuesta:**

**Si respondes "plan":**
- Ejecutar análisis completo del plan usando métricas 3-10
- Usar comandos específicos para `/contracts/plan/`
- Generar resumen ejecutivo con resultados del plan

**Si respondes "especificaciones":**
- Ejecutar análisis completo de especificaciones usando métricas 11-18
- Usar comandos específicos para `/contracts/principal/`
- Generar resumen ejecutivo con resultados de especificaciones

**Comandos generales de verificación (adaptar según respuesta):**
```bash
# Para plan
grep -r "término_buscado" contracts/plan/

# Para especificaciones
grep -r "término_buscado" contracts/principal/

# Contar menciones
echo "Término: $(grep -rc "término" contracts/plan/ | awk -F: '{sum+=$2} END {print sum}')"
```

## OUTPUT ESPERADO: RESUMEN EJECUTIVO

# Resumen Ejecutivo: Análisis Unificado [Plan/Especificaciones]

## 🎯 Objetivo Cumplido
Análisis completo de [trazabilidad/coherencia/dependencias/etc.] para [plan/especificaciones].

## 📊 Resultados Principales

### Métricas de Análisis
- **Trazabilidad:** X% (objetivo: ≥95%)
- **Coherencia:** X% (objetivo: ≥85%)
- **Dependencias:** X% documentadas (objetivo: 100%)
- **Patrones:** X% consistentes (objetivo: ≥80%)
- **Completitud:** X% (objetivo: ≥95%)
- **Complejidad:** [LOW/MEDIUM] (objetivo: ≤MEDIUM)
- **Riesgos:** X/X mitigados (objetivo: 100%)
- **Calidad:** X% (objetivo: ≥90%)

## ⚠️ Hallazgos Críticos
[Detallar gaps o problemas encontrados]

## ✅ Recomendaciones
1. [Acción inmediata]
2. [Acción a corto plazo]
3. [Acción a largo plazo]

## 📈 Estado General
✅ [PASS/NEEDS_IMPROVEMENT] - [Porcentaje] cumplimiento promedio

**Próxima verificación:** Después de próxima actualización
**Frecuencia recomendada:** Después de cambios mayores
```

---

# FIN DEL DOCUMENTO

## 📝 Notas Finales

**Total de prompts:** 23
**Fecha de creación:** 2025-10-05
**Versión:** 1.0

**Cómo usar este documento:**
1. Identificar la operación deseada (crear, actualizar, analizar)
2. Copiar el prompt correspondiente
3. Pegar en chat con LLM
4. Revisar resumen ejecutivo generado
5. Tomar acciones según recomendaciones

**Mantenimiento:**
- Actualizar prompts si cambian especificaciones
- Agregar nuevos prompts si se identifican necesidades
- Validar que outputs sigan formato de resumen ejecutivo

---

*Última actualización: 2025-10-06T16:42:34-03:00*
