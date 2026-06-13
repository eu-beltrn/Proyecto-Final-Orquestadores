## 4. Estrategia de Calidad, Observabilidad y MLOps (Nicole)

Para asegurar que nuestro proyecto solo use datos limpios y seguros, implementamos una estrategia enfocada en la calidad y el monitoreo continuo de los flujos de información.

### A. Control de Calidad de Datos (DAG 2)
Creamos un filtro de seguridad en el archivo `data_quality.py` que revisa automáticamente los datos crudos que vienen de la ingesta. Aplica las siguientes reglas antes de guardarlos:
* **Elimina Duplicados:** Borra las transacciones repetidas en el flujo de ventas para que no afecten los reportes financieros.
* **Envía a Cuarentena:** Si detecta datos corruptos o incompletos (como las ventas con montos en cero o negativos, o clientes sin ID y sin correo electrónico), el script los separa y los envía automáticamente a una carpeta de **Cuarentena** (`data/03_quarantine/`). Así, el proceso principal del grupo puede continuar trabajando sin que la data mala arruine el Data Warehouse de Eu.

### B. Monitoreo y Sistema de Alertas (DAG 4)
Para vigilar la salud de todo el pipeline, centralizamos el registro de eventos en `src/utils/logger.py`. Este componente clasifica los mensajes del sistema según su gravedad:
* **Alertas Críticas:** Cuando nuestro filtro de calidad detecta anomalías graves (como un registro enviado a Cuarentena), el sistema genera un aviso de tipo `CRITICAL`. 
* **Automatización a futuro:** En un entorno de producción real, este aviso funciona como un disparador automático (**Webhook**) que envía una notificación inmediata a los canales de comunicación del equipo técnico (como Slack o Microsoft Teams) para resolver el problema sin perder tiempo.

### C. Preparación para Inteligencia Artificial y MLOps (DAG 5)
Planificamos el diseño conceptual para que el negocio pueda usar Modelos de Inteligencia Artificial de forma automática y precisa a futuro (detallado en `docs/04_mlops_drift.md`):
* **Detección de Data Drift (Cambio de datos):** El sistema revisa semanalmente si la forma en que compran los clientes ha cambiado drásticamente comparado con los datos con los que entrenamos la IA originalmente.
* **Reentrenamiento Automático:** Si los datos cambian mucho, el sistema se activa solo para extraer la data limpia más reciente, volver a entrenar el modelo predictivo en segundo plano y actualizarlo sin interrumpir el servicio.