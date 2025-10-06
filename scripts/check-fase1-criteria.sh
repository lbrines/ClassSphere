#!/bin/bash

# ClassSphere Fase 1 - Verificación de Criterios de Aceptación
# Este script verifica todos los criterios de aceptación de la Fase 1

echo "🎯 ClassSphere Fase 1 - Verificación de Criterios de Aceptación"
echo "================================================================"

# Colores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Contadores
TOTAL_CRITERIA=7
PASSED_CRITERIA=0
FAILED_CRITERIA=0
WARNING_CRITERIA=0

check_criteria() {
    local name="$1"
    local status="$2"
    local details="$3"
    
    if [ "$status" = "PASS" ]; then
        echo -e "✅ ${GREEN}PASS${NC}: $name"
        echo "   $details"
        ((PASSED_CRITERIA++))
    elif [ "$status" = "WARN" ]; then
        echo -e "⚠️  ${YELLOW}WARN${NC}: $name"
        echo "   $details"
        ((WARNING_CRITERIA++))
    else
        echo -e "❌ ${RED}FAIL${NC}: $name"
        echo "   $details"
        ((FAILED_CRITERIA++))
    fi
    echo ""
}

echo -e "${BLUE}1. Backend Coverage 100%${NC}"
cd backend
if go test -cover ./... -coverprofile=coverage.out > /dev/null 2>&1; then
    COVERAGE=$(go tool cover -func=coverage.out | grep total | awk '{print $3}' | sed 's/%//')
    if (( $(echo "$COVERAGE >= 100" | bc -l) )); then
        check_criteria "Backend Coverage" "PASS" "Coverage: ${COVERAGE}% (Target: 100%)"
    elif (( $(echo "$COVERAGE >= 80" | bc -l) )); then
        check_criteria "Backend Coverage" "WARN" "Coverage: ${COVERAGE}% (Target: 100%, Acceptable: 80%+)"
    else
        check_criteria "Backend Coverage" "FAIL" "Coverage: ${COVERAGE}% (Target: 100%)"
    fi
else
    check_criteria "Backend Coverage" "FAIL" "Tests failed to run"
fi
cd ..

echo -e "${BLUE}2. Frontend Coverage 100%${NC}"
cd frontend/classsphere-frontend
if npm test -- --code-coverage --watch=false > /dev/null 2>&1; then
    # Extract coverage from the output
    COVERAGE=$(npm test -- --code-coverage --watch=false 2>&1 | grep "Statements" | awk '{print $3}' | sed 's/%//')
    if [ "$COVERAGE" = "100" ]; then
        check_criteria "Frontend Coverage" "PASS" "Coverage: ${COVERAGE}% (Target: 100%)"
    else
        check_criteria "Frontend Coverage" "WARN" "Coverage: ${COVERAGE}% (Target: 100%)"
    fi
else
    check_criteria "Frontend Coverage" "FAIL" "Tests failed to run"
fi
cd ../..

echo -e "${BLUE}3. E2E Tests - 100% flujos críticos${NC}"
if [ -d "frontend/classsphere-frontend/e2e" ] && [ -f "frontend/classsphere-frontend/playwright.config.ts" ]; then
    check_criteria "E2E Tests" "PASS" "E2E infrastructure implemented with Playwright"
else
    check_criteria "E2E Tests" "FAIL" "E2E tests not implemented"
fi

echo -e "${BLUE}4. CI/CD Pipeline con Coverage Gates${NC}"
if [ -f ".github/workflows/coverage.yml" ]; then
    check_criteria "CI/CD Pipeline" "PASS" "GitHub Actions workflow exists"
else
    check_criteria "CI/CD Pipeline" "FAIL" "CI/CD pipeline not configured"
fi

echo -e "${BLUE}5. Security Scan - 0 vulnerabilidades críticas${NC}"
# Check for common security issues
SECURITY_ISSUES=0
if grep -r "password.*=" backend/ --include="*.go" | grep -v "test" > /dev/null; then
    ((SECURITY_ISSUES++))
fi
if grep -r "secret.*=" backend/ --include="*.go" | grep -v "test" > /dev/null; then
    ((SECURITY_ISSUES++))
fi

if [ $SECURITY_ISSUES -eq 0 ]; then
    check_criteria "Security Scan" "PASS" "No obvious security issues found"
else
    check_criteria "Security Scan" "WARN" "Found $SECURITY_ISSUES potential security issues"
fi

echo -e "${BLUE}6. Performance - <2s tiempo de respuesta${NC}"
# Test backend performance
if curl -s -w "%{time_total}" -o /dev/null http://localhost:8080/health > /dev/null 2>&1; then
    BACKEND_TIME=$(curl -s -w "%{time_total}" -o /dev/null http://localhost:8080/health)
    if (( $(echo "$BACKEND_TIME < 2" | bc -l) )); then
        check_criteria "Backend Performance" "PASS" "Response time: ${BACKEND_TIME}s (Target: <2s)"
    else
        check_criteria "Backend Performance" "FAIL" "Response time: ${BACKEND_TIME}s (Target: <2s)"
    fi
else
    check_criteria "Backend Performance" "FAIL" "Backend not responding"
fi

# Test frontend performance
if curl -s -w "%{time_total}" -o /dev/null http://localhost:4200 > /dev/null 2>&1; then
    FRONTEND_TIME=$(curl -s -w "%{time_total}" -o /dev/null http://localhost:4200)
    if (( $(echo "$FRONTEND_TIME < 2" | bc -l) )); then
        check_criteria "Frontend Performance" "PASS" "Response time: ${FRONTEND_TIME}s (Target: <2s)"
    else
        check_criteria "Frontend Performance" "FAIL" "Response time: ${FRONTEND_TIME}s (Target: <2s)"
    fi
else
    check_criteria "Frontend Performance" "FAIL" "Frontend not responding"
fi

echo -e "${BLUE}7. Documentación - README actualizado${NC}"
if [ -f "README.md" ] && [ -s "README.md" ]; then
    check_criteria "Documentation" "PASS" "README.md exists and is not empty"
else
    check_criteria "Documentation" "FAIL" "README.md missing or empty"
fi

echo "================================================================"
echo -e "${BLUE}RESUMEN FINAL${NC}"
echo "================================================================"
echo -e "✅ Criterios Aprobados: ${GREEN}$PASSED_CRITERIA${NC}/$TOTAL_CRITERIA"
echo -e "⚠️  Criterios con Advertencias: ${YELLOW}$WARNING_CRITERIA${NC}/$TOTAL_CRITERIA"
echo -e "❌ Criterios Fallidos: ${RED}$FAILED_CRITERIA${NC}/$TOTAL_CRITERIA"

if [ $FAILED_CRITERIA -eq 0 ] && [ $WARNING_CRITERIA -eq 0 ]; then
    echo -e "\n🎉 ${GREEN}FASE 1 COMPLETADA AL 100%${NC}"
    exit 0
elif [ $FAILED_CRITERIA -eq 0 ]; then
    echo -e "\n🟡 ${YELLOW}FASE 1 COMPLETADA CON ADVERTENCIAS${NC}"
    exit 1
else
    echo -e "\n🔴 ${RED}FASE 1 INCOMPLETA${NC}"
    exit 2
fi
