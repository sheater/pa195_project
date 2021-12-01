package cz.muni.fi.pa195;

import org.apache.spark.sql.Dataset;
import org.apache.spark.sql.Row;
import org.apache.spark.sql.SparkSession;

import static org.apache.spark.sql.functions.col;

public class SpotifyChartsRankOneArtists {
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

        df.where(col("chart").equalTo("top200").and(col("rank").equalTo(1)))
                .groupBy(col("artist"))
                .count()
                .orderBy(col("count").asc())
                .show();
    }
}
