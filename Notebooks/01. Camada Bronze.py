# Databricks notebook source
# CAMADA BRONZE: INGESTÃO DE DADOS (1º VERSÃO - MANUAL)

# 📒 Notebook 01 - Camada Bronze (Ingestão)
from pyspark.sql import SparkSession

spark = SparkSession.builder.appName("OlistETL-Bronze").getOrCreate()

# Leitura dos arquivos CSV (Raw)
raw_path = "/Volumes/workspace/default/olist/raw/"

orders = spark.read.csv(f"{raw_path}/orders.csv", header=True, inferSchema=True)
order_items = spark.read.csv(f"{raw_path}/order_items.csv", header=True, inferSchema=True)
customers = spark.read.csv(f"{raw_path}/customers.csv", header=True, inferSchema=True)
sellers = spark.read.csv(f"{raw_path}/sellers.csv", header=True, inferSchema=True)
payments = spark.read.csv(f"{raw_path}/order_payments.csv", header=True, inferSchema=True)
reviews = spark.read.csv(f"{raw_path}/order_reviews.csv", header=True, inferSchema=True)


# COMMAND ----------

display(orders)

# COMMAND ----------

# Gravação em Delta
orders.write.format("delta").mode("overwrite").save("/Volumes/workspace/default/olist/bronze/orders")
order_items.write.format("delta").mode("overwrite").save("/Volumes/workspace/default/olist/bronze/order_items")
customers.write.format("delta").mode("overwrite").save("/Volumes/workspace/default/olist/bronze/customers")
sellers.write.format("delta").mode("overwrite").save("/Volumes/workspace/default/olist/bronze/sellers")
payments.write.format("delta").mode("overwrite").save("/Volumes/workspace/default/olist/bronze/payments")
reviews.write.format("delta").mode("overwrite").save("/Volumes/workspace/default/olist/bronze/reviews")

# COMMAND ----------

# MAGIC %fs
# MAGIC ls '/Volumes/workspace/default/olist/raw/'

# COMMAND ----------

# CAMADA BRONZE: INGESTÃO DE DADOS (2ª VERSÃO AUTOMÁTICA) - CONVERTER .CSV (RAW) EM ARQUIVOS .DELTA (BRONZE)

# 📒 Notebook 01 - Camada Bronze (Ingestão)
from pyspark.sql import SparkSession

# Lista de nomes dos arquivos CSV (sem extensão)
# Lista de arquivos a processar
file_names = [
    "customers",
    "order_items",
    "order_payments",
    "order_reviews",
    "orders",
    "product_category_name",
    "products",
    "sellers"
    ]

# Caminho de origem dos arquivos CSV
csv_base_path = "/Volumes/workspace/default/olist/raw/"

# Caminho de destino (Bronze - Delta)
bronze_base_path = "/Volumes/workspace/default/olist/bronze/"

# Loop para leitura e gravação em Delta
for name in file_names:
    csv_path = f"{csv_base_path}{name}.csv"
    bronze_path = f"{bronze_base_path}{name}"
    
    df = spark.read.option("header", True).option("inferSchema", True).csv(csv_path)
    
    print(f"✔️ Lido: {csv_path}")
    print(f"📦 Gravando em: {bronze_path}")
    
    #Salva os arquivos em formato Delta na camada bronze
    df.write.format("delta").mode("overwrite").save(bronze_path)

# Verificar gravação de exemplo
df_check = spark.read.format("delta").load(f"{bronze_base_path}orders")
display(df_check.limit(5))

# COMMAND ----------

# Verificar gravação de exemplo
df_check = spark.read.format("delta").load(f"{bronze_base_path}products")
display(df_check.limit(5))
