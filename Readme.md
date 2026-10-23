Features para Machine Learning (E-Commerce Churn)
    Propósito
        El objetivo de esta práctica es transformar datos crudos de comportamiento de usuarios provenientes de un escenario de e-commerce en un dataset de entrenamiento de alto valor analítico (Feature Engineering), utilizando SQL avanzado, optimizando el rendimiento y asegurando la consistencia de las variables directamente desde la base de datos.   
    Tecnologías y Herramientas Utilizadas 
       Python & Pandas: Carga y preprocesamiento inicial del archivo de transacciones (Online Retail.xlsx).
       SQLite: Creación de la base de datos relacional local para la ejecución de consultas estructuradas.   
       SQL Avanzado: Uso de CTEs (Common Table Expressions), agregaciones y funciones de ventana (LAG, AVG OVER, ROW_NUMBER).   
    Definición de Features Generadas
       La consulta SQL implementada genera un perfil consolidado por cada CustomerID con las siguientes métricas de comportamiento:
    Recency (Días desde la última compra):
       Lógica: Calcula la diferencia en días entre la última fecha de compra registrada del cliente y una fecha de corte de referencia (2011-12-10) utilizando funciones de fecha (julianday).
       Utilidad para Churn: Permite identificar la inactividad reciente; a mayor cantidad de días sin comprar, mayor probabilidad de abandono.
    Frequency (Frecuencia de compra):
       Lógica: Cuenta la cantidad de pedidos únicos (InvoiceNo) realizados por el usuario.
       Utilidad para Churn: Mide la lealtad y el nivel de engagement recurrente del cliente con la plataforma.
    Monetary (Gasto total acumulado):
       Lógica: Suma el valor monetario total (Quantity * UnitPrice) de todas las transacciones del usuario.
       Utilidad para Churn: Identifica el valor del cliente (Customer Lifetime Value); perder un cliente de alto valor monetario es más crítico.
    Trend (Tendencia de gasto mensual):
       Lógica: Compara el gasto del último mes activo del cliente frente a su promedio histórico de gasto utilizando funciones de ventana (LAG y AVG OVER particionadas por CustomerID). Se utiliza COALESCE para asegurar que los valores nulos se manejen de forma coherente (arrojando 0).
       Utilidad para Churn: Detecta caídas abruptas en el consumo reciente, lo cual es un indicador temprano de que un cliente está próximo a abandonar el servicio.

    Estructura del Repositorio
      data/: Contiene el archivo fuente de datos (Online Retail.xlsx).
      analisis.py: Script de Python encargado de cargar los datos a SQLite y ejecutar la consulta de ingeniería de features.
      feature_engineering.sql: Script SQL que contiene la consulta principal con las funciones de ventana y agregaciones.
      README.md: Documentación detallada del proyecto.