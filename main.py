import time
import os

# Importación del módulo de Jonathan (DAG 1)
from src.fase01_ingestion.load_to_landing import ejecutar_dag_ingesta

# Importaciones futuras de las compañeras (Descomentar cuando estén listas)
# from src.02_validation.data_quality import ejecutar_dag_calidad      # Módulo de Nicole
from src.fase02_validation.data_quality import ejecutar_dag_calidad
# from src.03_transformation.build_dwh import ejecutar_dag_dwh         # Módulo de Eu

def preparar_entorno():
    """Crea las carpetas base del Data Lake si no existen."""
    carpetas = ["data/01_landing", "data/02_raw", "data/03_quarantine", "data/04_warehouse"]
    for carpeta in carpetas:
        os.makedirs(carpeta, exist_ok=True)

def orquestador_airflow_simulado():
    preparar_entorno()
    print("="*60)
    print("🚀 INICIANDO ORQUESTADOR DE PIPELINES (Simulación Airflow)")
    print("="*60)
    
    # ---------------------------------------------------------
    # DAG 1: INGESTA TRANSACCIONAL A LANDING ZONE (JONATHAN)
    # ---------------------------------------------------------
    print("\n[DAG 1] Ejecutando: extraccion_landing_dag...")
    start_time = time.time()
    estado_dag_1 = ejecutar_dag_ingesta()
    
    if not estado_dag_1:
        print("❌ [ALERTA] DAG 1 Falló. Deteniendo el pipeline por seguridad.")
        return 
        
    print(f"✅ DAG 1 completado en {round(time.time() - start_time, 2)}s.")
    
    # ---------------------------------------------------------
    # DAG 2: CALIDAD DE DATOS (NICOLE)
    # ---------------------------------------------------------
    print("\n[DAG 2] Ejecutando: calidad_raw_dag...")
    start_time_dag2 = time.time()
    
    estado_dag_2 = ejecutar_dag_calidad()
    
    if not estado_dag_2:
        print("❌ [ALERTA] DAG 2 Falló. Deteniendo el pipeline por seguridad.")
        return
        
    print(f"✅ DAG 2 completado en {round(time.time() - start_time_dag2, 2)}s.")
    
    
    
    # ---------------------------------------------------------
    # DAG 3: CARGA A DATA WAREHOUSE (EU)
    # ---------------------------------------------------------
    print("\n[DAG 3] Ejecutando: transformacion_dwh_dag...")
    print("  -> (Esperando código de Eu para ejecutarse automáticamente)")
    # ejecutar_dag_dwh()

    print("\n" + "="*60)
    print("🎉 FLUJO DEL ORQUESTADOR FINALIZADO")
    print("="*60)

if __name__ == "__main__":
    orquestador_airflow_simulado()