# Arquitectura del Orquestador y Pipeline de Datos

## 1. Diseño del Flujo Principal (DAGs)
Nuestra plataforma utiliza un enfoque de **dependencia estricta de tareas**. Hemos diseñado el flujo dividiendo el proceso monolítico en tareas atómicas interdependientes, simulando el comportamiento de **Apache Airflow**.

El flujo consta de tres hitos secuenciales (ELT):
1. **DAG 1 (Ingesta - Extract & Load):** Conecta con las fuentes (APIs y Bases de Datos) y aterriza los datos en la `Landing Zone` en su formato original (JSON/CSV) sin aplicar transformaciones pesadas. Posee un sistema de *Retries* (Reintentos) para tolerar fallos de red.
2. **DAG 2 (Calidad - Validation):** Actúa como compuerta de seguridad. Solo inicia si el DAG 1 fue exitoso.
3. **DAG 3 (Transformación - Warehouse):** Solo inicia si los datos pasaron las pruebas de calidad del DAG 2.

## 2. Manejo de Errores e Idempotencia
Para evitar la corrupción de datos, el orquestador principal (`main.py`) aplica un freno de emergencia. Si una tarea crítica falla (ej. caída de la base de datos de origen), el pipeline se detiene exactamente en ese punto, evitando cargar datos incompletos al Data Warehouse. 

Además, las tareas están diseñadas para ser **idempotentes**: si el DAG 1 se ejecuta dos veces por error, los archivos en la `Landing Zone` simplemente se sobrescriben de manera segura, sin duplicar registros en las tablas finales.