---
id: "01"
title: "Create Development Plan"
category: "Gestión del Plan"
priority: "CRITICAL"
version: "2.0"
stack: "Go 1.21+ + Angular 19"
target: "/workspace/plan/"
source: "/workspace/contracts/"
date: "2025-10-07"
---

# PROMPT: Crear Nuevo Plan de Desarrollo ClassSphere

## OBJETIVO PRINCIPAL
Generar plan completo de desarrollo desde cero en `/workspace/plan/` siguiendo 100% las especificaciones de `@00_ClassSphere_index.md` y aplicando mejores prácticas de `@SOFTWARE_PROJECT_BEST_PRACTICES.md`.

## CONTEXTO DE EJECUCIÓN
- **Proyecto**: Repositorio vacío o sin plan existente
- **Enfoque**: Desarrollo desde cero con TDD estricto
- **Destino**: Crear estructura en `/workspace/plan/`
- **Audiencia**: LLM que ejecutará el plan paso a paso

## PASO 1: LEER ESPECIFICACIONES

**Archivos a leer:**
```bash
# Especificaciones principales
cat workspace/contracts/00_ClassSphere_index.md
cat workspace/contracts/04_ClassSphere_objetivos.md
cat workspace/contracts/05_ClassSphere_arquitectura.md
cat workspace/contracts/06_ClassSphere_funcionalidades.md
cat workspace/contracts/09_ClassSphere_testing.md
cat workspace/contracts/10_ClassSphere_plan_implementacion.md

# Mejores prácticas (si existen en workspace/extra/)
cat workspace/extra/SOFTWARE_PROJECT_BEST_PRACTICES.md
```

## PASO 2: EXTRAER REQUISITOS CLAVE

**Información crítica a extraer:**
- Stack tecnológico (versiones exactas)
- Metodología TDD-RunFix+
- Estructura de fases
- Cobertura de testing requerida
- Timeouts de testing
- Principios de seguridad
- Context management requirements
- Arquitectura hexagonal (ports & adapters)
- Puertos defaults (8080 backend, 4200 frontend)

## PASO 3: CREAR ARCHIVOS DEL PLAN

**Archivos a crear (usar write tool):**

### 3.1 Archivo Principal
- **Archivo**: `workspace/plan/01_plan_index.md`
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
- **Archivo**: `workspace/plan/02_plan_fase1_fundaciones.md`
- **Prioridad**: CRITICAL (2000 tokens max)
- **Duración**: 12 días
- **Contenido**:
  - Backend: Go 1.21+ + Echo v4 + JWT + OAuth 2.0 Google
  - Frontend: Angular 19 + esbuild + TailwindCSS 3.x
  - Testing: testify (Go) + Jasmine + Karma (Angular) + Playwright (E2E)
  - Puertos: 8080 (backend), 4200 (frontend)
  - Arquitectura: Hexagonal (ports & adapters) en backend
  - Instrucciones día por día con comandos específicos

### 3.3 Fase 2: Google Integration
- **Archivo**: `workspace/plan/03_plan_fase2_google_integration.md`
- **Prioridad**: HIGH (1500 tokens max)
- **Duración**: 10 días
- **Contenido**:
  - Google Classroom API con mocks
  - Modo dual (Google/Mock)
  - Dashboards por rol (4 tipos)
  - Gráficos interactivos

### 3.4 Fase 3: Visualización
- **Archivo**: `workspace/plan/04_plan_fase3_visualizacion.md`
- **Prioridad**: MEDIUM (1000 tokens max)
- **Duración**: 10 días
- **Contenido**:
  - Búsqueda avanzada multi-entidad
  - Notificaciones WebSocket real-time
  - Gráficos interactivos avanzados

### 3.5 Fase 4: Integración
- **Archivo**: `workspace/plan/05_plan_fase4_integracion.md`
- **Prioridad**: LOW (800 tokens max)
- **Duración**: 13 días
- **Contenido**:
  - Sincronización bidireccional Google
  - Accesibilidad WCAG 2.2 AA completa
  - CI/CD pipeline completo

### 3.6 Estrategia de Testing
- **Archivo**: `workspace/plan/06_plan_testing_strategy.md`
- **Contenido**:
  - Stack: testify (Go) + Jasmine + Karma (Angular) + Playwright (E2E)
  - Cobertura requerida: ≥80% global, ≥90% módulos críticos
  - Templates de tests
  - Comandos de verificación

### 3.7 Protocolos de Seguridad
- **Archivo**: `workspace/plan/07_plan_security_protocols.md`
- **Contenido**:
  - Principio de cero confianza
  - SAST, SCA, Secrets detection con Trivy
  - Prompt engineering de seguridad
  - Pipeline de seguridad CI/CD

### 3.8 Gestión de Contexto
- **Archivo**: `workspace/plan/08_plan_context_management.md`
- **Contenido**:
  - Chunking por prioridad (CRITICAL→LOW)
  - Estructura anti lost-in-the-middle
  - Logs estructurados con context_id
  - Context recovery mechanisms

### 3.9 Métricas de Evaluación
- **Archivo**: `workspace/plan/09_plan_evaluation_metrics.md`
- **Contenido**:
  - Precisión ≥95%
  - Completitud 100%
  - Coherencia ≥85%
  - Métricas técnicas (performance, cobertura, vulnerabilidades)

### 3.10 README
- **Archivo**: `workspace/plan/README.md`
- **Contenido**:
  - Descripción del plan
  - Guía de inicio rápido para LLMs
  - Stack tecnológico (Go + Angular)
  - Comandos de validación

## PASO 4: VALIDAR PLAN CREADO

**Comandos de validación:**
```bash
# Verificar archivos creados
ls -la workspace/plan/*.md | wc -l
# Debe retornar: 10

# Verificar estructura anti lost-in-the-middle
for file in workspace/plan/0[2-5]*.md; do
  echo "=== $file ==="
  grep -c "## 🎯 INICIO:" "$file"
  grep -c "## 📅 MEDIO:" "$file"
  grep -c "## ✅ FINAL:" "$file"
done

# Verificar coherencia de stack Go + Angular
grep -r "Go 1.21" workspace/plan/ | wc -l
grep -r "Angular 19" workspace/plan/ | wc -l
grep -r "Echo v4" workspace/plan/ | wc -l
grep -r "testify" workspace/plan/ | wc -l

# Verificar puertos defaults
grep -r "8080" workspace/plan/ | wc -l  # Backend
grep -r "4200" workspace/plan/ | wc -l  # Frontend

# Verificar que NO mencione tecnologías obsoletas
grep -r "FastAPI\|Next.js\|React\|Jest\|Vitest" workspace/plan/
# No debe retornar nada
```

## OUTPUT ESPERADO: RESUMEN EJECUTIVO

Generar resumen ejecutivo con este formato:

```markdown
# Resumen Ejecutivo: Creación del Plan ClassSphere

## 🎯 Objetivo Cumplido
Plan completo de desarrollo generado en `/workspace/plan/` con 10 archivos.

## 📊 Archivos Creados
- ✅ 01_plan_index.md (5.2 KB, CRITICAL)
- ✅ 02_plan_fase1_fundaciones.md (7.9 KB, CRITICAL)
- ✅ 03_plan_fase2_google_integration.md (9.4 KB, HIGH)
- ✅ 04_plan_fase3_visualizacion.md (11 KB, MEDIUM)
- ✅ 05_plan_fase4_integracion.md (12 KB, LOW)
- ✅ 06_plan_testing_strategy.md (13 KB)
- ✅ 07_plan_security_protocols.md (13 KB)
- ✅ 08_plan_context_management.md (12 KB)
- ✅ 09_plan_evaluation_metrics.md (10 KB)
- ✅ README.md (7.7 KB)

## 📈 Validaciones
- ✅ Estructura anti lost-in-the-middle: 100% (4/4 archivos de fase)
- ✅ Coherencia Go 1.21+: [X] menciones
- ✅ Coherencia Angular 19: [X] menciones
- ✅ Coherencia Echo v4: [X] menciones
- ✅ Coherencia testify: [X] menciones
- ✅ Puertos defaults (8080/4200): Verificados
- ✅ NO menciona tecnologías obsoletas: Correcto
- ✅ Chunking por prioridad: Aplicado

## ✅ Características del Plan
- Stack: Go 1.21+ (backend) + Angular 19 (frontend)
- Arquitectura: Hexagonal (ports & adapters) en backend
- Testing: testify + Jasmine + Karma + Playwright
- Puertos: 8080 (backend), 4200 (frontend) - defaults
- Completamente ejecutable desde repositorio vacío
- Instrucciones paso a paso sin ambigüedades
- TDD-RunFix+ estricto desde el inicio
- Seguridad de cero confianza
- Context management optimizado para LLMs
- Métricas objetivas de éxito

## 📍 Próximos Pasos
1. Revisar plan generado en `/workspace/plan/`
2. Comenzar con Fase 1: `cat workspace/plan/02_plan_fase1_fundaciones.md`
3. Ejecutar validaciones periódicas
4. Mantener sincronizado con especificaciones en `/workspace/contracts/`

## 📈 Estado General
✅ PLAN CREADO EXITOSAMENTE - Listo para ejecución
```

---

*Última actualización: 2025-10-07*

