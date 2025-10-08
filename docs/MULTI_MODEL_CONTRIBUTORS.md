# Multi-Model Contributors Setup

**ClassSphere - Configuración para múltiples modelos contribuidores**

---

## 🎯 Objetivo

Configurar Git para que cada modelo de IA aparezca como un contribuidor separado en el dashboard de GitHub/GitLab.

---

## 🔧 Configuración Inicial

### 1. Ejecutar script de configuración

```bash
# Configurar todas las identidades
./scripts/setup-git-identities.sh
```

### 2. Verificar configuración actual

```bash
# Ver configuración actual
git config user.name
git config user.email

# Ver configuración global
git config --global user.name
git config --global user.email
```

---

## 🤖 Modelos Configurados

| Modelo | Email | Uso |
|--------|-------|-----|
| Ibrines | ibrines@classsphere.dev | Desarrollador principal |
| Claude | claude@classsphere.ai | Análisis y arquitectura |
| GPT-4 | gpt4@classsphere.ai | Implementación de features |
| Gemini | gemini@classsphere.ai | Testing y documentación |

---

## 📝 Workflow por Modelo

### Cambiar a un modelo específico

```bash
# Usar script automatizado
./scripts/model-workflow.sh "Claude" "claude@classsphere.ai" "feat: add authentication system"

# O manualmente
git config user.name "Claude"
git config user.email "claude@classsphere.ai"
git add .
git commit -m "feat: implement OAuth integration"
```

### Ejemplos de uso

```bash
# Claude trabajando en autenticación
./scripts/model-workflow.sh "Claude" "claude@classsphere.ai" "feat(auth): implement JWT authentication"

# GPT-4 trabajando en frontend
./scripts/model-workflow.sh "GPT-4" "gpt4@classsphere.ai" "feat(frontend): add dashboard components"

# Gemini trabajando en testing
./scripts/model-workflow.sh "Gemini" "gemini@classsphere.ai" "test: add integration tests for API"
```

---

## 📊 Resultado en Dashboard

Cada modelo aparecerá como un contribuidor separado:

- **Commits individuales** por modelo
- **Líneas de código** atribuidas correctamente
- **Historial de contribuciones** separado
- **Estadísticas** independientes

---

## 🔄 Cambio Rápido Entre Modelos

### Script de cambio rápido

```bash
# Crear alias para cambio rápido
alias claude='git config user.name "Claude" && git config user.email "claude@classsphere.ai"'
alias gpt4='git config user.name "GPT-4" && git config user.email "gpt4@classsphere.ai"'
alias gemini='git config user.name "Gemini" && git config user.email "gemini@classsphere.ai"'
alias ibrines='git config user.name "Ibrines" && git config user.email "ibrines@classsphere.dev"'
```

### Uso de alias

```bash
# Cambiar a Claude
claude
git add .
git commit -m "feat: add new feature"

# Cambiar a GPT-4
gpt4
git add .
git commit -m "fix: resolve bug"
```

---

## ⚠️ Consideraciones Importantes

### 1. **Emails únicos**
- Cada modelo debe tener un email único
- Los emails deben ser válidos (pueden ser ficticios)
- GitHub reconoce contribuidores por email

### 2. **Consistencia**
- Usar siempre el mismo email para cada modelo
- Mantener nombres consistentes
- Documentar qué modelo hace qué tipo de trabajo

### 3. **Backup de configuración**
```bash
# Guardar configuración actual
git config --list > git-config-backup.txt

# Restaurar configuración
git config --file git-config-backup.txt
```

---

## 🎯 Mejores Prácticas

### 1. **Asignación de responsabilidades**
- **Claude**: Arquitectura, análisis, documentación
- **GPT-4**: Implementación, features, debugging
- **Gemini**: Testing, optimización, refactoring
- **Ibrines**: Code review, deployment, management

### 2. **Convenciones de commits**
```bash
# Claude - Análisis y arquitectura
feat(arch): design hexagonal architecture
docs(api): create API documentation
refactor(domain): improve domain models

# GPT-4 - Implementación
feat(auth): implement JWT authentication
fix(api): resolve CORS issues
feat(frontend): add dashboard components

# Gemini - Testing y optimización
test(api): add integration tests
perf(backend): optimize database queries
test(e2e): add end-to-end tests
```

### 3. **Verificación**
```bash
# Verificar contribuidor actual
git log --oneline -1 --pretty=format:"%an <%ae>"

# Ver historial de contribuidores
git log --pretty=format:"%an <%ae>" | sort | uniq
```

---

## 📈 Métricas y Seguimiento

### Ver contribuciones por modelo

```bash
# Commits por autor
git log --pretty=format:"%an" | sort | uniq -c | sort -nr

# Líneas de código por autor
git log --author="Claude" --pretty=tformat: --numstat | awk '{ add += $1; subs += $2; loc += $1 - $2 } END { printf "Claude: +%s -%s = %s\n", add, subs, loc }'
```

### Dashboard de GitHub
- Cada modelo aparecerá como contribuidor separado
- Estadísticas individuales de commits y líneas
- Gráficos de actividad por modelo
- Historial de contribuciones independiente

---

**Versión**: 1.0  
**Última actualización**: 2025-01-27
