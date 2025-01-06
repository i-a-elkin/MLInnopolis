"""Lesson25 Task2-1"""

from pyspark.sql import SparkSession

spark = SparkSession.builder.master("local").getOrCreate()

products = spark.read.load(
    r"C:\Users\ivana\MLInnopolis\Module2\Lesson25\data\products.csv",
    format="csv",
    sep=",",
    inferSchema=True,
    header="true",
)
brands = spark.read.load(
    r"C:\Users\ivana\MLInnopolis\Module2\Lesson25\data\brands.csv",
    format="csv",
    sep=",",
    inferSchema=True,
    header="true",
)

result = products.join(brands, products["brand_id"] == brands["brand_id"], "inner")
result = result.select("product_name", "brand_name")
result.show()

spark.stop()
