import sys
from pyspark import SparkConf, SparkContext
from pyspark.sql import SQLContext
from pyspark.sql import functions as F

sys.stdout = open(sys.stdout.fileno(), mode='w', encoding='utf8', buffering=1)

conf = SparkConf() \
    .setAppName("PySpark Cassandra Test") \
    .setMaster("spark://127.0.0.1:7077")

sc = SparkContext('local', conf=conf)
sql = SQLContext(sc)

df = sql.read \
    .format("org.apache.spark.sql.cassandra") \
    .load(keyspace="pa195", table="charts")

# filter out everything but "BTS" in "top200" charts
df_bts = df.filter((df.artist == "BTS") & (df.chart == "top200"))

# calculate highest rank for each region
df_ranked = df_bts.groupBy("region").agg(F.min("rank").alias("rank"))

# intermediate plot
df_ranked.show()

# filter records by joining with previous df
# then grouping by region and rank (to see it in the output)
# finally aggregate and sort by aggregation result
df_bts.join(df_ranked, ["region", "rank"], "inner") \
    .groupby("region", "rank") \
    .count() \
    .sort("count", ascending=False) \
    .show()
