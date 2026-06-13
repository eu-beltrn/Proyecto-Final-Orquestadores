import os
import sys
import pandas as pd
from typing import Tuple

# Inyección de rutas absolutas para garantizar que Python encuentre 'utils' sin errores
DIRECTORIO_ACTUAL = os.path.dirname(os.path.abspath(__file__))
RAIZ_PROYECTO = os.path.abspath(os.path.join(DIRECTORIO_ACTUAL, '../..'))
CARPETA_SRC = os.path.abspath(os.path.join(DIRECTORIO_ACTUAL, '..'))

for ruta in [RAIZ_PROYECTO, CARPETA_SRC]:
    if ruta not in sys.path:
        sys.path.insert(0, ruta)

# Importamos el logger desde el archivo que creamos arriba
from utils.logger import CentralizedLogger

class DataQualityGate:
    """
    Componente de la Fase 02 (Validación y Calidad). Actúa como filtro de seguridad
    aplicando reglas de negocio vectorizadas y ruteo perimetral (Branching)
    para proteger la integridad del Data Warehouse de Eu.
    """
    def __init__(self, landing_dir: str = "data/01_landing", 
                 raw_dir: str = "data/02_raw", 
                 quarantine_dir: str = "data/03_quarantine"):
        self.landing_dir = landing_dir
        self.raw_dir = raw_dir
        self.quarantine_dir = quarantine_dir
        self.logger = CentralizedLogger(name="DataQualityGate")
        
        # Garantizar la existencia física de las capas del Data Lake
        os.makedirs(self.raw_dir, exist_ok=True)
        os.makedirs(self.quarantine_dir, exist_ok=True)

    def procesar_fase_calidad(self) -> None:
        """Ejecuta de forma secuencial la auditoría de todas las fuentes de la ingesta."""
        self.logger.info("Iniciando ejecución del DAG 2: Control de Calidad de Datos.")
        
        # 1. Procesar Ventas (Jonathan)
        try:
            self.auditar_ventas(file_name="raw_ventas.csv")
        except Exception as e:
            self.logger.error(f"Fallo crítico procesando el flujo de ventas: {str(e)}")
            
        # 2. Procesar Clientes (Jonathan)
        try:
            self.auditar_clientes(file_name="raw_clientes.json")
        except Exception as e:
            self.logger.error(f"Fallo crítico procesando el flujo de clientes: {str(e)}")
            
        self.logger.info("DAG 2 finalizado. La capa data/02_raw/ ha sido actualizada.")

    def auditar_ventas(self, file_name: str = "raw_ventas.csv") -> Tuple[int, int]:
        """Regla: Remueve duplicados transaccionales y aísla montos nulos o <= 0."""
        source_path = os.path.join(self.landing_dir, file_name)
        
        if not os.path.exists(source_path):
            self.logger.warning(f"Aviso de DataOps: El archivo {file_name} NO se encuentra en Landing.")
            return 0, 0

        self.logger.info(f"Iniciando Data Quality Gate para el flujo de ventas: {file_name}")
        df = pd.read_csv(source_path)
        total_inicial = len(df)

        # Regla 1: Limpieza de duplicados
        df_unique = df.drop_duplicates(subset=["id_transaccion"], keep="first")
        duplicados = total_inicial - len(df_unique)
        if duplicados > 0:
            self.logger.warning(f"Remoción de {duplicados} transacciones duplicadas detectadas.")

        # Regla 2: Identificación de inconsistencias financieras
        condicion_corrupto = df_unique["monto"].isnull() | (df_unique["monto"] <= 0)
        df_quarantine = df_unique[condicion_corrupto]
        df_valid = df_unique[~condicion_corrupto]

        # Algoritmo de Branching a Cuarentena
        if not df_quarantine.empty:
            quarantine_path = os.path.join(self.quarantine_dir, f"corrupt_{file_name}")
            df_quarantine.to_csv(quarantine_path, index=False)
            self.logger.critical(f"Alerta de Gobierno: Se aislaron {len(df_quarantine)} ventas corruptas en Cuarentena.")

        raw_path = os.path.join(self.raw_dir, "ventas_validas.csv")
        df_valid.to_csv(raw_path, index=False)
        self.logger.info(f"Validación de ventas finalizada. {len(df_valid)} registros promovidos a Raw Zone.")
        return len(df_valid), len(df_quarantine)

    def auditar_clientes(self, file_name: str = "raw_clientes.json") -> Tuple[int, int]:
        """Regla: Valida que id_cliente no sea nulo y que el correo contenga un '@'."""
        source_path = os.path.join(self.landing_dir, file_name)
        
        if not os.path.exists(source_path):
            self.logger.warning(f"Aviso de DataOps: El archivo {file_name} NO se encuentra en Landing.")
            return 0, 0

        self.logger.info(f"Iniciando Data Quality Gate para el flujo de clientes: {file_name}")
        
        try:
            df = pd.read_json(source_path, lines=True)
        except Exception:
            df = pd.read_json(source_path)
            
        # Regla de Calidad
        condicion_valido = df["id_cliente"].notnull() & df["email"].str.contains("@", na=False)
        df_valid = df[condicion_valido]
        df_quarantine = df[~condicion_valido]

        # Algoritmo de Branching a Cuarentena
        if not df_quarantine.empty:
            quarantine_path = os.path.join(self.quarantine_dir, f"corrupt_{file_name}")
            df_quarantine.to_json(quarantine_path, orient="records", lines=True)
            self.logger.critical(f"Alerta de Gobierno: {len(df_quarantine)} clientes sin correo o id enviados a Cuarentena.")

        df_valid.to_json(os.path.join(self.raw_dir, "clientes_validos.json"), orient="records", lines=True)
        self.logger.info(f"Validación de clientes finalizada. {len(df_valid)} registros promovidos a Raw Zone.")
        return len(df_valid), len(df_quarantine)


def ejecutar_dag_calidad() -> bool:
    """Función de enganche que manda a llamar el orquestador principal (main.py)"""
    try:
        gate = DataQualityGate()
        gate.procesar_fase_calidad()
        return True
    except Exception as e:
        print(f"❌ Error crítico en el DAG 2 de Calidad: {str(e)}")
        return False

if __name__ == "__main__":
    gate = DataQualityGate()
    gate.procesar_fase_calidad()