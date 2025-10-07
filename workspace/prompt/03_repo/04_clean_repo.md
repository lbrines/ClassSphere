---
id: "04"
title: "Clean Repository - Keep Only Workspace"
category: "Gestión de Repositorio"
priority: "SPECIAL"
version: "2.0"
warning: "DESTRUCTIVE - IRREVERSIBLE"
preserves: "workspace/, CLAUDE.md, .git/, .gitignore, .gitmessage"
date: "2025-10-07"
---

# PROMPT: Limpiar Repositorio y Mantener Solo Workspace

## OBJETIVO
Eliminar todo el contenido del repositorio EXCEPTO el directorio `/workspace/` y su contenido, manteniendo el historial de Git completo y creando un commit descriptivo.

## ⚠️ ADVERTENCIA CRÍTICA
Esta operación es **DESTRUCTIVA** e **IRREVERSIBLE**. Asegúrate de:
1. Tener un backup completo del repositorio
2. Estar absolutamente seguro de que quieres eliminar todo excepto `/workspace/`
3. Haber verificado que `/workspace/` contiene todo lo necesario

## CONTEXTO
- **Directorio a preservar**: `/workspace/` y todo su contenido (contracts/, plan/, prompt/, extra/)
- **Archivo a preservar**: `CLAUDE.md` (notas de desarrollo)
- **Archivos Git a preservar**: `.git/`, `.gitignore`, `.gitmessage` (si existe)
- **Directorios a eliminar**: backend/, frontend/, scripts/, classsphere-backend/, etc.
- **Historial Git**: Se mantiene intacto
- **Acción**: Crear commit completo documentando la limpieza

## PASO 1: VERIFICAR ESTADO ACTUAL

**Comandos de verificación:**
```bash
# Ver estructura actual del repositorio
tree -L 2 -a

# Ver qué hay en workspace/
ls -la workspace/

# Ver tamaño de workspace/
du -sh workspace/

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
ls -d */ | grep -v "workspace/"

# Listar todos los archivos de primer nivel
ls -p | grep -v /

# Ver todo lo que NO es workspace/
find . -maxdepth 1 ! -name "." ! -name ".git" ! -name "workspace" -type d
find . -maxdepth 1 ! -name "." ! -name ".git" ! -name "workspace" ! -name "CLAUDE.md" ! -name ".gitignore" ! -name ".gitmessage" -type f
```

**Directorios típicos a eliminar:**
- backend/
- frontend/
- scripts/
- classsphere-backend/
- .benchmarks/
- node_modules/ (si existe)
- venv/ (si existe)
- __pycache__/ (si existe)
- contracts/ (si está duplicado fuera de workspace/)

**Archivos típicos a eliminar:**
- README.md (si existe)
- package.json (si existe)
- requirements.txt (si existe)
- go.mod, go.sum (si existen en raíz)
- Cualquier otro archivo de configuración en raíz

**Archivos a preservar (OBLIGATORIO):**
- CLAUDE.md (notas de desarrollo)
- .gitignore (configuración Git)
- .gitmessage (mensaje de commit, si existe)
- .git/ (directorio completo de Git)

## PASO 4: ELIMINAR ARCHIVOS Y DIRECTORIOS

**Comandos de eliminación:**
```bash
# Eliminar directorios (CUIDADO: IRREVERSIBLE)
rm -rf backend/
rm -rf frontend/
rm -rf scripts/
rm -rf classsphere-backend/
rm -rf .benchmarks/
rm -rf node_modules/
rm -rf venv/
rm -rf __pycache__/

# Eliminar contracts/ si está duplicado fuera de workspace/
rm -rf contracts/ 2>/dev/null || true

# Eliminar archivos raíz (preservando CLAUDE.md, .gitignore, .gitmessage)
rm -f README.md
rm -f package.json
rm -f requirements.txt
rm -f go.mod
rm -f go.sum
rm -f angular.json
rm -f tsconfig.json

# O eliminar todos los archivos de raíz EXCEPTO archivos Git y CLAUDE.md
find . -maxdepth 1 -type f ! -name ".gitignore" ! -name "CLAUDE.md" ! -name ".gitmessage" -delete

# Verificar que workspace/ sigue intacto
ls -la workspace/
tree workspace/ -L 2
```

## PASO 5: VERIFICAR ELIMINACIÓN

**Comandos de verificación:**
```bash
# Ver estructura resultante
tree -L 2 -a

# Debe mostrar solo:
# .
# ├── .git/              # Historial Git completo
# ├── .gitignore         # Configuración Git
# ├── .gitmessage        # Mensaje de commit (si existe)
# ├── CLAUDE.md          # Notas de desarrollo
# └── workspace/         # TODO PRESERVADO
#     ├── contracts/     # Especificaciones
#     ├── plan/          # Plan de desarrollo
#     ├── prompt/        # Prompts de gestión
#     └── extra/         # Documentación adicional

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
git commit -m "[repo] Clean repository - Keep only workspace directory

DESTRUCTIVE OPERATION: Removed all implementation code and kept only documentation.

Directories removed:
- backend/ (Go + Echo application code)
- frontend/ (Angular 19 application code)
- scripts/ (automation scripts)
- classsphere-backend/ (compiled binaries)
- .benchmarks/ (performance benchmarks)
- node_modules/ (if existed)
- venv/ (if existed)
- contracts/ (if duplicated outside workspace/)

Files removed:
- README.md (project readme)
- package.json (frontend dependencies)
- requirements.txt (backend dependencies)
- go.mod, go.sum (backend dependencies)
- angular.json, tsconfig.json (frontend config)
- All other root-level files (except Git files and CLAUDE.md)

Directories preserved:
- workspace/ (complete documentation and planning)
  - workspace/contracts/ (specifications)
  - workspace/plan/ (development plan with Go + Angular)
  - workspace/prompt/ (management prompts)
  - workspace/extra/ (best practices, guides)

Files preserved:
- CLAUDE.md (development notes and context)
- .gitignore (Git ignore rules)
- .gitmessage (commit message template, if exists)
- .git/ (complete Git history)

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
1. Verify workspace/ integrity
2. Push to remote if needed
3. Start fresh implementation from plan
4. Use workspace/plan/ as source of truth
5. Implement Go + Angular stack from workspace/contracts/ specs

Verification commands:
- tree -L 2 -a
- ls -la workspace/
- git log --oneline -10

Status: ✅ Repository cleaned successfully
Impact: MAJOR - All implementation code removed
Stack: Go 1.21+ (backend) + Angular 19 (frontend)
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

# Verificar que workspace/ está completo
git ls-files | grep "^workspace/"
```

## PASO 9: VALIDAR INTEGRIDAD DE WORKSPACE

**Comandos de validación:**
```bash
# Verificar estructura de workspace/
tree workspace/

# Verificar archivos principales
ls -la workspace/plan/
ls -la workspace/contracts/
ls -la workspace/prompt/
ls -la workspace/extra/

# Contar archivos en workspace/
find workspace/ -type f | wc -l

# Verificar que no hay archivos corruptos
find workspace/ -type f -exec file {} \; | grep -v "text"

# Verificar tamaño total
du -sh workspace/

# Verificar archivos Git preservados
ls -la .git/ .gitignore .gitmessage CLAUDE.md 2>/dev/null
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

```markdown
# Resumen Ejecutivo: Limpieza de Repositorio

## 🎯 Objetivo Cumplido
Repositorio limpiado exitosamente, manteniendo solo `/workspace/` y historial Git completo.

## 📊 Estadísticas de Limpieza

### Directorios Eliminados
- ✅ backend/ (Go + Echo code)
- ✅ frontend/ (Angular 19 code)
- ✅ scripts/ (automation scripts)
- ✅ classsphere-backend/ (compiled binaries)
- ✅ .benchmarks/ (performance tests)
- ✅ node_modules/ (si existía)
- ✅ venv/ (si existía)
- ✅ contracts/ (si estaba duplicado fuera de workspace/)

**Total directorios eliminados:** 7-8

### Archivos Eliminados
- ✅ README.md
- ✅ package.json
- ✅ requirements.txt
- ✅ go.mod, go.sum
- ✅ angular.json, tsconfig.json
- ✅ Otros archivos de configuración en raíz

**Total archivos eliminados:** ~60+

### Contenido Preservado en /workspace/
- ✅ workspace/contracts/ (12 archivos de especificaciones)
- ✅ workspace/plan/ (10 archivos del plan Go + Angular)
- ✅ workspace/prompt/ (prompts de gestión reorganizados)
- ✅ workspace/extra/ (archivos de mejores prácticas)

### Archivos Git y Desarrollo Preservados
- ✅ CLAUDE.md (notas de desarrollo)
- ✅ .gitignore (configuración Git)
- ✅ .gitmessage (template de commit, si existe)
- ✅ .git/ (historial completo)

**Total archivos preservados:** ~35+

## 📈 Estructura Resultante

ClassSphere/
├── .git/                         # ✅ Historial completo preservado
├── .gitignore                    # ✅ Configuración Git
├── .gitmessage                   # ✅ Template de commit (si existe)
├── CLAUDE.md                     # ✅ Notas de desarrollo
└── workspace/                    # ✅ TODO PRESERVADO
    ├── contracts/                # Especificaciones Go + Angular (12 archivos)
    ├── plan/                     # Plan desarrollo (10 archivos)
    ├── prompt/                   # Prompts gestión (5 archivos organizados)
    └── extra/                    # Mejores prácticas

## ✅ Validaciones Realizadas

- ✅ Backup creado: classsphere-backup-YYYYMMDD-HHMMSS.tar.gz
- ✅ Estructura workspace/ intacta
- ✅ Todos los archivos de workspace/ preservados
- ✅ Archivos Git preservados (.git/, .gitignore, .gitmessage)
- ✅ CLAUDE.md preservado
- ✅ Historial Git completo mantenido
- ✅ Commit descriptivo creado
- ✅ No hay archivos corruptos
- ✅ Tamaño de workspace/: ~540KB

## 📝 Commit Creado

**Hash:** [commit-hash]
**Mensaje:** [repo] Clean repository - Keep only workspace directory
**Archivos modificados:** ~70 eliminaciones
**Líneas eliminadas:** ~60,000+
**Tamaño reducido:** ~95% del repositorio
**Stack preservado:** Go 1.21+ + Angular 19 (en workspace/)

## ⚠️ Información Importante

### Reversibilidad
- **Backup disponible:** classsphere-backup-YYYYMMDD-HHMMSS.tar.gz
- **Ubicación:** Directorio padre
- **Restauración:** `tar -xzf classsphere-backup-*.tar.gz`

### Historial Git
- **Commits preservados:** Todos
- **Branches preservados:** Todas
- **Tags preservados:** Todos
- **Archivos Git:** .git/, .gitignore, .gitmessage preservados
- **Acceso a código anterior:** `git checkout <commit-hash>`

### Próximos Pasos
1. ✅ Verificar integridad de workspace/
2. ⏳ Push a remoto (si es necesario)
3. ⏳ Comenzar implementación desde plan con Go + Angular
4. ⏳ Usar workspace/plan/ como fuente de verdad
5. ⏳ Leer especificaciones de workspace/contracts/

## 📈 Estado General
✅ LIMPIEZA EXITOSA - Repositorio optimizado para documentación

**Impacto:** MAJOR (código eliminado, documentación preservada)
**Reversibilidad:** ALTA (backup completo disponible)
**Riesgo:** BAJO (workspace/ verificado e intacto)
```

---

## ⚠️ CHECKLIST DE SEGURIDAD

Antes de ejecutar este prompt, verifica:

- [ ] **Backup creado y verificado**
- [ ] **Estás en el repositorio correcto**
- [ ] **Entiendes que esto es irreversible sin backup**
- [ ] **Has revisado qué hay en workspace/**
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

*Última actualización: 2025-10-07*

