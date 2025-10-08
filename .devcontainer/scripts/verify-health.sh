#!/bin/bash
set -e

echo "🏥 ClassSphere Health Check Script"
echo "====================================="
echo ""

FAILED=0

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Backend Health
echo "🔍 Checking Backend (port 8080)..."
if curl -sf http://localhost:8080/health > /dev/null 2>&1; then
    echo -e "${GREEN}✅ Backend: HEALTHY${NC}"
    RESPONSE=$(curl -s http://localhost:8080/health)
    echo "   Response: $RESPONSE"
else
    echo -e "${RED}❌ Backend: UNHEALTHY${NC}"
    echo "   Error: Cannot connect to http://localhost:8080/health"
    FAILED=$((FAILED + 1))
fi
echo ""

# Frontend Health
echo "🔍 Checking Frontend (port 4200)..."
if curl -sf -I http://localhost:4200 > /dev/null 2>&1; then
    echo -e "${GREEN}✅ Frontend: HEALTHY${NC}"
    HTTP_STATUS=$(curl -s -o /dev/null -w "%{http_code}" http://localhost:4200)
    echo "   HTTP Status: $HTTP_STATUS"
else
    echo -e "${YELLOW}⚠️  Frontend: STARTING (may take 30-60s to compile)${NC}"
    echo "   Checking if Angular is compiling..."
    if docker logs classsphere-frontend 2>&1 | grep -q "Application bundle generation complete"; then
        echo "   ✓ Angular compiled successfully"
        echo "   Waiting for server to start..."
    else
        echo "   Still compiling... Check logs: docker logs classsphere-frontend"
    fi
fi
echo ""

# Redis Health
echo "🔍 Checking Redis (port 6379)..."
if docker exec classsphere-redis redis-cli ping > /dev/null 2>&1; then
    echo -e "${GREEN}✅ Redis: HEALTHY${NC}"
    REDIS_RESPONSE=$(docker exec classsphere-redis redis-cli ping)
    echo "   Response: $REDIS_RESPONSE"
else
    echo -e "${RED}❌ Redis: UNHEALTHY${NC}"
    echo "   Error: Cannot connect to Redis"
    FAILED=$((FAILED + 1))
fi
echo ""

# Workspace Check
echo "🔍 Checking Workspace container..."
if docker ps | grep -q classsphere-workspace; then
    echo -e "${GREEN}✅ Workspace: RUNNING${NC}"
    echo "   Container ID: $(docker ps | grep classsphere-workspace | awk '{print $1}')"
else
    echo -e "${RED}❌ Workspace: NOT RUNNING${NC}"
    FAILED=$((FAILED + 1))
fi
echo ""

# Docker Compose Status
echo "📊 Docker Compose Services Status:"
echo "-----------------------------------"
docker-compose -f .devcontainer/docker-compose.yml ps
echo ""

# Resource Usage
echo "💾 Resource Usage:"
echo "-----------------------------------"
docker stats --no-stream --format "table {{.Name}}\t{{.CPUPerc}}\t{{.MemUsage}}" | grep classsphere
echo ""

# Summary
echo "====================================="
if [ $FAILED -eq 0 ]; then
    echo -e "${GREEN}✅ All critical services are healthy!${NC}"
    exit 0
else
    echo -e "${RED}❌ $FAILED service(s) failed health check${NC}"
    echo ""
    echo "Troubleshooting steps:"
    echo "1. Check logs: docker-compose -f .devcontainer/docker-compose.yml logs"
    echo "2. Restart services: docker-compose -f .devcontainer/docker-compose.yml restart"
    echo "3. See TROUBLESHOOTING.md for detailed help"
    exit 1
fi

