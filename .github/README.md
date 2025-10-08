# GitHub Actions Workflows

This directory contains automated CI/CD workflows for the ClassSphere project.

## 📋 Available Workflows

### 1. Docker Hub Publish (`docker-publish.yml`)

**Purpose**: Automatically build, scan, and publish Docker images to Docker Hub.

**Triggers:**
- ✅ **Tags**: Any tag starting with `v*` (e.g., `v1.0.0`, `v2.1.3`)
- ✅ **Main branch**: Push to `main` branch
- ✅ **Pull Requests**: PRs to `main` (build only, no publish)
- ✅ **Manual**: Via "Run workflow" button in GitHub UI

**What it does:**
1. **Build** backend and frontend images in parallel
2. **Scan** for security vulnerabilities with Trivy
3. **Tag** images with semantic versioning
4. **Publish** to Docker Hub (if not PR)
5. **Update** Docker Hub repository description

**Image Tags Generated:**

For tag `v1.2.3`, creates:
- `lbrines/classsphere-backend:1.2.3` (specific version)
- `lbrines/classsphere-backend:1.2` (minor version)
- `lbrines/classsphere-backend:1` (major version)
- `lbrines/classsphere-backend:latest` (latest stable)
- `lbrines/classsphere-backend:sha-abc123` (git commit)
- `lbrines/classsphere-backend:production` (environment)

Same tags for frontend: `lbrines/classsphere-frontend:*`

**Duration**: ~10-15 minutes

**Requirements:**

GitHub repository secrets (Settings → Secrets → Actions):
- `DOCKERHUB_USERNAME`: Your Docker Hub username (e.g., `lbrines`)
- `DOCKERHUB_TOKEN`: Personal Access Token from Docker Hub

---

## 🚀 Usage Examples

### Publish a New Release

```bash
# 1. Commit your changes
git add .
git commit -m "feat: add new feature"

# 2. Create a version tag
git tag v1.0.0 -m "Release v1.0.0: Initial stable release"

# 3. Push to GitHub
git push origin main
git push origin v1.0.0

# 4. GitHub Actions automatically:
#    - Builds images
#    - Scans for vulnerabilities
#    - Publishes to Docker Hub
#
# Monitor progress: https://github.com/YOUR_USERNAME/ClassSphere/actions
```

### Publish a Hotfix

```bash
# 1. Fix the bug
git commit -m "fix: resolve critical OAuth issue"

# 2. Create patch version tag
git tag v1.0.1 -m "Hotfix v1.0.1: OAuth token expiration"

# 3. Push
git push origin main --tags

# 4. Automatic publication in ~12 minutes
```

### Test Build Without Publishing

```bash
# 1. Create a PR
git checkout -b feature/new-dashboard
git push origin feature/new-dashboard

# 2. Open PR on GitHub
# Workflow runs but DOES NOT publish (only builds and scans)
```

### Manual Trigger

1. Go to: `https://github.com/YOUR_USERNAME/ClassSphere/actions`
2. Select "Docker Hub Publish"
3. Click "Run workflow"
4. Choose branch
5. Click "Run workflow" button

---

## 🔐 Security

### Secrets Configuration

**Generate Docker Hub Token:**
1. Go to: https://hub.docker.com/settings/security
2. Click "New Access Token"
3. Name: `ClassSphere GitHub Actions`
4. Permissions: **Read, Write**
5. Copy token (shown only once)

**Add to GitHub:**
1. Repository → Settings → Secrets and variables → Actions
2. Click "New repository secret"
3. Add:
   - Name: `DOCKERHUB_USERNAME`
   - Value: `lbrines`
4. Add another:
   - Name: `DOCKERHUB_TOKEN`
   - Value: `[paste token]`

### Vulnerability Scanning

All images are scanned with Trivy before publication:
- ✅ **Pass**: No CRITICAL or HIGH vulnerabilities
- ❌ **Fail**: Blocks publication if vulnerabilities found

Results uploaded to GitHub Security tab:
`https://github.com/YOUR_USERNAME/ClassSphere/security/code-scanning`

---

## 📊 Workflow Status

Check workflow status:
- **Actions Tab**: https://github.com/YOUR_USERNAME/ClassSphere/actions
- **Badges**: Add to README.md:

```markdown
![Docker Publish](https://github.com/YOUR_USERNAME/ClassSphere/actions/workflows/docker-publish.yml/badge.svg)
```

---

## 🛠️ Customization

### Change Docker Hub Username

Edit `.github/workflows/docker-publish.yml`:

```yaml
env:
  DOCKER_USER: your-dockerhub-username  # Change here
  BACKEND_IMAGE: your-username/classsphere-backend
  FRONTEND_IMAGE: your-username/classsphere-frontend
```

### Add Multi-Platform Support

Edit `docker-publish.yml`:

```yaml
- name: Build and push backend to Docker Hub
  uses: docker/build-push-action@v5
  with:
    platforms: linux/amd64,linux/arm64,linux/arm/v7  # Add platforms
```

### Change Trigger Events

Edit `on:` section in workflow:

```yaml
on:
  push:
    tags:
      - 'v*'      # Keep: version tags
      - 'release-*'  # Add: release branches
  schedule:
    - cron: '0 2 * * 0'  # Add: weekly Sunday 2 AM
```

---

## 🐛 Troubleshooting

### Build Fails

**Check logs:**
1. Go to Actions tab
2. Click on failed workflow run
3. Click on failed job
4. Review error messages

**Common issues:**
- ❌ Missing secrets → Add `DOCKERHUB_USERNAME` and `DOCKERHUB_TOKEN`
- ❌ Dockerfile not found → Check paths in workflow
- ❌ Build context error → Verify `.dockerignore` configuration

### Publish Fails

**Possible causes:**
- ❌ Invalid Docker Hub credentials
- ❌ Token expired (rotate every 90 days)
- ❌ Repository doesn't exist on Docker Hub
- ❌ Insufficient permissions on token

**Solution:**
1. Regenerate Docker Hub token
2. Update `DOCKERHUB_TOKEN` secret in GitHub
3. Re-run workflow

### Vulnerability Scan Fails

**If Trivy finds CRITICAL/HIGH vulnerabilities:**
1. Check scan results in workflow logs
2. Update base images in Dockerfiles:
   ```dockerfile
   # Update versions
   FROM golang:1.24-alpine  # Use latest patch
   FROM node:20-alpine       # Use latest LTS
   ```
3. Update dependencies:
   ```bash
   # Go
   go get -u ./...
   
   # Node
   npm update
   ```
4. Commit and push again

---

## 📚 Additional Resources

- **Docker Hub Best Practices**: `workspace/extra/DOCKER_HUB_PUBLISHING_BEST_PRACTICES.md`
- **Publishing Script**: `scripts/publish-docker-images.sh` (manual fallback)
- **Docker Compose**: `docker-compose.production.yml`
- **Environment Config**: `env.production.example`

---

## 📝 Workflow Diagram

```
┌─────────────────┐
│   Git Push      │
│   (tag v1.0.0)  │
└────────┬────────┘
         │
         ▼
┌─────────────────────────────────────┐
│   GitHub Actions Trigger            │
└─────────┬───────────────────────────┘
          │
          ├──────────────┬──────────────┐
          ▼              ▼              ▼
    ┌─────────┐    ┌──────────┐   ┌──────────┐
    │ Build   │    │  Build   │   │  Build   │
    │ Backend │    │ Frontend │   │ Parallel │
    └────┬────┘    └────┬─────┘   └──────────┘
         │              │
         ▼              ▼
    ┌─────────┐    ┌──────────┐
    │  Scan   │    │  Scan    │
    │ Backend │    │ Frontend │
    │ (Trivy) │    │ (Trivy)  │
    └────┬────┘    └────┬─────┘
         │              │
         └──────┬───────┘
                ▼
         ┌─────────────┐
         │   Publish   │
         │ Docker Hub  │
         └──────┬──────┘
                ▼
         ┌─────────────┐
         │  ✅ Done    │
         │ (~12 min)   │
         └─────────────┘
```

---

**Last Updated**: 2025-10-08  
**Maintained by**: ClassSphere Development Team

