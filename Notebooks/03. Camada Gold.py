# Databricks notebook source
 #📒 Notebook 03 - Camada Gold (Agregações para análise)

from pyspark.sql.functions import avg, count

silver_path = "/Volumes/workspace/default/olist/silver/"
gold_path = "/Volumes/workspace/default/olist/gold/"

# Leitura da camada Silver
orders_customers = spark.read.format("delta").load(f"{silver_path}orders_customers")

# COMMAND ----------

display(orders_customers)

# COMMAND ----------

# MAGIC %md
# MAGIC Insight dos dados do negócio:
# MAGIC 1. Total de pedidos por estado
# MAGIC 2. Tempo médio de entrega por estado
# MAGIC 3. Valor médio por tipo de pagamento
# MAGIC 4. Média de itens por pedido
# MAGIC 5. Média de avaliação por estado

# COMMAND ----------

# 1. Total de pedidos por estado
orders_by_state = orders_customers.groupBy("customer_state").agg(count("order_id").alias("total_orders"))
orders_by_state.write.format("delta").mode("overwrite").save(f"{gold_path}/orders_by_state")


# COMMAND ----------

display(orders_by_state)

# COMMAND ----------

# 2.Tempo médio de entrega por estado
from pyspark.sql.functions import avg, datediff, round

#order_delivered_customer_date (data da entrega)
#order_purchase_timestamp (data da compra)

# Cria a coluna de dias de entrega como número inteiro
orders_with_delivery_days = orders_customers.withColumn(
    "delivery_days", 
    datediff("order_delivered_customer_date", "order_purchase_timestamp")
)

# Agrupa por estado e calcula a média arredondada
avg_delivery_by_state = orders_with_delivery_days.groupBy("customer_state").agg(
    round(avg("delivery_days"), 0).alias("avg_delivery_days")  # arredondado para 2 casas decimais
)

# Salva na camada Gold
avg_delivery_by_state.write.format("delta").mode("overwrite").save(f"{gold_path}/avg_delivery_by_state")



# COMMAND ----------

display(avg_delivery_by_state)

# COMMAND ----------

#Leitura da camada Silver
bronze_path = "/Volumes/workspace/default/olist/bronze/"
payments = spark.read.format("delta").load(f"{bronze_path}order_payments")
display(payments)


# COMMAND ----------

# 3. Valor médio por tipo de pagamento

avg_payment_by_type = payments.groupBy("payment_type").agg(
    round(avg("payment_value"), 2).alias("avg_payment_value")
)
avg_payment_by_type.write.format("delta").mode("overwrite").save(f"{gold_path}/avg_payment_by_type")

# COMMAND ----------

display(avg_payment_by_type)

# COMMAND ----------

#Leitura da camada Silver
bronze_path = "/Volumes/workspace/default/olist/bronze/"
orders_items= spark.read.format("delta").load(f"{bronze_path}order_items")
display(orders_items)

# COMMAND ----------

# 4. Média de itens por pedido
items_per_order = orders_items.groupBy("order_id").count()
avg_items_per_order = items_per_order.agg(
    round(avg("count"), 2).alias("avg_items_per_order")
)
avg_items_per_order.write.format("delta").mode("overwrite").save(f"{gold_path}/avg_items_per_order")
display(avg_items_per_order)


# COMMAND ----------

#5. Média de avaliações por estado

#  1️⃣ Leitura das tabelas da camada bronze
orders = spark.read.format("delta").load(f"{bronze_path}orders")
customers = spark.read.format("delta").load(f"{bronze_path}customers")
reviews = spark.read.format("delta").load(f"{bronze_path}order_reviews")

# 2️⃣ Join entre reviews, orders e customers para trazer o estado do cliente junto com a nota de avaliação
reviews_with_state = reviews\
    .join(orders, "order_id")\
    .join(customers, "customer_id")\
    .select("customer_state", "review_score")\
    .dropna()

# 3️⃣ Cálculo da média das notas de avaliação por estado   
avg_score_by_state = reviews_with_state.groupBy("customer_state").agg(round(avg("review_score"),2).alias("avg_review_score"))

# 4️⃣ Salvamento da tabela na camada Gold
avg_score_by_state.write.format("delta").mode("overwrite").save(f"{gold_path}/avg_score_by_state")

# COMMAND ----------

display(avg_score_by_state)
