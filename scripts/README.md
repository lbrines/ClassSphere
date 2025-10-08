# ClassSphere Scripts

Collection of utility scripts for ClassSphere project management and deployment.

## Available Scripts

### 1. publish-docker-images.sh

Builds and publishes ClassSphere Docker images to Docker Hub.

**Purpose**: Automates the process of building production images and pushing them to Docker Hub registry.

**Usage**:

```bash
# Basic usage (version 1.0.0)
./scripts/publish-docker-images.sh

# Specify version
./scripts/publish-docker-images.sh 1.2.3

# From project root
cd /home/lbrines/projects/AI/ClassSphere
./scripts/publish-docker-images.sh 1.0.0
```

**Prerequisites**:

1. **Docker Installed**:
   ```bash
   docker --version  # Should be 20.10+
   ```

2. **Docker Hub Authentication**:
   ```bash
   docker login
   # Username: lbrines
   # Password: [your password or token]
   ```

3. **Project Structure**:
   - `.devcontainer/backend/Dockerfile` - Backend multi-stage Dockerfile
   - `.devcontainer/frontend/Dockerfile` - Frontend multi-stage Dockerfile

**What it does**:

1. ✅ Validates Docker Hub authentication
2. 🏗️ Builds backend image (Go 1.24 + Echo v4)
3. 🔍 Scans for vulnerabilities (if Trivy installed)
4. 🏷️ Tags with version, latest, production, git-sha
5. 📤 Pushes backend to Docker Hub
6. 🏗️ Builds frontend image (Angular 19 + Nginx)
7. 🔍 Scans frontend for vulnerabilities
8. 🏷️ Tags frontend images
9. 📤 Pushes frontend to Docker Hub
10. 📊 Shows summary with sizes and URLs

**Output**:

```
========================================
ClassSphere Docker Image Publisher
========================================
User: lbrines
Version: 1.0.0
Git SHA: a1b2c3d
Build Date: 2025-10-08T12:00:00Z
========================================

✓ Published Images:

  Backend:
    lbrines/classsphere-backend:1.0.0 (150MB)
    lbrines/classsphere-backend:latest
    lbrines/classsphere-backend:production
    lbrines/classsphere-backend:sha-a1b2c3d

  Frontend:
    lbrines/classsphere-frontend:1.0.0 (50MB)
    lbrines/classsphere-frontend:latest
    lbrines/classsphere-frontend:production
    lbrines/classsphere-frontend:sha-a1b2c3d

Docker Hub:
  https://hub.docker.com/r/lbrines/classsphere-backend
  https://hub.docker.com/r/lbrines/classsphere-frontend
```

**Security Scanning**:

The script automatically scans images if Trivy is installed:

```bash
# Install Trivy
# macOS
brew install aquasecurity/trivy/trivy

# Linux
wget -qO - https://aquasecurity.github.io/trivy-repo/deb/public.key | sudo apt-key add -
echo "deb https://aquasecurity.github.io/trivy-repo/deb $(lsb_release -sc) main" | sudo tee -a /etc/apt/sources.list.d/trivy.list
sudo apt-get update && sudo apt-get install trivy
```

**Troubleshooting**:

| Issue | Solution |
|-------|----------|
| "Not logged in" error | Run `docker login` first |
| Build fails | Check Dockerfiles exist in `.devcontainer/` |
| Push permission denied | Verify you're logged in as `lbrines` |
| Image too large | Review Dockerfile optimization |
| Vulnerability warnings | Update base images and dependencies |

---

### 2. commit-as-model.sh

Commits changes with a standardized format.

**Usage**:

```bash
./scripts/commit-as-model.sh
```

---

### 3. setup-models.sh

Sets up model configurations for the project.

**Usage**:

```bash
./scripts/setup-models.sh
```

---

### 4. switch-model.sh

Switches between different model configurations.

**Usage**:

```bash
./scripts/switch-model.sh [model-name]
```

---

## Docker Hub Publishing Workflow

### Step-by-Step Guide

#### 1. Prepare for Release

```bash
# Ensure you're on the correct branch
git checkout main
git pull origin main

# Verify builds locally
docker build -f .devcontainer/backend/Dockerfile --target production .
docker build -f .devcontainer/frontend/Dockerfile --target production .
```

#### 2. Update Version

```bash
# Tag release in git
git tag -a v1.0.0 -m "Release version 1.0.0"
git push origin v1.0.0
```

#### 3. Login to Docker Hub

```bash
docker login
# Username: lbrines
# Password: [use Personal Access Token for security]
```

**Generate Personal Access Token**:
1. Go to https://hub.docker.com/settings/security
2. Click "New Access Token"
3. Set description: "ClassSphere Publishing"
4. Set permissions: Read, Write, Delete
5. Copy token (shown only once)
6. Use token as password in `docker login`

#### 4. Run Publishing Script

```bash
# From project root
./scripts/publish-docker-images.sh 1.0.0
```

#### 5. Verify Publication

```bash
# Check on Docker Hub
open https://hub.docker.com/r/lbrines/classsphere-backend
open https://hub.docker.com/r/lbrines/classsphere-frontend

# Test pull
docker pull lbrines/classsphere-backend:1.0.0
docker pull lbrines/classsphere-frontend:1.0.0

# Test run
docker run -d -p 8080:8080 \
  -e JWT_SECRET="test-secret-12345678901234567890123456789012" \
  lbrines/classsphere-backend:1.0.0
```

#### 6. Update Documentation

Update Docker Hub repository descriptions:
1. Go to https://hub.docker.com/r/lbrines/classsphere-backend
2. Click "Edit"
3. Paste content from `docs/DOCKER_HUB_README.md`
4. Repeat for frontend repository

---

## Best Practices

### Before Publishing

- [ ] All tests passing
- [ ] No linter errors
- [ ] Documentation updated
- [ ] CHANGELOG.md updated
- [ ] Version bumped in relevant files
- [ ] Git tag created

### Security

- [ ] No secrets in images
- [ ] Vulnerability scan passed
- [ ] Base images up to date
- [ ] Non-root user configured
- [ ] Personal Access Token used (not password)

### Versioning

- [ ] Semantic versioning followed (MAJOR.MINOR.PATCH)
- [ ] Git tag matches Docker image version
- [ ] Multiple tags applied (specific version + latest)
- [ ] Git SHA tag included for traceability

### After Publishing

- [ ] Images pullable from Docker Hub
- [ ] Docker Hub description updated
- [ ] GitHub release created
- [ ] Team notified
- [ ] Production deployment scheduled

---

## Additional Resources

- **Docker Hub Best Practices**: `workspace/extra/DOCKER_HUB_PUBLISHING_BEST_PRACTICES.md`
- **Container Best Practices**: `workspace/extra/CONTAINERS_BEST_PRACTICES.md`
- **Docker Hub README**: `docs/DOCKER_HUB_README.md`
- **Production Compose**: `docker-compose.production.yml`

---

## Support

For issues with these scripts:
- Check troubleshooting section above
- Review script source code
- Open issue on GitHub
- Contact DevOps team

---

**Last Updated**: 2025-10-08  
**Maintained by**: ClassSphere Development Team

