#!/bin/bash

# Script para cambiar entre modelos y hacer commits
# ClassSphere - Model switching workflow

MODEL_NAME="$1"
MODEL_EMAIL="$2"
COMMIT_MESSAGE="$3"

if [ -z "$MODEL_NAME" ] || [ -z "$MODEL_EMAIL" ] || [ -z "$COMMIT_MESSAGE" ]; then
    echo "❌ Uso: $0 <nombre-modelo> <email> <mensaje-commit>"
    echo ""
    echo "Ejemplos:"
    echo "  $0 'Claude' 'claude@classsphere.ai' 'feat: add authentication'"
    echo "  $0 'GPT-4' 'gpt4@classsphere.ai' 'fix: resolve dashboard bug'"
    echo "  $0 'Gemini' 'gemini@classsphere.ai' 'docs: update API documentation'"
    exit 1
fi

echo "🤖 Cambiando a modelo: $MODEL_NAME"
echo "📧 Email: $MODEL_EMAIL"
echo "💬 Commit: $COMMIT_MESSAGE"
echo ""

# Configurar identidad del modelo
git config user.name "$MODEL_NAME"
git config user.email "$MODEL_EMAIL"

# Verificar configuración
echo "✅ Configuración actual:"
echo "   Nombre: $(git config user.name)"
echo "   Email: $(git config user.email)"
echo ""

# Hacer commit con la identidad del modelo
git add .
git commit -m "$COMMIT_MESSAGE"

echo "🎉 Commit realizado por $MODEL_NAME"
echo "📊 Aparecerá en el dashboard de contribuidores"
