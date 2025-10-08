#!/bin/bash

# ClassSphere - Cambio rápido entre modelos contribuidores

MODEL="$1"

if [ -z "$MODEL" ]; then
    echo "❌ Uso: $0 <modelo>"
    echo ""
    echo "Modelos disponibles:"
    echo "   claude  - Claude (claude@classsphere.ai)"
    echo "   gpt4    - GPT-4 (gpt4@classsphere.ai)"
    echo "   gemini  - Gemini (gemini@classsphere.ai)"
    echo "   ibrines - Leopoldo Brines (leopoldo.brines@leobrines.com)"
    echo ""
    echo "Ejemplo: $0 claude"
    exit 1
fi

case $MODEL in
    "claude")
        git config user.name "Claude"
        git config user.email "claude@classsphere.ai"
        echo "🤖 Cambiado a Claude (claude@classsphere.ai)"
        ;;
    "gpt4")
        git config user.name "GPT-4"
        git config user.email "gpt4@classsphere.ai"
        echo "🤖 Cambiado a GPT-4 (gpt4@classsphere.ai)"
        ;;
    "gemini")
        git config user.name "Gemini"
        git config user.email "gemini@classsphere.ai"
        echo "🤖 Cambiado a Gemini (gemini@classsphere.ai)"
        ;;
    "ibrines")
        git config user.name "Leopoldo Brines"
        git config user.email "leopoldo.brines@leobrines.com"
        echo "👨‍💻 Cambiado a Leopoldo Brines (leopoldo.brines@leobrines.com)"
        ;;
    *)
        echo "❌ Modelo no reconocido: $MODEL"
        echo "Modelos disponibles: claude, gpt4, gemini, ibrines"
        exit 1
        ;;
esac

echo "✅ Configuración actual:"
echo "   Nombre: $(git config user.name)"
echo "   Email: $(git config user.email)"
echo ""
echo "💡 Ahora puedes hacer commits que aparecerán como contribuciones de $MODEL"
