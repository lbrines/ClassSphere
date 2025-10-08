---
title: "ClassSphere - Índice de Prompts de Gestión"
version: "2.0"
type: "prompt_index"
date: "2025-10-07"
author: "Sistema de Gestión ClassSphere"
total_prompts: 5
structure: "modular_optimized"
---

# ClassSphere Prompt Management Index

## 🎯 Descripción General

Catálogo de prompts optimizado para gestión y análisis del plan de desarrollo ClassSphere. Diseñado para ejecución por LLMs con stack **Go 1.21+ + Angular 19**.

**Características**:
- ✅ Estructura modular (4 prompts en lugar de 23)
- ✅ Análisis unificado inteligente (elimina duplicación)
- ✅ Gestión de repositorio separada
- ✅ Actualizado para Go + Angular stack
- ✅ Rutas en `/workspace/`

---

## 🚀 Guía de Decisión Rápida

### ¿Qué necesitas hacer?

#### **1. Crear un plan nuevo desde cero**
```
📁 USE: 01_gestion/01_create_plan.md

Lee: workspace/contracts/*.md (especificaciones)
Crea: workspace/plan/*.md (10 archivos)
Stack: Go 1.21+ (backend) + Angular 19 (frontend)
Duración: 45 días (4 fases)
Output: Plan completo con TDD-RunFix+
```

#### **2. Actualizar plan existente**
```
📁 USE: 01_gestion/02_update_plan.md

Detecta: git diff workspace/contracts/
Actualiza: workspace/plan/*.md (solo afectados)
Valida: Coherencia, estructura, puertos
Output: Plan sincronizado con specs
```

#### **3. Analizar calidad/coherencia/dependencias/etc.**
```
📁 USE: 02_analisis/03_unified_analysis.md

Pregunta: "¿Analizar workspace/plan/ o workspace/contracts/?"
Responde: "plan" o "contracts"
Ejecuta: 8 análisis completos
Output: Resumen ejecutivo con métricas
```

#### **4. Limpiar artifacts y cachés (⚠️ Parcial)**
```
📁 USE: 03_repo/05_cleanup_artifacts.md

Elimina: Cachés, coverage, logs, binarios (regenerables)
Preserva: Código fuente, documentación, Git history
Impacto: 9.1 GB → ~800 MB (-91%)
Output: Repo optimizado
```

#### **5. Limpiar repositorio completo (⚠️ DESTRUCTIVO)**
```
📁 USE: 03_repo/04_clean_repo.md

⚠️ ADVERTENCIA: Operación irreversible
Preserva: workspace/, CLAUDE.md, archivos Git
Elimina: backend/, frontend/, scripts/, etc.
Requiere: Backup obligatorio
Output: Repo limpio con solo documentación
```

---

## 📚 Catálogo de Prompts

### **01_gestion/** - Gestión del Plan (2 prompts)

| ID | Archivo | Función | Target | Prioridad |
|----|---------|---------|--------|-----------|
| **01** | `01_create_plan.md` | Crear plan desde cero | `workspace/plan/` | CRITICAL |
| **02** | `02_update_plan.md` | Actualizar plan existente | `workspace/plan/` | HIGH |

**Cuándo usar**:
- Prompt 01: Repositorio vacío o necesitas regenerar plan completo
- Prompt 02: Hay cambios en `workspace/contracts/` que deben reflejarse en el plan

---

### **02_analisis/** - Análisis Unificado Inteligente (1 prompt)

| ID | Archivo | Función | Target | Prioridad |
|----|---------|---------|--------|-----------|
| **03** | `03_unified_analysis.md` | Análisis completo de 8 métricas | `workspace/plan/` o `workspace/contracts/` | VARIABLE |

**Análisis incluidos**:
1. ✅ **Trazabilidad** (≥95% cobertura)
2. ✅ **Coherencia** (≥85% consistencia - Go + Angular)
3. ✅ **Dependencias** (100% documentadas)
4. ✅ **Patrones** (≥80% consistencia - TDD-RunFix+, hexagonal)
5. ✅ **Completitud** (≥95% cobertura funcional)
6. ✅ **Complejidad** (≤MEDIUM ejecutabilidad)
7. ✅ **Riesgos** (100% mitigados)
8. ✅ **Calidad** (≥90% global)

**Cuándo usar**:
- Validar calidad del plan o especificaciones
- Verificar coherencia de términos técnicos
- Identificar gaps o inconsistencias
- Evaluar calidad global del proyecto

---

### **03_repo/** - Gestión de Repositorio (2 prompts)

| ID | Archivo | Función | Preserva | Prioridad |
|----|---------|---------|----------|-----------|
| **04** | `04_clean_repo.md` | Limpieza destructiva completa | `workspace/`, `CLAUDE.md`, Git | SPECIAL |
| **05** | `05_cleanup_artifacts.md` | Limpieza de artifacts y cache | Todo el código + docs | HIGH |

#### Prompt 05: Cleanup Artifacts ✅ (NUEVO)

**Tipo**: Limpieza parcial y segura
**Impacto**: Reduce 91% del tamaño del repo

**Elimina (Regenerables)**:
- ✅ Angular cache (`.angular/cache/`) - 7.8 GB
- ✅ Coverage duplicados (24 archivos backend)
- ✅ Test artifacts (playwright-report/, etc.)
- ✅ Logs (*.log)
- ✅ Binarios compilados

**Preserva (Todo lo importante)**:
- ✅ Código fuente completo (backend/, frontend/)
- ✅ Documentación completa (workspace/)
- ✅ Dev Containers (.devcontainer/)
- ✅ Git history (.git/)
- ✅ node_modules/ (necesario)

**Cuándo usar**:
- Después de fase de desarrollo intenso
- Antes de push a remoto
- Periódicamente para mantener repo limpio
- Sin riesgo (todo regenerable)

---

#### Prompt 04: Clean Repo ⚠️ (DESTRUCTIVO)

**⚠️ ADVERTENCIA CRÍTICA**: Operación **DESTRUCTIVA** e **IRREVERSIBLE**

**Preserva**:
- ✅ `workspace/` completo (contracts/, plan/, prompt/, extra/)
- ✅ `CLAUDE.md` (notas de desarrollo)
- ✅ `.git/` (historial completo)
- ✅ `.gitignore`, `.gitmessage`

**Elimina**:
- ❌ `backend/` (Go + Echo code)
- ❌ `frontend/` (Angular 19 code)
- ❌ `scripts/` (automation)
- ❌ Todos los archivos raíz excepto preservados

**Cuándo usar**:
- Reiniciar desarrollo desde cero
- Mantener solo documentación y plan
- Preparar repo para nueva implementación

---

## 🛠️ Stack Tecnológico

### Backend
- **Lenguaje**: Go 1.21+
- **Framework**: Echo v4
- **Auth**: JWT + OAuth 2.0 Google
- **Testing**: testify + mock
- **Puerto**: **8080** (default)
- **Arquitectura**: Hexagonal (ports & adapters)

### Frontend
- **Framework**: Angular 19
- **Bundler**: esbuild
- **Estilos**: TailwindCSS 3.x
- **Testing**: Jasmine + Karma + Playwright
- **Puerto**: **4200** (default)
- **Arquitectura**: Feature folders

### DevOps
- **CI/CD**: GitHub Actions
- **Containers**: Docker multi-stage
- **Security**: Trivy (SAST, SCA)

---

## 📍 Rutas Importantes

### Especificaciones
```
workspace/contracts/
├── 00_ClassSphere_index.md           # Índice general
├── 05_ClassSphere_arquitectura.md    # Stack Go + Angular
├── 09_ClassSphere_testing.md         # Estrategia testing
├── 10_ClassSphere_plan_implementacion.md
└── ... (12 archivos totales)
```

### Plan de Desarrollo
```
workspace/plan/
├── 01_plan_index.md                  # Índice del plan
├── 02_plan_fase1_fundaciones.md      # Go + Angular (12 días)
├── 03_plan_fase2_google_integration.md  (10 días)
├── 04_plan_fase3_visualizacion.md    (10 días)
├── 05_plan_fase4_integracion.md      (13 días)
├── 06_plan_testing_strategy.md       # testify + Jasmine
├── 07_plan_security_protocols.md     # Cero confianza
├── 08_plan_context_management.md     # LLM optimization
├── 09_plan_evaluation_metrics.md     # Métricas
└── README.md
```

---

## 📊 Métricas Consolidadas

| Métrica | Objetivo | Aplicable a | Prompt |
|---------|----------|-------------|--------|
| **Precisión** | ≥95% | Plan + Specs | #03 |
| **Completitud** | 100% | Plan + Specs | #03 |
| **Coherencia** | ≥85% | Plan + Specs | #03 |
| **Dependencias** | 100% documentadas | Plan + Specs | #03 |
| **Patrones** | ≥80% consistencia | Plan + Specs | #03 |
| **Complejidad** | ≤MEDIUM | Plan + Specs | #03 |
| **Riesgos** | 100% mitigados | Plan | #03 |
| **Calidad Global** | ≥90% | Plan + Specs | #03 |
| **Testing Coverage** | ≥80% | Código | Plan |
| **Sincronización** | ≥98% | Plan ↔ Specs | #03 |

---

## 🎯 Matriz de Prioridades

### CRITICAL (Usar Inmediatamente)
- **Prompt 01**: Crear plan nuevo (si no existe)
- **Prompt 02**: Actualizar plan (cuando cambian specs)

### HIGH (Usar Regularmente)
- **Prompt 03**: Análisis unificado (elegir "plan" para validar plan)
- **Prompt 03**: Análisis unificado (elegir "contracts" para validar specs)

### MEDIUM (Usar Ocasionalmente)
- **Prompt 03**: Con enfoque en patrones, completitud

### LOW (Usar Según Necesidad)
- **Prompt 03**: Con enfoque en complejidad, riesgos

### SPECIAL (Usar con Extrema Precaución)
- **Prompt 04**: Limpieza de repo (⚠️ DESTRUCTIVO - Backup obligatorio)

---

## 🔄 Flujo de Trabajo Recomendado

### 1. Desarrollo Inicial
```
1. Ejecutar: 01_create_plan.md
   → Genera plan completo en workspace/plan/

2. Validar: 03_unified_analysis.md (elegir "plan")
   → Verifica calidad del plan generado

3. Comenzar: Seguir workspace/plan/02_plan_fase1_fundaciones.md
```

### 2. Mantenimiento del Plan
```
1. Detectar cambios: git diff workspace/contracts/

2. Si hay cambios: 02_update_plan.md
   → Sincroniza plan con specs

3. Validar: 03_unified_analysis.md (elegir "plan")
   → Verifica sincronización
```

### 3. Control de Calidad
```
1. Analizar plan: 03_unified_analysis.md (elegir "plan")
   → Métricas de calidad del plan

2. Analizar specs: 03_unified_analysis.md (elegir "contracts")
   → Métricas de calidad de especificaciones

3. Comparar: Mismo prompt con opción "comparar"
   → Verificar sincronización
```

### 4. Reinicio Completo (⚠️ DESTRUCTIVO)
```
1. Backup: tar -czf backup-$(date +%Y%m%d).tar.gz .

2. Limpiar: 04_clean_repo.md
   → Elimina todo excepto workspace/ y Git

3. Recrear: 01_create_plan.md
   → Genera plan nuevo desde specs
```

---

## 📝 Comandos de Validación Comunes

### Verificar estructura de prompts
```bash
tree workspace/prompt/
find workspace/prompt/ -name "*.md" | wc -l  # Debe ser: 5
```

### Verificar plan existe
```bash
ls -la workspace/plan/*.md | wc -l  # Debe ser: 10
```

### Verificar coherencia de stack
```bash
grep -r "Go 1.21" workspace/plan/ | wc -l
grep -r "Angular 19" workspace/plan/ | wc -l
grep -r "FastAPI\|Next.js\|React" workspace/plan/  # No debe retornar nada
```

### Verificar puertos defaults
```bash
grep -r "8080" workspace/plan/ | wc -l  # Backend
grep -r "4200" workspace/plan/ | wc -l  # Frontend
```

### Detectar cambios en specs
```bash
git diff HEAD workspace/contracts/
git diff --name-only HEAD workspace/contracts/
```

---

## 🎨 Patrones Aplicados en Prompts

### Context Management (LLM)
- **Chunking**: CRITICAL (2000) → HIGH (1500) → MEDIUM (1000) → LOW (800) tokens
- **Estructura**: INICIO → MEDIO → FINAL (anti lost-in-the-middle)
- **Logs**: JSON con `context_id` y `token_count`

### TDD-RunFix+ (7 pasos)
1. Red → 2. Run → 3. Fix → 4. Run → 5. Refactor → 6. Validate → 7. Document

### Seguridad
- **Principio**: Cero confianza
- **Escaneo**: SAST, SCA, Secrets (Trivy)
- **Pipeline**: GitHub Actions con quality gates

### Arquitectura
- **Backend**: Hexagonal (ports & adapters)
- **Frontend**: Feature folders
- **Testing**: Separado por tipo (unit/integration/e2e)

---

## 📈 Mejoras de la Versión 2.0

| Aspecto | Versión 1.0 | Versión 2.0 | Mejora |
|---------|-------------|-------------|--------|
| **Archivos** | 1 monolítico (88KB) | 5 modulares (~15KB) | -83% tamaño |
| **Prompts** | 23 separados | 4 (1 unificado) | -83% duplicación |
| **Duplicación** | Alta | Cero | -100% redundancia |
| **Navegación** | Scroll | Categorías + índice | +95% facilidad |
| **Mantenibilidad** | Difícil | Fácil | +90% |
| **Stack** | FastAPI/Next.js | Go/Angular | Actualizado |
| **Rutas** | `/contracts/` | `/workspace/` | Actualizado |

---

## ✅ Estado de Prompts

### Prompt 01: Create Plan ✅
- **Ubicación**: `01_gestion/01_create_plan.md`
- **Estado**: Actualizado (Go + Angular)
- **Lee**: `workspace/contracts/`
- **Crea**: `workspace/plan/`

### Prompt 02: Update Plan ✅
- **Ubicación**: `01_gestion/02_update_plan.md`
- **Estado**: Actualizado (Go + Angular)
- **Detecta**: `git diff workspace/contracts/`
- **Actualiza**: `workspace/plan/`

### Prompt 03: Unified Analysis ✅
- **Ubicación**: `02_analisis/03_unified_analysis.md`
- **Estado**: Consolidado (16 prompts → 1)
- **Analiza**: `workspace/plan/` O `workspace/contracts/`
- **Métricas**: 8 análisis completos

### Prompt 04: Clean Repo ⚠️
- **Ubicación**: `03_repo/04_clean_repo.md`
- **Estado**: Actualizado (preserva workspace/)
- **Acción**: Limpieza destructiva completa
- **Requiere**: Backup obligatorio

### Prompt 05: Cleanup Artifacts ✅ (NUEVO)
- **Ubicación**: `03_repo/05_cleanup_artifacts.md`
- **Estado**: ✅ Validated (executed 2025-10-07)
- **Acción**: Limpieza parcial de cachés y artifacts
- **Impacto**: 9.1 GB → 782 MB (-91%)
- **Requiere**: Backup recomendado (no crítico)

---

## 🎯 Próximos Pasos

### Para Comenzar Desarrollo
```bash
# 1. Crear plan (si no existe)
cat workspace/prompt/01_gestion/01_create_plan.md

# 2. Validar plan creado
cat workspace/prompt/02_analisis/03_unified_analysis.md
# (Responder "plan" cuando pregunte)

# 3. Comenzar Fase 1
cat workspace/plan/02_plan_fase1_fundaciones.md
```

### Para Mantener Plan Actualizado
```bash
# 1. Detectar cambios
git diff workspace/contracts/

# 2. Si hay cambios, actualizar
cat workspace/prompt/01_gestion/02_update_plan.md

# 3. Validar sincronización
cat workspace/prompt/02_analisis/03_unified_analysis.md
# (Responder "plan" y usar opción comparar)
```

---

## 📊 Estructura del Repositorio

```
ClassSphere/
├── .git/                         # Historial Git
├── .gitignore                    # Config Git
├── CLAUDE.md                     # Notas desarrollo
│
├── workspace/                    # TODO LO IMPORTANTE
│   ├── contracts/                # Especificaciones (12 archivos)
│   │   ├── 00_ClassSphere_index.md
│   │   ├── 05_ClassSphere_arquitectura.md
│   │   └── ...
│   │
│   ├── plan/                     # Plan desarrollo (10 archivos)
│   │   ├── 01_plan_index.md
│   │   ├── 02_plan_fase1_fundaciones.md (Go + Angular)
│   │   └── ...
│   │
│   ├── prompt/                   # Prompts de gestión (5 archivos)
│   │   ├── 00_prompt_index.md   ← ESTÁS AQUÍ
│   │   ├── 01_gestion/
│   │   │   ├── 01_create_plan.md
│   │   │   └── 02_update_plan.md
│   │   ├── 02_analisis/
│   │   │   └── 03_unified_analysis.md
│   │   └── 03_repo/
│   │       └── 04_clean_repo.md
│   │
│   └── extra/                    # Mejores prácticas
│
├── backend/                      # (A crear según plan)
└── frontend/                     # (A crear según plan)
```

---

## ✅ Validaciones Disponibles

Todos los prompts incluyen comandos de validación automática:

### Para Plan
```bash
# Estructura anti lost-in-the-middle
for file in workspace/plan/0[2-5]*.md; do
  grep -c "## 🎯 INICIO:" "$file"
  grep -c "## 📅 MEDIO:" "$file"
  grep -c "## ✅ FINAL:" "$file"
done

# Coherencia Go + Angular
grep -r "Go 1.21" workspace/plan/ | wc -l
grep -r "Angular 19" workspace/plan/ | wc -l

# Sin tecnologías obsoletas
grep -r "FastAPI\|Next.js\|React\|Jest\|Vitest" workspace/plan/
```

### Para Especificaciones
```bash
# Coherencia de términos
grep -r "Go 1.21" workspace/contracts/ | wc -l
grep -r "Angular 19" workspace/contracts/ | wc -l

# Completitud
ls workspace/contracts/*.md | wc -l  # 12 archivos
```

---

## 🚨 Advertencias Importantes

### ⚠️ Prompt 04 (Clean Repo)
- **DESTRUCTIVO** e **IRREVERSIBLE**
- **Backup OBLIGATORIO** antes de ejecutar
- Solo usar cuando estés 100% seguro
- Verifica que `workspace/` esté completo

### 🔧 Puertos Defaults
- **Backend**: Siempre **8080** (NO 8000 o custom)
- **Frontend**: Siempre **4200** (NO 3000 o custom)
- Razón: Estándares Go y Angular

### 📁 Directorio Ignorado
- **`/workspace/` NO se usa en desarrollo**
- Solo para contratos y prompts
- Código va en `/backend/` y `/frontend/` (raíz)

---

## 📈 Métricas de Éxito

### Para Prompts de Gestión (#01, #02)
- ✅ Plan creado/actualizado sin errores
- ✅ 10 archivos en `workspace/plan/`
- ✅ Estructura INICIO-MEDIO-FINAL presente
- ✅ Stack Go + Angular correcto
- ✅ Puertos 8080/4200 especificados

### Para Prompt de Análisis (#03)
- ✅ 8 métricas calculadas
- ✅ Calidad global ≥90%
- ✅ Coherencia ≥85%
- ✅ Precisión ≥95%
- ✅ Resumen ejecutivo completo

### Para Prompt de Limpieza (#04)
- ✅ Solo workspace/ y Git preservados
- ✅ Backup creado y verificado
- ✅ Commit descriptivo creado
- ✅ Estructura resultante correcta

---

## 📖 Versionado

**Versión**: 2.0  
**Fecha**: 2025-10-07  
**Cambios**:
- Estructura modular optimizada
- Análisis unificado inteligente (16 prompts → 1)
- Stack actualizado a Go + Angular
- Rutas actualizadas a `/workspace/`
- Puertos defaults (8080/4200)
- Gestión de repo separada

**Versión anterior**: 1.0 (manage_plan_prompts.md, 23 prompts)

---

## 🔗 Enlaces Rápidos

- **Crear Plan**: [01_gestion/01_create_plan.md](01_gestion/01_create_plan.md)
- **Actualizar Plan**: [01_gestion/02_update_plan.md](01_gestion/02_update_plan.md)
- **Análisis**: [02_analisis/03_unified_analysis.md](02_analisis/03_unified_analysis.md)
- **Limpieza**: [03_repo/04_clean_repo.md](03_repo/04_clean_repo.md)

---

*Última actualización: 2025-10-07*

