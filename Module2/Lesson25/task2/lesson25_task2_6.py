"""Lesson25 Task2-6"""

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

result = customers.join(
    orders, customers["customer_id"] == orders["customer_id"], "inner"
)
result = result.groupBy(
    customers["customer_id"], customers["first_name"], customers["last_name"]
).agg({"order_id": "count"})
result = result.select("first_name", "last_name", "count(order_id)")
result = result.filter(result["count(order_id)"] >= 1)
result = result.orderBy("first_name", "last_name")
result.show()

spark.stop()
