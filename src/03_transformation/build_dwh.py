import pandas as pd
import os
from src.utils.security import aplicar_gobernanza_datos

def ejecutar_dag_dwh():
    """
    Representa el DAG 3 (transformacion_dwh_dag).
    Construye las dimensiones y la tabla de hechos aplicando reglas de negocio y seguridad.
    """
    raw_path = "data/02_raw/"
    dwh_path = "data/04_warehouse/"
    os.makedirs(dwh_path, exist_ok=True)
    
    try:
        print("  [Tarea 3.1] Extrayendo datos limpios de la Zona Raw...")
        # Nota: Simulamos que los datos ya están limpios. En la práctica, 
        # estos archivos son generados por el DAG 2 de Nicole.
        df_ventas = pd.read_csv(f"{raw_path}ventas_validas.csv")
        df_clientes = pd.read_json(f"{raw_path}clientes_validos.json", lines=True)
        
        print("  [Tarea 3.2] Construyendo Dimensión Cliente (Aplicando Enmascaramiento)...")
        # Eu aplica la regla de gobierno de datos: ocultar el nombre y email
        dim_cliente = aplicar_gobernanza_datos(df_clientes, columnas_sensibles=["nombre", "email"])
        dim_cliente.to_parquet(f"{dwh_path}dim_cliente.parquet", index=False)
        
        print("  [Tarea 3.3] Construyendo Tabla de Hechos (Fact_Ventas)...")
        fact_ventas = df_ventas.copy()
        # Generar llave foránea de fecha
        fact_ventas['id_fecha'] = pd.to_datetime(fact_ventas['fecha_venta']).dt.strftime('%Y%m%d').astype(int)
        
        # Seleccionar solo las columnas necesarias para los cálculos numéricos
        fact_ventas = fact_ventas[['id_transaccion', 'id_cliente', 'id_producto', 'id_fecha', 'monto', 'metodo_pago']]
        fact_ventas.to_parquet(f"{dwh_path}fact_ventas.parquet", index=False)
        
        print(f"  [Éxito] Esquema Estrella guardado en formato columnar (Parquet) en {dwh_path}.")
        return True
        
    except Exception as e:
        print(f"  [ERROR] Fallo al construir el Data Warehouse: {str(e)}")
        return False