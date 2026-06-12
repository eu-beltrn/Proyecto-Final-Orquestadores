# Arquitectura del Data Warehouse y Gobierno de Datos

## 1. Diseño Dimensional (Esquema Estrella)
Hemos consolidado la información dispersa de la empresa en un **Esquema Estrella** centralizado. Esta decisión arquitectónica se justifica por su altísimo rendimiento en herramientas de BI (como Power BI o Tableau).
* **Almacenamiento Columnar (Parquet):** A diferencia de un CSV tradicional, decidimos guardar el Warehouse en formato `.parquet`. Esto comprime el tamaño de los archivos hasta en un 70% y permite que las consultas analíticas sean exponencialmente más rápidas y económicas, ya que el motor solo lee las columnas solicitadas en lugar de escanear filas enteras.

## 2. Implementación de Gobierno de Datos (Data Governance)
Para garantizar el cumplimiento de normativas de privacidad de datos, diseñamos dos capas de seguridad:

* **Control de Acceso (RBAC - Role-Based Access Control):** A nivel teórico en la base de datos, los permisos están estrictamente segregados. Un analista de negocios solo tiene permisos de `SELECT` sobre el Data Warehouse, pero tiene completamente bloqueado el acceso a la Zona Cruda (`Raw Zone`) del Data Lake para evitar manipulación indebida.
* **Enmascaramiento de PII:** Como se evidencia en nuestro pipeline de transformación (`build_dwh.py`), todos los datos de Identificación Personal (PII), como los nombres y correos de los clientes, son ofuscados utilizando un algoritmo irreversible (SHA-256) antes de llegar a la capa de análisis. Esto asegura que el analista pueda agrupar y ver las tendencias de compra de un cliente específico, sin revelar jamás la identidad real del mismo.