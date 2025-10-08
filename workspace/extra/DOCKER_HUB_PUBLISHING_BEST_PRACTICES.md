# Docker Hub Publishing Best Practices

**Version**: 1.0.0  
**Last Updated**: 2025-10-08  
**Maintained by**: ClassSphere Development Team

---

## 📚 Table of Contents

1. [Introduction](#introduction)
2. [Prerequisites](#prerequisites)
3. [Authentication & Security](#authentication--security)
4. [Building Efficient Images](#building-efficient-images)
5. [Image Tagging Strategy](#image-tagging-strategy)
6. [Security Best Practices](#security-best-practices)
7. [Publishing to Docker Hub](#publishing-to-docker-hub)
8. [CI/CD Automation](#cicd-automation)
9. [Documentation & Metadata](#documentation--metadata)
10. [Monitoring & Maintenance](#monitoring--maintenance)
11. [Best Practices Checklist](#best-practices-checklist)
12. [References](#references)

---

## Introduction

Publishing Docker images to Docker Hub is a critical process that requires careful consideration of security, efficiency, and maintainability. This document provides comprehensive best practices based on official Docker documentation and industry standards.

### Why This Matters

- **Security**: Prevent exposure of secrets and vulnerabilities
- **Performance**: Optimize image size and build time
- **Maintainability**: Enable version control and rollback capabilities
- **Reliability**: Ensure consistent deployments across environments
- **Compliance**: Meet security and audit requirements

### Document Scope

This guide covers:
- Image building optimization
- Security considerations
- Tagging and versioning strategies
- Publishing workflows
- Automation with CI/CD
- Monitoring and maintenance

---

## Prerequisites

### Required Tools

```bash
# Docker Engine 20.10+
docker --version

# Docker Compose 2.0+ (optional)
docker-compose --version

# Git (for version control)
git --version
```

### Docker Hub Account

1. Create account at https://hub.docker.com
2. Generate Personal Access Token (PAT) for automation
3. Configure organization/team access if applicable

### Repository Structure

```
project/
├── Dockerfile                 # Main production Dockerfile
├── Dockerfile.dev            # Development variant (optional)
├── .dockerignore             # Exclude unnecessary files
├── docker-compose.yml        # Multi-service configuration
├── .github/
│   └── workflows/
│       └── docker-publish.yml # CI/CD pipeline
└── docs/
    └── docker/
        └── README.md          # Docker documentation
```

---

## Authentication & Security

### 1. Docker Hub Login

#### Using Password (Development)

```bash
docker login
# Username: your_username
# Password: your_password
```

#### Using Personal Access Token (Production/CI)

**Generate Token**:
1. Go to Docker Hub → Account Settings → Security
2. Create New Access Token
3. Set description and permissions (Read, Write, Delete)
4. Copy token (shown only once)

**Login with Token**:

```bash
# Interactive
docker login -u your_username

# Non-interactive (CI/CD)
echo $DOCKER_TOKEN | docker login -u your_username --password-stdin
```

### 2. Secure Token Storage

#### Local Development

```bash
# Store in secure credential manager
# Linux: ~/.docker/config.json (encrypted)
# macOS: Keychain
# Windows: Credential Manager
```

#### CI/CD Environments

**GitHub Actions**:
```yaml
# Repository → Settings → Secrets → Actions
# Add secrets:
# - DOCKERHUB_USERNAME
# - DOCKERHUB_TOKEN
```

**GitLab CI**:
```yaml
# Settings → CI/CD → Variables
# Add protected variables:
# - DOCKER_USER
# - DOCKER_TOKEN
```

### 3. Security Best Practices

✅ **DO**:
- Use Personal Access Tokens instead of passwords
- Rotate tokens every 90 days
- Use read-only tokens when possible
- Enable 2FA on Docker Hub account
- Limit token scope to specific repositories

❌ **DON'T**:
- Commit tokens to version control
- Share tokens across teams
- Use root account in production
- Store plaintext credentials
- Reuse tokens across environments

---

## Building Efficient Images

### 1. Use Official Base Images

**Recommended Base Images**:

```dockerfile
# Alpine Linux (minimal, 5-10MB)
FROM alpine:3.19

# Debian Slim (minimal Debian, ~80MB)
FROM debian:bookworm-slim

# Ubuntu Minimal (~30MB)
FROM ubuntu:22.04

# Scratch (empty base, 0MB - for static binaries)
FROM scratch

# Distroless (Google maintained, minimal)
FROM gcr.io/distroless/static-debian12
```

**Language-Specific Official Images**:

```dockerfile
# Go
FROM golang:1.24-alpine

# Node.js
FROM node:20-alpine

# Python
FROM python:3.12-slim

# Java
FROM eclipse-temurin:21-jre-alpine
```

### 2. Multi-Stage Builds

**Pattern**: Separate build and runtime stages

```dockerfile
# ========================================
# Stage 1: Build
# ========================================
FROM golang:1.24-alpine AS builder

WORKDIR /build

# Copy dependencies first (cache layer)
COPY go.mod go.sum ./
RUN go mod download

# Copy source and build
COPY . .
RUN CGO_ENABLED=0 GOOS=linux go build \
    -a -installsuffix cgo \
    -ldflags="-w -s" \
    -o app ./cmd/api

# ========================================
# Stage 2: Runtime
# ========================================
FROM alpine:3.19

# Install CA certificates (for HTTPS)
RUN apk --no-cache add ca-certificates

WORKDIR /app

# Copy only binary (not source code)
COPY --from=builder /build/app .

# Run as non-root user
RUN addgroup -g 1001 appuser && \
    adduser -D -u 1001 -G appuser appuser && \
    chown -R appuser:appuser /app

USER appuser

EXPOSE 8080

ENTRYPOINT ["/app/app"]
```

**Benefits**:
- ✅ Smaller final image (only runtime dependencies)
- ✅ No build tools in production image
- ✅ Improved security (reduced attack surface)
- ✅ Faster deployment

### 3. Layer Optimization

**Bad Practice** ❌:
```dockerfile
FROM node:20-alpine
WORKDIR /app
COPY package.json .
RUN npm install
COPY package-lock.json .
RUN npm ci
COPY . .
RUN npm run build
```

**Good Practice** ✅:
```dockerfile
FROM node:20-alpine AS builder
WORKDIR /app

# Layer 1: Dependencies (changes rarely)
COPY package.json package-lock.json ./
RUN npm ci --production

# Layer 2: Source code (changes frequently)
COPY . .
RUN npm run build

# Production stage
FROM node:20-alpine
WORKDIR /app
COPY --from=builder /app/dist ./dist
COPY --from=builder /app/node_modules ./node_modules
CMD ["node", "dist/main.js"]
```

### 4. .dockerignore Configuration

**Essential .dockerignore**:

```gitignore
# Version Control
.git
.gitignore
.gitattributes

# Documentation
*.md
docs/
README*
LICENSE

# Development Files
*.log
*.tmp
*.swp
*~

# Dependencies
node_modules/
vendor/
__pycache__/
*.pyc

# Build Artifacts
dist/
build/
target/
*.o
*.a

# IDE
.vscode/
.idea/
*.iml
.DS_Store

# Testing
coverage/
*.test
*.spec.ts

# CI/CD
.github/
.gitlab-ci.yml
Jenkinsfile

# Environment
.env
.env.*
*.local

# Docker
docker-compose*.yml
Dockerfile*
!Dockerfile

# Temporary
tmp/
temp/
*.bak
```

### 5. Minimize Layers

**Combine RUN Commands**:

```dockerfile
# Bad: 3 layers ❌
RUN apt-get update
RUN apt-get install -y curl git
RUN apt-get clean

# Good: 1 layer ✅
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        curl \
        git \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*
```

### 6. Build Arguments & Cache

**Use Build Args for Flexibility**:

```dockerfile
ARG GO_VERSION=1.24
ARG ALPINE_VERSION=3.19

FROM golang:${GO_VERSION}-alpine AS builder

# Build-time configuration
ARG BUILD_DATE
ARG VCS_REF
ARG VERSION

LABEL org.opencontainers.image.created=$BUILD_DATE \
      org.opencontainers.image.revision=$VCS_REF \
      org.opencontainers.image.version=$VERSION
```

**Build with Args**:

```bash
docker build \
    --build-arg VERSION=1.0.0 \
    --build-arg BUILD_DATE=$(date -u +'%Y-%m-%dT%H:%M:%SZ') \
    --build-arg VCS_REF=$(git rev-parse --short HEAD) \
    -t myapp:1.0.0 .
```

---

## Image Tagging Strategy

### 1. Semantic Versioning

**Format**: `MAJOR.MINOR.PATCH`

```bash
# Example: 1.2.3
# 1 = Major version (breaking changes)
# 2 = Minor version (new features)
# 3 = Patch version (bug fixes)
```

### 2. Recommended Tagging Scheme

```bash
# Build image
docker build -t myapp:build .

# Tag with multiple versions
docker tag myapp:build username/myapp:1.2.3        # Specific version
docker tag myapp:build username/myapp:1.2          # Minor version
docker tag myapp:build username/myapp:1            # Major version
docker tag myapp:build username/myapp:latest       # Latest stable
docker tag myapp:build username/myapp:sha-abc123   # Git commit
docker tag myapp:build username/myapp:production   # Environment
```

### 3. Tag Naming Conventions

| Tag Type | Example | Use Case |
|----------|---------|----------|
| **Semantic** | `1.2.3` | Production releases |
| **Major.Minor** | `1.2` | Track minor versions |
| **Major** | `1` | Track major versions |
| **Latest** | `latest` | Latest stable (avoid in prod) |
| **Git SHA** | `sha-a1b2c3d` | Exact commit reference |
| **Branch** | `main`, `develop` | Branch-specific builds |
| **Environment** | `production`, `staging` | Environment-specific |
| **Date** | `2025-10-08` | Date-based releases |

### 4. Tagging Best Practices

✅ **DO**:
- Use semantic versioning for releases
- Tag with git commit SHA for traceability
- Maintain multiple version tags (1, 1.2, 1.2.3)
- Use immutable tags in production (1.2.3, not latest)
- Document tagging strategy in README

❌ **DON'T**:
- Use `latest` tag in production
- Overwrite existing version tags
- Use ambiguous tags like `v1`, `prod`, `final`
- Mix tagging schemes inconsistently

### 5. Example Tagging Workflow

```bash
#!/bin/bash
# Tag and push script

VERSION="1.2.3"
IMAGE="username/myapp"
GIT_SHA=$(git rev-parse --short HEAD)
BUILD_DATE=$(date -u +'%Y-%m-%d')

# Build
docker build -t ${IMAGE}:build .

# Tag all versions
docker tag ${IMAGE}:build ${IMAGE}:${VERSION}
docker tag ${IMAGE}:build ${IMAGE}:1.2
docker tag ${IMAGE}:build ${IMAGE}:1
docker tag ${IMAGE}:build ${IMAGE}:latest
docker tag ${IMAGE}:build ${IMAGE}:sha-${GIT_SHA}
docker tag ${IMAGE}:build ${IMAGE}:${BUILD_DATE}

# Push all tags
docker push ${IMAGE}:${VERSION}
docker push ${IMAGE}:1.2
docker push ${IMAGE}:1
docker push ${IMAGE}:latest
docker push ${IMAGE}:sha-${GIT_SHA}
docker push ${IMAGE}:${BUILD_DATE}

echo "Published ${IMAGE} with tags:"
echo "  - ${VERSION}"
echo "  - 1.2"
echo "  - 1"
echo "  - latest"
echo "  - sha-${GIT_SHA}"
echo "  - ${BUILD_DATE}"
```

---

## Security Best Practices

### 1. Vulnerability Scanning

#### Docker Scan (Built-in)

```bash
# Scan local image
docker scan myapp:latest

# Scan on Docker Hub
docker scan username/myapp:1.0.0

# Scan with specific severity
docker scan --severity high myapp:latest

# Output to JSON
docker scan --json myapp:latest > scan-results.json
```

#### Trivy (Recommended)

```bash
# Install Trivy
# macOS
brew install aquasecurity/trivy/trivy

# Linux
wget -qO - https://aquasecurity.github.io/trivy-repo/deb/public.key | sudo apt-key add -
echo "deb https://aquasecurity.github.io/trivy-repo/deb $(lsb_release -sc) main" | sudo tee -a /etc/apt/sources.list.d/trivy.list
sudo apt-get update && sudo apt-get install trivy

# Scan image
trivy image username/myapp:1.0.0

# Scan with specific severity
trivy image --severity HIGH,CRITICAL username/myapp:1.0.0

# Output to SARIF (for GitHub)
trivy image --format sarif --output trivy-results.sarif username/myapp:1.0.0
```

#### Snyk

```bash
# Install Snyk
npm install -g snyk

# Authenticate
snyk auth

# Scan Docker image
snyk container test username/myapp:1.0.0

# Monitor image
snyk container monitor username/myapp:1.0.0
```

### 2. Run as Non-Root User

**Bad Practice** ❌:
```dockerfile
FROM alpine:3.19
COPY app /app
EXPOSE 8080
CMD ["/app"]
# Runs as root (UID 0)
```

**Good Practice** ✅:
```dockerfile
FROM alpine:3.19

# Create non-root user
RUN addgroup -g 1001 appuser && \
    adduser -D -u 1001 -G appuser appuser

WORKDIR /app
COPY --chown=appuser:appuser app /app

# Switch to non-root
USER appuser

EXPOSE 8080
CMD ["/app"]
```

### 3. Secrets Management

#### Never Include Secrets in Image

❌ **BAD**:
```dockerfile
# NEVER DO THIS
FROM node:20-alpine
COPY .env /app/.env
ENV API_KEY="abc123secret"
```

✅ **GOOD**:
```dockerfile
# Use runtime environment variables
FROM node:20-alpine
WORKDIR /app
COPY package*.json ./
RUN npm ci --production
COPY . .
# Secrets provided at runtime via -e or docker-compose
CMD ["node", "server.js"]
```

#### Proper Secrets Handling

**Docker Run**:
```bash
docker run -e API_KEY="$API_KEY" myapp:latest
```

**Docker Compose**:
```yaml
services:
  app:
    image: myapp:latest
    environment:
      - API_KEY=${API_KEY}
    # Or use secrets (Docker Swarm/Compose)
    secrets:
      - api_key

secrets:
  api_key:
    file: ./secrets/api_key.txt
```

**Kubernetes**:
```yaml
apiVersion: v1
kind: Secret
metadata:
  name: app-secrets
type: Opaque
data:
  api-key: YWJjMTIzc2VjcmV0  # base64 encoded
---
apiVersion: v1
kind: Pod
metadata:
  name: myapp
spec:
  containers:
  - name: app
    image: username/myapp:1.0.0
    env:
    - name: API_KEY
      valueFrom:
        secretKeyRef:
          name: app-secrets
          key: api-key
```

### 4. Image Signing & Verification

#### Docker Content Trust (DCT)

```bash
# Enable DCT
export DOCKER_CONTENT_TRUST=1

# Push signed image
docker push username/myapp:1.0.0
# Will prompt for passphrase

# Pull and verify
docker pull username/myapp:1.0.0
# Automatically verifies signature
```

#### Cosign (Sigstore)

```bash
# Install cosign
brew install cosign

# Generate key pair
cosign generate-key-pair

# Sign image
cosign sign --key cosign.key username/myapp:1.0.0

# Verify signature
cosign verify --key cosign.pub username/myapp:1.0.0
```

### 5. Security Checklist

- [ ] Base image from official/trusted source
- [ ] Scan for vulnerabilities (Trivy/Snyk)
- [ ] Run as non-root user
- [ ] No secrets in image layers
- [ ] Minimal attack surface (distroless/alpine)
- [ ] HTTPS/TLS for all communications
- [ ] Image signing enabled
- [ ] Regular security updates
- [ ] Audit logs enabled
- [ ] Least privilege principle

---

## Publishing to Docker Hub

### 1. Manual Publishing

#### Basic Workflow

```bash
# 1. Build image
docker build -t myapp:latest .

# 2. Tag for Docker Hub
docker tag myapp:latest username/myapp:1.0.0
docker tag myapp:latest username/myapp:latest

# 3. Push to Docker Hub
docker push username/myapp:1.0.0
docker push username/myapp:latest

# 4. Verify
docker pull username/myapp:1.0.0
```

#### Complete Publishing Script

```bash
#!/bin/bash
# scripts/publish-docker.sh

set -e

# Configuration
DOCKER_USER="${DOCKER_USER:-username}"
IMAGE_NAME="myapp"
VERSION="${1:-latest}"
DOCKERFILE="${2:-Dockerfile}"

echo "========================================="
echo "Docker Image Publisher"
echo "========================================="
echo "User: $DOCKER_USER"
echo "Image: $IMAGE_NAME"
echo "Version: $VERSION"
echo "Dockerfile: $DOCKERFILE"
echo "========================================="

# Verify Docker login
if ! docker info | grep -q "Username: $DOCKER_USER"; then
    echo "Error: Not logged in to Docker Hub"
    echo "Run: docker login"
    exit 1
fi

# Build image
echo "Building image..."
docker build \
    -f "$DOCKERFILE" \
    -t "${IMAGE_NAME}:build" \
    --build-arg VERSION="$VERSION" \
    --build-arg BUILD_DATE="$(date -u +'%Y-%m-%dT%H:%M:%SZ')" \
    .

# Scan for vulnerabilities
echo "Scanning for vulnerabilities..."
if command -v trivy &> /dev/null; then
    trivy image --severity HIGH,CRITICAL "${IMAGE_NAME}:build"
else
    echo "Warning: Trivy not installed, skipping scan"
fi

# Tag image
echo "Tagging image..."
docker tag "${IMAGE_NAME}:build" "${DOCKER_USER}/${IMAGE_NAME}:${VERSION}"
docker tag "${IMAGE_NAME}:build" "${DOCKER_USER}/${IMAGE_NAME}:latest"

# Get image size
SIZE=$(docker images "${DOCKER_USER}/${IMAGE_NAME}:${VERSION}" --format "{{.Size}}")
echo "Image size: $SIZE"

# Push to Docker Hub
echo "Pushing to Docker Hub..."
docker push "${DOCKER_USER}/${IMAGE_NAME}:${VERSION}"
docker push "${DOCKER_USER}/${IMAGE_NAME}:latest"

echo "========================================="
echo "✓ Successfully published!"
echo "Image: ${DOCKER_USER}/${IMAGE_NAME}:${VERSION}"
echo "URL: https://hub.docker.com/r/${DOCKER_USER}/${IMAGE_NAME}"
echo "========================================="
```

### 2. Repository Configuration

#### Set Description on Docker Hub

1. Go to https://hub.docker.com/repository/docker/username/myapp
2. Click "Edit"
3. Add:
   - **Short Description**: One-line summary (max 100 chars)
   - **Full Description**: Detailed README (supports Markdown)

#### Example README for Docker Hub

```markdown
# MyApp - Production-Ready Application

[![Docker Pulls](https://img.shields.io/docker/pulls/username/myapp)](https://hub.docker.com/r/username/myapp)
[![Docker Image Size](https://img.shields.io/docker/image-size/username/myapp/latest)](https://hub.docker.com/r/username/myapp)

## Quick Start

```bash
docker run -d -p 8080:8080 username/myapp:latest
```

## Supported Tags

- `1.0.0`, `1.0`, `1`, `latest` - Latest stable release
- `sha-abc123` - Specific commit builds

## Configuration

### Environment Variables

- `API_KEY` - Required API key
- `PORT` - Server port (default: 8080)
- `LOG_LEVEL` - Logging level (default: info)

### Volumes

- `/app/data` - Persistent data storage

### Ports

- `8080` - HTTP server

## Example Usage

### Basic

```bash
docker run -d \
    -p 8080:8080 \
    -e API_KEY=your_key \
    username/myapp:latest
```

### With Docker Compose

```yaml
services:
  myapp:
    image: username/myapp:latest
    ports:
      - "8080:8080"
    environment:
      - API_KEY=your_key
    volumes:
      - app-data:/app/data

volumes:
  app-data:
```

## Health Check

```bash
curl http://localhost:8080/health
```

## Support

- GitHub: https://github.com/username/myapp
- Issues: https://github.com/username/myapp/issues
- Docs: https://myapp.example.com/docs

## License

MIT License - see LICENSE file
```

### 3. Multi-Platform Images

Build for multiple architectures:

```bash
# Setup buildx
docker buildx create --name multiarch --use
docker buildx inspect --bootstrap

# Build for multiple platforms
docker buildx build \
    --platform linux/amd64,linux/arm64,linux/arm/v7 \
    -t username/myapp:1.0.0 \
    --push \
    .

# Verify
docker buildx imagetools inspect username/myapp:1.0.0
```

---

## CI/CD Automation

### 1. GitHub Actions

**Complete Workflow** (`.github/workflows/docker-publish.yml`):

```yaml
name: Docker Publish

on:
  push:
    branches: [ main ]
    tags: [ 'v*' ]
  pull_request:
    branches: [ main ]
  workflow_dispatch:

env:
  REGISTRY: docker.io
  IMAGE_NAME: username/myapp

jobs:
  # ==========================================
  # Build and Test
  # ==========================================
  build:
    runs-on: ubuntu-latest
    permissions:
      contents: read
      packages: write

    steps:
      - name: Checkout repository
        uses: actions/checkout@v4

      - name: Set up Docker Buildx
        uses: docker/setup-buildx-action@v3

      - name: Extract metadata
        id: meta
        uses: docker/metadata-action@v5
        with:
          images: ${{ env.IMAGE_NAME }}
          tags: |
            type=ref,event=branch
            type=ref,event=pr
            type=semver,pattern={{version}}
            type=semver,pattern={{major}}.{{minor}}
            type=semver,pattern={{major}}
            type=sha,prefix=sha-

      - name: Build Docker image
        uses: docker/build-push-action@v5
        with:
          context: .
          push: false
          load: true
          tags: ${{ steps.meta.outputs.tags }}
          labels: ${{ steps.meta.outputs.labels }}
          cache-from: type=gha
          cache-to: type=gha,mode=max

      - name: Run tests
        run: |
          docker run --rm ${{ env.IMAGE_NAME }}:${{ github.sha }} npm test

  # ==========================================
  # Security Scan
  # ==========================================
  scan:
    runs-on: ubuntu-latest
    needs: build
    permissions:
      security-events: write

    steps:
      - name: Checkout repository
        uses: actions/checkout@v4

      - name: Build image for scanning
        run: docker build -t scan-image .

      - name: Run Trivy vulnerability scanner
        uses: aquasecurity/trivy-action@master
        with:
          image-ref: scan-image
          format: 'sarif'
          output: 'trivy-results.sarif'
          severity: 'CRITICAL,HIGH'

      - name: Upload Trivy results to GitHub Security
        uses: github/codeql-action/upload-sarif@v3
        with:
          sarif_file: 'trivy-results.sarif'

      - name: Fail on HIGH/CRITICAL vulnerabilities
        uses: aquasecurity/trivy-action@master
        with:
          image-ref: scan-image
          exit-code: '1'
          severity: 'CRITICAL,HIGH'

  # ==========================================
  # Publish to Docker Hub
  # ==========================================
  publish:
    runs-on: ubuntu-latest
    needs: [build, scan]
    if: github.event_name != 'pull_request'
    permissions:
      contents: read

    steps:
      - name: Checkout repository
        uses: actions/checkout@v4

      - name: Set up Docker Buildx
        uses: docker/setup-buildx-action@v3

      - name: Log in to Docker Hub
        uses: docker/login-action@v3
        with:
          username: ${{ secrets.DOCKERHUB_USERNAME }}
          password: ${{ secrets.DOCKERHUB_TOKEN }}

      - name: Extract metadata
        id: meta
        uses: docker/metadata-action@v5
        with:
          images: ${{ env.IMAGE_NAME }}
          tags: |
            type=ref,event=branch
            type=semver,pattern={{version}}
            type=semver,pattern={{major}}.{{minor}}
            type=semver,pattern={{major}}
            type=sha,prefix=sha-
            type=raw,value=latest,enable={{is_default_branch}}

      - name: Build and push Docker image
        uses: docker/build-push-action@v5
        with:
          context: .
          platforms: linux/amd64,linux/arm64
          push: true
          tags: ${{ steps.meta.outputs.tags }}
          labels: ${{ steps.meta.outputs.labels }}
          cache-from: type=gha
          cache-to: type=gha,mode=max

      - name: Update Docker Hub description
        uses: peter-evans/dockerhub-description@v4
        with:
          username: ${{ secrets.DOCKERHUB_USERNAME }}
          password: ${{ secrets.DOCKERHUB_TOKEN }}
          repository: ${{ env.IMAGE_NAME }}
          readme-filepath: ./docs/DOCKER_README.md
```

### 2. GitLab CI

**Complete Pipeline** (`.gitlab-ci.yml`):

```yaml
variables:
  DOCKER_DRIVER: overlay2
  DOCKER_TLS_CERTDIR: "/certs"
  IMAGE_NAME: username/myapp
  DOCKER_BUILDKIT: 1

stages:
  - build
  - test
  - scan
  - publish

# ==========================================
# Build Stage
# ==========================================
build:
  stage: build
  image: docker:24-git
  services:
    - docker:24-dind
  before_script:
    - docker login -u $CI_REGISTRY_USER -p $CI_REGISTRY_PASSWORD
  script:
    - docker build -t ${IMAGE_NAME}:${CI_COMMIT_SHA} .
    - docker save ${IMAGE_NAME}:${CI_COMMIT_SHA} -o image.tar
  artifacts:
    paths:
      - image.tar
    expire_in: 1 hour

# ==========================================
# Test Stage
# ==========================================
test:
  stage: test
  image: docker:24
  services:
    - docker:24-dind
  dependencies:
    - build
  script:
    - docker load -i image.tar
    - docker run --rm ${IMAGE_NAME}:${CI_COMMIT_SHA} npm test

# ==========================================
# Security Scan
# ==========================================
trivy-scan:
  stage: scan
  image: aquasec/trivy:latest
  dependencies:
    - build
  script:
    - trivy image --exit-code 0 --severity LOW,MEDIUM ${IMAGE_NAME}:${CI_COMMIT_SHA}
    - trivy image --exit-code 1 --severity HIGH,CRITICAL ${IMAGE_NAME}:${CI_COMMIT_SHA}
  allow_failure: false

# ==========================================
# Publish to Docker Hub
# ==========================================
publish:
  stage: publish
  image: docker:24-git
  services:
    - docker:24-dind
  dependencies:
    - build
  only:
    - main
    - tags
  before_script:
    - echo $DOCKERHUB_TOKEN | docker login -u $DOCKERHUB_USERNAME --password-stdin
  script:
    - docker load -i image.tar
    - |
      # Tag with commit SHA
      docker tag ${IMAGE_NAME}:${CI_COMMIT_SHA} ${IMAGE_NAME}:sha-${CI_COMMIT_SHORT_SHA}
      
      # Tag with branch name
      if [ "$CI_COMMIT_BRANCH" = "main" ]; then
        docker tag ${IMAGE_NAME}:${CI_COMMIT_SHA} ${IMAGE_NAME}:latest
      fi
      
      # Tag with version if git tag
      if [ -n "$CI_COMMIT_TAG" ]; then
        docker tag ${IMAGE_NAME}:${CI_COMMIT_SHA} ${IMAGE_NAME}:${CI_COMMIT_TAG}
      fi
      
      # Push all tags
      docker push ${IMAGE_NAME} --all-tags
```

### 3. CircleCI

**Configuration** (`.circleci/config.yml`):

```yaml
version: 2.1

orbs:
  docker: circleci/docker@2.4.0

workflows:
  build-test-publish:
    jobs:
      - build-and-test
      - scan:
          requires:
            - build-and-test
      - publish:
          requires:
            - scan
          filters:
            branches:
              only: main

jobs:
  build-and-test:
    docker:
      - image: cimg/base:stable
    steps:
      - checkout
      - setup_remote_docker:
          docker_layer_caching: true
      - run:
          name: Build Docker image
          command: |
            docker build -t myapp:${CIRCLE_SHA1} .
      - run:
          name: Run tests
          command: |
            docker run --rm myapp:${CIRCLE_SHA1} npm test

  scan:
    docker:
      - image: aquasec/trivy:latest
    steps:
      - checkout
      - setup_remote_docker
      - run:
          name: Scan for vulnerabilities
          command: |
            trivy image --exit-code 1 --severity HIGH,CRITICAL myapp:${CIRCLE_SHA1}

  publish:
    docker:
      - image: cimg/base:stable
    steps:
      - checkout
      - setup_remote_docker:
          docker_layer_caching: true
      - run:
          name: Build and push to Docker Hub
          command: |
            echo $DOCKERHUB_TOKEN | docker login -u $DOCKERHUB_USERNAME --password-stdin
            docker build -t username/myapp:latest -t username/myapp:${CIRCLE_SHA1} .
            docker push username/myapp --all-tags
```

---

## Documentation & Metadata

### 1. Image Labels (OCI Standard)

**Dockerfile with Labels**:

```dockerfile
FROM alpine:3.19

# OCI Image Labels
LABEL org.opencontainers.image.title="MyApp" \
      org.opencontainers.image.description="Production-ready application" \
      org.opencontainers.image.version="1.0.0" \
      org.opencontainers.image.authors="Your Team <team@example.com>" \
      org.opencontainers.image.url="https://github.com/username/myapp" \
      org.opencontainers.image.source="https://github.com/username/myapp" \
      org.opencontainers.image.documentation="https://docs.example.com" \
      org.opencontainers.image.vendor="Your Company" \
      org.opencontainers.image.licenses="MIT" \
      org.opencontainers.image.created="2025-10-08T12:00:00Z" \
      org.opencontainers.image.revision="abc123"

# Custom labels
LABEL maintainer="team@example.com" \
      app.version="1.0.0" \
      app.environment="production"

# Application code
WORKDIR /app
COPY . .

CMD ["/app/start.sh"]
```

**Inspect Labels**:

```bash
# View all labels
docker inspect username/myapp:1.0.0 | jq '.[0].Config.Labels'

# Filter specific label
docker inspect username/myapp:1.0.0 | jq -r '.[0].Config.Labels["org.opencontainers.image.version"]'
```

### 2. Health Checks

**In Dockerfile**:

```dockerfile
FROM node:20-alpine

WORKDIR /app
COPY package*.json ./
RUN npm ci --production
COPY . .

EXPOSE 3000

# Health check configuration
HEALTHCHECK --interval=30s \
            --timeout=3s \
            --start-period=30s \
            --retries=3 \
  CMD node healthcheck.js || exit 1

CMD ["node", "server.js"]
```

**healthcheck.js**:

```javascript
const http = require('http');

const options = {
  host: 'localhost',
  port: 3000,
  path: '/health',
  timeout: 2000
};

const request = http.request(options, (res) => {
  if (res.statusCode === 200) {
    process.exit(0);
  } else {
    process.exit(1);
  }
});

request.on('error', () => {
  process.exit(1);
});

request.end();
```

### 3. Build Information

**Inject Build Info at Build Time**:

```dockerfile
ARG BUILD_DATE
ARG VCS_REF
ARG VERSION

LABEL org.opencontainers.image.created=$BUILD_DATE \
      org.opencontainers.image.revision=$VCS_REF \
      org.opencontainers.image.version=$VERSION
```

**Build Script**:

```bash
#!/bin/bash

VERSION=$(git describe --tags --always)
BUILD_DATE=$(date -u +'%Y-%m-%dT%H:%M:%SZ')
VCS_REF=$(git rev-parse --short HEAD)

docker build \
  --build-arg VERSION="$VERSION" \
  --build-arg BUILD_DATE="$BUILD_DATE" \
  --build-arg VCS_REF="$VCS_REF" \
  -t username/myapp:${VERSION} \
  .
```

---

## Monitoring & Maintenance

### 1. Image Size Monitoring

```bash
# Check image sizes
docker images --format "table {{.Repository}}\t{{.Tag}}\t{{.Size}}" | grep myapp

# Compare image layers
docker history username/myapp:1.0.0

# Detailed layer analysis
dive username/myapp:1.0.0
```

**Install dive**:
```bash
# macOS
brew install dive

# Linux
wget https://github.com/wagoodman/dive/releases/download/v0.11.0/dive_0.11.0_linux_amd64.deb
sudo apt install ./dive_0.11.0_linux_amd64.deb
```

### 2. Pull Statistics

Monitor Docker Hub statistics:

```bash
# Via Docker Hub API
curl -s https://hub.docker.com/v2/repositories/username/myapp/ | jq '{name, pull_count, star_count}'
```

### 3. Automated Updates

**Dependabot for Dockerfile** (`.github/dependabot.yml`):

```yaml
version: 2
updates:
  # Update Docker base images
  - package-ecosystem: "docker"
    directory: "/"
    schedule:
      interval: "weekly"
    open-pull-requests-limit: 5
    reviewers:
      - "team-devops"
    labels:
      - "docker"
      - "dependencies"
```

### 4. Retention Policy

**Manual Cleanup**:

```bash
# List all tags
curl -s https://hub.docker.com/v2/repositories/username/myapp/tags/ | jq -r '.results[].name'

# Delete old tag (requires auth token)
TOKEN=$(curl -s -H "Content-Type: application/json" -X POST \
  -d '{"username":"'$DOCKERHUB_USERNAME'","password":"'$DOCKERHUB_PASSWORD'"}' \
  https://hub.docker.com/v2/users/login/ | jq -r .token)

curl -X DELETE \
  -H "Authorization: JWT ${TOKEN}" \
  https://hub.docker.com/v2/repositories/username/myapp/tags/old-tag/
```

**Automated Cleanup Script**:

```bash
#!/bin/bash
# scripts/cleanup-old-images.sh

REPO="username/myapp"
KEEP_TAGS=("latest" "production" "staging")
KEEP_LAST_N=10

echo "Cleaning up old Docker images from $REPO"

# Get auth token
TOKEN=$(curl -s -H "Content-Type: application/json" -X POST \
  -d "{\"username\":\"$DOCKERHUB_USERNAME\",\"password\":\"$DOCKERHUB_PASSWORD\"}" \
  https://hub.docker.com/v2/users/login/ | jq -r .token)

# Get all tags
TAGS=$(curl -s https://hub.docker.com/v2/repositories/$REPO/tags/ | jq -r '.results[].name')

# Delete old tags
for TAG in $TAGS; do
  # Skip protected tags
  if [[ " ${KEEP_TAGS[@]} " =~ " ${TAG} " ]]; then
    echo "Skipping protected tag: $TAG"
    continue
  fi
  
  # Delete old tags (implement your logic)
  echo "Would delete: $TAG"
  # Uncomment to actually delete:
  # curl -X DELETE -H "Authorization: JWT ${TOKEN}" \
  #   https://hub.docker.com/v2/repositories/$REPO/tags/$TAG/
done
```

---

## Best Practices Checklist

### Pre-Publishing

- [ ] **Dockerfile optimized**
  - [ ] Multi-stage build implemented
  - [ ] Minimal base image (alpine/distroless)
  - [ ] Layers optimized (combined RUN commands)
  - [ ] .dockerignore configured
  - [ ] Build cache utilized

- [ ] **Security hardened**
  - [ ] Run as non-root user
  - [ ] No secrets in image
  - [ ] Vulnerabilities scanned (Trivy/Snyk)
  - [ ] Base image from trusted source
  - [ ] Security updates applied

- [ ] **Properly tagged**
  - [ ] Semantic versioning used
  - [ ] Multiple tags applied (1.0.0, 1.0, 1, latest)
  - [ ] Git SHA tagged
  - [ ] Immutable tags for production

- [ ] **Documented**
  - [ ] README.md in repository
  - [ ] Docker Hub description updated
  - [ ] OCI labels configured
  - [ ] Usage examples provided
  - [ ] Environment variables documented

### Publishing

- [ ] **Build process**
  - [ ] Clean build environment
  - [ ] Build arguments set
  - [ ] Multi-platform if needed
  - [ ] Build logs reviewed

- [ ] **Testing**
  - [ ] Unit tests passed
  - [ ] Integration tests passed
  - [ ] Health check verified
  - [ ] Smoke tests on image

- [ ] **Verification**
  - [ ] Image size reasonable (<500MB production)
  - [ ] All tags pushed
  - [ ] Image pullable from Docker Hub
  - [ ] Labels correct (docker inspect)

### Post-Publishing

- [ ] **Monitoring**
  - [ ] Pull statistics tracked
  - [ ] Vulnerability alerts configured
  - [ ] Update notifications enabled

- [ ] **Maintenance**
  - [ ] Retention policy defined
  - [ ] Old images cleaned up
  - [ ] CI/CD pipeline functional
  - [ ] Dependencies updated regularly

- [ ] **Documentation**
  - [ ] Release notes published
  - [ ] Changelog updated
  - [ ] Migration guide (if breaking changes)
  - [ ] Security advisories documented

---

## References

### Official Documentation

1. **Docker Hub**
   - https://docs.docker.com/docker-hub/
   - https://docs.docker.com/docker-hub/repos/

2. **Dockerfile Best Practices**
   - https://docs.docker.com/develop/develop-images/dockerfile_best-practices/
   - https://docs.docker.com/build/building/best-practices/

3. **Multi-Stage Builds**
   - https://docs.docker.com/build/building/multi-stage/

4. **Security**
   - https://docs.docker.com/engine/security/
   - https://snyk.io/learn/docker-security-scanning/

5. **OCI Image Spec**
   - https://github.com/opencontainers/image-spec/blob/main/annotations.md

### Tools

1. **Trivy** (Vulnerability Scanner)
   - https://github.com/aquasecurity/trivy

2. **Dive** (Image Analysis)
   - https://github.com/wagoodman/dive

3. **Hadolint** (Dockerfile Linter)
   - https://github.com/hadolint/hadolint

4. **Cosign** (Image Signing)
   - https://github.com/sigstore/cosign

### Community Resources

1. **Docker Best Practices**
   - https://testdriven.io/blog/docker-best-practices/
   - https://sysdig.com/blog/dockerfile-best-practices/

2. **Security Guides**
   - https://cheatsheetseries.owasp.org/cheatsheets/Docker_Security_Cheat_Sheet.html
   - https://kubernetes.io/docs/concepts/containers/images/

3. **CI/CD Examples**
   - https://github.com/docker/build-push-action
   - https://docs.gitlab.com/ee/ci/docker/using_docker_build.html

---

## Appendix: ClassSphere Example

### Project Context

ClassSphere uses multi-stage Dockerfiles for backend (Go) and frontend (Angular).

**Repository Structure**:
```
ClassSphere/
├── .devcontainer/
│   ├── backend/
│   │   └── Dockerfile          # Multi-stage: development + production
│   ├── frontend/
│   │   └── Dockerfile          # Multi-stage: development + production
│   └── docker-compose.yml
└── scripts/
    └── publish-docker-images.sh
```

### Publishing Script for ClassSphere

```bash
#!/bin/bash
# scripts/publish-docker-images.sh
# Publishes ClassSphere backend and frontend to Docker Hub

set -e

DOCKER_USER="${DOCKER_USER:-lbrines}"
VERSION="${1:-1.0.0}"
PROJECT_ROOT="/home/lbrines/projects/AI/ClassSphere"

echo "========================================="
echo "ClassSphere Docker Image Publisher"
echo "========================================="
echo "User: $DOCKER_USER"
echo "Version: $VERSION"
echo "========================================="

# Check authentication
if ! docker info | grep -q "Username: $DOCKER_USER"; then
    echo "Error: Not logged in to Docker Hub"
    echo "Run: docker login"
    exit 1
fi

cd "$PROJECT_ROOT"

# ==========================================
# Backend (Go 1.24 + Echo v4)
# ==========================================
echo ""
echo "Building Backend..."
docker build \
    -f .devcontainer/backend/Dockerfile \
    -t ${DOCKER_USER}/classsphere-backend:${VERSION} \
    -t ${DOCKER_USER}/classsphere-backend:latest \
    -t ${DOCKER_USER}/classsphere-backend:production \
    --target production \
    .

echo "Scanning Backend..."
if command -v trivy &> /dev/null; then
    trivy image --severity HIGH,CRITICAL ${DOCKER_USER}/classsphere-backend:${VERSION}
fi

echo "Pushing Backend..."
docker push ${DOCKER_USER}/classsphere-backend:${VERSION}
docker push ${DOCKER_USER}/classsphere-backend:latest
docker push ${DOCKER_USER}/classsphere-backend:production

# ==========================================
# Frontend (Angular 19 + Nginx)
# ==========================================
echo ""
echo "Building Frontend..."
docker build \
    -f .devcontainer/frontend/Dockerfile \
    -t ${DOCKER_USER}/classsphere-frontend:${VERSION} \
    -t ${DOCKER_USER}/classsphere-frontend:latest \
    -t ${DOCKER_USER}/classsphere-frontend:production \
    --target production \
    .

echo "Scanning Frontend..."
if command -v trivy &> /dev/null; then
    trivy image --severity HIGH,CRITICAL ${DOCKER_USER}/classsphere-frontend:${VERSION}
fi

echo "Pushing Frontend..."
docker push ${DOCKER_USER}/classsphere-frontend:${VERSION}
docker push ${DOCKER_USER}/classsphere-frontend:latest
docker push ${DOCKER_USER}/classsphere-frontend:production

# ==========================================
# Summary
# ==========================================
echo ""
echo "========================================="
echo "✓ All images published successfully!"
echo "========================================="
echo ""
echo "Backend:  ${DOCKER_USER}/classsphere-backend:${VERSION}"
echo "Frontend: ${DOCKER_USER}/classsphere-frontend:${VERSION}"
echo ""
echo "Docker Hub: https://hub.docker.com/u/${DOCKER_USER}"
echo ""
echo "Image Sizes:"
docker images | grep "classsphere" | grep -E "${VERSION}|latest|production"
```

### Usage

```bash
# Make executable
chmod +x scripts/publish-docker-images.sh

# Publish
./scripts/publish-docker-images.sh 1.0.0
```

---

**End of Document**

*This document is part of the ClassSphere project documentation.*  
*For questions or improvements, please open an issue or pull request.*

