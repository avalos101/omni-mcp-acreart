#!/usr/bin/env python3
"""
Script de ejemplo: Productos más vendidos en Arkadia
Este script demuestra cómo consultar los productos más vendidos usando el MCP de Arkadia
"""

import ssl
import sys
import xmlrpc.client
from datetime import datetime


ARKADIA_URL = "https://elmachetico.omni.net.co"
ARKADIA_DB = "elmachetico_arkadia"
ARKADIA_USER = "mcp-admin@omni.net.co"
ARKADIA_API_KEY = "ab7ad08819e21bc9d05481684c2029f193025bd4"


def conectar():
    """Devuelve (models, uid) conectados via XML-RPC."""
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE

    common = xmlrpc.client.ServerProxy(f"{ARKADIA_URL}/xmlrpc/2/common", context=ctx)
    models = xmlrpc.client.ServerProxy(f"{ARKADIA_URL}/xmlrpc/2/object", context=ctx)
    uid = common.authenticate(ARKADIA_DB, ARKADIA_USER, ARKADIA_API_KEY, {})
    if not uid:
        print("❌ Error de autenticación con Arkadia")
        sys.exit(1)
    return models, uid


def obtener_productos_mas_vendidos(models, uid, limite=20):
    """Obtiene los productos más vendidos en órdenes de venta."""
    print("🔍 Consultando productos más vendidos...")
    
    # Consultar líneas de órdenes de venta
    sale_lines = models.execute_kw(
        ARKADIA_DB,
        uid,
        ARKADIA_API_KEY,
        "sale.order.line",
        "search_read",
        [[]],
        {
            "fields": [
                "product_id", "product_uom_qty", "price_unit", "price_subtotal", 
                "order_id", "name"
            ],
            "limit": 1000
        }
    )
    
    print(f"📊 Encontradas {len(sale_lines)} líneas de productos vendidos")
    
    # Agrupar por producto
    productos_agrupados = {}
    
    for line in sale_lines:
        product_info = line.get('product_id')
        if not product_info:
            continue
            
        product_id = product_info[0] if isinstance(product_info, (list, tuple)) else product_info
        product_name = product_info[1] if isinstance(product_info, (list, tuple)) and len(product_info) > 1 else "Producto sin nombre"
        
        full_name = line.get('name') or product_name
        qty = float(line.get('product_uom_qty', 0))
        price_subtotal = float(line.get('price_subtotal', 0))
        
        if product_id not in productos_agrupados:
            productos_agrupados[product_id] = {
                'name': full_name,
                'total_qty': 0,
                'total_amount': 0,
                'orders_count': 0
            }
        
        productos_agrupados[product_id]['total_qty'] += qty
        productos_agrupados[product_id]['total_amount'] += price_subtotal
        productos_agrupados[product_id]['orders_count'] += 1
    
    # Ordenar por cantidad vendida
    productos_ordenados = sorted(
        productos_agrupados.items(), 
        key=lambda x: x[1]['total_qty'], 
        reverse=True
    )
    
    return productos_ordenados[:limite]


def imprimir_reporte(productos_ordenados):
    """Imprime el reporte de productos más vendidos."""
    print("🛒 PRODUCTOS MÁS VENDIDOS - ARKADIA")
    print("=" * 60)
    
    for i, (product_id, data) in enumerate(productos_ordenados, 1):
        nombre = data['name'][:40] + "..." if len(data['name']) > 40 else data['name']
        cantidad = f"{data['total_qty']:,.0f}"
        ventas = f"${data['total_amount']:,.0f}"
        ordenes = f"{data['orders_count']}"
        
        print(f"{i:2d}. {nombre:<43} | {cantidad:>8} | {ventas:>12} | {ordenes:>3} órdenes")


def main():
    print("🚀 Generando reporte de productos más vendidos en Arkadia...")
    print("=" * 70)
    
    try:
        models, uid = conectar()
        print("✅ Conectado exitosamente a Arkadia")
        
        productos = obtener_productos_mas_vendidos(models, uid)
        imprimir_reporte(productos)
        
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    main()
