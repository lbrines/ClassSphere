#!/bin/bash

# ClassSphere - Cambio rápido entre modelos contribuidores

MODEL="$1"

if [ -z "$MODEL" ]; then
    echo "❌ Uso: $0 <modelo>"
    echo ""
    echo "Herramientas disponibles:"
    echo "   claude  - Claude (claude@classsphere.ai)"
    echo "   codex   - Codex (codex@classsphere.ai)"
    echo "   cursor  - Cursor (cursor@classsphere.ai)"
    echo "   windsurf - Windsurf (windsurf@classsphere.ai)"
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
    "codex")
        git config user.name "Codex"
        git config user.email "codex@classsphere.ai"
        echo "🤖 Cambiado a Codex (codex@classsphere.ai)"
        ;;
    "cursor")
        git config user.name "Cursor"
        git config user.email "cursor@classsphere.ai"
        echo "🤖 Cambiado a Cursor (cursor@classsphere.ai)"
        ;;
    "windsurf")
        git config user.name "Windsurf"
        git config user.email "windsurf@classsphere.ai"
        echo "🤖 Cambiado a Windsurf (windsurf@classsphere.ai)"
        ;;
    "ibrines")
        git config user.name "Leopoldo Brines"
        git config user.email "leopoldo.brines@leobrines.com"
        echo "👨‍💻 Cambiado a Leopoldo Brines (leopoldo.brines@leobrines.com)"
        ;;
    *)
        echo "❌ Herramienta no reconocida: $MODEL"
        echo "Herramientas disponibles: claude, codex, cursor, windsurf, ibrines"
        exit 1
        ;;
esac

echo "✅ Configuración actual:"
echo "   Nombre: $(git config user.name)"
echo "   Email: $(git config user.email)"
echo ""
echo "💡 Ahora puedes hacer commits que aparecerán como contribuciones de $MODEL"
