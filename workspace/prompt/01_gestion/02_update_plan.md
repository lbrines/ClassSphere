---
id: "02"
title: "Update Development Plan"
category: "Gestión del Plan"
priority: "HIGH"
version: "2.0"
stack: "Go 1.21+ + Angular 19"
target: "/workspace/plan/"
source: "/workspace/contracts/"
date: "2025-10-07"
---

# PROMPT: Actualizar Plan de Desarrollo Existente

## OBJETIVO PRINCIPAL
Actualizar el plan en `/workspace/plan/` basado en cambios detectados en especificaciones (`/workspace/contracts/`) usando Git como herramienta de detección.

## CONTEXTO
- **Plan actual**: `/workspace/plan/` (10 archivos)
- **Especificaciones**: `/workspace/contracts/`
- **Método**: Git diff para detectar cambios
- **Acción**: Actualizar solo archivos afectados (NO crear nuevos)

## PASO 1: DETECTAR CAMBIOS CON GIT

**Comandos a ejecutar:**
```bash
# Ver cambios en especificaciones desde último commit
git diff HEAD workspace/contracts/

# Ver archivos modificados
git diff --name-only HEAD workspace/contracts/

# Ver cambios con contexto
git diff HEAD workspace/contracts/ --unified=5

# Ver historial reciente
git log --oneline -10 workspace/contracts/

# Ver cambios específicos en un archivo
git diff HEAD workspace/contracts/05_ClassSphere_arquitectura.md
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
git diff HEAD workspace/contracts/ | grep "^+" | head -20
git diff HEAD workspace/contracts/ | grep "^-" | head -20

# Buscar cambios críticos (Go + Angular stack)
git diff HEAD workspace/contracts/ | grep -i "version\|stack\|tdd\|security\|go\|angular"
```

**Clasificación:**
- **CRITICAL**: Stack tecnológico (Go/Angular), metodología TDD-RunFix+, seguridad, puertos
- **HIGH**: Nuevas funcionalidades, cambios en endpoints, arquitectura hexagonal
- **MEDIUM**: Cambios en documentación, refinamientos
- **LOW**: Typos, formateo, enlaces

## PASO 4: ACTUALIZAR ARCHIVOS DEL PLAN

**Para cada cambio identificado:**

1. **Localizar sección en plan:**
```bash
grep -n "término_buscado" workspace/plan/*.md
```

2. **Usar search_replace tool para actualizar:**
   - Preservar estructura INICIO-MEDIO-FINAL
   - Mantener chunking por prioridad
   - Actualizar comandos de verificación si aplica
   - Actualizar criterios de aceptación si aplica
   - Verificar stack Go + Angular (NO FastAPI/Next.js/React)

3. **Validar coherencia:**
```bash
# Verificar consistencia de términos (Go + Angular)
grep -c "Go 1.21" workspace/plan/*.md
grep -c "Angular 19" workspace/plan/*.md
grep -c "Echo v4" workspace/plan/*.md
grep "Go" workspace/plan/*.md | grep -v "1.21"
```

## PASO 5: VALIDAR ACTUALIZACIÓN

**Comandos de validación:**
```bash
# 1. Coherencia semántica (Go + Angular stack)
grep -r "Go 1.21" workspace/plan/ | wc -l
grep -r "Angular 19" workspace/plan/ | wc -l
grep -r "Echo v4" workspace/plan/ | wc -l
grep -r "testify" workspace/plan/ | wc -l

# Verificar que NO mencione tecnologías obsoletas
grep -r "FastAPI\|Next.js\|React\|Jest\|Vitest" workspace/plan/
# No debe retornar nada

# 2. Estructura anti lost-in-the-middle
for file in workspace/plan/0[2-5]*.md; do
  grep -c "## 🎯 INICIO:" "$file"
  grep -c "## 📅 MEDIO:" "$file"
  grep -c "## ✅ FINAL:" "$file"
done

# 3. Puertos defaults
grep -r "8080" workspace/plan/ | wc -l  # Backend
grep -r "4200" workspace/plan/ | wc -l  # Frontend

# 4. Referencias cruzadas
grep -r "\[.*\](.*\.md)" workspace/plan/ | wc -l

# 5. Completitud
ls workspace/plan/*.md | wc -l  # Debe ser 10
```

## PASO 6: DOCUMENTAR CAMBIOS

**Crear commit:**
```bash
# Ver cambios realizados
git diff workspace/plan/

# Agregar archivos modificados
git add workspace/plan/

# Commit descriptivo
git commit -m "[plan] Update based on spec changes

Changes:
- Updated [componente] in [archivo]
- Modified [sección] to reflect [cambio]
- Synchronized with specs version [versión]

Stack: Go 1.21+ (backend) + Angular 19 (frontend)
Triggered by: git diff HEAD workspace/contracts/"
```

## OUTPUT ESPERADO: RESUMEN EJECUTIVO

```markdown
# Resumen Ejecutivo: Actualización del Plan

## 🎯 Objetivo Cumplido
Plan actualizado basado en cambios detectados en especificaciones.

## 📊 Cambios Detectados
**Archivos de specs modificados:**
- 05_ClassSphere_arquitectura.md (X líneas cambiadas)
- 09_ClassSphere_testing.md (X líneas cambiadas)

**Tipo de cambios:**
- Actualización de stack: [cambio detectado]
- Nuevo requisito: [especificar]
- Refinamiento: [detallar]

## 🔄 Archivos del Plan Actualizados
- ✅ 01_plan_index.md (actualizado stack tecnológico Go + Angular)
- ✅ 02_plan_fase1_fundaciones.md (actualizado backend Go/frontend Angular)
- ✅ 06_plan_testing_strategy.md (actualizado testify + Jasmine)
- ✅ 09_plan_evaluation_metrics.md (actualizadas métricas)

## ✅ Validaciones Post-Actualización
- ✅ Coherencia Go 1.21+: [X] menciones
- ✅ Coherencia Angular 19: [X] menciones
- ✅ Coherencia Echo v4: [X] menciones
- ✅ Coherencia testify: [X] menciones
- ✅ Puertos defaults (8080/4200): Verificados
- ✅ NO menciona tecnologías obsoletas: Correcto
- ✅ Estructura anti lost-in-the-middle: Preservada
- ✅ Referencias cruzadas: Sin enlaces rotos
- ✅ Completitud: 10 archivos intactos

## 📝 Commit Creado
```
[plan] Update based on spec changes

Changes:
- Updated [componente] in [archivo]
- Modified [sección] to reflect [cambio]
- Synchronized with specs version [versión]

Stack: Go 1.21+ (backend) + Angular 19 (frontend)
Triggered by: git diff HEAD workspace/contracts/
```

## 📈 Estado General
✅ PLAN ACTUALIZADO EXITOSAMENTE - Sincronizado con specs en /workspace/contracts/
```

---

*Última actualización: 2025-10-07*

