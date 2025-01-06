"""Lesson25 Task2-3"""

from pyspark.sql import SparkSession

spark = SparkSession.builder.master("local").getOrCreate()

customers = spark.read.load(
    r"C:\Users\ivana\MLInnopolis\Module2\Lesson25\data\customers.csv",
    format="csv",
    sep=",",
    inferSchema=True,
    header="true",
)
orders = spark.read.load(
    r"C:\Users\ivana\MLInnopolis\Module2\Lesson25\data\orders.csv",
    format="csv",
    sep=",",
    inferSchema=True,
    header="true",
)
stores = spark.read.load(
    r"C:\Users\ivana\MLInnopolis\Module2\Lesson25\data\stores.csv",
    format="csv",
    sep=",",
    inferSchema=True,
    header="true",
)

customers_orders = customers.join(
    orders, customers["customer_id"] == orders["customer_id"], "inner"
)
result = customers_orders.join(
    stores, customers_orders["store_id"] == stores["store_id"], "inner"
)
result = result.filter(result["store_name"] == "Santa Cruz Bikes")
result = result.select(
    customers_orders["first_name"],
    customers_orders["last_name"],
    customers_orders["email"],
    customers_orders["phone"],
).distinct()
result.show()

spark.stop()
