import pandas as pd
import random
from datetime import datetime, timedelta

def extraer_api_ventas(num_registros=100):
    """Simula la extracción de datos desde una API REST de Ventas (Ej. Shopify)."""
    datos = []
    for i in range(1, num_registros + 1):
        datos.append({
            "id_transaccion": i,
            "id_cliente": random.randint(1, 20),
            "id_producto": random.randint(100, 110),
            "fecha_venta": (datetime.now() - timedelta(days=random.randint(0, 10))).strftime("%Y-%m-%d"),
            "monto": round(random.uniform(15.0, 500.0), 2),
            "metodo_pago": random.choice(["Tarjeta", "Efectivo", "Transferencia"])
        })
    return pd.DataFrame(datos)

def extraer_bd_clientes(num_registros=20):
    """Simula una extracción desde una base de datos operativa PostgreSQL."""
    datos = []
    for i in range(1, num_registros + 1):
        # Introducimos nulos intencionales para probar el DAG 2 de Nicole
        nombre = f"Cliente_Demo_{i}" if i % 5 != 0 else None 
        
        datos.append({
            "id_cliente": i,
            "nombre": nombre,
            "email": f"cliente{i}@empresa.com" if nombre else None,
            "region": random.choice(["Norte", "Sur", "Este", "Oeste"])
        })
    
    # Introducimos un duplicado intencional para la cuarentena
    datos.append(datos[0])
    return pd.DataFrame(datos)