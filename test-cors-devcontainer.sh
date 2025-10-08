#!/bin/bash
# Script para ejecutar tests CORS en devcontainer
# Usage: ./test-cors-devcontainer.sh

echo "🐳 Ejecutando tests CORS en devcontainer..."
echo ""

# Opción 1: Si ya estás EN el devcontainer
if command -v go &> /dev/null && go version | grep -q "1.2[2-9]"; then
    echo "✅ Go 1.22+ detectado, ejecutando tests..."
    cd backend
    go test ./internal/adapters/http -v -run TestCORS
    exit $?
fi

# Opción 2: Ejecutar desde host usando docker-compose
echo "📦 Ejecutando desde host usando devcontainer..."
docker-compose -f .devcontainer/docker-compose.yml run --rm backend sh -c "
    cd /workspace/backend && \
    go mod download && \
    go test ./internal/adapters/http -v -run TestCORS
"

exit $?

