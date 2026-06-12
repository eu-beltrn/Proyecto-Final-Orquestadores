# 🚀 Proyecto Integrador: Plataforma Moderna de Ingeniería de Datos

Este repositorio contiene la implementación práctica y teórica de una arquitectura de datos escalable, abarcando desde la orquestación y almacenamiento, hasta el gobierno de datos y MLOps.

## 👥 Equipo de Desarrollo
* **Jonathan:** Orquestación, Pipelines e Ingesta de Datos (Simulación Airflow).
* **Eu:** Arquitectura de Infraestructura, Data Warehouse (Esquema Estrella) y Gobierno de Datos.
* **Nicole:** Data Analytics, Calidad de Datos (Branching), DataOps y MLOps.

## ⚙️ Arquitectura Conceptual
1. **Ingesta (Landing Zone):** Extracción transaccional de APIs y Bases de Datos.
2. **Calidad de Datos:** Evaluación de nulos/duplicados y desvío a Zona de Cuarentena o Zona Raw.
3. **Transformación:** Construcción de Modelo Dimensional y enmascaramiento de datos sensibles (PII).
4. **Observabilidad:** Centralización de logs y alertas.

## 🛠️ Cómo ejecutar el proyecto localmente
Para simular el flujo completo del orquestador en tu máquina local:

1. Clona este repositorio.
2. Instala las dependencias:
   ```bash
   pip install -r requirements.txt