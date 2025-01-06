"""Lesson25 Task2-2"""

from pyspark.sql import SparkSession

spark = SparkSession.builder.master("local").getOrCreate()

staffs = spark.read.load(
    r"C:\Users\ivana\MLInnopolis\Module2\Lesson25\data\staffs.csv",
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

result = staffs.join(stores, staffs["store_id"] == stores["store_id"], "inner")
result = result.filter(result["active"] == 1)
result = result.select("first_name", "last_name", "store_name")
result.show()

spark.stop()
