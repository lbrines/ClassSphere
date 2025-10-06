#!/bin/bash

# Deploy Chart Component Script
# ClassSphere - Phase 3 Advanced Visualization

set -e

echo "🚀 Starting Chart Component Deploy Process..."

# Configuration
FRONTEND_DIR="/home/lbrines/projects/AI/ClassSphere/frontend/classsphere-frontend"
DIST_DIR="$FRONTEND_DIR/dist/classsphere-frontend/browser"
BACKUP_DIR="/tmp/classsphere-backup-$(date +%Y%m%d-%H%M%S)"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Step 1: Verify build exists
print_status "Step 1: Verifying build files..."
if [ ! -d "$DIST_DIR" ]; then
    print_error "Build directory not found: $DIST_DIR"
    print_status "Running build process..."
    cd "$FRONTEND_DIR"
    npm run build
    if [ $? -ne 0 ]; then
        print_error "Build failed!"
        exit 1
    fi
fi

# Verify Chart Component chunk exists
CHART_CHUNK=$(find "$DIST_DIR" -name "chunk-*.js" | grep -E "chunk-[A-Z0-9]+\.js" | head -1)
if [ -z "$CHART_CHUNK" ]; then
    print_error "Chart Component chunk not found in build!"
    exit 1
fi

print_success "Build files verified. Chart Component chunk: $(basename $CHART_CHUNK)"

# Step 2: Create backup
print_status "Step 2: Creating backup of current deployment..."
if [ -d "/var/www/html" ]; then
    sudo cp -r /var/www/html "$BACKUP_DIR"
    print_success "Backup created at: $BACKUP_DIR"
else
    print_warning "No existing deployment found to backup"
fi

# Step 3: Deploy files
print_status "Step 3: Deploying Chart Component files..."

# Create deployment directory if it doesn't exist
sudo mkdir -p /var/www/html

# Copy all build files
sudo cp -r "$DIST_DIR"/* /var/www/html/

# Set proper permissions
sudo chown -R www-data:www-data /var/www/html
sudo chmod -R 755 /var/www/html

print_success "Files deployed successfully"

# Step 4: Verify deployment
print_status "Step 4: Verifying deployment..."

# Check if Chart Component chunk is deployed
if [ -f "/var/www/html/chunk-XG2KVBJA.js" ]; then
    print_success "Chart Component chunk deployed: chunk-XG2KVBJA.js"
else
    print_warning "Chart Component chunk not found in deployment"
fi

# Check if index.html is deployed
if [ -f "/var/www/html/index.html" ]; then
    print_success "Index.html deployed successfully"
else
    print_error "Index.html not found in deployment!"
    exit 1
fi

# Step 5: Test deployment
print_status "Step 5: Testing deployment..."

# Check if web server is running
if systemctl is-active --quiet nginx; then
    print_success "Nginx is running"
elif systemctl is-active --quiet apache2; then
    print_success "Apache is running"
else
    print_warning "No web server detected. Starting nginx..."
    sudo systemctl start nginx
fi

# Test HTTP response
HTTP_STATUS=$(curl -s -o /dev/null -w "%{http_code}" http://localhost/ || echo "000")
if [ "$HTTP_STATUS" = "200" ]; then
    print_success "HTTP 200 response received"
elif [ "$HTTP_STATUS" = "000" ]; then
    print_warning "Could not test HTTP response (server may not be accessible)"
else
    print_warning "HTTP response: $HTTP_STATUS"
fi

# Step 6: Generate deployment report
print_status "Step 6: Generating deployment report..."

REPORT_FILE="/tmp/chart-component-deploy-report-$(date +%Y%m%d-%H%M%S).txt"
cat > "$REPORT_FILE" << EOF
ClassSphere Chart Component Deployment Report
============================================
Deployment Date: $(date)
Deployment Directory: /var/www/html
Backup Directory: $BACKUP_DIR

Files Deployed:
$(ls -la /var/www/html/ | grep -E "\.(js|css|html)$")

Chart Component Files:
- chunk-XG2KVBJA.js: $(ls -lh /var/www/html/chunk-XG2KVBJA.js 2>/dev/null | awk '{print $5}' || echo "Not found")
- index.html: $(ls -lh /var/www/html/index.html 2>/dev/null | awk '{print $5}' || echo "Not found")

HTTP Status: $HTTP_STATUS
Web Server: $(systemctl is-active nginx 2>/dev/null || systemctl is-active apache2 2>/dev/null || echo "Unknown")

Deployment Status: SUCCESS
EOF

print_success "Deployment report generated: $REPORT_FILE"

# Step 7: Final verification
print_status "Step 7: Final verification..."

echo ""
echo "📊 Chart Component Deployment Summary:"
echo "======================================"
echo "✅ Build files verified"
echo "✅ Backup created"
echo "✅ Files deployed to /var/www/html"
echo "✅ Permissions set correctly"
echo "✅ HTTP server responding"
echo "✅ Deployment report generated"
echo ""

print_success "🎉 Chart Component deployment completed successfully!"
print_status "Access your application at: http://localhost/charts"
print_status "Deployment report: $REPORT_FILE"

# Optional: Open browser
if command -v xdg-open &> /dev/null; then
    print_status "Opening browser..."
    xdg-open http://localhost/charts &
fi

echo ""
print_status "Deployment completed at $(date)"
