#!/bin/bash
set -e

echo "🚀 ClassSphere Dev Container Setup"
echo "Context ID: critical-day1-post-create"
echo "Timestamp: $(date -Iseconds)"

# ============================================
# Backend Setup
# ============================================
echo "📦 Installing Go dependencies..."
cd /workspace/backend
go mod download

echo "✅ Go version: $(go version)"
echo "✅ Air (hot reload): $(air -v 2>&1 | head -1)"

# ============================================
# Frontend Setup
# ============================================
echo "📦 Installing npm dependencies..."
cd /workspace/frontend
npm ci

# Verify TailwindCSS version (prevent v4 issue)
TAILWIND_VERSION=$(npm list tailwindcss --depth=0 2>/dev/null | grep tailwindcss | awk -F@ '{print $NF}')
echo "✅ TailwindCSS version: $TAILWIND_VERSION"
if [[ $TAILWIND_VERSION == 4.* ]]; then
  echo "⚠️  WARNING: TailwindCSS v4 detected! Phase 1 validated v3.4.0"
fi

echo "✅ Node version: $(node --version)"
echo "✅ Angular CLI: $(npx ng version --no-color 2>&1 | head -1)"

# ============================================
# Health Checks
# ============================================
echo "🏥 Running health checks..."

if redis-cli -h redis ping >/dev/null 2>&1; then
  echo "✅ Redis: OK"
else
  echo "⚠️  Redis not ready yet (waiting for health check)"
fi

# ============================================
# Port Availability
# ============================================
echo "🔌 Verifying port availability..."
for port in 8080 4200 6379; do
  if nc -z localhost $port 2>/dev/null; then
    echo "⚠️  Port $port already in use"
  else
    echo "✅ Port $port: Available"
  fi
done

# ============================================
# Git Configuration
# ============================================
echo "📝 Configuring Git..."
git config --global core.editor "code --wait"
git config --global init.defaultBranch main

# ============================================
# Final Instructions
# ============================================
echo ""
echo "✅ Dev Container setup complete!"
echo ""
echo "📝 Next steps:"
echo "   - Backend: cd /workspace/backend && go run cmd/api/main.go"
echo "   - Frontend: cd /workspace/frontend && npm start"
echo "   - Tests: cd /workspace/backend && go test ./..."
echo ""
echo "📚 Documentation: /workspace/README.md"
echo "🐛 Troubleshooting: /workspace/.devcontainer/TROUBLESHOOTING.md"

