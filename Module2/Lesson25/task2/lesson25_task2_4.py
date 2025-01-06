"""Lesson25 Task2-4"""

from pyspark.sql import SparkSession

spark = SparkSession.builder.master("local").getOrCreate()

products = spark.read.load(
    r"C:\Users\ivana\MLInnopolis\Module2\Lesson25\data\products.csv",
    format="csv",
    sep=",",
    inferSchema=True,
    header="true",
)
categories = spark.read.load(
    r"C:\Users\ivana\MLInnopolis\Module2\Lesson25\data\categories.csv",
    format="csv",
    sep=",",
    inferSchema=True,
    header="true",
)

result = products.join(
    categories, products["category_id"] == categories["category_id"], "inner"
)
result = result.groupBy("category_name").count()
result.show()

spark.stop()
