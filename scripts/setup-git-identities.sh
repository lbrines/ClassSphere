#!/bin/bash

# Script para configurar identidades Git para diferentes modelos
# ClassSphere - Multi-model contributor setup

echo "🔧 Configurando identidades Git para modelos..."

# Función para configurar identidad
setup_identity() {
    local model_name="$1"
    local model_email="$2"
    local model_key="$3"
    
    echo "📝 Configurando identidad para: $model_name"
    
    # Crear configuración local
    git config user.name "$model_name"
    git config user.email "$model_email"
    
    # Si tienes diferentes claves SSH, configurar aquí
    if [ ! -z "$model_key" ]; then
        git config core.sshCommand "ssh -i $model_key"
    fi
    
    echo "✅ $model_name configurado con email: $model_email"
}

# Identidades sugeridas para ClassSphere
echo "🤖 Configurando modelos para ClassSphere..."

# Modelo principal (desarrollador)
setup_identity "Ibrines" "ibrines@classsphere.dev" ""

# Modelos de IA
setup_identity "Claude" "claude@classsphere.ai" ""
setup_identity "GPT-4" "gpt4@classsphere.ai" ""
setup_identity "Gemini" "gemini@classsphere.ai" ""

echo ""
echo "🎯 Para cambiar entre modelos:"
echo "git config user.name 'Nombre del Modelo'"
echo "git config user.email 'email@classsphere.ai'"
echo ""
echo "📊 Los commits aparecerán separados en el dashboard de contribuidores"
