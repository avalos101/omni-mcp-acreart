# Omni MCP - Arkadia

Este proyecto proporciona un servidor MCP (Model Context Protocol) para integrar Arkadia con Cursor AI, permitiendo consultas directas a la base de datos de Arkadia.

## 🏢 Sobre Arkadia

Arkadia es un sistema ERP basado en Omni que permite la gestión integral de empresas. Este MCP facilita el acceso a los datos de Arkadia desde Cursor AI para realizar consultas, análisis y reportes.

## 🚀 Instalación

### Requisitos Previos

- Python 3.9 o superior
- Cursor AI instalado
- Acceso a la instancia de Arkadia

### Pasos de Instalación

1. **Clonar el repositorio:**
   ```bash
   git clone <url-del-repositorio>
   cd omni-mcp-arkadia
   ```

2. **Instalar dependencias:**
   ```bash
   cd mcp-server-omni
   pip install -e .
   ```

3. **Configurar variables de entorno:**
   ```bash
   cp .env.arkadia.example .env.arkadia
   # Editar .env.arkadia con tus credenciales
   ```

4. **Configurar Cursor:**
   - Copiar el contenido de `cursor_config.json` a tu configuración de Cursor
   - O usar el archivo directamente en la configuración de MCP

## ⚙️ Configuración

### Variables de Entorno

Edita el archivo `.env.arkadia` con tus credenciales:

```bash
# Configuración del servidor MCP Arkadia
OMNI_URL=https://elmachetico.omni.net.co
OMNI_USER=tu_usuario@arkadia.com
OMNI_API_KEY=tu_api_key_aqui
OMNI_DB=elmachetico_arkadia

# Configuración opcional
OMNI_MCP_LOG_LEVEL=INFO
OMNI_MCP_DEFAULT_LIMIT=10
OMNI_MCP_MAX_LIMIT=100
OMNI_MCP_MAX_SMART_FIELDS=15
OMNI_MCP_TRANSPORT=stdio
OMNI_MCP_HOST=localhost
OMNI_MCP_PORT=8003
```

### Configuración de Cursor

El archivo `cursor_config.json` contiene la configuración necesaria para Cursor AI. Puedes copiarlo a tu configuración de Cursor o usarlo como referencia.

## 🏃‍♂️ Uso

### Iniciar el Servidor MCP

```bash
./start_arkadia_mcp.sh
```

O manualmente:

```bash
cd mcp-server-omni
python3 -m mcp_server_omni
```

### Ejemplos de Uso en Cursor

Una vez configurado, puedes usar comandos como:

- "Conecta a Arkadia y dame un reporte de productos más vendidos"
- "Consulta las órdenes de venta del mes actual"
- "Genera un reporte de clientes activos"
- "Muestra las facturas pendientes de pago"

## 📊 Funcionalidades Disponibles

### Modelos Soportados

- **product.product**: Gestión de productos
- **sale.order**: Órdenes de venta
- **sale.order.line**: Líneas de órdenes de venta
- **account.move**: Facturas
- **account.move.line**: Líneas de factura
- **res.partner**: Clientes y proveedores
- **stock.move**: Movimientos de inventario

### Operaciones Disponibles

- **Consultas**: Búsqueda y lectura de datos
- **Reportes**: Generación de reportes personalizados
- **Análisis**: Análisis de datos y métricas
- **Agrupaciones**: Agrupación de datos por diferentes criterios

## 🔧 Desarrollo

### Estructura del Proyecto

```
omni-mcp-arkadia/
├── mcp-server-omni/          # Servidor MCP
│   ├── mcp_server_omni/      # Código fuente
│   ├── pyproject.toml        # Configuración del proyecto
│   └── README.md            # Documentación del servidor
├── scripts/                 # Scripts de utilidad
├── examples/                # Ejemplos de uso
├── .env.arkadia            # Variables de entorno
├── cursor_config.json      # Configuración de Cursor
├── start_arkadia_mcp.sh    # Script de inicio
└── README.md               # Este archivo
```

### Agregar Nuevas Funcionalidades

Para agregar nuevas funcionalidades al MCP:

1. Edita `mcp-server-omni/mcp_server_omni/tools.py`
2. Agrega nuevos métodos en `mcp-server-omni/mcp_server_omni/server.py`
3. Actualiza la documentación

## 🐛 Solución de Problemas

### Error de Conexión

Si tienes problemas de conexión:

1. Verifica las credenciales en `.env.arkadia`
2. Confirma que tienes acceso a la instancia de Arkadia
3. Revisa los logs del servidor MCP

### Error de Autenticación

Si hay errores de autenticación:

1. Verifica tu usuario y API key
2. Confirma que tu usuario tiene permisos en Arkadia
3. Contacta al administrador de Arkadia si es necesario

## 📞 Soporte

Para soporte técnico o preguntas sobre este proyecto:

- Crear un issue en el repositorio
- Contactar al equipo de desarrollo
- Revisar la documentación de Omni ERP

## 📄 Licencia

Este proyecto está bajo la licencia especificada en el archivo LICENSE.

## 🔄 Actualizaciones

Para mantener el proyecto actualizado:

```bash
git pull origin main
cd mcp-server-omni
pip install -e .
```

## 📝 Changelog

Ver `CHANGELOG.md` para el historial de cambios y nuevas funcionalidades.
