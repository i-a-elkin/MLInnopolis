"""Lesson25 Task2-10"""

from pyspark.sql import SparkSession
from pyspark.sql import functions as F

spark = SparkSession.builder.master("local").getOrCreate()

orders = spark.read.load(
    r"C:\Users\ivana\MLInnopolis\Module2\Lesson25\data\orders.csv",
    format="csv",
    sep=",",
    inferSchema=True,
    header="true",
)
customers = spark.read.load(
    r"C:\Users\ivana\MLInnopolis\Module2\Lesson25\data\customers.csv",
    format="csv",
    sep=",",
    inferSchema=True,
    header="true",
)
order_items = spark.read.load(
    r"C:\Users\ivana\MLInnopolis\Module2\Lesson25\data\order_items.csv",
    format="csv",
    sep=",",
    inferSchema=True,
    header="true",
)

joined = orders.join(
    customers, orders["customer_id"] == customers["customer_id"], "inner"
)
result = joined.join(
    order_items, joined["order_id"] == order_items["order_id"], "inner"
)
result = result.groupBy(
    customers["customer_id"], customers["first_name"], customers["last_name"]
).agg(
    (F.sum(result["quantity"] * result["list_price"] * (1 - result["discount"]))).alias(
        "total_spent"
    )
)
result = (
    result.sort("total_spent", ascending=False)
    .select("first_name", "last_name", "total_spent")
    .limit(5)
)
result = result.withColumn("total_spent", F.round(result["total_spent"]))
result.show()

spark.stop()
