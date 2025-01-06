"""Lesson25 Task2-8"""

from pyspark.sql import SparkSession

spark = SparkSession.builder.master("local").getOrCreate()

orders = spark.read.load(
    r"C:\Users\ivana\MLInnopolis\Module2\Lesson25\data\orders.csv",
    format="csv",
    sep=",",
    inferSchema=True,
    header="true",
)

result = (
    orders.groupBy("order_status")
    .count()
    .withColumnRenamed("count", "number_of_orders")
    .orderBy("order_status")
)
result.show()

spark.stop()
