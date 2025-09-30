#!/usr/bin/env python3
"""
Script de prueba de conexión a Arkadia
Verifica que la conexión y autenticación funcionen correctamente
"""

import ssl
import sys
import xmlrpc.client

ARKADIA_URL = "https://elmachetico.omni.net.co"
ARKADIA_DB = "elmachetico_arkadia"
ARKADIA_USER = "mcp-admin@omni.net.co"
ARKADIA_API_KEY = "ab7ad08819e21bc9d05481684c2029f193025bd4"

def test_connection():
    """Prueba la conexión a Arkadia"""
    try:
        print("🔍 Probando conexión a Arkadia...")
        
        # Configurar SSL
        ctx = ssl.create_default_context()
        ctx.check_hostname = False
        ctx.verify_mode = ssl.CERT_NONE

        # Conectar
        common = xmlrpc.client.ServerProxy(f"{ARKADIA_URL}/xmlrpc/2/common", context=ctx)
        models = xmlrpc.client.ServerProxy(f"{ARKADIA_URL}/xmlrpc/2/object", context=ctx)
        
        print("✅ Servidores XML-RPC conectados")
        
        # Autenticar
        uid = common.authenticate(ARKADIA_DB, ARKADIA_USER, ARKADIA_API_KEY, {})
        if not uid:
            print("❌ Error de autenticación")
            return False
            
        print(f"✅ Autenticación exitosa - UID: {uid}")
        
        # Probar consultas básicas
        print("🔍 Probando consultas básicas...")
        
        # Contar productos
        products = models.execute_kw(ARKADIA_DB, uid, ARKADIA_API_KEY, 'product.product', 'search_count', [[]])
        print(f"📊 Total productos: {products}")
        
        # Contar órdenes de venta
        sale_orders = models.execute_kw(ARKADIA_DB, uid, ARKADIA_API_KEY, 'sale.order', 'search_count', [[]])
        print(f"📊 Total órdenes de venta: {sale_orders}")
        
        # Contar líneas de órdenes
        sale_lines = models.execute_kw(ARKADIA_DB, uid, ARKADIA_API_KEY, 'sale.order.line', 'search_count', [[]])
        print(f"📊 Total líneas de órdenes: {sale_lines}")
        
        # Contar facturas
        invoices = models.execute_kw(ARKADIA_DB, uid, ARKADIA_API_KEY, 'account.move', 'search_count', [[]])
        print(f"📊 Total facturas: {invoices}")
        
        print("\n🎉 ¡Conexión exitosa! El MCP de Arkadia está funcionando correctamente.")
        return True
        
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_connection()
    sys.exit(0 if success else 1)
