#!/bin/bash

# ClassSphere - Commit con modelo específico

MODEL="$1"
MESSAGE="$2"

if [ -z "$MODEL" ] || [ -z "$MESSAGE" ]; then
    echo "❌ Uso: $0 <modelo> <mensaje-commit>"
    echo ""
    echo "Modelos disponibles:"
    echo "   claude  - Claude (claude@classsphere.ai)"
    echo "   gpt4    - GPT-4 (gpt4@classsphere.ai)"
    echo "   gemini  - Gemini (gemini@classsphere.ai)"
    echo "   ibrines - Leopoldo Brines (leopoldo.brines@leobrines.com)"
    echo ""
    echo "Ejemplos:"
    echo "   $0 claude 'feat: add authentication system'"
    echo "   $0 gpt4 'fix: resolve dashboard bug'"
    echo "   $0 gemini 'test: add integration tests'"
    exit 1
fi

echo "🤖 Configurando modelo: $MODEL"
echo "💬 Mensaje: $MESSAGE"
echo ""

# Cambiar a modelo específico
./scripts/switch-model.sh "$MODEL"

# Verificar que hay cambios para commitear
if [ -z "$(git status --porcelain)" ]; then
    echo "⚠️  No hay cambios para commitear"
    echo "💡 Haz algunos cambios primero, luego ejecuta:"
    echo "   $0 $MODEL '$MESSAGE'"
    exit 1
fi

# Hacer commit
echo "📝 Haciendo commit como $MODEL..."
git add .
git commit -m "$MESSAGE"

echo ""
echo "✅ Commit realizado por $MODEL"
echo "📊 Aparecerá en el dashboard de contribuidores"
echo "🔍 Verificar con: git log --oneline -1"
