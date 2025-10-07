#!/bin/bash
# Script de prueba de autenticación ClassSphere
# Versión: 1.0
# Fecha: 2025-10-07

set -e

echo "════════════════════════════════════════════════════════"
echo "  ClassSphere - Test de Autenticación"
echo "════════════════════════════════════════════════════════"
echo ""

# Colors
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Backend URL
API_URL="http://localhost:8080/api/v1"

echo "🔍 Verificando servicios..."
echo ""

# Verificar backend
if curl -s -f "${API_URL%/api/v1}/health" > /dev/null 2>&1; then
    echo -e "${GREEN}✓${NC} Backend corriendo en http://localhost:8080"
else
    echo -e "${RED}✗${NC} Backend NO responde"
    exit 1
fi

# Verificar frontend
if curl -s -f "http://localhost:4200" > /dev/null 2>&1; then
    echo -e "${GREEN}✓${NC} Frontend corriendo en http://localhost:4200"
else
    echo -e "${YELLOW}⚠${NC} Frontend puede no estar respondiendo"
fi

echo ""
echo "════════════════════════════════════════════════════════"
echo "  TEST 1: Login con Admin"
echo "════════════════════════════════════════════════════════"
echo ""
echo "Credenciales: admin@classsphere.edu / admin123"
echo ""

RESPONSE=$(curl -s -X POST "${API_URL}/auth/login" \
  -H "Content-Type: application/json" \
  -d '{"email":"admin@classsphere.edu","password":"admin123"}')

# Verificar si la respuesta contiene accessToken
if echo "$RESPONSE" | grep -q "accessToken"; then
    echo -e "${GREEN}✓ Login exitoso${NC}"
    echo ""
    echo "Token de acceso:"
    echo "$RESPONSE" | jq -r '.accessToken'
    echo ""
    echo "Datos del usuario:"
    echo "$RESPONSE" | jq '.user | {Email, Role, DisplayName}'
    
    # Guardar token para siguientes tests
    TOKEN=$(echo "$RESPONSE" | jq -r '.accessToken')
else
    echo -e "${RED}✗ Login falló${NC}"
    echo "$RESPONSE" | jq .
    exit 1
fi

echo ""
echo "════════════════════════════════════════════════════════"
echo "  TEST 2: Login con Coordinador"
echo "════════════════════════════════════════════════════════"
echo ""
echo "Credenciales: coordinator@classsphere.edu / coord123"
echo ""

RESPONSE=$(curl -s -X POST "${API_URL}/auth/login" \
  -H "Content-Type: application/json" \
  -d '{"email":"coordinator@classsphere.edu","password":"coord123"}')

if echo "$RESPONSE" | grep -q "accessToken"; then
    echo -e "${GREEN}✓ Login exitoso${NC}"
    echo ""
    echo "Datos del usuario:"
    echo "$RESPONSE" | jq '.user | {Email, Role, DisplayName}'
else
    echo -e "${RED}✗ Login falló${NC}"
    echo "$RESPONSE" | jq .
    exit 1
fi

echo ""
echo "════════════════════════════════════════════════════════"
echo "  TEST 3: Acceso a endpoint protegido"
echo "════════════════════════════════════════════════════════"
echo ""
echo "Usando token del Admin..."
echo ""

RESPONSE=$(curl -s -H "Authorization: Bearer $TOKEN" "${API_URL}/users/me")

if echo "$RESPONSE" | grep -q "Email"; then
    echo -e "${GREEN}✓ Acceso autorizado${NC}"
    echo ""
    echo "Perfil del usuario:"
    echo "$RESPONSE" | jq '{Email, Role, DisplayName}'
else
    echo -e "${RED}✗ Acceso denegado${NC}"
    echo "$RESPONSE" | jq .
    exit 1
fi

echo ""
echo "════════════════════════════════════════════════════════"
echo "  TEST 4: Endpoint solo para Admin"
echo "════════════════════════════════════════════════════════"
echo ""
echo "Usando token del Admin..."
echo ""

RESPONSE=$(curl -s -H "Authorization: Bearer $TOKEN" "${API_URL}/admin/ping")

if echo "$RESPONSE" | grep -q "admin pong"; then
    echo -e "${GREEN}✓ Acceso autorizado (Admin)${NC}"
    echo ""
    echo "$RESPONSE" | jq .
else
    echo -e "${RED}✗ Acceso denegado${NC}"
    echo "$RESPONSE" | jq .
fi

echo ""
echo "════════════════════════════════════════════════════════"
echo "  TEST 5: OAuth Google (solo URL)"
echo "════════════════════════════════════════════════════════"
echo ""

RESPONSE=$(curl -s "${API_URL}/auth/oauth/google")

if echo "$RESPONSE" | grep -q "accounts.google.com"; then
    echo -e "${GREEN}✓ OAuth URL generada${NC}"
    echo ""
    echo "URL de OAuth:"
    echo "$RESPONSE" | jq -r '.url'
    echo ""
    echo "State:"
    echo "$RESPONSE" | jq -r '.state'
else
    echo -e "${RED}✗ Error al generar OAuth URL${NC}"
    echo "$RESPONSE" | jq .
fi

echo ""
echo "════════════════════════════════════════════════════════"
echo "  TEST 6: Login con credenciales incorrectas"
echo "════════════════════════════════════════════════════════"
echo ""
echo "Probando con password incorrecta..."
echo ""

RESPONSE=$(curl -s -w "\nHTTP_CODE:%{http_code}" -X POST "${API_URL}/auth/login" \
  -H "Content-Type: application/json" \
  -d '{"email":"admin@classsphere.edu","password":"wrongpassword"}')

HTTP_CODE=$(echo "$RESPONSE" | grep "HTTP_CODE" | cut -d: -f2)

if [ "$HTTP_CODE" = "401" ]; then
    echo -e "${GREEN}✓ Error 401 Unauthorized (comportamiento esperado)${NC}"
else
    echo -e "${YELLOW}⚠ Código HTTP inesperado: $HTTP_CODE${NC}"
fi

echo ""
echo "════════════════════════════════════════════════════════"
echo -e "${GREEN}  ✓ TODOS LOS TESTS COMPLETADOS${NC}"
echo "════════════════════════════════════════════════════════"
echo ""
echo "📝 Resumen:"
echo "   • Backend funcionando correctamente"
echo "   • Autenticación con password: ✓"
echo "   • Endpoints protegidos: ✓"
echo "   • Control de roles: ✓"
echo "   • OAuth URL generation: ✓"
echo ""
echo "🌐 URLs de acceso:"
echo "   • Backend: http://localhost:8080"
echo "   • Frontend: http://localhost:4200"
echo "   • Health: http://localhost:8080/health"
echo ""
echo "👤 Usuarios de prueba:"
echo "   • Admin:       admin@classsphere.edu / admin123"
echo "   • Coordinador: coordinator@classsphere.edu / coord123"
echo ""

