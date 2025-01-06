"""Lesson25 Task2-9"""

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
order_items = spark.read.load(
    r"C:\Users\ivana\MLInnopolis\Module2\Lesson25\data\order_items.csv",
    format="csv",
    sep=",",
    inferSchema=True,
    header="true",
)

joined = orders.join(
    order_items, orders["order_id"] == order_items["order_id"], "inner"
)
result = joined.select(
    F.month("order_date").alias("month"), "quantity", "list_price", "discount"
)
result = result.groupBy("month").agg(
    (F.sum(result["quantity"] * result["list_price"] * (1 - result["discount"]))).alias(
        "total_monthly_sales"
    )
)
result = result.withColumn(
    "total_monthly_sales", F.round(result["total_monthly_sales"])
)
result = result.sort("month")
result.show()

spark.stop()
