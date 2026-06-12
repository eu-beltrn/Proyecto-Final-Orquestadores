import os
from .generate_mock_data import extraer_api_ventas, extraer_bd_clientes

def ejecutar_dag_ingesta():
    """
    Representa el DAG 1 (extraccion_landing_dag). 
    Extrae de las fuentes y guarda en la Zona de Aterrizaje sin transformar.
    """
    ruta_landing = "data/01_landing/"
    os.makedirs(ruta_landing, exist_ok=True)
    
    try:
        print("  [Tarea 1.1] Conectando a API de Ventas...")
        df_ventas = extraer_api_ventas()
        df_ventas.to_csv(f"{ruta_landing}raw_ventas.csv", index=False)
        print(f"  [Éxito] Ventas extraídas y guardadas en Landing ({len(df_ventas)} filas).")
        
        print("  [Tarea 1.2] Conectando a Base de Datos de Clientes...")
        df_clientes = extraer_bd_clientes()
        # Guardamos en formato JSON Lines para variar el tipo de fuente
        df_clientes.to_json(f"{ruta_landing}raw_clientes.json", orient="records", lines=True)
        print(f"  [Éxito] Clientes extraídos y guardados en Landing ({len(df_clientes)} filas).")
        
        return True # El DAG finalizó correctamente
        
    except Exception as e:
        print(f"  [ERROR] Fallo crítico durante la ingesta: {str(e)}")
        return False # El DAG falló