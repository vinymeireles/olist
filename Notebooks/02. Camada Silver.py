# Databricks notebook source
# 📒 Notebook 02 - Camada Silver (Limpeza e Transformação)

from pyspark.sql.functions import col, to_date, datediff

#caminho de leitura (Bronze) e escrita (Silver)
bronze_path = "/Volumes/workspace/default/olist/bronze/"
silver_path = "/Volumes/workspace/default/olist/silver/"

#Leitura do dataframe bronze
orders = spark.read.format("delta").load(f"{bronze_path}orders")
order_items = spark.read.format("delta").load(f"{bronze_path}order_items")
customers = spark.read.format("delta").load(f"{bronze_path}customers")
sellers = spark.read.format("delta").load(f"{bronze_path}sellers")
payments = spark.read.format("delta").load(f"{bronze_path}order_payments")
reviews = spark.read.format("delta").load(f"{bronze_path}order_reviews")


# COMMAND ----------

#limpeza e transformação dos dados (Conversão de datas e limpeza - null) > Orders
orders_clean = orders.dropna(subset=["order_id", "order_status", "customer_id"])
orders_clean = orders_clean.withColumn("order_purchase_date", to_date("order_purchase_timestamp"))
orders_clean = orders_clean.withColumn("order_delivered_date", to_date("order_delivered_customer_date"))
orders_clean = orders_clean.withColumn("delivery_days", to_date("order_delivered_date", "order_purchase_date"))


# COMMAND ----------

#clientes com localização válida
customers_clean = customers.dropna(subset=["customer_id", "customer_state"])

# COMMAND ----------

# Join de pedidos com clientes
orders_customers = orders_clean.join(customers_clean, on="customer_id", how="inner")

#Salvar na camada Silver - dados tratados
orders_customers.write.format("delta").mode("overwrite").save(f"{silver_path}orders_customers")
