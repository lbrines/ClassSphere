# Multi-Model Contributor Setup

**ClassSphere - Configuración para múltiples modelos contribuidores**

## 🎯 Objetivo

Configurar Git para que cada modelo de IA aparezca como un contribuidor separado en el dashboard de GitHub/GitLab.

## 🔧 Scripts Disponibles

### 1. Cambio entre modelos
```bash
./scripts/switch-model.sh <modelo>
```

**Modelos disponibles:**
- `claude` - Claude (claude@classsphere.ai)
- `gpt4` - GPT-4 (gpt4@classsphere.ai)  
- `gemini` - Gemini (gemini@classsphere.ai)
- `ibrines` - Leopoldo Brines (leopoldo.brines@leobrines.com)

### 2. Commit con modelo específico
```bash
./scripts/commit-as-model.sh <modelo> <mensaje>
```

**Ejemplos:**
```bash
./scripts/commit-as-model.sh claude "feat: add authentication system"
./scripts/commit-as-model.sh gpt4 "fix: resolve dashboard bug"
./scripts/commit-as-model.sh gemini "test: add integration tests"
```

## 📊 Resultado en Dashboard

Cada modelo aparecerá como contribuidor separado:
- **Commits individuales** por modelo
- **Líneas de código** atribuidas correctamente  
- **Historial de contribuciones** separado
- **Estadísticas** independientes

## 🎯 Asignación de Responsabilidades

| Modelo | Responsabilidad | Ejemplo de Commits |
|--------|----------------|-------------------|
| **Claude** | Análisis y arquitectura | `feat(arch): design hexagonal architecture` |
| **GPT-4** | Implementación de features | `feat(auth): implement JWT authentication` |
| **Gemini** | Testing y documentación | `test(api): add integration tests` |
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
