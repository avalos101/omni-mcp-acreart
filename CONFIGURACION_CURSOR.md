# Configuración de Cursor AI para Arkadia MCP

Esta guía te ayudará a configurar Cursor AI para usar el MCP de Arkadia.

## 📋 Pasos de Configuración

### 1. Instalar el Proyecto

```bash
git clone <url-del-repositorio>
cd omni-mcp-arkadia
./install.sh
```

### 2. Configurar Credenciales

Edita el archivo `.env.arkadia` con tus credenciales de Arkadia:

```bash
cp .env.arkadia.example .env.arkadia
# Edita .env.arkadia con tus credenciales
```

### 3. Configurar Cursor AI

#### Opción A: Usar el archivo de configuración incluido

1. Copia el contenido de `cursor_config.json`
2. En Cursor, ve a **Settings** → **Extensions** → **MCP Servers**
3. Pega la configuración en el archivo de configuración de MCP

#### Opción B: Configuración manual

Agrega la siguiente configuración a tu archivo de configuración de Cursor:

```json
{
  "mcpServers": {
    "arkadia": {
      "command": "python3",
      "args": ["-m", "mcp_server_omni"],
      "cwd": "/ruta/completa/a/omni-mcp-arkadia",
      "env": {
        "OMNI_URL": "https://elmachetico.omni.net.co",
        "OMNI_USER": "tu_usuario@arkadia.com",
        "OMNI_API_KEY": "tu_api_key_aqui",
        "OMNI_DB": "elmachetico_arkadia",
        "OMNI_MCP_LOG_LEVEL": "INFO",
        "OMNI_MCP_DEFAULT_LIMIT": "10",
        "OMNI_MCP_MAX_LIMIT": "100",
        "OMNI_MCP_MAX_SMART_FIELDS": "15",
        "OMNI_MCP_TRANSPORT": "stdio",
        "OMNI_MCP_HOST": "localhost",
        "OMNI_MCP_PORT": "8003"
      }
    }
  }
}
```

### 4. Probar la Configuración

```bash
# Probar conexión
./scripts/test_connection.py

# Iniciar servidor MCP
./start_arkadia_mcp.sh
```

## 🎯 Uso en Cursor

Una vez configurado, puedes usar comandos como:

### Consultas Básicas
- "Conecta a Arkadia y muestra los productos más vendidos"
- "Genera un reporte de ventas del mes actual"
- "Lista los clientes con facturas pendientes"

### Análisis Avanzados
- "Analiza las tendencias de ventas por producto"
- "Muestra el rendimiento por cliente"
- "Genera un dashboard de métricas clave"

### Reportes Personalizados
- "Crea un reporte de inventario con stock bajo"
- "Muestra las órdenes de venta por vendedor"
- "Analiza la rentabilidad por producto"

## 🔧 Solución de Problemas

### Error de Conexión
1. Verifica que las credenciales en `.env.arkadia` sean correctas
2. Confirma que tienes acceso a la instancia de Arkadia
3. Revisa que el servidor MCP esté ejecutándose

### Error de Autenticación
1. Verifica tu usuario y API key
2. Confirma que tu usuario tiene permisos en Arkadia
3. Contacta al administrador de Arkadia si es necesario

### Error de Configuración de Cursor
1. Verifica que la ruta en `cwd` sea correcta
2. Confirma que Python 3 esté disponible
3. Revisa que el módulo MCP esté instalado

## 📞 Soporte

Si tienes problemas con la configuración:

1. Revisa la documentación en `README.md`
2. Consulta los ejemplos en `examples/`
3. Verifica los logs del servidor MCP
4. Contacta al equipo de soporte

## 🔄 Actualizaciones

Para mantener el proyecto actualizado:

```bash
git pull origin main
./install.sh
```

Esto actualizará las dependencias y reiniciará el servidor MCP.
