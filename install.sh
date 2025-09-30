#!/bin/bash
# Script de instalación para Omni MCP - Arkadia

echo "🚀 Instalando Omni MCP - Arkadia..."
echo "===================================="

# Verificar Python
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 no está instalado. Por favor instala Python 3.9 o superior."
    exit 1
fi

echo "✅ Python 3 encontrado: $(python3 --version)"

# Verificar pip
if ! command -v pip3 &> /dev/null; then
    echo "❌ pip3 no está instalado. Por favor instala pip."
    exit 1
fi

echo "✅ pip3 encontrado"

# Crear entorno virtual si no existe
if [ ! -d "venv" ]; then
    echo "📦 Creando entorno virtual..."
    python3 -m venv venv
fi

# Activar entorno virtual
echo "🔧 Activando entorno virtual..."
source venv/bin/activate

# Instalar dependencias del servidor MCP
echo "📥 Instalando dependencias del servidor MCP..."
cd mcp-server-omni
pip install -e .

# Volver al directorio raíz
cd ..

# Crear archivo de configuración si no existe
if [ ! -f ".env.arkadia" ]; then
    echo "⚙️ Creando archivo de configuración..."
    cp .env.arkadia.example .env.arkadia
    echo "📝 Por favor edita el archivo .env.arkadia con tus credenciales de Arkadia"
fi

# Hacer ejecutables los scripts
chmod +x start_arkadia_mcp.sh
chmod +x scripts/*.py

echo ""
echo "🎉 ¡Instalación completada!"
echo ""
echo "📋 Próximos pasos:"
echo "1. Edita el archivo .env.arkadia con tus credenciales"
echo "2. Ejecuta: ./scripts/test_connection.py para probar la conexión"
echo "3. Configura Cursor con el archivo cursor_config.json"
echo "4. Inicia el servidor MCP con: ./start_arkadia_mcp.sh"
echo ""
echo "📖 Para más información, consulta README.md"
