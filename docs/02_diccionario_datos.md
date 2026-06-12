# 02. Diccionario de Datos - Esquema Estrella (Data Warehouse)

Este documento contiene la especificación técnica del modelo de datos multidimensional (Esquema Estrella) alojado en la capa de almacenamiento final (`data/04_warehouse/`). El modelo ha sido diseñado por **Eu** (Arquitecta de Infraestructura y Gobierno) y optimizado en formato columnar **Parquet** para maximizar el rendimiento analítico y mitigar riesgos de privacidad.

---

## 1. Resumen de la Arquitectura del Modelo

* **Tipo de Modelado:** Esquema Estrella (Star Schema)
* **Formato de Almacenamiento:** Apache Parquet (`.parquet`)
* **Compresión:** Snappy (Nativa de Parquet)
* **Objetivo:** Centralizar métricas transaccionales e implementar *Security by Design* mediante el enmascaramiento automático de Datos de Identificación Personal (PII).

---

## 2. Tabla de Hechos (Fact Table)

### `Fact_Ventas`
Representa el núcleo del negocio. Registra los eventos cuantitativos (transacciones de venta) y contiene las llaves foráneas para cruzar la información con los contextos de análisis.

| Nombre del Campo | Tipo de Dato (Esquema) | Llave | Descripción / Reglas de Negocio |
| :--- | :--- | :---: | :--- |
| `id_transaccion` | `INT` | **PK** | Identificador único y correlativo de la venta generada. |
| `id_cliente` | `INT` | **FK** | Clave foránea que conecta con la dimensión `Dim_Cliente`. |
| `id_producto` | `INT` | **FK** | Clave foránea que conecta con la dimensión `Dim_Producto`. |
| `id_fecha` | `INT` | **FK** | Clave foránea que conecta con `Dim_Tiempo`. Formato entero rígido (`YYYYMMDD`). |
| `monto` | `DECIMAL(10,2)` | - | Valor monetario total bruto de la venta. |
| `metodo_pago` | `VARCHAR(50)` | - | Medio utilizado por el cliente (ej. Tarjeta, Efectivo, Transferencia). |

---

## 3. Tablas de Dimensiones (Dimension Tables)

### `Dim_Cliente`
Contiene la información descriptiva de los consumidores. Incorpora la capa de Gobierno de Datos mediante anonimización criptográfica.

| Nombre del Campo | Tipo de Dato (Esquema) | Llave | Descripción y Reglas de Gobierno |
| :--- | :--- | :---: | :--- |
| `id_cliente` | `INT` | **PK** | Identificador único del cliente. |
| `hash_identidad` | `VARCHAR(256)` | - | **[PII Enmascarado]** Hash irreversible generado con el algoritmo **SHA-256** mediante `security.py`. Reemplaza y unifica de manera segura los campos originales de `nombre` y `email`. |
| `segmento` | `VARCHAR(50)` | - | Clasificación comercial del cliente (ej. Premium, Standard). |
| `region` | `VARCHAR(50)` | - | Zona geográfica o país de residencia del usuario. |

### `Dim_Producto`
Almacena el catálogo y los atributos de los artículos disponibles en la plataforma.

| Nombre del Campo | Tipo de Dato (Esquema) | Llave | Descripción / Reglas de Negocio |
| :--- | :--- | :---: | :--- |
| `id_producto` | `INT` | **PK** | Identificador único del producto. |
| `nombre_producto` | `VARCHAR(100)` | - | Nombre comercial del artículo o ítem de inventario. |
| `categoria` | `VARCHAR(50)` | - | Agrupación lógica de la línea de productos (ej. Electrónica, Ropa, Hogar). |

### `Dim_Tiempo`
Dimensión optimizada para análisis temporales eficientes. Evita el cálculo costoso de funciones de fecha en tiempo de ejecución de los Dashboards.

| Nombre del Campo | Tipo de Dato (Esquema) | Llave | Descripción / Reglas de Negocio |
| :--- | :--- | :---: | :--- |
| `id_fecha` | `INT` | **PK** | Llave entera artificial con formato `YYYYMMDD` (Ejemplo numérico: `20260612`). |
| `fecha_completa` | `DATE` | - | Formato de fecha estándar del calendario (`YYYY-MM-DD`). |
| `anio` | `INT` | - | Año calendario extraído (Útil para agrupaciones anuales). |
| `mes` | `INT` | - | Número de mes (1 al 12) para análisis estacionales. |
| `dia_semana` | `VARCHAR(20)` | - | Nombre del día correspondiente (ej. Lunes, Martes) para análisis de comportamiento semanal. |

---

## 4. Notas de Implementación (Gobernanza y Rendimiento)

1. **Inmutabilidad:** Los datos almacenados en formato Parquet en la capa de producción son de **solo lectura (`SELECT`)** para perfiles analíticos. Cualquier corrección debe aplicarse aguas arriba reejecutando el pipeline de calidad (DAG 2) desde la zona `Raw`.
2. **Trazabilidad:** La columna `hash_identidad` permite a los Data Scientists y analistas agrupar transacciones y entrenar modelos de comportamiento sin conocer la identidad real del cliente, garantizando el cumplimiento normativo por diseño (*Privacy by Design*).