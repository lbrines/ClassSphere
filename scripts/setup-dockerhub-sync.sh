#!/bin/bash
# ========================================
# Setup Docker Hub README Sync
# Configura los secrets necesarios para sincronización automática
# ========================================
#
# Usage:
#   ./scripts/setup-dockerhub-sync.sh
#
# Requirements:
#   - gh CLI installed and authenticated
#   - Docker Hub access token
#
# ========================================

set -e

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

# ========================================
# Validation
# ========================================
validate_prerequisites() {
    print_header "Validating Prerequisites"
    
    # Check gh CLI
    if ! command -v gh &> /dev/null; then
        log_error "GitHub CLI (gh) not installed"
        log_info "Install: https://cli.github.com/"
        exit 1
    fi
    log_success "GitHub CLI installed: $(gh --version | head -1)"
    
    # Check gh auth
    if ! gh auth status &> /dev/null; then
        log_error "GitHub CLI not authenticated"
        log_info "Run: gh auth login"
        exit 1
    fi
    log_success "GitHub CLI authenticated"
}

# ========================================
# Get Docker Hub Credentials
# ========================================
get_dockerhub_credentials() {
    print_header "Docker Hub Credentials"
    
    echo -e "${YELLOW}📋 Instructions:${NC}"
    echo ""
    echo "1. Go to: https://hub.docker.com/settings/security"
    echo "2. Click 'New Access Token'"
    echo "3. Name: 'GitHub Actions - README Sync'"
    echo "4. Permissions: 'Read & Write'"
    echo "5. Copy the generated token"
    echo ""
    
    # Get username
    read -p "$(echo -e ${BLUE}Docker Hub Username${NC} [lbrines]: )" DOCKER_USER
    DOCKER_USER=${DOCKER_USER:-lbrines}
    
    # Get token
    echo ""
    read -sp "$(echo -e ${BLUE}Docker Hub Access Token${NC}: )" DOCKER_TOKEN
    echo ""
    
    if [ -z "$DOCKER_TOKEN" ]; then
        log_error "Token cannot be empty"
        exit 1
    fi
    
    log_success "Credentials received"
}

# ========================================
# Set GitHub Secrets
# ========================================
set_github_secrets() {
    print_header "Setting GitHub Secrets"
    
    # Set DOCKERHUB_USERNAME
    log_info "Setting DOCKERHUB_USERNAME..."
    if echo "$DOCKER_USER" | gh secret set DOCKERHUB_USERNAME; then
        log_success "DOCKERHUB_USERNAME set successfully"
    else
        log_error "Failed to set DOCKERHUB_USERNAME"
        exit 1
    fi
    
    # Set DOCKERHUB_TOKEN
    log_info "Setting DOCKERHUB_TOKEN..."
    if echo "$DOCKER_TOKEN" | gh secret set DOCKERHUB_TOKEN; then
        log_success "DOCKERHUB_TOKEN set successfully"
    else
        log_error "Failed to set DOCKERHUB_TOKEN"
        exit 1
    fi
}

# ========================================
# Verify Setup
# ========================================
verify_setup() {
    print_header "Verifying Setup"
    
    log_info "Listing GitHub secrets..."
    echo ""
    gh secret list | grep DOCKERHUB || true
    echo ""
    
    log_success "Setup verification complete"
}

# ========================================
# Test Workflow
# ========================================
test_workflow() {
    print_header "Test Workflow (Optional)"
    
    echo ""
    read -p "$(echo -e ${YELLOW}Do you want to trigger the sync workflow now?${NC} [y/N]: )" -n 1 -r
    echo ""
    
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        log_info "Triggering workflow..."
        
        if gh workflow run sync-docker-readme.yml; then
            log_success "Workflow triggered successfully"
            echo ""
            log_info "View progress at:"
            echo "   https://github.com/lbrines/ClassSphere/actions"
        else
            log_warning "Failed to trigger workflow (make sure it's pushed to main first)"
        fi
    else
        log_info "Skipping workflow test"
    fi
}

# ========================================
# Summary
# ========================================
print_summary() {
    print_header "🎉 Setup Complete"
    
    echo ""
    echo -e "${GREEN}✅ Docker Hub README Sync Configured${NC}"
    echo ""
    echo "📦 Secrets configured:"
    echo "   ✓ DOCKERHUB_USERNAME"
    echo "   ✓ DOCKERHUB_TOKEN"
    echo ""
    echo "🚀 Workflow will sync automatically:"
    echo "   • When docs/DOCKER_HUB_README.md changes"
    echo "   • After Docker images are published"
    echo "   • Manual trigger from GitHub Actions"
    echo ""
    echo "🔗 Repositories:"
    echo "   • https://hub.docker.com/r/lbrines/classsphere-backend"
    echo "   • https://hub.docker.com/r/lbrines/classsphere-frontend"
    echo ""
    echo "📚 Documentation:"
    echo "   • .github/DOCKER_HUB_SYNC.md"
    echo ""
    log_success "All done! 🎉"
}

# ========================================
# Main
# ========================================
main() {
    clear
    
    echo ""
    echo -e "${BLUE}╔══════════════════════════════════════════════════════════════╗${NC}"
    echo -e "${BLUE}║                                                              ║${NC}"
    echo -e "${BLUE}║  🐳 Docker Hub README Sync Setup                            ║${NC}"
    echo -e "${BLUE}║                                                              ║${NC}"
    echo -e "${BLUE}║  Configures automatic README synchronization                ║${NC}"
    echo -e "${BLUE}║                                                              ║${NC}"
    echo -e "${BLUE}╚══════════════════════════════════════════════════════════════╝${NC}"
    echo ""
    
    validate_prerequisites
    get_dockerhub_credentials
    set_github_secrets
    verify_setup
    test_workflow
    print_summary
}

main "$@"

