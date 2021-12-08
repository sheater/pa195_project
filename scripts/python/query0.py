from pyspark import SparkConf, SparkContext
from pyspark.sql import SQLContext

conf = SparkConf() \
    .setAppName("PySpark Cassandra Query 0") \
    .setMaster("spark://127.0.0.1:7077")

sc = SparkContext('local', conf=conf)
sql = SQLContext(sc)

df = sql.read \
    .format("org.apache.spark.sql.cassandra") \
    .load(keyspace="pa195", table="charts")

total = df.where((df.region == "Slovakia") & (df.chart == "top200")) \
    .count()

print("Total:", total)

