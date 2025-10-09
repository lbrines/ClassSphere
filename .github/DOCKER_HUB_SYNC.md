# Docker Hub README Sync

Este documento explica cómo funciona la sincronización automática del README de Docker Hub.

## 📋 Descripción

El workflow `sync-docker-readme.yml` sincroniza automáticamente el archivo `docs/DOCKER_HUB_README.md` con las páginas de overview de Docker Hub para ambas imágenes:
- `lbrines/classsphere-backend`
- `lbrines/classsphere-frontend`

## 🚀 Cómo Funciona

### Triggers Automáticos

El workflow se ejecuta automáticamente cuando:

1. **Push a main** - Solo si se modifica `docs/DOCKER_HUB_README.md`
   ```bash
   git add docs/DOCKER_HUB_README.md
   git commit -m "Update Docker Hub README"
   git push origin main
   ```

2. **Después de publicar imágenes** - Cuando el workflow "Docker Publish" completa
   - Se ejecuta automáticamente después de `docker-publish.yml`

3. **Manualmente** - Desde la UI de GitHub Actions
   - Ve a: Actions → Sync Docker Hub README → Run workflow

## ⚙️ Configuración de Secrets

Para que funcione, necesitas configurar estos secrets en GitHub:

### 1. Obtener Docker Hub Access Token

```bash
# 1. Ve a https://hub.docker.com/settings/security
# 2. Click "New Access Token"
# 3. Name: "GitHub Actions - README Sync"
# 4. Permissions: "Read & Write"
# 5. Copia el token generado
```

### 2. Agregar Secrets a GitHub

```bash
# Opción A: Desde la UI de GitHub
# 1. Ve a: Settings → Secrets and variables → Actions
# 2. Click "New repository secret"
# 3. Agrega:
#    - Name: DOCKERHUB_USERNAME
#      Value: lbrines
#    - Name: DOCKERHUB_TOKEN
#      Value: [tu-token-generado]

# Opción B: Usando GitHub CLI
gh secret set DOCKERHUB_USERNAME --body "lbrines"
gh secret set DOCKERHUB_TOKEN --body "tu-token-aqui"
```

### 3. Verificar Secrets

```bash
# Listar secrets configurados
gh secret list

# Deberías ver:
# DOCKERHUB_USERNAME
# DOCKERHUB_TOKEN
```

## 📝 Uso Manual

### Ejecutar Sync Manualmente

```bash
# Opción 1: Desde GitHub UI
# 1. Ve a: Actions → Sync Docker Hub README
# 2. Click "Run workflow"
# 3. Select branch: main
# 4. Click "Run workflow"

# Opción 2: Usando GitHub CLI
gh workflow run sync-docker-readme.yml
```

### Forzar Actualización

```bash
# Si quieres forzar una actualización sin cambios
git commit --allow-empty -m "chore: trigger Docker Hub README sync"
git push origin main
```

## 🔍 Verificar Resultados

### 1. Revisa el Workflow

```bash
# Ver últimas ejecuciones
gh run list --workflow=sync-docker-readme.yml

# Ver logs de última ejecución
gh run view --log
```

### 2. Revisa Docker Hub

Verifica que el README se actualizó:
- Backend: https://hub.docker.com/r/lbrines/classsphere-backend
- Frontend: https://hub.docker.com/r/lbrines/classsphere-frontend

## 🛠️ Troubleshooting

### Error: "Authentication failed"

**Causa**: Secrets no configurados o token inválido

**Solución**:
```bash
# Regenera el token en Docker Hub
# Actualiza el secret
gh secret set DOCKERHUB_TOKEN --body "nuevo-token"
```

### Error: "Repository not found"

**Causa**: Nombre de repositorio incorrecto o sin permisos

**Solución**:
```bash
# Verifica que las imágenes existen
docker pull lbrines/classsphere-backend:latest
docker pull lbrines/classsphere-frontend:latest

# Verifica los permisos del token en Docker Hub
```

### Error: "README file not found"

**Causa**: Ruta del archivo incorrecta

**Solución**:
```bash
# Verifica que el archivo existe
ls -la docs/DOCKER_HUB_README.md

# Verifica la ruta en el workflow
cat .github/workflows/sync-docker-readme.yml | grep readme-filepath
```

### El README no se actualiza

**Causa**: Push a branch diferente de main

**Solución**:
```bash
# El workflow solo se ejecuta en main
git checkout main
git push origin main
```

## 📊 Estructura del Workflow

```yaml
Jobs:
├── sync-backend-readme     # Actualiza backend
│   └── peter-evans/dockerhub-description@v4
├── sync-frontend-readme    # Actualiza frontend
│   └── peter-evans/dockerhub-description@v4
└── notify-completion       # Resumen
    └── Runs after both complete
```

## 🔗 Referencias

- GitHub Action: [peter-evans/dockerhub-description](https://github.com/peter-evans/dockerhub-description)
- Docker Hub API: [Repositories API](https://docs.docker.com/docker-hub/api/latest/)
- GitHub Actions Docs: [Workflow Syntax](https://docs.github.com/en/actions/reference/workflow-syntax-for-github-actions)

## ✅ Checklist de Setup

- [ ] Crear token en Docker Hub
- [ ] Agregar `DOCKERHUB_USERNAME` a GitHub Secrets
- [ ] Agregar `DOCKERHUB_TOKEN` a GitHub Secrets
- [ ] Push `sync-docker-readme.yml` a main
- [ ] Ejecutar workflow manualmente (test)
- [ ] Verificar README en Docker Hub
- [ ] Modificar `DOCKER_HUB_README.md` y hacer push (test automático)

---

**Última actualización**: 2025-10-09  
**Mantenido por**: ClassSphere Development Team

