#!/bin/bash

# ClassSphere - Commit con modelo específico

MODEL="$1"
MESSAGE="$2"

if [ -z "$MODEL" ] || [ -z "$MESSAGE" ]; then
    echo "❌ Uso: $0 <modelo> <mensaje-commit>"
    echo ""
    echo "Herramientas disponibles:"
    echo "   claude   - Claude (claude@classsphere.ai)"
    echo "   codex    - Codex (codex@classsphere.ai)"
    echo "   cursor   - Cursor (cursor@classsphere.ai)"
    echo "   windsurf - Windsurf (windsurf@classsphere.ai)"
    echo "   ibrines  - Leopoldo Brines (leopoldo.brines@leobrines.com)"
    echo ""
    echo "Ejemplos:"
    echo "   $0 claude 'feat: add authentication system'"
    echo "   $0 codex 'fix: resolve dashboard bug'"
    echo "   $0 cursor 'test: add integration tests'"
    echo "   $0 windsurf 'docs: update API documentation'"
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

# Hacer commit con co-authored-by
echo "📝 Haciendo commit como $MODEL con co-authored-by..."
git add .

# Crear mensaje con co-authored-by
COMMIT_MESSAGE="$MESSAGE

Co-authored-by: Claude <claude@anthropic.com>
Co-authored-by: Cursor <cursor@cursor.com>
Co-authored-by: OpenAI <openai@openai.com>"

git commit -m "$COMMIT_MESSAGE"

echo ""
echo "✅ Commit realizado por $MODEL"
echo "📊 Aparecerá en el dashboard de contribuidores"
echo "🔍 Verificar con: git log --oneline -1"
