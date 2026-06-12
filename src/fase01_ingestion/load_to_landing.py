import os
import time
from .generate_mock_data import extraer_api_ventas, extraer_bd_clientes

def ejecutar_dag_ingesta(intentos_maximos=3):
    """
    Representa el DAG 1. Incluye simulación de 'Retries' de Airflow.
    """
    ruta_landing = "data/01_landing/"
    os.makedirs(ruta_landing, exist_ok=True)
    
    intento_actual = 1
    
    while intento_actual <= intentos_maximos:
        try:
            print(f"  [Intento {intento_actual}/{intentos_maximos}] Conectando a fuentes de datos...")
            
            df_ventas = extraer_api_ventas()
            df_ventas.to_csv(f"{ruta_landing}raw_ventas.csv", index=False)
            
            df_clientes = extraer_bd_clientes()
            df_clientes.to_json(f"{ruta_landing}raw_clientes.json", orient="records", lines=True)
            
            print(f"  [Éxito] Datos extraídos y guardados en Landing Zone.")
            return True # Salió bien, rompemos el bucle y devolvemos True
            
        except Exception as e:
            print(f"  [ERROR] Fallo de conexión: {str(e)}")
            if intento_actual < intentos_maximos:
                print("  [*] Reintentando en 2 segundos... (Simulando Airflow Retry)")
                time.sleep(2)
            intento_actual += 1
            
    print("  [ERROR CRÍTICO] Se agotaron los reintentos. El DAG 1 ha fallado.")
    return False