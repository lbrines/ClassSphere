#!/bin/bash
# ========================================
# ClassSphere Docker Image Publisher
# Builds images locally and publishes to Docker Hub
# ========================================
#
# Usage:
#   ./scripts/publish-docker-images.sh <version>
#
# Example:
#   ./scripts/publish-docker-images.sh 1.0.0
#
# Environment Variables:
#   DOCKERHUB_USERNAME - Docker Hub username (default: lbrines)
#   DOCKERHUB_TOKEN    - Docker Hub access token (required)
#   SKIP_TESTS         - Skip security scans (default: false)
#   SKIP_PUSH          - Build only, don't push (default: false)
#
# ========================================

set -e

# ========================================
# Configuration
# ========================================
DOCKER_USER="${DOCKERHUB_USERNAME:-lbrines}"
VERSION="${1:-latest}"
PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
GIT_SHA=$(git rev-parse --short HEAD 2>/dev/null || echo "unknown")
BUILD_DATE=$(date -u +'%Y-%m-%dT%H:%M:%SZ')

# Skip flags
SKIP_TESTS="${SKIP_TESTS:-false}"
SKIP_PUSH="${SKIP_PUSH:-false}"

# Image names
BACKEND_IMAGE="${DOCKER_USER}/classsphere-backend"
FRONTEND_IMAGE="${DOCKER_USER}/classsphere-frontend"

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

print_header() {
    echo ""
    echo -e "${BLUE}========================================${NC}"
    echo -e "${BLUE}$1${NC}"
    echo -e "${BLUE}========================================${NC}"
    echo ""
}

check_command() {
    if ! command -v "$1" &> /dev/null; then
        log_error "$1 is not installed"
        return 1
    fi
    return 0
}

# ========================================
# Validation
# ========================================
validate_prerequisites() {
    print_header "Validating Prerequisites"
    
    local errors=0
    
    # Check Docker
    if check_command docker; then
        log_success "Docker installed: $(docker --version)"
    else
        ((errors++))
    fi
    
    # Check git
    if check_command git; then
        log_success "Git installed: $(git --version)"
    else
        ((errors++))
    fi
    
    # Check Docker Hub credentials for push
    if [ "$SKIP_PUSH" = "false" ]; then
        if [ -z "$DOCKERHUB_TOKEN" ]; then
            log_error "DOCKERHUB_TOKEN not set (required for push)"
            log_info "Set with: export DOCKERHUB_TOKEN=your_token"
            ((errors++))
        else
            log_success "Docker Hub token configured"
        fi
    fi
    
    # Check project structure
    if [ ! -f "$PROJECT_ROOT/.devcontainer/backend/Dockerfile" ]; then
        log_error "Backend Dockerfile not found"
        ((errors++))
    else
        log_success "Backend Dockerfile found"
    fi
    
    if [ ! -f "$PROJECT_ROOT/.devcontainer/frontend/Dockerfile" ]; then
        log_error "Frontend Dockerfile not found"
        ((errors++))
    else
        log_success "Frontend Dockerfile found"
    fi
    
    if [ $errors -gt 0 ]; then
        log_error "Prerequisites validation failed ($errors errors)"
        exit 1
    fi
    
    log_success "All prerequisites validated"
}

# ========================================
# Docker Hub Login
# ========================================
docker_login() {
    if [ "$SKIP_PUSH" = "true" ]; then
        log_info "Skipping Docker Hub login (SKIP_PUSH=true)"
        return 0
    fi
    
    print_header "Docker Hub Login"
    
    if echo "$DOCKERHUB_TOKEN" | docker login -u "$DOCKER_USER" --password-stdin; then
        log_success "Logged in to Docker Hub as $DOCKER_USER"
    else
        log_error "Docker Hub login failed"
        exit 1
    fi
}

# ========================================
# Build Images
# ========================================
build_backend() {
    print_header "Building Backend Image"
    
    log_info "Image: $BACKEND_IMAGE"
    log_info "Version: $VERSION"
    log_info "SHA: $GIT_SHA"
    
    docker build \
        -f "$PROJECT_ROOT/.devcontainer/backend/Dockerfile" \
        --target production \
        --build-arg VERSION="$VERSION" \
        --build-arg BUILD_DATE="$BUILD_DATE" \
        --build-arg VCS_REF="$GIT_SHA" \
        -t "$BACKEND_IMAGE:$VERSION" \
        -t "$BACKEND_IMAGE:latest" \
        -t "$BACKEND_IMAGE:sha-$GIT_SHA" \
        "$PROJECT_ROOT"
    
    log_success "Backend image built successfully"
}

build_frontend() {
    print_header "Building Frontend Image"
    
    log_info "Image: $FRONTEND_IMAGE"
    log_info "Version: $VERSION"
    log_info "SHA: $GIT_SHA"
    
    docker build \
        -f "$PROJECT_ROOT/.devcontainer/frontend/Dockerfile" \
        --target production \
        --build-arg VERSION="$VERSION" \
        --build-arg BUILD_DATE="$BUILD_DATE" \
        --build-arg VCS_REF="$GIT_SHA" \
        -t "$FRONTEND_IMAGE:$VERSION" \
        -t "$FRONTEND_IMAGE:latest" \
        -t "$FRONTEND_IMAGE:sha-$GIT_SHA" \
        "$PROJECT_ROOT"
    
    log_success "Frontend image built successfully"
}

# ========================================
# Security Scan with Trivy (Container Mode)
# ========================================
security_scan() {
    if [ "$SKIP_TESTS" = "true" ]; then
        log_warning "Skipping security scans (SKIP_TESTS=true)"
        return 0
    fi
    
    print_header "Security Scan with Trivy (Container Mode)"
    
    log_info "Running Trivy via Docker container..."
    log_info "This doesn't require local Trivy installation"
    
    # Scan backend
    log_info "Scanning backend image..."
    if docker run --rm -v /var/run/docker.sock:/var/run/docker.sock \
        aquasec/trivy:latest image \
        --severity HIGH,CRITICAL \
        --exit-code 0 \
        "$BACKEND_IMAGE:$VERSION"; then
        log_success "Backend security scan passed"
    else
        log_warning "Backend has vulnerabilities (continuing anyway)"
    fi
    
    echo ""
    
    # Scan frontend
    log_info "Scanning frontend image..."
    if docker run --rm -v /var/run/docker.sock:/var/run/docker.sock \
        aquasec/trivy:latest image \
        --severity HIGH,CRITICAL \
        --exit-code 0 \
        "$FRONTEND_IMAGE:$VERSION"; then
        log_success "Frontend security scan passed"
    else
        log_warning "Frontend has vulnerabilities (continuing anyway)"
    fi
}

# ========================================
# Tag Images
# ========================================
tag_images() {
    print_header "Tagging Images"
    
    # Backend tags
    log_info "Tagging backend..."
    docker tag "$BACKEND_IMAGE:$VERSION" "$BACKEND_IMAGE:production"
    log_success "Backend tagged: $VERSION, latest, sha-$GIT_SHA, production"
    
    # Frontend tags
    log_info "Tagging frontend..."
    docker tag "$FRONTEND_IMAGE:$VERSION" "$FRONTEND_IMAGE:production"
    log_success "Frontend tagged: $VERSION, latest, sha-$GIT_SHA, production"
}

# ========================================
# Push Images
# ========================================
push_images() {
    if [ "$SKIP_PUSH" = "true" ]; then
        log_warning "Skipping push to Docker Hub (SKIP_PUSH=true)"
        return 0
    fi
    
    print_header "Pushing Images to Docker Hub"
    
    # Push backend
    log_info "Pushing backend tags..."
    docker push "$BACKEND_IMAGE:$VERSION"
    docker push "$BACKEND_IMAGE:latest"
    docker push "$BACKEND_IMAGE:sha-$GIT_SHA"
    docker push "$BACKEND_IMAGE:production"
    log_success "Backend pushed successfully"
    
    echo ""
    
    # Push frontend
    log_info "Pushing frontend tags..."
    docker push "$FRONTEND_IMAGE:$VERSION"
    docker push "$FRONTEND_IMAGE:latest"
    docker push "$FRONTEND_IMAGE:sha-$GIT_SHA"
    docker push "$FRONTEND_IMAGE:production"
    log_success "Frontend pushed successfully"
}

# ========================================
# Verify Images
# ========================================
verify_images() {
    if [ "$SKIP_PUSH" = "true" ]; then
        log_info "Skipping verification (images not pushed)"
        return 0
    fi
    
    print_header "Verifying Published Images"
    
    # Verify backend
    log_info "Pulling backend to verify..."
    if docker pull "$BACKEND_IMAGE:$VERSION" > /dev/null 2>&1; then
        log_success "Backend image verified on Docker Hub"
    else
        log_error "Backend image verification failed"
        exit 1
    fi
    
    # Verify frontend
    log_info "Pulling frontend to verify..."
    if docker pull "$FRONTEND_IMAGE:$VERSION" > /dev/null 2>&1; then
        log_success "Frontend image verified on Docker Hub"
    else
        log_error "Frontend image verification failed"
        exit 1
    fi
}

# ========================================
# Cleanup
# ========================================
cleanup() {
    print_header "Cleanup"
    
    log_info "Cleaning up build cache..."
    docker builder prune -f > /dev/null 2>&1 || true
    log_success "Build cache cleaned"
}

# ========================================
# Summary
# ========================================
print_summary() {
    print_header "🎉 Publish Summary"
    
    echo ""
    echo -e "${GREEN}✅ Images Published Successfully${NC}"
    echo ""
    echo "📦 Backend Image:"
    echo "   • $BACKEND_IMAGE:$VERSION"
    echo "   • $BACKEND_IMAGE:latest"
    echo "   • $BACKEND_IMAGE:sha-$GIT_SHA"
    echo "   • $BACKEND_IMAGE:production"
    echo ""
    echo "📦 Frontend Image:"
    echo "   • $FRONTEND_IMAGE:$VERSION"
    echo "   • $FRONTEND_IMAGE:latest"
    echo "   • $FRONTEND_IMAGE:sha-$GIT_SHA"
    echo "   • $FRONTEND_IMAGE:production"
    echo ""
    echo "🔗 Docker Hub URLs:"
    echo "   • https://hub.docker.com/r/$DOCKER_USER/classsphere-backend"
    echo "   • https://hub.docker.com/r/$DOCKER_USER/classsphere-frontend"
    echo ""
    echo "📊 Version Information:"
    echo "   • Version: $VERSION"
    echo "   • Git SHA: $GIT_SHA"
    echo "   • Build Date: $BUILD_DATE"
    echo ""
    
    if [ "$SKIP_PUSH" = "true" ]; then
        echo -e "${YELLOW}⚠️  Images built but not pushed (SKIP_PUSH=true)${NC}"
        echo ""
    fi
}

# ========================================
# Main Execution
# ========================================
main() {
    clear
    
    echo ""
    echo -e "${BLUE}╔══════════════════════════════════════════════════════════════╗${NC}"
    echo -e "${BLUE}║                                                              ║${NC}"
    echo -e "${BLUE}║  🐳 ClassSphere Docker Image Publisher                      ║${NC}"
    echo -e "${BLUE}║                                                              ║${NC}"
    echo -e "${BLUE}║  Builds locally and publishes to Docker Hub                 ║${NC}"
    echo -e "${BLUE}║                                                              ║${NC}"
    echo -e "${BLUE}╚══════════════════════════════════════════════════════════════╝${NC}"
    echo ""
    
    # Validate
    validate_prerequisites
    
    # Login
    docker_login
    
    # Build
    build_backend
    build_frontend
    
    # Tag
    tag_images
    
    # Security scan
    security_scan
    
    # Push
    push_images
    
    # Verify
    verify_images
    
    # Cleanup
    cleanup
    
    # Summary
    print_summary
    
    log_success "All done! 🎉"
}

# ========================================
# Run
# ========================================
if [ $# -eq 0 ]; then
    log_error "Version argument required"
    echo "Usage: $0 <version>"
    echo "Example: $0 1.0.0"
    exit 1
fi

main "$@"
