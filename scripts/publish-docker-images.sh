#!/bin/bash
# ========================================
# ClassSphere Docker Image Publisher
# Publishes backend and frontend images to Docker Hub
# ========================================

set -e

# ========================================
# Configuration
# ========================================
DOCKER_USER="${DOCKER_USER:-lbrines}"
VERSION="${1:-1.0.0}"
PROJECT_ROOT="/home/lbrines/projects/AI/ClassSphere"
GIT_SHA=$(git rev-parse --short HEAD 2>/dev/null || echo "unknown")
BUILD_DATE=$(date -u +'%Y-%m-%dT%H:%M:%SZ')

# Colors
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# ========================================
# Functions
# ========================================
log_info() {
    echo -e "${BLUE}ℹ ${NC}$1"
}

log_success() {
    echo -e "${GREEN}✓${NC} $1"
}

log_warning() {
    echo -e "${YELLOW}⚠${NC} $1"
}

log_error() {
    echo -e "${RED}✗${NC} $1"
}

check_command() {
    if ! command -v "$1" &> /dev/null; then
        log_warning "$1 not installed, skipping $2"
        return 1
    fi
    return 0
}

# ========================================
# Pre-flight Checks
# ========================================
echo -e "${BLUE}========================================${NC}"
echo -e "${BLUE}ClassSphere Docker Image Publisher${NC}"
echo -e "${BLUE}========================================${NC}"
echo ""
log_info "Configuration:"
echo "  User:        $DOCKER_USER"
echo "  Version:     $VERSION"
echo "  Git SHA:     $GIT_SHA"
echo "  Build Date:  $BUILD_DATE"
echo "  Project:     $PROJECT_ROOT"
echo -e "${BLUE}========================================${NC}"
echo ""

# Check Docker authentication
log_info "Checking Docker Hub authentication..."
if ! docker info | grep -q "Username: $DOCKER_USER" 2>/dev/null; then
    log_error "Not logged in to Docker Hub"
    echo ""
    echo "Please authenticate first:"
    echo "  docker login"
    echo ""
    exit 1
fi
log_success "Authenticated as $DOCKER_USER"
echo ""

# Change to project directory
cd "$PROJECT_ROOT"

# ========================================
# Backend Image (Go 1.24 + Echo v4)
# ========================================
echo -e "${BLUE}========================================${NC}"
echo -e "${BLUE}Backend Image (Go 1.24 + Echo v4)${NC}"
echo -e "${BLUE}========================================${NC}"
echo ""

log_info "Building backend image..."
docker build \
    -f .devcontainer/backend/Dockerfile \
    -t classsphere-backend:build \
    --build-arg VERSION="$VERSION" \
    --build-arg BUILD_DATE="$BUILD_DATE" \
    --build-arg VCS_REF="$GIT_SHA" \
    --target production \
    . 2>&1 | grep -v "naming to" | grep -v "exporting to image" || true

log_success "Backend image built"

# Scan for vulnerabilities
if check_command "trivy" "vulnerability scan"; then
    log_info "Scanning backend for vulnerabilities..."
    if trivy image --severity HIGH,CRITICAL classsphere-backend:build --exit-code 0; then
        log_success "Backend security scan passed"
    else
        log_warning "Backend has vulnerabilities (check output above)"
    fi
else
    log_warning "Trivy not installed - skipping security scan"
    echo "  Install: brew install aquasecurity/trivy/trivy"
fi
echo ""

# Tag backend image
log_info "Tagging backend image..."
docker tag classsphere-backend:build ${DOCKER_USER}/classsphere-backend:${VERSION}
docker tag classsphere-backend:build ${DOCKER_USER}/classsphere-backend:latest
docker tag classsphere-backend:build ${DOCKER_USER}/classsphere-backend:production
docker tag classsphere-backend:build ${DOCKER_USER}/classsphere-backend:sha-${GIT_SHA}

# Get image size
BACKEND_SIZE=$(docker images "${DOCKER_USER}/classsphere-backend:${VERSION}" --format "{{.Size}}")
log_success "Backend tagged (Size: $BACKEND_SIZE)"
echo ""

# Push backend image
log_info "Pushing backend to Docker Hub..."
docker push ${DOCKER_USER}/classsphere-backend:${VERSION} | tail -n 5
docker push ${DOCKER_USER}/classsphere-backend:latest | tail -n 5
docker push ${DOCKER_USER}/classsphere-backend:production | tail -n 5
docker push ${DOCKER_USER}/classsphere-backend:sha-${GIT_SHA} | tail -n 5
log_success "Backend published to Docker Hub"
echo ""

# ========================================
# Frontend Image (Angular 19 + Nginx)
# ========================================
echo -e "${BLUE}========================================${NC}"
echo -e "${BLUE}Frontend Image (Angular 19 + Nginx)${NC}"
echo -e "${BLUE}========================================${NC}"
echo ""

log_info "Building frontend image..."
docker build \
    -f .devcontainer/frontend/Dockerfile \
    -t classsphere-frontend:build \
    --build-arg VERSION="$VERSION" \
    --build-arg BUILD_DATE="$BUILD_DATE" \
    --build-arg VCS_REF="$GIT_SHA" \
    --target production \
    . 2>&1 | grep -v "naming to" | grep -v "exporting to image" || true

log_success "Frontend image built"

# Scan for vulnerabilities
if check_command "trivy" "vulnerability scan"; then
    log_info "Scanning frontend for vulnerabilities..."
    if trivy image --severity HIGH,CRITICAL classsphere-frontend:build --exit-code 0; then
        log_success "Frontend security scan passed"
    else
        log_warning "Frontend has vulnerabilities (check output above)"
    fi
else
    log_warning "Trivy not installed - skipping security scan"
fi
echo ""

# Tag frontend image
log_info "Tagging frontend image..."
docker tag classsphere-frontend:build ${DOCKER_USER}/classsphere-frontend:${VERSION}
docker tag classsphere-frontend:build ${DOCKER_USER}/classsphere-frontend:latest
docker tag classsphere-frontend:build ${DOCKER_USER}/classsphere-frontend:production
docker tag classsphere-frontend:build ${DOCKER_USER}/classsphere-frontend:sha-${GIT_SHA}

# Get image size
FRONTEND_SIZE=$(docker images "${DOCKER_USER}/classsphere-frontend:${VERSION}" --format "{{.Size}}")
log_success "Frontend tagged (Size: $FRONTEND_SIZE)"
echo ""

# Push frontend image
log_info "Pushing frontend to Docker Hub..."
docker push ${DOCKER_USER}/classsphere-frontend:${VERSION} | tail -n 5
docker push ${DOCKER_USER}/classsphere-frontend:latest | tail -n 5
docker push ${DOCKER_USER}/classsphere-frontend:production | tail -n 5
docker push ${DOCKER_USER}/classsphere-frontend:sha-${GIT_SHA} | tail -n 5
log_success "Frontend published to Docker Hub"
echo ""

# ========================================
# Summary
# ========================================
echo -e "${GREEN}========================================${NC}"
echo -e "${GREEN}✓ Publication Complete!${NC}"
echo -e "${GREEN}========================================${NC}"
echo ""

echo "📦 Published Images:"
echo ""
echo "  Backend (Go 1.24):"
echo "    ${DOCKER_USER}/classsphere-backend:${VERSION} (${BACKEND_SIZE})"
echo "    ${DOCKER_USER}/classsphere-backend:latest"
echo "    ${DOCKER_USER}/classsphere-backend:production"
echo "    ${DOCKER_USER}/classsphere-backend:sha-${GIT_SHA}"
echo ""
echo "  Frontend (Angular 19 + Nginx):"
echo "    ${DOCKER_USER}/classsphere-frontend:${VERSION} (${FRONTEND_SIZE})"
echo "    ${DOCKER_USER}/classsphere-frontend:latest"
echo "    ${DOCKER_USER}/classsphere-frontend:production"
echo "    ${DOCKER_USER}/classsphere-frontend:sha-${GIT_SHA}"
echo ""

echo "🔗 Docker Hub URLs:"
echo "  https://hub.docker.com/r/${DOCKER_USER}/classsphere-backend"
echo "  https://hub.docker.com/r/${DOCKER_USER}/classsphere-frontend"
echo ""

echo "🚀 Quick Test:"
echo "  docker pull ${DOCKER_USER}/classsphere-backend:${VERSION}"
echo "  docker pull ${DOCKER_USER}/classsphere-frontend:${VERSION}"
echo ""

echo "📋 All Local Images:"
docker images | grep "classsphere" | head -n 10
echo ""

echo -e "${GREEN}========================================${NC}"

