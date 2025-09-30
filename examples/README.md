# Ejemplos de Uso - Arkadia MCP

Este directorio contiene ejemplos de cómo usar el MCP de Arkadia con Cursor AI.

## 📋 Ejemplos Disponibles

### 1. Consultas Básicas

#### Productos Más Vendidos
```bash
python3 scripts/productos_mas_vendidos.py
```

#### Prueba de Conexión
```bash
python3 scripts/test_connection.py
```

### 2. Comandos para Cursor AI

Una vez que tengas el MCP configurado en Cursor, puedes usar comandos como:

#### Análisis de Ventas
- "Conecta a Arkadia y dame un reporte de productos más vendidos este mes"
- "Muestra las órdenes de venta del último trimestre"
- "Genera un análisis de ventas por cliente"

#### Gestión de Productos
- "Lista todos los productos con stock bajo"
- "Muestra los productos más rentables"
- "Consulta la información de un producto específico"

#### Reportes Financieros
- "Genera un reporte de facturas pendientes"
- "Muestra las ventas por período"
- "Consulta los pagos recibidos esta semana"

#### Análisis de Clientes
- "Lista los clientes más activos"
- "Muestra los clientes con facturas pendientes"
- "Genera un reporte de nuevos clientes"

### 3. Ejemplos de Consultas Específicas

#### Ventas del Mes Actual
```
"Conecta a Arkadia y consulta las órdenes de venta del mes actual, 
agrupadas por día y mostrando el total de ventas"
```

#### Productos con Mayor Rotación
```
"Analiza los productos con mayor rotación en Arkadia, 
mostrando cantidad vendida y frecuencia de venta"
```

#### Clientes con Mayor Valor
```
"Muestra los clientes con mayor valor de compras en Arkadia, 
ordenados por monto total"
```

## 🔧 Personalización

Puedes crear tus propios scripts basándote en los ejemplos proporcionados:

1. Copia un script existente
2. Modifica las consultas según tus necesidades
3. Agrega nuevos campos o filtros
4. Personaliza el formato de salida

## 📊 Modelos Disponibles

El MCP de Arkadia soporta los siguientes modelos principales:

- **product.product**: Productos
- **sale.order**: Órdenes de venta
- **sale.order.line**: Líneas de órdenes
- **account.move**: Facturas
- **account.move.line**: Líneas de factura
- **res.partner**: Clientes y proveedores
- **stock.move**: Movimientos de inventario

## 💡 Consejos

1. **Usa filtros específicos**: Especifica fechas, estados o categorías para obtener resultados más precisos
2. **Limita los resultados**: Para consultas grandes, usa límites para evitar tiempos de respuesta largos
3. **Agrupa los datos**: Usa agrupaciones para obtener resúmenes más útiles
4. **Combina modelos**: Relaciona datos de diferentes modelos para análisis más completos

## 🐛 Solución de Problemas

Si tienes problemas con los ejemplos:

1. Verifica que el servidor MCP esté ejecutándose
2. Confirma que las credenciales en `.env.arkadia` sean correctas
3. Revisa los logs del servidor para errores específicos
4. Asegúrate de tener permisos para acceder a los modelos consultados
