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

echo "🎯 Modelos configurados:"
echo "   1. Leopoldo Brines (leopoldo.brines@leobrines.com) - Desarrollador principal"
echo "   2. Claude (claude@classsphere.ai) - Análisis y arquitectura"
echo "   3. GPT-4 (gpt4@classsphere.ai) - Implementación de features"
echo "   4. Gemini (gemini@classsphere.ai) - Testing y documentación"
echo ""

echo "📝 Para cambiar entre modelos, usa:"
echo "   ./scripts/switch-model.sh claude"
echo "   ./scripts/switch-model.sh gpt4"
echo "   ./scripts/switch-model.sh gemini"
echo "   ./scripts/switch-model.sh ibrines"
echo ""

echo "🚀 Para hacer commit con modelo específico:"
echo "   ./scripts/commit-as-model.sh claude 'feat: add authentication'"
echo ""

echo "✅ Configuración completada. Cada modelo aparecerá como contribuidor separado en el dashboard."
