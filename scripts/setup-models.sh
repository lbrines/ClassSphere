#!/bin/bash

# ClassSphere - Configuración de múltiples modelos contribuidores
# Este script configura identidades Git para que cada modelo aparezca como contribuidor separado

echo "🔧 Configurando identidades Git para modelos de ClassSphere..."

# Función para mostrar configuración actual
show_current_config() {
    echo "📋 Configuración actual:"
    echo "   Nombre: $(git config user.name)"
    echo "   Email: $(git config user.email)"
    echo ""
}

# Mostrar configuración inicial
echo "🔍 Configuración inicial:"
show_current_config

# Crear directorio de scripts si no existe
mkdir -p scripts

echo "✅ Scripts de configuración creados:"
echo "   - scripts/setup-models.sh (este archivo)"
echo "   - scripts/switch-model.sh (cambio rápido entre modelos)"
echo "   - scripts/commit-as-model.sh (commit con modelo específico)"
echo ""

echo "🎯 Herramientas configuradas:"
echo "   1. Leopoldo Brines (leopoldo.brines@leobrines.com) - Desarrollador principal"
echo "   2. Claude (claude@classsphere.ai) - Análisis y arquitectura"
echo "   3. Codex (codex@classsphere.ai) - Generación de código"
echo "   4. Cursor (cursor@classsphere.ai) - IDE inteligente"
echo "   5. Windsurf (windsurf@classsphere.ai) - Desarrollo colaborativo"
echo ""

echo "📝 Para cambiar entre herramientas, usa:"
echo "   ./scripts/switch-model.sh claude"
echo "   ./scripts/switch-model.sh codex"
echo "   ./scripts/switch-model.sh cursor"
echo "   ./scripts/switch-model.sh windsurf"
echo "   ./scripts/switch-model.sh ibrines"
echo ""

echo "🚀 Para hacer commit con herramienta específica:"
echo "   ./scripts/commit-as-model.sh claude 'feat: add authentication'"
echo "   ./scripts/commit-as-model.sh codex 'fix: resolve bug'"
echo "   ./scripts/commit-as-model.sh cursor 'test: add tests'"
echo "   ./scripts/commit-as-model.sh windsurf 'docs: update docs'"
echo ""

echo "✅ Configuración completada. Cada herramienta aparecerá como contribuidor separado en el dashboard."
