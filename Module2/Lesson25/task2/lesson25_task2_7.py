"""Lesson25 Task2-7"""

from pyspark.sql import SparkSession
from pyspark.sql import functions as F

spark = SparkSession.builder.master("local").getOrCreate()

products = spark.read.load(
    r"C:\Users\ivana\MLInnopolis\Module2\Lesson25\data\products.csv",
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

joined = products.join(
    order_items, products["product_id"] == order_items["product_id"], "inner"
)
result = joined.groupBy("product_name").agg(
    (
        F.sum(joined["quantity"] * order_items["list_price"] * (1 - joined["discount"]))
    ).alias("total_sales")
)
result = result.withColumn("total_sales", F.round(result["total_sales"]))
result.show()

spark.stop()
