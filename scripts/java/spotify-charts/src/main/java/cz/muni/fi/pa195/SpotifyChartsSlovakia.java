package cz.muni.fi.pa195;

import org.apache.spark.sql.Dataset;
import org.apache.spark.sql.Row;
import org.apache.spark.sql.SparkSession;

import static org.apache.spark.sql.functions.col;

public class SpotifyChartsSlovakia {
    public static void main(String[] args) {
        SparkSession session = SparkSession.builder()
                .appName("Spark Cassandra Spotify charts")
                .master("spark://pa195-spark-master:7077")
                .getOrCreate();

        Dataset<Row> df = session.read()
                .format("org.apache.spark.sql.cassandra")
                .option("keyspace", "pa195")
                .option("table", "charts")
                .load();

        Long count = df.filter(col("region").equalTo("Slovakia")
                .and(col("chart").equalTo("top200")))
                .count();
        System.out.printf("Total: %s%n", count);
    }
}
