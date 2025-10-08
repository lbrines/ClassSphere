# Multi-Tool Contributor Setup

**ClassSphere - Configuración para múltiples herramientas contribuidoras**

## 🎯 Objetivo

Configurar Git para que cada herramienta de desarrollo aparezca como un contribuidor separado en el dashboard de GitHub/GitLab.

## 🔧 Scripts Disponibles

### 1. Cambio entre herramientas
```bash
./scripts/switch-model.sh <herramienta>
```

**Herramientas disponibles:**
- `claude` - Claude (claude@classsphere.ai)
- `codex` - Codex (codex@classsphere.ai)  
- `cursor` - Cursor (cursor@classsphere.ai)
- `windsurf` - Windsurf (windsurf@classsphere.ai)
- `ibrines` - Leopoldo Brines (leopoldo.brines@leobrines.com)

### 2. Commit con herramienta específica
```bash
./scripts/commit-as-model.sh <herramienta> <mensaje>
```

**Ejemplos:**
```bash
./scripts/commit-as-model.sh claude "feat: add authentication system"
./scripts/commit-as-model.sh codex "fix: resolve dashboard bug"
./scripts/commit-as-model.sh cursor "test: add integration tests"
./scripts/commit-as-model.sh windsurf "docs: update API documentation"
```

## 📊 Resultado en Dashboard

Cada herramienta aparecerá como contribuidor separado:
- **Commits individuales** por herramienta
- **Líneas de código** atribuidas correctamente  
- **Historial de contribuciones** separado
- **Estadísticas** independientes

## 🎯 Asignación de Responsabilidades

| Herramienta | Responsabilidad | Ejemplo de Commits |
|-------------|----------------|-------------------|
| **Claude** | Análisis y arquitectura | `feat(arch): design hexagonal architecture` |
| **Codex** | Generación de código | `feat(auth): implement JWT authentication` |
| **Cursor** | IDE inteligente | `fix(ui): resolve component issues` |
| **Windsurf** | Desarrollo colaborativo | `docs: update API documentation` |
| **Ibrines** | Code review y management | `chore: update dependencies` |

## ✅ Verificación

```bash
# Ver contribuidor actual
git config user.name
git config user.email

# Ver último commit
git log --oneline -1 --pretty=format:"%an <%ae> - %s"

# Ver historial de contribuidores
git log --pretty=format:"%an <%ae>" | sort | uniq
```

## 🚀 Uso Diario

1. **Cambiar a modelo específico:**
   ```bash
   ./scripts/switch-model.sh claude
   ```

2. **Hacer cambios en el código**

3. **Commit con identidad del modelo:**
   ```bash
   git add .
   git commit -m "feat: implement new feature"
   ```

4. **Verificar contribuidor:**
   ```bash
   git log --oneline -1
   ```

---

**Versión**: 1.0  
**Última actualización**: 2025-01-27
