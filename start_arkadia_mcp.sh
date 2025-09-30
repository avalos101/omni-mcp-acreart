#!/bin/bash
# Script de inicio para el servidor MCP Arkadia

echo "🚀 Iniciando servidor MCP Arkadia..."
echo "===================================="

# Verificar si existe el archivo de configuración
if [ ! -f ".env.arkadia" ]; then
    echo "❌ Error: No se encontró el archivo .env.arkadia"
    echo "   Por favor copia .env.arkadia.example a .env.arkadia y configura tus credenciales"
    exit 1
fi

# Cargar variables de entorno
export $(cat .env.arkadia | grep -v '^#' | xargs)

# Verificar que las variables necesarias estén configuradas
if [ -z "$OMNI_URL" ] || [ -z "$OMNI_USER" ] || [ -z "$OMNI_API_KEY" ] || [ -z "$OMNI_DB" ]; then
    echo "❌ Error: Variables de entorno incompletas"
    echo "   Por favor verifica tu archivo .env.arkadia"
    exit 1
fi

# Cambiar al directorio del servidor MCP
cd mcp-server-omni

echo "📊 Configuración:"
echo "  URL: $OMNI_URL"
echo "  Usuario: $OMNI_USER"
echo "  Base de datos: $OMNI_DB"
echo "  Puerto: $OMNI_MCP_PORT"
echo ""

# Verificar que Python esté disponible
if ! command -v python3 &> /dev/null; then
    echo "❌ Error: Python 3 no está instalado"
    exit 1
fi

# Verificar que el módulo MCP esté instalado
if ! python3 -c "import mcp_server_omni" 2>/dev/null; then
    echo "❌ Error: El servidor MCP no está instalado"
    echo "   Ejecuta: ./install.sh"
    exit 1
fi

# Ejecutar el servidor MCP
echo "🔧 Iniciando servidor MCP..."
echo "   Para detener el servidor, presiona Ctrl+C"
echo ""

python3 -m mcp_server_omni

