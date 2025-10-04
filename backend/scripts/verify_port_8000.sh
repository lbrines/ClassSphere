#!/bin/bash
# Script TDD para verificación de puerto 8000

echo "🔧 TDD: Iniciando verificación de puerto 8000..."

# Limpieza previa
pkill -f uvicorn || true
sleep 2

echo "🔍 TDD: Verificación de puerto 8000..."
if lsof -Pi :8000 -sTCP:LISTEN -t >/dev/null 2>&1; then
    echo "⚠️  TDD: Puerto ocupado. Limpieza automática..."
    pkill -f "port 8000" || true
    sleep 3
fi

echo "🚀 TDD: Iniciando servidor en puerto 8000..."
cd "$(dirname "$0")/.."
source ../venv/bin/activate
python -m uvicorn src.app.main:app --host 127.0.0.1 --port 8000 &
SERVER_PID=$!

# Esperar a que el servidor esté listo
sleep 3

# Verificar que el servidor está funcionando
if ! curl -s -o /dev/null -w "%{http_code}" http://127.0.0.1:8000/health | grep -q "200"; then
    echo "❌ TDD: Error al iniciar servidor en puerto 8000"
    kill $SERVER_PID
    exit 1
fi

echo "✅ TDD: Servidor funcionando correctamente en puerto 8000"
echo "📊 TDD: PID del servidor: $SERVER_PID"
echo "🌐 TDD: Health check: http://127.0.0.1:8000/health"
echo "📚 TDD: API docs: http://127.0.0.1:8000/docs"