import pandas as pd
import sqlite3

df = pd.read_excel('data/Online Retail.xlsx')
print(df.head())



# 1. Leer el archivo Excel desde la carpeta data
print("Leyendo el archivo Excel...")
df = pd.read_excel('data/Online Retail.xlsx')

# 2. Conectar a una base de datos SQLite local
conn = sqlite3.connect('retail.db')

# 3. Volcar los datos del DataFrame a una tabla SQL llamada 'transactions'
df.to_sql('transactions', conn, if_exists='replace', index=False)
print("¡Datos cargados en la base de datos SQLite con éxito!")


## DESCRIPCIÓN: Extracción de métricas de comportamiento (RFM) y tendencias
# 4. Escribir y ejecutar tu consulta SQL con funciones de ventana (RANK, LAG, OVER) y RFM

query = """
-- 1. Agrupa las transacciones por cliente y mes, calculando el gasto total mensual
WITH monthly_sales AS (
    SELECT 
        CustomerID,
        strftime('%Y-%m', InvoiceDate) AS sales_month,
        SUM(Quantity * UnitPrice) AS monthly_spend
    FROM transactions
    WHERE CustomerID IS NOT NULL
    GROUP BY CustomerID, sales_month
),
-- 2. Utiliza funciones analíticas OVER y PARTITION BY para evaluar el comportamiento temporal
ranked_sales AS (
    SELECT 
        CustomerID,
        sales_month,
        monthly_spend,
        LAG(monthly_spend, 1) OVER (PARTITION BY CustomerID ORDER BY sales_month) AS prev_month_spend,
        AVG(monthly_spend) OVER (PARTITION BY CustomerID) AS avg_historical_spend,
        ROW_NUMBER() OVER (PARTITION BY CustomerID ORDER BY sales_month DESC) AS rn
    FROM monthly_sales
),
-- 3. Calcula las métricas clásicas de comportamiento transaccional por cliente
rfm_base AS (
    SELECT 
        CustomerID,
        MAX(InvoiceDate) AS last_purchase_date,
        COUNT(DISTINCT InvoiceNo) AS frequency,
        SUM(Quantity * UnitPrice) AS monetary
    FROM transactions
    WHERE CustomerID IS NOT NULL
    GROUP BY CustomerID
)
-- 4. Une la base RFM con los datos mensuales más recientes para estructurar el dataset final
SELECT 
    r.CustomerID,
    r.frequency,
    r.monetary,
    CAST(julianday('2011-12-10') - julianday(r.last_purchase_date) AS INTEGER) AS recency_days,
    COALESCE(ts.monthly_spend, 0) - COALESCE(ts.avg_historical_spend, 0) AS trend_delta
FROM rfm_base r
LEFT JOIN ranked_sales ts 
    ON r.CustomerID = ts.CustomerID 
    AND ts.rn = 1;
"""

# Ejecutar la consulta y traer el resultado a un DataFrame de Pandas
df_features = pd.read_sql_query(query, conn)
conn.close()

# Mostrar las primeras filas de las features generadas
print("\nPrimeras features calculadas:")
print(df_features.head())