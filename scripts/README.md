# Scripts Directory

This directory contains utility scripts for ClassSphere development and deployment.

## 📦 Docker Image Publishing

### `publish-docker-images.sh`

Builds Docker images locally and publishes them to Docker Hub.

**Why local builds?**
- ✅ Reduces GitHub Actions minutes usage
- ✅ Full control over build process
- ✅ Faster iterations (no CI queue wait)
- ✅ Test images locally before publishing

**Usage:**
```bash
# Basic usage
./scripts/publish-docker-images.sh 1.0.0

# Build only (skip push)
SKIP_PUSH=true ./scripts/publish-docker-images.sh 1.0.0

# Skip security scans
SKIP_TESTS=true ./scripts/publish-docker-images.sh 1.0.0

# Custom Docker Hub user
DOCKERHUB_USERNAME=myuser ./scripts/publish-docker-images.sh 1.0.0
```

**Prerequisites:**
1. Docker installed and running
2. Docker Hub account and token
3. Git repository

**Setup:**
```bash
# Set Docker Hub credentials
export DOCKERHUB_USERNAME=lbrines
export DOCKERHUB_TOKEN=your_token_here

# Optional: Add to ~/.bashrc or ~/.zshrc
echo 'export DOCKERHUB_TOKEN=your_token_here' >> ~/.bashrc
```

**Features:**
- ✅ Builds both backend and frontend
- ✅ Multi-tag support (version, latest, sha, production)
- ✅ Security scanning with Trivy (containerized, no local install needed)
- ✅ Automatic verification after push
- ✅ Colorized output
- ✅ Error handling and validation

**Tags Created:**
- `lbrines/classsphere-backend:1.0.0` (version)
- `lbrines/classsphere-backend:latest` (latest)
- `lbrines/classsphere-backend:sha-abc123` (git sha)
- `lbrines/classsphere-backend:production` (production tag)

Same for frontend.

**Security Scan:**
The script uses Trivy via Docker container, so you don't need to install Trivy locally:
```bash
# Trivy runs automatically via:
docker run --rm -v /var/run/docker.sock:/var/run/docker.sock \
  aquasec/trivy:latest image --severity HIGH,CRITICAL <image>
```

**Troubleshooting:**

*Error: DOCKERHUB_TOKEN not set*
```bash
export DOCKERHUB_TOKEN=your_token_here
```

*Error: Docker daemon not running*
```bash
sudo systemctl start docker
```

*Error: Permission denied*
```bash
sudo usermod -aG docker $USER
# Then log out and log back in
```

---

## 🧪 Runtime Config Verification

### `verify-runtime-config.sh`

Verifies the TDD implementation of runtime configuration.

**Usage:**
```bash
# Full verification
./scripts/verify-runtime-config.sh

# Skip backend tests
./scripts/verify-runtime-config.sh --skip-backend

# Skip frontend tests
./scripts/verify-runtime-config.sh --skip-frontend

# Skip E2E tests
./scripts/verify-runtime-config.sh --skip-e2e
```

**What it checks:**
- ✅ Backend CORS configuration
- ✅ Frontend EnvironmentService
- ✅ Docker runtime injection (generate-env.sh)
- ✅ Multi-mode support (mock/test/dev/prod)
- ✅ All configuration files exist
- ✅ Documentation completeness

---

## 🔄 CI/CD Workflow

### GitHub Actions

**File:** `.github/workflows/ci.yml`

**What it does:**
- ✅ Runs tests (backend Go, frontend Angular)
- ✅ Runs linters (golangci-lint, biome)
- ✅ Builds applications (validation only)
- ❌ Does NOT build Docker images
- ❌ Does NOT publish to Docker Hub

**Why?**
- Reduces GitHub Actions minutes
- Images are built locally for full control
- CI focuses on code quality, not deployment

**Manual publish workflow:**
```
1. Code changes → commit → push
2. GitHub Actions runs CI tests
3. If tests pass → locally run:
   ./scripts/publish-docker-images.sh 1.0.0
4. Images published to Docker Hub
5. Deploy using docker-compose
```

---

## 📝 Additional Scripts

### `commit-as-model.sh`
Commits changes with model information.

### `setup-models.sh`
Sets up AI model configurations.

### `switch-model.sh`
Switches between AI models.

---

## 🔗 Related Documentation

- [Runtime Config Implementation](../RUNTIME_CONFIG_IMPLEMENTATION.md)
- [Docker Hub README](../docs/DOCKER_HUB_README.md)
- [Contributing Guide](../CONTRIBUTING.md)

---

## 💡 Tips

**Fast development cycle:**
```bash
# 1. Make changes
# 2. Build locally (no push)
SKIP_PUSH=true ./scripts/publish-docker-images.sh dev

# 3. Test locally
docker-compose up -d

# 4. If good, publish
./scripts/publish-docker-images.sh 1.0.0
```

**Security-first approach:**
```bash
# Always scan before publishing
# (default behavior, but can explicitly enable)
SKIP_TESTS=false ./scripts/publish-docker-images.sh 1.0.0
```

**Quick verification:**
```bash
# After publish, verify images work
docker pull lbrines/classsphere-backend:1.0.0
docker pull lbrines/classsphere-frontend:1.0.0
docker-compose up -d
```

---

**Last Updated:** 2025-10-09  
**Maintainer:** ClassSphere Team
